import cv2
import pyrealsense2
import time
import numpy as np
from realsense_depth import *

point = (400, 200)

far_dist = 300
near_dist = 100
set_time_dur = 10
rep_time_dur = 1
sets = []

# global start
start = False
set_start = False
rep_far = False

rows, cols = (10,10)
distance_array = [[0]*cols]*rows
rep = 0
set_timer = 0
rep_timer = 0
ref_distance = 0

#mosue position, to change to center of weights when computer vision is done
def show_distance(event, x, y, args, params):
    global point
    if (start == 0):
        point = (x, y)

# Initialize Intel Realsense Camera
dc = DepthCamera()

# Create mouse event
cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame", show_distance)




while True:
    ret, depth_frame, color_frame = dc.get_frame()

    # Show distance for specific point
    cv2.circle(color_frame, point, 4, (0, 0, 255))

    distance_array[5][5] = depth_frame[point[1],point[0]]

    for i in range(int(rows/2)):
        for j in range (int(cols/2)):
            if (point[1]-i) >= 0 and (point[0]-j) >= 0:
                distance_array[int(rows/2)-i][int(cols/2)-j] = depth_frame [point[1]-i,point[0]-j]
            else:
                distance_array[int(rows/2)-i][int(cols/2)-j] = 0
            
            if (point[1]+i) <= 480 and (point[0]+j) <= 640:
                distance_array[int(rows/2)+i][int(cols/2)+j] = depth_frame [point[1]+i,point[0]+j]
            else:
                distance_array[int(rows/2)+i][int(cols/2)+j] = 0
    
    distance_mean = 0
    distance_total = 0
    distance_count = 0

    for i in range(rows):
        for j in range (cols):
            if (distance_array[i][j] < 3000 and distance_array[i][j] > 50):
                distance_total += distance_array[i][j]
                distance_count += 1

    if (distance_count != 0):
        distance_mean = int(distance_total / distance_count)

    # distance = depth_frame[point[1],point[0]]

    cv2.rectangle(color_frame, (point[0]+35, point[1]-120), (point[0]+300,point[1]+95) ,(0,0,0), -1)
    cv2.putText(color_frame, "{} mm".format(distance_mean), (point[0] + 40, point[1] - 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(color_frame, "{} rep".format(rep), (point[0] + 40, point[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(color_frame, "{} sets".format(len(sets)), (point[0] + 40, point[1] + 90), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(color_frame, "{} mm ref".format(ref_distance), (point[0] + 40, point[1] + 0), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(color_frame, "{} rep_far".format(rep_far), (point[0] + 40, point[1] + 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(color_frame, "{} set_timer".format(set_timer), (point[0] + 40, point[1] - 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(color_frame, "{} time".format(round(time.monotonic())), (point[0] + 40, point[1] - 90), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

    #cv2.imshow ("Depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
    # print(sets)
    #spacebar start counting reps
    if key == 32:
        start = ~start
        if start:
            ref_distance = distance_mean
            rep = 0
            if sets:
                sets.clear()
                # print ("hi")
            set_start = True
            print ("Start Recording Exercise.")
        else:
            ref_distance = 0
            if set_start and rep != 0:
                sets.append(rep)
                # print ("hi2")
            print ("Stop Recording Exercise. Exercise Recorded:")
            print(sets)
        set_timer = 0

    if start:
        if rep_far:
            if (abs(distance_mean - ref_distance) < near_dist):
                rep_far = ~rep_far
                rep += 1
                set_timer = round(time.monotonic())
                set_start = True
                rep_timer = round(time.monotonic())
        else:
            if (abs(distance_mean - ref_distance) > far_dist) and (time.monotonic() - rep_timer > rep_time_dur) and (distance_mean != 0):
                rep_far = ~rep_far
            if set_start:
                if (round(time.monotonic())-set_timer > set_time_dur):
                    set_start = False
                    # if sets:
                    #     sets[0] = rep
                    #     rep = 0
                    # else:
                    #     sets.append(rep)
                    #     rep = 0
                    if rep != 0:
                        sets.append(rep)
                        print ("Set Completed. Current Sets:")
                        print (sets)
                        rep = 0
