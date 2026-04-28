# ROS2 Drone SLAM

A simulated quadrotor drone that autonomously maps its environment using SLAM (Simultaneous Localization And Mapping), built with **ROS2 Humble** and **Gazebo**.

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Gazebo](https://img.shields.io/badge/Gazebo-Classic-orange)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-green)
![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)

##  Project Overview
This project simulates a quadrotor UAV in a closed indoor environment. The drone is equipped with:
- A **2D Lidar** (360° laser scanner) for environment sensing
- An **IMU** (Inertial Measurement Unit) for orientation and acceleration data
- A **Planar motion plugin** for keyboard-controlled flight
Using this sensor data, **SLAM Toolbox** builds a real-time 2D map of the environment while the drone flies around.
---
## 🗂️ Project Structure
```
ros2_drone_slam_ws/
└── src/
    ├── drone_description/      # URDF model + Gazebo world + launch
    │   ├── urdf/
    │   │   └── quadrotor.urdf.xacro   # Drone blueprint (body, rotors, sensors)
    │   ├── config/
    │   │   ├── slam_world.world       # Gazebo environment (room + obstacles)
    │   │   └── drone.rviz             # RViz2 visualization config
    │   ├── launch/
    │   │   └── spawn_drone.launch.py  # Main launch file
    │   ├── package.xml
    │   └── CMakeLists.txt
    │
    ├── drone_control/          # (coming soon) Keyboard teleop + velocity control
    ├── drone_slam/             # (coming soon) SLAM Toolbox configuration
    └── drone_bringup/          # (coming soon) Master launch for everything
```

---

## ⚙️ Prerequisites

- Ubuntu 22.04
- ROS2 Humble
- Gazebo Classic (comes with ROS2 Humble)

---
## 📦 Installation
### 1. Clone the repository
```bash
git clone https://github.com/mee-113/ros2_drone_slam.git ~/ros2_drone_slam_ws
cd ~/ros2_drone_slam_ws
```
### 2. Install dependencies
```bash
sudo apt update
sudo apt install -y \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher \
  ros-humble-xacro \
  ros-humble-rviz2 \
  ros-humble-slam-toolbox \
  ros-humble-teleop-twist-keyboard
```
### 3. Build the workspace
```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```
---
## Usage
###Launh the simulation
```bash
ros2 launch drone_description spawn_drone.launch.py
```
This opens:
- **Gazebo** — 3D simulation with the drone and obstacles
- **RViz2** — live visualization of the drone, lidar scan and transforms

### Control the drone (in a new terminal)

```bash
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

| Key | Action        |
|-----|---------------|
| `i` | Forward       |
| `,` | Backward      |
| `j` | Turn left     |
| `l` | Turn right    |
| `k` | **Stop**      |
| `q` | Speed up      |
| `z` | Speed down    |

### Check active topics

```bash
ros2 topic list
ros2 topic echo /scan   # live lidar data
ros2 topic echo /odom   # live drone position
```

---

## 🏗️Architecture

```
Keyboard Input
      ↓ /cmd_vel
Gazebo planar_move plugin  →  moves drone in simulation
      ↓ /odom
Robot Localization (EKF)   →  fuses IMU + odometry
      ↓
Lidar Plugin               →  publishes /scan (360° laser)
      ↓
SLAM Toolbox               →  builds 2D map in real time
      ↓
RViz2                      →  displays everything visually
```

---

## 🗺️ Gazebo World

The simulation environment is a **10×10 meter indoor room** containing:
- 4 surrounding walls
- 2 box obstacles
- 1 cylindrical obstacle
- 1 inner wall partition

These obstacles are intentional — SLAM requires unique environmental features to localize correctly.
---
##  Roadmap
- [x] Drone URDF model (body, arms, rotors, lidar, IMU)
- [x] Gazebo world with obstacles
- [x] Launch file (Gazebo + RViz2 + robot_state_publisher)
- [ ] Keyboard teleoperation package
- [ ] SLAM Toolbox integration
- [ ] Map saving and loading
- [ ] Nav2 autonomous navigation
---
##  Author
**Adam Benjabbar**
- GitHub: [@1st-adambenjabbar](https://github.com/1st-adambenjabbar)
