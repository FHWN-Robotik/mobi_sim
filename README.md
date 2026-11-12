# mobi_sim
ROS 2 Jazzy Simulationspaket für den mobilen Roboter Mobi mit Gazebo Harmonic.

Dieses Paket enthält die vollständige Roboterbeschreibung und Simulationsumgebung für Mobi, einschließlich des URDF/Xacro-Modells, der Differential-Drive-Steuerung, LiDAR, IMU, Odometry und der RViz-Visualisierung.

## Schnellstart
> [!IMPORTANT]
> **Wenn ROS 2 und alle Abhängigkeiten bereits installiert sind:**

```bash
cd ~/ros2_ws

source /opt/ros/jazzy/setup.bash

colcon build --symlink-install
```
```bash
source install/setup.bash

ros2 launch mobi_sim mobi_gazebo.launch.py
```

Damit sollte die Mobi-Simulation direkt in Gazebo Harmonic starten.

> [!TIP]
> Sorgfältig lesen. :blush:

# Mobi Sim – Inbetriebnahme

## 1. Voraussetzungen

Benötigt werden:

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- `ros_gz_sim`
- `xacro`
- `robot_state_publisher`
- `rviz2`

ROS 2 Jazzy muss vor dem Build gesourced sein:

```bash
source /opt/ros/jazzy/setup.bash
```

## 2. Repo klonen
Falls kein Workspace vorhanden ist:
```bash
mkdir -p ~/ros2_ws/src
```
ansonsten:
```bash
cd ~/ros2_ws/src
git clone <GITHUB-REPOSITORY-URL>
```

danach:
```bash
cd ~/ros2_ws
```

## 3. Abhängigkeiten installieren
```bash
sudo apt update

sudo apt install -y \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-rviz2 \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-ros-gz-bridge
```

## 4. Package bauen
```bash
cd ~/ros2_ws

source /opt/ros/jazzy/setup.bash

colcon build --symlink-install
```
```bash
source install/setup.bash
```

## 5. Mobi in Gazebo starten
```bash
cd ~/ros2_ws

source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch mobi_sim mobi_gazebo.launch.py
```

## 6. ROS 2 Topics überprüfen

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 topic list
```

Wichtige Topics:
/cmd_vel
/odom
/scan
/imu
/tf
/tf_static
/joint_states
/robot_description

## 7. Mobi bewegen

Zum Testen langsam fahren:
```bash
ros2 topic pub -r 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1}, angular: {z: 0.0}}"
```
Der Roboter fährt mit 0.1 m/s geradeaus.

Zum Stoppen:
```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
```
## 8. RViz2
```bash
ros2 run rviz2 rviz2
```
