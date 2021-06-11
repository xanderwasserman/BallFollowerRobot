#!/usr/bin/env python3

import rospy
import wiringpi

from std_msgs.msg import Int32
from geometry_msgs.msg import Twist

MAX_SPEED = 480 # 19.2 MHz / 2 / 480 = 20 kHz

# setup pins for motor driver
wiringpi.wiringPiSetupGpio()
#x = wiringpi.wiringPiSetupSys()
wiringpi.pinMode(12, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetRange(MAX_SPEED)
wiringpi.pwmSetClock(2)

wiringpi.pinMode(5, wiringpi.GPIO.OUTPUT)
wiringpi.pinMode(6, wiringpi.GPIO.OUTPUT)

wiringpi.digitalWrite(5, 1)
wiringpi.pwmWrite(12, 0)

wiringpi.digitalWrite(6, 0)
wiringpi.pwmWrite(13, 0)

# global variables for motor control
control = Twist();
control.linear.x = 0
control.angular.z = 0

def motor_cmd_callback(msg):
    control.linear.x = msg.linear.x
    control.angular.z = msg.angular.z

# ROS initializations
rospy.init_node('motor_commander')

# get left motor gain
if rospy.has_param('left_gain') and rospy.has_param('right_gain'):
    K_left = rospy.get_param('left_gain')
    K_right = rospy.get_param('right_gain')
else:
    K_left = 1.0
    K_right = 1.0
print('K_left = ' + str(K_left))
print('K_right = ' + str(K_right))

# get right motor gain

sub = rospy.Subscriber('/turtle1/cmd_vel', Twist, motor_cmd_callback)

# control rate is 200Hz
rate = rospy.Rate(200)


while not rospy.is_shutdown():
   
    leftmotor = K_left*(control.linear.x - (control.angular.z/2))/2*250
    rightmotor = K_right*(control.linear.x + (control.angular.z/2))/2*250
    
    if leftmotor > 0:
        if leftmotor > MAX_SPEED:
            leftmotor = MAX_SPEED
            
        wiringpi.digitalWrite(5, 1)
        wiringpi.pwmWrite(12, int(leftmotor))
    else:
        if leftmotor < -MAX_SPEED:
            leftmotor = -MAX_SPEED    
    
        wiringpi.digitalWrite(5, 0)
        wiringpi.pwmWrite(12, -int(leftmotor))
        
    if rightmotor > 0:
        if leftmotor > MAX_SPEED:
            leftmotor = MAX_SPEED
    
        wiringpi.digitalWrite(6, 1)
        wiringpi.pwmWrite(13, int(rightmotor))
    else:
        if leftmotor < -MAX_SPEED:
            leftmotor = -MAX_SPEED    
    
        wiringpi.digitalWrite(6, 0)
        wiringpi.pwmWrite(13, -int(rightmotor))
    
    control.linear.x = 0
    control.angular.z = 0
    
    rate.sleep()
