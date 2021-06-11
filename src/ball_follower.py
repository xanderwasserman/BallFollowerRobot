#!/usr/bin/env python3

import rospy
import wiringpi

from std_msgs.msg import Int32
from geometry_msgs.msg import Twist, Point

ball_pos = 0
turn_flag = false

twist_out = Twist()

def callback(point):
    global ball_pos
    ball_pos = point.x
    
def direction(pos, twist):
    twist.angular.z = 0
    twist.linear.x = 0
    if pos != 0:
        if pos < 260:
            twist.angular.z = 4
            #print("Turning Left")
            return twist
        elif pos > 380:
            twist.angular.z = -4
            #print("Turning Right")
            return twist
        elif pos >= 240 and pos <= 400:
            # if the robot sees the ball and it is within the detection limits then the robot follows.
            # if it gets too close or loses the ball, it stops
            twist.linear.x = 2
            #print("Going Forward")
            return twist
    return twist    

rospy.init_node('ball_follower')
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/ball_location', Point, callback)
rate = rospy.Rate(500)
count = 0


while not rospy.is_shutdown():
    twist_out = direction(ball_pos, twist_out)
    pub.publish(twist_out)
    rate.sleep()
    
