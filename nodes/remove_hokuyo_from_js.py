#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState


def hokuyo_joint_remover():
    rospy.init_node('hokuyo_joint_remover')

    js_out_pub = rospy.Publisher('joint_states_out', JointState, queue_size=1)

    def callback(msg):
        msg2 = JointState()
        names = list(msg.name)
        if 'hokuyo_joint' in names:
            velocities = list(msg.velocity)
            efforts = list(msg.effort)
            positions = list(msg.position)
            index = names.index('hokuyo_joint')
            del positions[index]
            del velocities[index]
            del efforts[index]
            del names[index]
            rospy.loginfo('removed hokuyo joint')
            msg2.name = tuple(names)
            msg2.effort = tuple(efforts)
            msg2.velocity = tuple(velocities)
            msg2.position = tuple(positions)
            js_out_pub.publish(msg2)
        else:
            js_out_pub.publish(msg)
    rospy.Subscriber('joint_states_in', JointState, callback)

    rospy.spin()


if __name__ == '__main__':
    hokuyo_joint_remover()
