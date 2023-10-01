import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction, SetLaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch.conditions import IfCondition

from launch_ros.actions import Node, PushRosNamespace

def generate_launch_description():
    is_sim_arg = DeclareLaunchArgument(
        'is_sim', default_value=TextSubstitution(text='1')
    ) 
    is_robot1_arg = DeclareLaunchArgument(
        'is_robot1', default_value=TextSubstitution(text='1')
    ) 
    robot_name_arg = DeclareLaunchArgument(
        'robot_name', 
        default_value='robot1'
    )
    IfCondition(
        condition=LaunchConfiguration('is_robot1'),
        actions=[
            SetLaunchConfiguration('robot_name', 'robot1')
        ],
        else_actions=[
            SetLaunchConfiguration('robot_name', 'robot2')
        ]
    )
    
    map_to_odom_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='map_to_odom',
        arguments=['0', '0', '0', '0', '0', '0', 
            LaunchConfiguration('robot_name') + '/map',
            LaunchConfiguration('robot_name') + '/odom',
            '30']
    )

    navigator_node = GroupAction(
        actions=[
            PushRosNamespace(robot_name_arg),
            map_to_odom_node,
                        
        ]
    )