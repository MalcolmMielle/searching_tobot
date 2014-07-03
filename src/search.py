#!/usr/bin/env python


import roslib
import rospy
import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

from goalmaker import *

def callback(data):
	rospy.loginfo('Callback')


class Mover:
	def __init__(self):
		self.goalmaker=GoalMaker(True, 1)
		self.flag=False
		




def main():
	rospy.init_node('Search')
	rospy.loginfo('Starting the searching node')
	move=Mover()
	
	rospy.Subscriber("search_state", Bool, callback)
	
	rospy.spin()
	

if __name__ == '__main__':
	main()
	