import numpy as np

'''
script to generate lens shape to reflect a point source into user's eye
output is a series of csv files that can be imported by solidworks to approximately define the lens shape
    solidworks is capable of accepting a list of 3d coordniates and will connect them with a spline
each csv will be a horizontal slice of the lens, so each csv will describe the surface at a different height level

conventions:
    center of eye is coordinate origin and referred to as the observer point (OP)
        x axis = out of right ear
        y axis = out of face
        z axis = up out of head
    the source image emitter is a point source (can be achieved with a concave lens)
    the eye in question is assumed to be the right eye
    all dimensions are in mm, all angles are in degrees

inputs to this script are:
    desired horizontal fov
    desired vertical fov
    horiztonal and vertical step sizes
    lens initial distance from OP through center axis
    coordinates of point source

The above parameters will define an array of points bound within an ellipse that will iteravely generate the lens surface starting from the center
'''

h_fov = 90
v_fov = 90

# step sizes refer to the length of each line segment that composes the lens approximation
h_step = 2
v_step = 3

# this param is the seed distance from the OP to the lens
init_center_dist = 50

# coordinates of the point source relative to OP
src_coord = np.array([[50], [-10], [0]])

# useful vectors
x_u = np.array([[1],[0],[0]])
y_u = np.array([[0],[1],[0]])
z_u = np.array([[0],[0],[1]])


'''
define helper functions
'''

def get_surface_normal(surface_coord):
    # return the correct surface normal for a given point in space
    OP_vec = surface_coord
    src_vec = surface_coord - src_coord

    OP_vec_unit = OP_vec / np.linalg.norm(OP_vec)
    src_vec_unit = src_vec / np.linalg.norm(src_vec)

    return (OP_vec_unit + src_vec_unit) / 2

def get_next_surface_coord_delta(prev_surface_normal, horizontal=True):
    # returns a vector of mag h_step or v_step that denotes the displacement from the previous surface_coord along the lens surface
    # the vector will always point in positive x or z, so invert the vector if you wish to displace in negative x or z
    if horizontal:
        orth_vec = np.cross(prev_surface_normal.T, z_u.T).T
        disp_vec = orth_vec * h_step / np.linalg.norm(orth_vec)
        if np.dot(disp_vec.T, x_u) < 0:
            disp_vec *= -1
    else:
        orth_vec = np.cross(prev_surface_normal.T, x_u.T).T
        disp_vec = orth_vec * v_step / np.linalg.norm(orth_vec)
        if np.dot(disp_vec.T, z_u) < 0:
            disp_vec *= -1
    return disp_vec

def is_within_bounds(surface_coord):
    # checks to see if point is within bounds of the ellipse defined by the horizontal and vertical fov's
    # the normal vector of the plane that contains the ellipse is the y axis
    # the plane also contains the seed point which is how far this virtual ellipse will exist from the face
    # this function will take the surface coord and cast it to this plane, then see if it lies within the ellipse
    
    # first get ellipse param (ellipse in x-z plane)
    r_x = init_center_dist * np.sin(h_fov/2 * np.pi/180)
    r_z = init_center_dist * np.sin(v_fov/2 * np.pi/180)

    # cast point to ellipse plane
    cast_point = surface_coord * (init_center_dist / np.dot(surface_coord.T, y_u))

    # plug point into ellipse equation and see if <= 1
    return np.dot(cast_point, x_u) ** 2 / r_x ** 2 + np.dot(cast_point, z_u) ** 2 / r_z ** 2 <= 1

n = get_surface_normal(init_center_dist * y_u)
print(n)
d = get_next_surface_coord_delta(n)
print(d)
print(np.linalg.norm(d))




