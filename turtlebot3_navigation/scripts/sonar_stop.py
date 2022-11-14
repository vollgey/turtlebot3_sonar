#!/usr/bin/env python3        

import os
import rospy
import tf 
from sensor_msgs.msg import Range
from actionlib_msgs.msg import GoalID

class SonarStop():
    def __init__(self):
        rospy.on_shutdown(self.shutdown)
        self.distance = -100 #distance from ultrasonic_sensor
    
    def shutdown(self):
        rospy.loginfo("subscribed")
        rospy.loginfo("The robot was terminated.")                               
        # self.ac.cancel_goal()

    def cancelGoal(self):
        cancel_pub = rospy.Publisher("/move_base/cancel", GoalID, queue_size=1)
        cancel_msg = GoalID()
        cancel_pub.publish(cancel_msg)
        print("published cancel_goal signal")

    def sonarCallback(self, msg):
        rospy.loginfo(int(msg.range))
        self.distance = int(msg.range)

    def process(self):
        if (0<self.distance<10):
            self.cancelGoal()

    def rosinit(self):
        rospy.init_node('sonarStop', anonymous=True)
        rospy.Subscriber("/sonar", Range, self.sonarCallback)
        while not rospy.is_shutdown():
            self.process()

if __name__ == '__main__':
    try:
        sonar_stop = SonarStop()
        sonar_stop.rosinit()

    except rospy.ROSInterruptException:
        pass
