#!/usr/bin/env python


import roslib
import rospy
import actionlib
import tf
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import *

from goalmaker import *

def callback(data, move):
	rospy.loginfo('Callback ')
	print 'we read ' +str(data)
	#print move.goalmaker.time_to_obj
	move.flag=data.data


class Mover:
	def __init__(self):
		self.goalmaker=GoalMaker(True, 1)
		self.flag=False
		

class QuatZ(object):
	def __init__(angle):
		self.q0=cos(angle/2)
		self.q1=0
		self.q2=0
		self.q3=cos(angle/2)
		
	def add(self, rot):
		
	


def main():
	rospy.init_node('Search')
	rospy.loginfo('Starting the searching node')
	move=Mover()
	
	rospy.Subscriber("search_state", Bool, callback, callback_args=move)
	
	listener = tf.TransformListener()
	listener.waitForTransform("/map", "/base_link", rospy.Time(), rospy.Duration(4.0))
	while not rospy.is_shutdown():
		if move.flag==True:
			print 'flag is true'
			now = rospy.Time.now()
			listener.waitForTransform("/map", "/base_link", now, rospy.Duration(4.0))
			(trans,rot) = listener.lookupTransform("/map", "/base_link", now)
			
			print 'position : ' + str(trans[0]) +' '+ str(trans[1])+' '+ str(trans[2]) + ' oritentation ' + str(rot[0]) +' '+ str(rot[1]) +' '+ str(rot[2]) +' '+ str(rot[3]) +' '
			poseStam = PoseStamped()
			
			poseStam.pose.position.x=trans[0]
			poseStam.pose.position.y=trans[1]
			poseStam.pose.position.z=trans[2]
			
			poseStam.pose.orientation.x=rot[0]
			poseStam.pose.orientation.y=rot[1]
			poseStam.pose.orientation.z=rot[2]
			poseStam.pose.orientation.w=rot[3]
			
			#add two quaternion is multiplying them
				#We want a plane and orientation only around the z axis.
			"""Quaternion : 
			q[0]=cos(r/2)
			q[1]=cos(r/2)*x
			q[2]=cos(r/2)*y
			q[3]=cos(r/2)*z
			
			So we 0 out the y and x"""
			#print str(ud.pose_user.position.x)
	
			
			
			move.goalmaker.move(poseStam)
			
			
	

if __name__ == '__main__':
	main()