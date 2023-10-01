import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():
    basic_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('nav2_run'), 'launch'), 
            '/basic.launch.py']),
        launch_arguments={
            'is_robot1': '1',
            'is_sim': '1'
        }.items()
    )
    rviz_config = os.path.join(
        get_package_share_directory('nav2_run'),
        'rviz',
        'rviz_sim.rviz'
    )
    rviz_node = Node(
         package='rviz2',
         executable='rviz2',
         name='rviz2',
         arguments=['-d', rviz_config]
    )
    

    return LaunchDescription([
        basic_node,
        rviz_node 
    ])