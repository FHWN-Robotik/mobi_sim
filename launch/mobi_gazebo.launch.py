import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    package_name = 'mobi_sim'

    package_share = get_package_share_directory(package_name)

    xacro_file = os.path.join(
        package_share,
        'urdf',
        'mobi.urdf.xacro'
    )

    world_file = os.path.join(
        package_share,
        'worlds',
        'empty.sdf'
    )

    # ---------------------------------------------------------
    # Robot description
    # ---------------------------------------------------------

    robot_description = Command([
        'xacro ',
        xacro_file
    ])

    # ---------------------------------------------------------
    # Robot State Publisher
    # ---------------------------------------------------------

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': ParameterValue(
                    robot_description,
                    value_type=str
                ),
                'use_sim_time': True
            }
        ]
    )

    # ---------------------------------------------------------
    # Gazebo Harmonic
    # ---------------------------------------------------------

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': world_file + ' -r'
        }.items()
    )

    # ---------------------------------------------------------
    # Spawn robot
    # ---------------------------------------------------------

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'mobi',
            '-topic', 'robot_description',
            '-x', '0',
            '-y', '0',
            '-z', '0.15'
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            # /scan is bridged separately by laser_bridge (sets frame_id to laser_frame)
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/model/mobi/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/world/empty/model/mobi/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
        ],
        remappings=[
            ('/model/mobi/tf', '/tf'),
            ('/world/empty/model/mobi/joint_state', '/joint_states')
        ],
        output='screen'
    )

    laser_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'
        ],
        parameters=[
            {'override_frame_id': 'laser_frame'}
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        bridge,
        laser_bridge,
        spawn_robot
    ])