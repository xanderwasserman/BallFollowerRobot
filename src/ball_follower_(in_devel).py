#!/usr/bin/env python3

import rospy
import wiringpi
import time

from std_msgs.msg import Int32
from geometry_msgs.msg import Twist, Point

relative_pos = 0
leftFlag = False
rightFlag = False
forwardFlag = False

def callback(point):
    global relative_pos
    # condition pos to be relative to robots coordinate system
    # if robot_pos is negative, ball is to the left, right if positive
    relative_pos = point.x -290 #x=290 is middle-ish
    

def turnleft(speed, cmd_out):
    cmd_out.angular.z = speed
    return cmd_out
    
def turnright(speed, cmd_out):
    cmd_out.angular.z = -speed
    return cmd_out
    
def forward(speed, cmd_out):
    cmd_out.linear.x
    return cmd_out
    
def stop(cmd_out):
    cmd_out.angular.z = 0
    cmd_out.linear.x = 0
    return cmd_out

def control(pos):
    global leftFlag
    global rightFlag
    global forwardFlag
    
    if relative_pos < -50 and rightFlag == False:
        leftFlag = True
        
    if relative_pos > 50 and leftFlag == False:
        rightFlag = True
        
    if relative_pos > -50 and relative_pos < 50 and rightFlag == False and leftFlag == False:
        forwardFlag = True
        
    # to handle overshoot
    if rightFlag == True and relative_pos < -50:
        rightFlag = False
        time.sleep(1)
    # to handle overshoot    
    if leftFlag == True and relative_pos < 50:
        leftFlag = False
        time.sleep(1)
    
   
    
    

rospy.init_node('ball_follower')
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/ball_location', Point, callback)
rate = rospy.Rate(500)

while not rospy.is_shutdown():
    twist_out = control(ball_pos, twist_out)
    pub.publish(twist_out)
    rate.sleep()
