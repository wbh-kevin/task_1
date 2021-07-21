#!/usr/bin/env python 

import roslib
roslib.load_manifest('learning_tf')
import rospy
import tf
import turtlesim.msg

def handle_turtle_pose(msg, turtlename):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x+4, msg.y, 0),
                    tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                    rospy.Time.now(),
                    turtlename,
                    "world")
#播报一个距离海龟x轴为4的点
if __name__ == '__main__':
    rospy.init_node('turtle_tf_broadcaster')
    turtlename = rospy.get_param('~turtle')
    rospy.Subscriber('/%s/pose' % turtlename,
                    turtlesim.msg.Pose,
                    handle_turtle_pose,
                    turtlename)
    rospy.spin()
