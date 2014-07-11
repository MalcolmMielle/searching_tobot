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
		
	def mult(self, rot):
		#Let Q1 and Q2 be two quaternions, which are defined, respectively, as (w1, x1, y1, z1) and (w2, x2, y2, z2).
		#(Q1 * Q2).w = (w1w2 - x1x2 - y1y2 - z1z2)
		#(Q1 * Q2).x = (w1x2 + x1w2 + y1z2 - z1y2)
		#(Q1 * Q2).y = (w1y2 - x1z2 + y1w2 + z1x2)
		#(Q1 * Q2).z = (w1z2 + x1y2 - y1x2 + z1w2
		
		#Multiplying
		q0 = (q0*rot[0] - q1*rot[1] - q2*rot[2] - q3*rot[3])
		q1 = (q0*rot[1] + q1*rot[0] + q2*rot[3] - q3*rot[2])
		q2 = (q0*rot[2] - q1*rot[3] + q2*rot[0] + q3*rot[1])
		q3 = (q0*rot[3] + q1*rot[2] - q2*rot[1] + q3*rot[0])
		
	def mult_arg(self, rot):
		#Let Q1 and Q2 be two quaternions, which are defined, respectively, as (w1, x1, y1, z1) and (w2, x2, y2, z2).
		#(Q1 * Q2).w = (w1w2 - x1x2 - y1y2 - z1z2)
		#(Q1 * Q2).x = (w1x2 + x1w2 + y1z2 - z1y2)
		#(Q1 * Q2).y = (w1y2 - x1z2 + y1w2 + z1x2)
		#(Q1 * Q2).z = (w1z2 + x1y2 - y1x2 + z1w2
		
		#Multiplying
		rot[0] = (q0*rot[0] - q1*rot[1] - q2*rot[2] - q3*rot[3])
		rot[1] = (q0*rot[1] + q1*rot[0] + q2*rot[3] - q3*rot[2])
		rot[2] = (q0*rot[2] - q1*rot[3] + q2*rot[0] + q3*rot[1])
		rot[3] = (q0*rot[3] + q1*rot[2] - q2*rot[1] + q3*rot[0])
	


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
	
			angle=QuatZ(180)
			
			angle.mult_arg(rot)
			
			
			
			move.goalmaker.move(poseStam)
			
			
	

if __name__ == '__main__':
	main()