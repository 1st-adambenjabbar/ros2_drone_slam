# ROS2 Drone SLAM

Un drone quadrotor simulé qui cartographie de manière autonome son environnement en utilisant le SLAM (Simultaneous Localization And Mapping), construit avec **ROS2 Humble** et **Gazebo**.

![Drone Simulation Demo](https://private-us-east-1.manuscdn.com/sessionFile/ESokvG6NaM8fsZUz6430c3/sandbox/OAyKO9aqAKExUsctfu3WVD-images_1777405804074_na1fn_L2hvbWUvdWJ1bnR1L3JvczJfZHJvbmVfc2xhbS9kcm9uZV9kZW1v.gif?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvRVNva3ZHNk5hTThmc1pVejY0MzBjMy9zYW5kYm94L09BeUtPOWFxQUtFeFVzY3RmdTNXVkQtaW1hZ2VzXzE3Nzc0MDU4MDQwNzRfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzSnZjekpmWkhKdmJtVmZjMnhoYlM5a2NtOXVaVjlrWlcxdi5naWYiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=WGKA6fFlFXwrx1LJt0GqTX1CBpiE-2R65ewTNoKRf6GEchS3VPpHarEW26rDBxNdlqzrF5lO8KbvLVrIC-O51HJ0FLFgp1LhsB4ZokVavgpHApw2-op2BZuAd1Qm3T9DfsPnLVp3iF-SBB7wER5EGjgohsd06QyjeE0xkIZUhANBa3-2JvZY0F6mlUzjX1JJwn-yog6hX4QS4zt94kUZS4zmYu7MxzJbbqRx6Xh5MZY3Of5TQTa9azSvU2C7Ki5q3~uy5z-F7bSuWjjLWAZNIsgwTsFQISj~KdNSR5mOG16M9T100QZoT7Vf-KePTqHQzqbxls-CZ5QtH8TnNYGDaw__)

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Gazebo](https://img.shields.io/badge/Gazebo-Classic-orange)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-green)
![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)

## Aperçu du projet
Ce projet simule un drone quadrotor UAV dans un environnement intérieur fermé. Le drone est équipé de :
- Un **Lidar 2D** (scanner laser 360°) pour la détection de l'environnement
- Une **IMU** (Inertial Measurement Unit) pour les données d'orientation et d'accélération
- Un **plugin de mouvement planaire** pour le vol contrôlé au clavier
En utilisant ces données de capteurs, **SLAM Toolbox** construit une carte 2D en temps réel de l'environnement pendant que le drone vole.

---
## 🗂️ Structure du projet
```
ros2_drone_slam_ws/
└── src/
    └── drone_description/      # URDF model + Gazebo world + launch
        ├── urdf/
        │   └── quadrotor.urdf.xacro   # Drone blueprint (body, rotors, sensors)
        ├── config/
        │   ├── slam_world.world       # Gazebo environment (room + obstacles)
        │   ├── drone.rviz             # RViz2 visualization config
        │   └── test_gazebo_spawn.py   # Automated test for Gazebo spawn
        ├── launch/
        │   ├── spawn_drone.launch.py  # Main launch file
        │   └── rotor_animation.py     # Script for rotor animation
        ├── package.xml
        └── CMakeLists.txt
```

---

## ⚙️ Prérequis

- Ubuntu 22.04
- ROS2 Humble
- Gazebo Classic (fourni avec ROS2 Humble)

---
## 📦 Installation
### 1. Cloner le dépôt
```bash
git clone https://github.com/1st-adambenjabbar/ros2_drone_slam.git ~/ros2_drone_slam_ws/src/drone_description
cd ~/ros2_drone_slam_ws
```
### 2. Installer les dépendances
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
### 3. Construire l'espace de travail
```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```
---
## Utilisation
### Lancer la simulation
```bash
ros2 launch drone_description spawn_drone.launch.py
```
Ceci ouvre :
- **Gazebo** — Simulation 3D avec le drone et les obstacles, incluant l'animation des rotors.
- **RViz2** — Visualisation en direct du drone, du scan lidar et des transformations.

### Contrôler le drone (dans un nouveau terminal)

```bash
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

| Touche | Action        |
|-----|---------------|
| `i` | Avancer       |
| `,` | Reculer      |
| `j` | Tourner à gauche     |
| `l` | Tourner à droite    |
| `k` | **Arrêter**      |
| `q` | Accélérer      |
| `z` | Ralentir    |

### Vérifier les topics actifs

```bash
ros2 topic list
ros2 topic echo /scan   # données lidar en direct
ros2 topic echo /odom   # position du drone en direct
```

---

## 🧪 Tests automatisés
Pour vérifier que le drone est correctement spawné dans Gazebo, vous pouvez exécuter le script de test :
```bash
source /opt/ros/humble/setup.bash
ros2 run drone_description test_gazebo_spawn.py
```
Ce test vérifiera la présence de l'entité 'quadrotor' dans Gazebo et affichera un message de succès ou d'échec.

---

## 🏗️ Architecture

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

## 🗺️ Monde Gazebo

L'environnement de simulation est une **pièce intérieure de 10×10 mètres** contenant :
- 4 murs périphériques
- 2 obstacles en forme de boîte
- 1 obstacle cylindrique
- 1 cloison intérieure

Ces obstacles sont intentionnels — le SLAM nécessite des caractéristiques environnementales uniques pour se localiser correctement.
---
##  Feuille de route
- [x] Modèle URDF du drone (corps, bras, rotors, lidar, IMU)
- [x] Monde Gazebo avec obstacles
- [x] Fichier de lancement (Gazebo + RViz2 + robot_state_publisher)
- [ ] Package de téléopération au clavier
- [ ] Intégration de SLAM Toolbox
- [ ] Sauvegarde et chargement de la carte
- [ ] Navigation autonome Nav2
- [x] Animation des rotors
- [x] Test automatisé de spawn Gazebo
---
##  Auteur
**Adam Benjabbar**
- GitHub: [@1st-adambenjabbar](https://github.com/1st-adambenjabbar)
---
## 📄 Licence
Ce projet est sous licence Apache 2.0.
