import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from std_msgs.msg import Float64


class ThrusterController(Node):

    def __init__(self):
        super().__init__("thruster_controller")
        self.vel_publisher = self.create_publisher(Float64, "/model/robot/joint/forward_thruster_joint/cmd_thrust", 10)
        self.joy_subscriber = self.create_subscription(Joy, "/joy", self.callback, 10)

    def callback(self, msg):
        thruster_value = msg.axes[4]
        # Deadzone in case of bad joystick
        if (abs(thruster_value) < 0.05):
            thruster_value = 0.0
        
        msg = Float64()
        msg.data = thruster_value
        self.vel_publisher.publish(msg)




def main(args=None):
    rclpy.init(args=args)
    thruster_controller = ThrusterController()
    rclpy.spin(thruster_controller)
    thruster_controller.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

