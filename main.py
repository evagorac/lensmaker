

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
h_step = 1
v_step = 1

# this param is the seed distance from the OP to the lens
init_center_dist = 50

# coordinates of the point source relative to OP
src_crd = (50, -10)




