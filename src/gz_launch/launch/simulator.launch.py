import os
import yaml

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import LogInfo
from launch.actions import EmitEvent, ExecuteProcess
from launch.actions import RegisterEventHandler
from launch.actions import IncludeLaunchDescription
from launch.events import matches_action
from launch.event_handlers import OnProcessStart
from launch_ros.actions import Node
from launch_ros.actions import LifecycleNode
from launch_ros.events.lifecycle import ChangeState
from launch_ros.event_handlers import OnStateTransition
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    
    # Parameter names
    robot_name = "cylinder_bot"
    world_path = "src/gz_sim/worlds/world.sdf"
    sim_pkg = get_package_share_directory("ros_gz_sim")

    # Simulator Node
    gz_sim = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(sim_pkg, "launch", "gz_sim.launch.py")),
            launch_arguments={"gz_args": world_path}.items(),
            )


    # Joystick Node
    gz_joy = Node(
            package="joy",
            executable="joy_node",
            name=robot_name+"_joystick"
            )

    # Thruster Node
    gz_thruster = Node(
            package="ps4_controller",
            executable="thrusters",
            name=robot_name+"_thrusters"
            )

    # Gazebo-ROS Brigde
    gz_bridge = Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=[
                "/model/robot/joint/forward_thruster_joint/cmd_thrust@std_msgs/Float64]gz.msgs.Double",
                "/robot/camera@sensor_msgs/msg/Image[gz.msgs.Image",
                ],
            )
    
    # Launch Description
    return LaunchDescription([
        gz_sim,
        gz_joy,
        gz_thruster,
        gz_bridge
    ])

