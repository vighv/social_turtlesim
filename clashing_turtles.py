#!/usr/bin/env python

import roslib
import rospy
import math
from geometry_msgs.msg import Twist, Vector3
import turtlesim.srv
from turtlesim.msg import Pose
import random


Num_turtles = 2
x1 = 0
x2 = 0

def where1(pose_data):
    global x1
    x1 = pose_data.x

def where2(pose_data):
    global x2
    x2 = pose_data.x


# Spawn and kill turtles to draw the boundary, draw the boundary in red (255,0,0) ||Need to refactor!
def draw_boundary():
    rospy.wait_for_service('spawn')

    draw_artist = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    draw_artist(0, 5.5, 0, 'artist1')
    draw_artist(6, 5.5, 0, 'artist2')

    artist1_set_pen = rospy.ServiceProxy('artist1/set_pen', turtlesim.srv.SetPen)
    artist1_set_pen(255, 0, 0, 2, 0)

    artist2_set_pen = rospy.ServiceProxy('artist2/set_pen', turtlesim.srv.SetPen)
    artist2_set_pen(255, 0, 0, 2, 0)

    rospy.wait_for_service('kill')
    kill_artist = rospy.ServiceProxy('kill', turtlesim.srv.Kill)

    rospy.Subscriber('artist1/pose',Pose,where1)
    global x1
    while x1 < 5:
        tpub = rospy.Publisher("artist1/cmd_vel", Twist, queue_size=10)
        tpub.publish(Twist(Vector3(10, 0, 0), Vector3(0, 0, 0)))
    kill_artist('artist1')

    rospy.Subscriber('artist2/pose', Pose, where2)
    global x2
    while x2 < 11:
        tpub2 = rospy.Publisher("artist2/cmd_vel", Twist, queue_size=10)
        tpub2.publish(Twist(Vector3(10, 0, 0), Vector3(0, 0, 0)))
    kill_artist('artist2')
    #rospy.spin()
    #rospy.signal_shutdown("Done drawing")

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

def send_vel(turtle_params):
    name = turtle_params[3]
    vels = gen_vel()
    tpub = rospy.Publisher(name + "/cmd_vel", Twist, queue_size=10)
    tpub.publish(vels)



if __name__ == "__main__":
    rospy.init_node("social_turtle_node")

    rospy.wait_for_service('kill')
    kill_first_turtle = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    kill_first_turtle('turtle1')

    draw_boundary()

    turtle1_params = (3,3,math.radians(90),'turtle1')
    turtle2_params = (7,7,math.radians(180),'turtle2')

    spawn_turtle(turtle1_params)
    spawn_turtle(turtle2_params)

    t_params = (turtle1_params, turtle2_params)

    while not rospy.is_shutdown():
        for t in t_params:
            send_vel(t)
            rate = rospy.Rate(5)
        rate.sleep()



