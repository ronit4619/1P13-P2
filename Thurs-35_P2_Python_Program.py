## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import time
import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)


## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Example to rotate the base: arm.rotateBase(90)

#Function 1 Author: James Lindsay
def iD(x):                                      #Function that determins dropoff locations depending on the conainter id. Uses parameter x as container id
    if x == 1: #Small Red                                 # x represents the different objects dropped into the autoclave
        location = [-0.58, 0.2411, 0.3963]
    elif x == 2: #Small Green
        location = [0.0, -0.639, 0.3963]
    elif x == 3: #Small Blue
        location = [0.0, 0.639, 0.3963]
    elif x == 4: # Large Red
        location = [-0.3888, 0.1415, 0.3]
    elif x == 5: # Large Green 
        location = [0.0, -0.4137, 0.3]
    elif x == 6: #Large Blue
        location = [0.0, 0.4137, 0.3]
    return location                             #Returns value of dropoff location for given container id
#Function 2 Author: James Lindsay
def gripperControl(gripper):                    #Function to control gripper using muscle sensor values. Gripper parameter is to determine whether the gripper is open or closed
    while True:                                 #Loops gripper function to constantly run while receiving muscle sensor input
        time.sleep(1)
        if gripper == False:                    #If gripper is false, it is open and will close and vice versa if sensor value exceeds some threshhold defined below (0.5) 
            if arm.emg_right() > 0.5:           
                    if arm.emg_left() == 0:     #if sensor value of right arm exceeds threshhold and left arm is0, gripper opens or closes
                        arm.control_gripper(40)
                        gripper = True
                        time.sleep(0.5)
                        break                   #breaks function once gripper is controlled so that another function can be called within the main function

        elif gripper == True:
            if arm.emg_right() > 0.5:
                if arm.emg_left() == 0:
                    arm.control_gripper(-40)
                    gripper = False
                    time.sleep(1)
                    arm.home()                  #Arm returns home when gripper is opened as it only opens when dropping off a container at an autoclave
                    break
                    

#Function 3 Authors: Ronit Ahuja and James Lindsay
def moveEndEffector(location, gripper):         #Function to move to a specific XYZ location in the quanser environment 
    while True:
        if arm.emg_right() > 0.5:
                if arm.emg_left() > 0.5:        #Only executes when both arm sensors exceed a threshhold of 0.5
                    if gripper == True:         #If the gripper is closed (true) it will move to the dropoff location of the current container being held by the gripper
                        arm.move_arm(0.4064, 0.0, 0.4826)       
                        time.sleep(1)
                        arm.move_arm(location[0], location[1], location[2])
                        time.sleep(1)
                        break
                    elif gripper == False:
                        arm.move_arm(location[0], location[1], location[2]) #When gripper is opened (false), it only needs to move to pickup location
                        time.sleep(1)
                        break
#Function 4 Author: Ronit Ahuja
def autoclaveDrawer(drawer, item):
    while True:
        time.sleep(1)
        if item == 4:                                       #Runs through each situation where the autocalve drawer may need to be opened (only large container with id as 4,5, and/or 6)
            if drawer == False:                             #if the drawer is closed (false) it will be opened when function is called
                if arm.emg_left() > 0.5:                    #Only executes when the left arm exceeds a threshhold of 0.5 and right arm is 0
                        if arm.emg_right() == 0:
                            arm.open_red_autoclave(True)
                            time.sleep(0.5)
                            break

            elif drawer == True:                            #if the drawer is open (true) it will be closed when function is called
                if arm.emg_left() > 0.5:
                    if arm.emg_right() == 0:
                        arm.open_red_autoclave(False)
                        time.sleep(0.5)
                        break
        elif item == 5:
            if drawer == False:                             
                if arm.emg_left() > 0.5:
                        if arm.emg_right() == 0:
                            arm.open_green_autoclave(True)
                            time.sleep(0.5)
                            break

            elif drawer == True:
                if arm.emg_left() > 0.5:
                    if arm.emg_right() == 0:
                        arm.open_green_autoclave(False)
                        time.sleep(0.5)
                        break

        elif item == 6:
            if drawer == False:
                if arm.emg_left() > 0.5:
                        if arm.emg_right() == 0:
                            arm.open_blue_autoclave(True)
                            time.sleep(0.5)
                            break

            elif drawer == True:
                if arm.emg_left() > 0.5:
                    if arm.emg_right() == 0:
                        arm.open_blue_autoclave(False)
                        time.sleep(0.5)
                        break

        else:
            break



#Main Function Author: Ronit Ahuja
def main():                             #Main function to call all other pre-defined functions in specified order
    pickup = [0.5055, 0.0, 0.0227]      #Sets pickup location for all container as they all have the same pickup location
    containers = [1,2,3,4,5,6]          #Initiates a list of container that still need to be place in their respective autoclaves


    while True:                         #Loops indefinitely until conditional at the bottom is met
        gripper = False                 #Setting gripper to False (open)
        drawer = False                  #Setting autoclave drawer to False (closed)
        import random   
        current = random.choice(containers) #Using random library, picks a container randomly from the containers list above
        containers.remove(current)          #Removes the container selected above from the container inventory list so it cannot be spawned in the quanser environment again
        print (containers)

        drop_location = iD(current)     #Sets the drop location using the function that determines said location
        arm.spawn_cage(current)         #Spawns cage that was randomly determined above
        moveEndEffector(pickup, gripper)
        gripperControl(gripper)
        gripper = True                  #Once the gripper is closed, the gripper is set to true (closed) so that the fucntion below moves to dropoff location instead of pickup location
        moveEndEffector(drop_location, gripper)
        autoclaveDrawer(drawer, current)
        gripperControl(gripper)
        drawer = True                   #Drawer was opened above so drawer is set to true so that it can be closed again on the next line
        autoclaveDrawer(drawer, current)
        

        if containers == []:            #Once inventory of containers is empty, the main  function breaks and all containers have been placed in their corresponding autoclave locations
            break


        

