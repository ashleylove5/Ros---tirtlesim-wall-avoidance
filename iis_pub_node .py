#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class TurtleControlNode(Node):
    def __init__(self):
        super().__init__('turtle_control')

        # Create a publisher for turtle velocity commands
        self.publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        # Create a subscriber for turtle pose information
        self.subscriber = self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)

        # Create a timer to control the turtle
        self.timer = self.create_timer(0.1, self.control_turtle)

        # Initialize pose and twist variables
        self.pose = None
        self.twist = Twist()

        # Log that the Turtle control node has started
        self.get_logger().info('Turtle control node has been started')

    def pose_callback(self, msg):
        # Update the pose information when a new pose message is received
        self.pose = msg

    def control_turtle(self):
        if self.pose is not None:
            # Calculate the distance to the center of the screen
            distance_to_center = math.sqrt((self.pose.x - 5.5) ** 2 + (self.pose.y - 5.5) ** 2)

            # Check if the turtle is close to a wall
            if self.pose.x < 2 or self.pose.x > 8.5:
                # If it is, turn back
                self.twist.linear.x = 0.8
                self.twist.angular.z = 1.0
            else:
                # If it is not, move towards the center
                self.twist.linear.x = 2.0
                self.twist.angular.z = 0.0

            # Publish the twist command
            self.publisher.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleControlNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
