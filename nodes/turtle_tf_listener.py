#!/usr/bin/env python 

import roslib
roslib.load_manifest('learning_tf')
from nav_msgs.msg import Odom3try
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv
import time

def cmd_vel_cb(msg):
    odom = Odemetry()
    odom.header.frame_id = "odom"
    ct = rospy.Time.now()
    vx = msg.linear.x
    vy = msg.linear.y
    vtheta = msg.angular.z
    dx = ( vx * math.cos(th) - vy * math.sin(th) )*0.01
    dy = ( vx * math.sin(th) + vy * math.cos(th) )*0.01
    dtheta = vtheta * 0.01
    global x
    global y
    global theta
    x += dx
    y += dy
    theta += dtheta
    odom.header.stamp = ct
    q = quaternion_from_euler ( 0, 0, theta)
    odom.pose.pose.position.x = x
    odom.pose.pose.position.y = y
    odom.pose.pose.position.z = 0.0
    odom.pose.pose.orientation.x = q[0]
    odom.pose.pose.orientation.y = q[1]
    odom.pose.pose.orientation.z = q[2]
    odom.pose.pose.orientation.w = q[3]
    rospy.loginfo ("call back")
    pub.publish(odom);


if __name__ == '__main__':
    
    

    rospy.init_node('turtle1_odom')
    sub = rospy.Subscriber("turtle1/listener", Twist, cmd_vel_cb)
    pub = rospy.Publisher("turtle1/odom", Odometry, queue_size = 10010)
    #里程计
    
    rospy.init_node('tf_turtle')
    listener = tf.TransformListener()

    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(4, 6, 0, 'turtle2')
#生成turtle2
    turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist, queue_size=1)
    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/turtle2', '/carrot1',rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
#接受自己相对于carrot1坐标系的位姿
        angular = 10 * math.atan2(trans[1], trans[0])
        linear = 5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel.publish(cmd)
#设置线速度与角速度    
        rate.sleep()

