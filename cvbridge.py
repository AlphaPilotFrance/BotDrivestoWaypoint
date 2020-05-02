#!/usr/bin/env python
from __future__ import print_function

import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import numpy as np
import cv2
from std_msgs.msg import String
#from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


		#cv2.drawContours(frame, contours, -1, (0,255,0), 2)#dessiner contours


        #cv2.imshow("frame", cv_image)
        #cv2.imshow("greenmask", greenmask)
        #cv2.imshow("redmask", redmask)
        #cv2.imshow("opening", opening_masked_img)
        #cv2.imshow("masked_img", G_masked_img)
        #cv2.imshow("Image window", cv_image)
        #cv2.waitKey(1)



class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image, queue_size=1000)
    #self.twist_pub = rospy.Publisher("robot_base_velocity_controller/cmd_vel", Twist, queue_size=1000);
    self.gate_pub= rospy.Publisher("gate_state", String, queue_size=10);
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("rrbot/camera1/image_raw",Image,self.callback)






#####################     CALLBACK   ###########################################
  def callback(self,data):
    

########################   GATE_STATE ###########################################
#start as: SEARCHING
#if red found: FOUND
#THEN if green found: OBSTRUCTED

    #First find destination (0 or 1) ###########################################3
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV) #Camera video to HSV
    redmask = cv2.inRange(hsv, l_b2, u_b2)
    #-----Reduce Noise using morphology opening-----
    R_opening_masked_img = cv2.morphologyEx(redmask, cv2.MORPH_OPEN, kernel)
    #-----Resulting image-----
    R_masked_img = cv2.bitwise_and(cv_image, cv_image, mask=redmask)
    #-----Finding contours and drawing it on the result image-----    
    (R_contours, R_hierarchy) = cv2.findContours(R_opening_masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(masked_img, contours, -1, (255,255,255), 3)
    for contours in R_contours:
        (x, y, w, h) = cv2.boundingRect(contours)  # sauvegarder coordonnees contours
        if w>100:
                #print(x,y,w,h, data.width)
		#if cv2.contourArea(contours) < 3500:  # supprimer les petits contours, supprimer le bruit
		#    continue
                x2 = x + (w/2)
                y2 = y + (h/2)
                x2 = int(round(x2))
                y2 = int(round(y2))
                deviation = float(x2 - (data.width / 2))
                #print(deviation);
                velocity= float(2*(deviation)/data.width);
                #print (velocity);
                #destination=1
		#if (abs(deviation)>5) and w<400: #If looking away from obstacle
		#	#no forward velocity
		#	if deviation>5:
		#		twist_vel.angular.z=-0.5;
		#	if deviation<5:
		#		twist_vel.angular.z=0.5;
		#else: #if looking at obstacle
		#	#no rotation        		
		#	twist_vel.linear.x=abs(1-velocity); #accelerate
                #twist_vel.linear.x=0.0;
		#twist_vel.angular.z=0.0;
                                    # INTERFACE #########################################
                cv2.line(cv_image,(400,480),(x2,y2),(0,255,0),1)
                font = cv2.FONT_HERSHEY_COMPLEX
                if -velocity<0 :
                    text = 'Gauche'
                else :
                    text = 'Droite'
                cv2.putText(cv_image, text, (20, 20), font, 1, (0, 255, 0), 1, cv2.LINE_4)
                cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		#cv2.drawContours(frame, contours, -1, (0,255,0), 2)#dessiner contours
                                   # DESTINATION EXISTENCE ###############################
        #else:
	        #destination=0
    cv2.imshow("Red_maskimg", R_masked_img)
    cv2.waitKey(1)
    #return destination	
    if (R_contours):
          for contours in R_contours:
            (x, y, w, h) = cv2.boundingRect(contours)  # sauvegarder coordonnees contours
            if w>100:
               #print(R_contours)
               destination =1
            else:
               destination =0
          
    else:
          destination =0


    if (destination == 1):
        gate_status="found"
        #Second find obstacle (0 or 1) ###########################################3
        try:
          cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
          print(e)
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV) #Camera video to HSV
        greenmask = cv2.inRange(hsv, l_b1, u_b1)
        #-----Reduce Noise using morphology opening-----
        G_opening_masked_img = cv2.morphologyEx(greenmask, cv2.MORPH_OPEN, kernel)
        #-----Resulting image-----
        G_masked_img = cv2.bitwise_and(cv_image, cv_image, mask=greenmask)
        #-----Finding contours and drawing it on the result image-----    
        (G_contours, G_hierarchy) = cv2.findContours(G_opening_masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(masked_img, contours, -1, (255,255,255), 3)
        for contours in G_contours:
          (x, y, w, h) = cv2.boundingRect(contours)  # sauvegarder coordonnees contours
          if w>100:
                #print(x,y,w,h, data.width)
		#if cv2.contourArea(contours) < 3500:  # supprimer les petits contours, supprimer le bruit
		#    continue
                x2 = x + (w/2)
                y2 = y + (h/2)
                x2 = int(round(x2))
                y2 = int(round(y2))
                deviation = float(x2 - (data.width / 2))
                #print(deviation);
                velocity= float(2*(deviation)/data.width);
                #print (velocity);
                obstacle=1
		#if (abs(deviation)>5) and w<400: #If looking away from obstacle
		#	#no forward velocity
		#	if deviation>5:
		#		twist_vel.angular.z=-0.5;
		#	if deviation<5:
		#		twist_vel.angular.z=0.5;
		#else: #if looking at obstacle
		#	#no rotation        		
		#	twist_vel.linear.x=abs(1-velocity); #accelerate
                #twist_vel.linear.x=0.0;
		#twist_vel.angular.z=0.0;

###################################  INTERFACE #########################################
                cv2.line(cv_image,(400,480),(x2,y2),(0,255,0),1)
                font = cv2.FONT_HERSHEY_COMPLEX
                if -velocity<0 :
                    text = 'Gauche'
                else :
                    text = 'Droite'
                cv2.putText(cv_image, text, (20, 20), font, 1, (0, 255, 0), 1, cv2.LINE_4)
                cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#################################### OBSTACLE EXISTENCE ###############################
          cv2.imshow("Green_maskimg", G_masked_img)
          cv2.waitKey(1)
        if (G_contours):
          for contours in G_contours:
            (x, y, w, h) = cv2.boundingRect(contours)  # sauvegarder coordonnees contours
            if w>100:
               #print(G_contours)
               obstacle =1
            else:
               obstacle =0
          
        else:
          obstacle =0
	 
        if (obstacle ==1):
                gate_status="found but obstructed"
        else:
                gate_status="found"
    else:
        gate_status="searching"
 
    print(gate_status)
    try:
        self.gate_pub.publish(gate_status)
    except CvBridgeError as e:
        print(e)
#    try:
#      self.image_pub.publish(self.bridge.cv2_to_imgmsg(G_masked_img, "bgr8"))
#      #self.twist_pub.publish(twist_vel);
#      
      
#    except CvBridgeError as e:
#        print(e)

def main(args):
  rospy.init_node('image_converter', anonymous=True)
  global l_b1 
  global u_b1
  global l_b2 
  global u_b2
  global kernel
  #RED
  l_b1 = np.array([40, 180, 40])
  u_b1= np.array([80, 255, 255])
  l_b2 = np.array([0, 10, 80])
  u_b2= np.array([10, 255, 255])
  #l_b1 = np.array([0, 0, 0])
  #u_b1= np.array([0, 255, 0])
  #l_b2 = np.array([170, 10, 80])
  #u_b2= np.array([180, 255, 255])
  kernel = np.ones((3,3), np.uint8) #Matrix used for opening 
  ic = image_converter()
  #global twist_vel
  #twist_vel = Twist()
  gate_status = String()
  
  rate = rospy.Rate(10) # 10hz
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
