import wiringpi
import time

MAX_SPEED = 480 # 19.2 MHz / 2 / 480 = 20 kHz
def zero_motor_pins():
    wiringpi.digitalWrite(5, 0)
    wiringpi.pwmWrite(12, 0)

    wiringpi.digitalWrite(6, 0)
    wiringpi.pwmWrite(13, 0)

def forward():
    wiringpi.digitalWrite(5, 1)
    wiringpi.pwmWrite(12, 250)

    wiringpi.digitalWrite(6, 1)
    wiringpi.pwmWrite(13, 250)

def reverse():
    wiringpi.digitalWrite(5, 0)
    wiringpi.pwmWrite(12, 450)

    wiringpi.digitalWrite(6, 0)
    wiringpi.pwmWrite(13, 450)
    
def turn_right():
    wiringpi.digitalWrite(5, 1)
    wiringpi.pwmWrite(12, 250)
    
    wiringpi.digitalWrite(6, 0)
    wiringpi.pwmWrite(13, 0)

def turn_left():
    wiringpi.digitalWrite(5, 0)
    wiringpi.pwmWrite(12, 0)
    
    wiringpi.digitalWrite(6, 1)
    wiringpi.pwmWrite(13, 250)
    
# setup control pins and PWM
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(12, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetRange(MAX_SPEED)
wiringpi.pwmSetClock(2)

wiringpi.pinMode(5, wiringpi.GPIO.OUTPUT)
wiringpi.pinMode(6, wiringpi.GPIO.OUTPUT)

zero_motor_pins()
print("Basic motor testing...Running")

print("Going forwards")
forward()
time.sleep(5)
zero_motor_pins()
print("Going backwards")
reverse()
time.sleep(5)
zero_motor_pins()
print("Turning right")
turn_right()
time.sleep(5)
zero_motor_pins()
print("Turning left")
turn_left()
time.sleep(5)
zero_motor_pins()

print("Basic motor testing...Complete")


