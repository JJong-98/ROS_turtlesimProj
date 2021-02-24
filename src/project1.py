#!/usr/bin/python
#-*- encoding: utf-8 -*-

import cv2, rospy, time
import numpy as np
import math

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from turtlesim.msg import Pose

bridge = CvBridge()
img = np.empty(shape=[0])
x, y, theta = 0, 0, 0

control_msg = Twist()

def image_callback(img_data):
	global bridge
	global img
	img = bridge.imgmsg_to_cv2(img_data, "bgr8")


def pose_callback(pose_data):
	global x
	global y
	global theta

	x = pose_data.x
	y = pose_data.y
	theta = pose_data.theta

def control_msg_publish(linear_x, angular_z):
		control_msg.linear.x = linear_x
		control_msg.linear.y = 0
		control_msg.linear.z = 0
		control_msg.angular.x = 0
		control_msg.angular.y = 0
		control_msg.angular.z = angular_z

		pub.publish(control_msg)
	
def getAngle(cur):
	return math.atan2(x - cur[0],  y - cur[1])	

def getDistance(cur):
	return np.sqrt(pow(cur[0] - x, 2) + pow(cur[1] - y, 2))

def setDir(curdir):
	angle = getAngle(curdir) * -1 #목표좌표~현재좌표사이의 angle
	#set Angle
	if (angle > theta): #방향에 따라 
		while(theta <= angle): 
			control_msg_publish(0, angle * 0.5)
	else:
		while(theta >= angle): 
			control_msg_publish(0, angle * -0.5)
	#set Distance
	control_msg_publish(getDistance(curdir) * 0.1, 0) #목표~현재좌표의 거리만큼 => xx 너무 빠름 =>.....................

if __name__ == "__main__":
	# set Nodes
	rospy.init_node("foscar_project")
	rospy.Subscriber("/usb_cam/image_raw", Image, image_callback)
	rospy.Subscriber("/turtle1/pose", Pose, pose_callback)
	pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)

	time.sleep(1)
	imgTmp = [0.015, 0.02]
	while not rospy.is_shutdown():
		# 이미지 hsv 변환해서 저장하기
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		dst = cv2.inRange(img_hsv, (160, 150, 50), (180, 255, 255))
		hsvResult = cv2.bitwise_and(img, img, mask=dst)
		nonHsv = hsvResult.nonzero()

		curDir = [nonHsv[1].mean() * imgTmp[0], nonHsv[0].mean() * imgTmp[1]] #색상추출한 곳의 좌표 (turtle과 이미지상이 다름)
		if nonHsv: setDir(curDir) #색상이 추출된 경우
		else: control_msg_publish(0, 0)

		# 거북이 pose 정보 출력
		print("x : ", x)
		print("y : ", y)
		print("theta : ", theta)
		print("")

		# 격자무늬 시각화
		cv2.line(img, (0, 160), (639, 160), (0, 0, 0), 1)
		cv2.line(img, (0, 320), (639, 320), (0, 0, 0), 1)
		cv2.line(img, (210, 0), (210, 480), (0, 0, 0), 1)
		cv2.line(img, (420, 0), (420, 480), (0, 0, 0), 1)

		# 비디오 화면 띄우기
		# 동시에 여러 창 띄우는것도 가능
		cv2.imshow("image", img)
		cv2.imshow("hsv_image", hsvResult)
		if cv2.waitKey(1) & 0xff == ord("q"):
			break

	cv2.destroyAllWindows()
