#!/usr/bin/env python

import roslib
import rospy
import math
from geometry_msgs.msg import Twist, Vector3
import turtlesim.srv
from turtlesim.msg import Pose
import random
import numpy

Num_turtles = 2
#x1 = 0
x = 0
y = 0
thet = 0

# def where(pose_data):
#     # global x1
#     draw_boundary_func.x1 = pose_data.x

# def where(pose_data):
#     # global x1
#     global x
#     x = pose_data.x
#     global y
#     y = pose_data.y
#     global thet
#     thet = pose_data.theta


# Create artist turtles with specified end point to draw the boundary

def draw_boundary():
    artist1 = (0, 5.5, 0, 'artist1')
    end1 = 4.5
    draw_boundary_func(artist1 , end1)
    end2 = 11
    artist2 = (6.5, 5.5, 0, 'artist2')
    draw_boundary_func(artist2 , end2)

# Spawn and kill turtles to draw the boundary, draw the boundary in red (255,0,0), width 2

def draw_boundary_func(artist_params, end_pt):
    rospy.wait_for_service('spawn')

    draw_artist = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    draw_artist(*artist_params)

    artist_set_pen = rospy.ServiceProxy(artist_params[3]+'/set_pen', turtlesim.srv.SetPen)
    artist_set_pen(255, 0, 0, 2, 0)

    rospy.wait_for_service('kill')
    kill_artist = rospy.ServiceProxy('kill', turtlesim.srv.Kill)

    draw_boundary_func.x1 = 0 # Variable storing the x position of a turtle

    def where(pose_data):
        # global x1
        draw_boundary_func.x1 = pose_data.x


    rospy.Subscriber(artist_params[3]+'/pose',Pose, where)
    #global x1
    while draw_boundary_func.x1 < end_pt:
        tpub = rospy.Publisher(artist_params[3]+"/cmd_vel", Twist, queue_size=10)
        tpub.publish(Twist(Vector3(50, 0, 0), Vector3(0, 0, 0)))
    kill_artist(artist_params[3])


# Spawn a turtle with given (x,y) position, angle and name given in the parameters:

def spawn_turtle(turtle_params):
    rospy.wait_for_service('spawn')
    new_turtle = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    new_turtle(*turtle_params)


def gen_vel():
	cur_vel = 1
	ang_vel = 1
	prob = random.uniform(0,1)
	if prob > 0.2:
		velocity = Twist(Vector3(cur_vel, 0, 0), Vector3(0, 0, ang_vel))
	else:
		new_vel = cur_vel * random.uniform(0, 3)
		new_ang = ang_vel*random.uniform(-5, 5)
		velocity = Twist(Vector3(new_vel, 0, 0), Vector3(0, 0, new_ang))
	return velocity

# Center waypoint is (5.5,5.5)
# Function to find new velocity for a turtle
def calc_vel(turtle_params, cx, cy, cthet):
    wp = 5.5
    # Motion towards the waypoint:
    # global x, y, thet
    #
    # # Current pose callback
    # # def where(pose_data):
    # #     # global x1
    # #     calc_vel.x = pose_data.x
    # #     calc_vel.y = pose_data.y
    # #     calc_vel.thet = pose_data.theta
    #
    #
    # rospy.Subscriber(turtle_params[3] + '/pose', Pose, where)
    # cx = x # Variable storing the x position of a turtle
    # cy = y  # Variable storing the x position of a turtle
    # cthet = thet

    vel_lin = 0
    vel_ang = 0

    #Find direction to waypoint:

    if cthet < 0:
        cthet += math.radians(360)

    #Angle to waypoint
    ang_wp = math.atan2(wp - cy, wp - cx)

    if ang_wp < 0:
         ang_wp += math.radians(360)

    del_t = math.fabs(ang_wp - cthet)

    ome = 0.5

    #Quadrant1&2
    if ang_wp > 0 and ang_wp <= math.radians(180):
        if cthet > ang_wp and cthet < math.radians(180) + ang_wp:
            vel_ang = min(-ome*del_t,-1)
    else:
            vel_ang = max(ome*del_t,1)

    # # Quadrant2
    # if ang_wp > math.radians(90) and ang_wp <= math.radians(180):
    #     if cthet > ang_wp and cthet < math.radians(180) + ang_wp:
    #             vel_ang = -del_t
    #     else:
    #         vel_ang = del_t

    # Quadrant3&4
    if ang_wp > math.radians(180) and ang_wp <= math.radians(360):
        if cthet < ang_wp and cthet >= -math.radians(180) + ang_wp:
            vel_ang = max(ome*del_t,1)
        else:
            vel_ang = min(-ome*del_t,-1)

    if del_t<0.05:
        vel_lin = 2
    # vel_lin = 2
    # if ang_wp < math.radians(180):
    #     if del_t > 0 and del_t < math.radians(180):
    #         vel_ang = -1 #-1
    #     elif del_t > 0 and del_t > math.radians(180):
    #         vel_ang = +1
    #     # elif del_t < 0 and math.fabs(del_t) < math.radians(180):
    #     #     vel_ang = +1
    #     # elif del_t < 0 and math.fabs(del_t) > math.radians(180):
    #     #     vel_ang = +1 #-1
    #
    # else:
    #     if del_t < math.radians(180):
    #         vel_ang = -1
    #     else:
    #         vel_ang = +1


    velocity = Twist(Vector3(vel_lin, 0, 0), Vector3(0, 0, vel_ang))
    return velocity

def reflect_pos(cx,cy,cthet):
    if cthet < math.radians(80):
        cthet = 0
        cx = 0
        cy = 0

    velocity = Twist(Vector3(cx, cy, 0), Vector3(0, 0, cthet))
    return velocity

def send_vel(t_params):



    def get_pos(pose):
        send_vel.cx = pose.x
        send_vel.cy = pose.y
        send_vel.cthet = pose.x

    send_vel.cx = 0
    send_vel.cy = 0
    send_vel.cthet = 0


    for turtle_params in t_params:
        rospy.Subscriber(turtle_params[3] + '/pose', Pose, get_pos)
        # global x
        # cx = x  # Variable storing the x position of a turtle
        # global y
        # cy = y  # Variable storing the x position of a turtle
        # global thet
        # cthet = thet
        name = turtle_params[3]
        vels = reflect_pos(send_vel.cx, send_vel.cy, send_vel.cthet)#gen_vel()#calc_vel(turtle_params, send_vel.cx, send_vel.cy, send_vel.cthet)
        tpub = rospy.Publisher(name + "/cmd_vel", Twist, queue_size=10)
        tpub.publish(vels)



if __name__ == "__main__":
    rospy.init_node("social_turtle_node")

    rospy.wait_for_service('kill')
    kill_first_turtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    kill_first_turtle('turtle1')

    draw_boundary()

    turtle1_params = (5.5,10,math.radians(120),'turtle_1') #Down moving turtle
    turtle2_params = (2,1,math.radians(60),'turtle_2') #Up moving turtle

    spawn_turtle(turtle1_params)
    spawn_turtle(turtle2_params)

    t_params = (turtle1_params, turtle2_params)

    while not rospy.is_shutdown():
        #for t in t_params:
        send_vel(t_params)
        rate = rospy.Rate(20)
        rate.sleep()



