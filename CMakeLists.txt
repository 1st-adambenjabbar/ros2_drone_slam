cmake_minimum_required(VERSION 3.8)
project(drone_description)

find_package(ament_cmake REQUIRED)

# Install all directories
install(DIRECTORY
  urdf
  launch
  meshes
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
