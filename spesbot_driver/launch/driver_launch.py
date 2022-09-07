import pathlib
import os

from ament_index_python.packages import get_package_share_directory
import launch
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_dir = get_package_share_directory('spesbot_driver')
    robot_description = pathlib.Path(os.path.join(package_dir, 'resource', 'ros2_control.urdf')).read_text()
    controller_params_file = os.path.join(package_dir, 'resource', 'ros2_control.yaml')

    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {'robot_description': robot_description},
            controller_params_file
        ],
        remappings=[
            ('/diffdrive_controller/cmd_vel_unstamped', 'cmd_vel'),
            ('/odom', 'odom'),
            ('/tf', 'tf')
        ],
        output='screen'
    )

    diffdrive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        output='screen',
        arguments=['diffdrive_controller', '--controller-manager-timeout', '50'],
    )

    tf_map_odom = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        output='screen',
        arguments=[
            '--x', '0.0',
            '--frame-id', 'map',
            '--child-frame-id', 'odom'
        ],
    )

    return LaunchDescription([
        diffdrive_controller_spawner,
        tf_map_odom,
        controller_manager_node
    ])