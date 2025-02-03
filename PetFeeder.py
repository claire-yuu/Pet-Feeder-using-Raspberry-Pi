# PetFeeder Project @ Fairmont Schools, CA
# Documented by Claire Yu, 2024

# Some required packages
import RPi.GPIO as GPIO
from gpiozero import LED 
import time 

# define
T_FoodRelease = 10				# feeder food release duration per trigger, in second

# set GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

# define key hardware connection info - for our specific parts and wiring
nMP = 4				# number of stepper motor phase
iGPIO_Switch = 2	# GPIO pin id for LED
iGPIO_LED = 4		# GPIO pin id for LED
MPs = [22, 23, 24, 25]	# GPIO pin id for 4 motor phases

# Step motor driver parameters
# Reference: Youtube video https://www.youtube.com/watch?v=avrdDZD7qEQ
# Motor/driver part: WWZMDiB 28BYJ-48 ULN2003 motor/driver kit from Amazon.com
for iMP in range(nMP):
    GPIO.setup(MPs[iMP], GPIO.OUT)
    GPIO.output(MPs[iMP], 0)
STEPs = []
STEPs.append([1, 0, 0, 0])
STEPs.append([0, 1, 0, 0])
STEPs.append([0, 0, 1, 0])
STEPs.append([0, 0, 0, 1])
dt_MP = 0.0048		# delay time between motor phase actuation, minimal 0.002 

# set LED: in parallel to motor and will light when motor moves 
red = LED(iGPIO_LED)
red.off()

# set input pin 2 as the switch to activate feed dispenser
GPIO.setup(iGPIO_Switch, GPIO.IN) 
while True:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
# wait for button/pedal press
    while True:
        if GPIO.input(iGPIO_Switch) == 0: 
            print("Button is pressed")
            break

# button press detected, turn on LED        
    red.on()    #turn led on 

# run motor to dispense food
    t0 = time.time()
#   loop unitl required motor running duration is reached
    while time.time() - t0 < T_FoodRelease:   
        for iStep in range(nMP):
            for iMP in range(nMP):
                GPIO.output(MPs[iMP], STEPs[iStep][iMP])
# wait for this step to finish
            time.sleep(dt_MP)
# turn off motor
    for iMP in range(nMP):
        GPIO.output(MPs[iMP], 0)

# turn led off
    red.off()    

                                                                                                                           
