import os
from ament_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():

    pkg_desc   = get_package_share_directory('drone_description')
    pkg_gazebo = get_package_share_directory('gazebo_ros')

    # ---------- Process URDF ----------
    xacro_file = os.path.join(pkg_desc, 'urdf', 'quadrotor.urdf.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # ---------- World ----------
    world_file = os.path.join(pkg_desc, 'config', 'slam_world.world')

    # ---------- Nodes ----------

    # Gazebo server + client
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file, 'verbose': 'false'}.items()
    )

    # Robot State Publisher  →  publishes TF from URDF
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': True,
        }]
    )

    # Spawn the drone entity in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'quadrotor',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.3',    # spawn slightly above ground
        ],
        output='screen'
    )

    # RViz2
    rviz_config = os.path.join(pkg_desc, 'config', 'drone.rviz')
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config] if os.path.exists(rviz_config) else [],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        rviz,
    ])
