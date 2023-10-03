import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction, SetLaunchConfiguration, LogInfo
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
    robot_name = LaunchConfiguration('robot_name')
    print(f'robot_name={robot_name}')

    map_file = os.path.join(
        get_package_share_directory('nav2_run'),
        'maps',
        'basic_map.yaml'
    )
    print('map-file=====' + map_file)
    
    map_to_odom_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='map_to_odom',
        arguments=[
            '--frame-id', f'/robot1/map',
            '--child-frame-id', f'/robot1/odom',
        ]
    )

    odom_to_base_link = Node(
        package='nav2_run',
        executable='odometry_sim',
        name='odometry',
        parameters=[
            {'tf_prefix': LaunchConfiguration('robot_name')}
        ]
    )

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        arguments=[
            {'yaml_filename': map_file}
        ]
    )

    use_respawn = True

    navigator_node = GroupAction(
        actions=[
            PushRosNamespace(LaunchConfiguration('robot_name')),
            map_to_odom_node,
            map_server_node,
            odom_to_base_link,

            Node(
                package='nav2_bt_navigator',
                executable='bt_navigator',
                name='bt_navigator',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
                # parameters=[configured_params],
                # arguments=['--ros-args', '--log-level', log_level],
                # remappings=remappings
            ),
            
            Node(
                package='nav2_controller',
                executable='controller_server',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
                # parameters=[configured_params],
                # arguments=['--ros-args', '--log-level', log_level],
                # remappings=remappings + [('cmd_vel', 'cmd_vel_nav')]
            ),
            
            Node(
                package='nav2_planner',
                executable='planner_server',
                name='planner_server',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
                # parameters=[configured_params],
                # arguments=['--ros-args', '--log-level', log_level],
                # remappings=remappings
            ),
            
        ]
    )

    # start_lifecycle_manager_cmd = Node(
    #     package='nav2_lifecycle_manager',
    #     executable='lifecycle_manager',
    #     name='lifecycle_manager',
    #     output='screen',
    #     emulate_tty=True,
    #     parameters=[{'use_sim_time': True},
    #                 {'autostart': True},
    #                 {'node_names': ['map_server'] }])

    return LaunchDescription([
        is_sim_arg,
        is_robot1_arg,
        navigator_node,
    ])