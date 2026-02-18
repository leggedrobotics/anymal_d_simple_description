import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory("anymal_d_simple_description")
    default_urdf_path = os.path.join(pkg_share, "urdf", "anymal.urdf")

    description_file = LaunchConfiguration("description_file")
    joint_states_topic = LaunchConfiguration("joint_states_topic")
    robot_description_topic = LaunchConfiguration("robot_description_topic")
    launch_rviz = LaunchConfiguration("launch_rviz")
    launch_joint_state_publisher_gui = LaunchConfiguration("launch_joint_state_publisher_gui")

    robot_description = Command(["cat ", description_file])

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "description_file",
                default_value=default_urdf_path,
                description="Path to the robot URDF file",
            ),
            DeclareLaunchArgument(
                "joint_states_topic",
                default_value="/joint_states_anymal_d",
                description="Joint state topic name",
            ),
            DeclareLaunchArgument(
                "robot_description_topic",
                default_value="/robot_description_anymal_d",
                description="Robot description topic name",
            ),
            DeclareLaunchArgument(
                "launch_joint_state_publisher_gui",
                default_value="false",
                description="Whether to launch joint_state_publisher_gui",
            ),
            DeclareLaunchArgument(
                "launch_rviz",
                default_value="false",
                description="Whether to launch RViz",
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher",
                output="screen",
                parameters=[{"robot_description": robot_description, "rate": 100}],
                remappings=[
                    ("joint_states", joint_states_topic),
                    ("robot_description", robot_description_topic),
                ],
                condition=IfCondition(launch_joint_state_publisher_gui),
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {"robot_description": robot_description},
                    {"publish_frequency": 100.0},
                    {"use_tf_static": True},
                ],
                remappings=[
                    ("joint_states", joint_states_topic),
                    ("robot_description", robot_description_topic),
                ],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz",
                arguments=["-d", os.path.join(pkg_share, "config", "rviz", "standalone.rviz")],
                output="screen",
                condition=IfCondition(launch_rviz),
            ),
        ]
    )
