#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry

class DroneController:
    def __init__(self, drone_id, odom_topic="visual_slam/odom"):
        self.drone_id = drone_id
        self.odom_topic = odom_topic

        # Publisher for waypoint
        self.waypoint_pub = rospy.Publisher(
            f"/drone_{self.drone_id}_planning/waypoint",
            PoseStamped,
            queue_size=10
        )

        # Subscriber for odometry
        self.odom_sub = rospy.Subscriber(
            f"/drone_{self.drone_id}_{self.odom_topic}",
            Odometry,
            self.odom_callback
        )

    def odom_callback(self, msg):
        # Process odometry feedback here
        position = msg.pose.pose.position
        print(f"Drone {self.drone_id} position: x={position.x}, y={position.y}, z={position.z}")

    def publish_waypoint(self, x, y, z, yaw=0.0):
        waypoint = PoseStamped()
        waypoint.header.stamp = rospy.Time.now()
        waypoint.header.frame_id = "world"
        waypoint.pose.position.x = x
        waypoint.pose.position.y = y
        waypoint.pose.position.z = z

        # You can set orientation if needed (here using only yaw)
        # Currently using simple quaternion with no rotation
        waypoint.pose.orientation.w = 1.0

        self.waypoint_pub.publish(waypoint)
        print(f"Published waypoint to Drone {self.drone_id}: ({x}, {y}, {z})")

if __name__ == "__main__":
    rospy.init_node("drone_controller")

    # Example: control drone_0
    controller = DroneController(drone_id=0)

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        # Example waypoint
        controller.publish_waypoint(19.0, 15.0, 1.0)
        rate.sleep()
