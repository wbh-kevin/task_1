#!/usr/bin/env python 
import roslib
roslib.load_manifest('learning_tf')

import rospy
import tf
import math
#接受播报并将其转化为播报距离原海龟y轴为2的点，记为carrot1
if __name__ == '__main__':
    rospy.init_node('my_tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        t = rospy.Time.now().to_sec() * math.pi
        br.sendTransform((0.0, 2.0, 0.0),
                        (1.0, 0.0, 0.0, 0.0),
                        rospy.Time.now(),
                        "carrot1",
                        "turtle1")
        rate.sleep()

