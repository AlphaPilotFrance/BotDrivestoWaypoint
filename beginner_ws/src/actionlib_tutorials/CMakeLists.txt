cmake_minimum_required(VERSION 2.8.3)
project(actionlib_tutorials)

find_package(catkin REQUIRED COMPONENTS roscpp actionlib actionlib_msgs std_msgs message_generation)
find_package(Boost REQUIRED COMPONENTS system)

add_action_files(
  DIRECTORY action
  FILES Fibonacci.action
  FILES Averaging.action
  FILES Machine.action
)

generate_messages(
  DEPENDENCIES actionlib_msgs std_msgs
)

catkin_package(
  CATKIN_DEPENDS actionlib_msgs
)

include_directories(include ${catkin_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

add_executable(fibonacci_server src/fibonacci_server.cpp)

target_link_libraries(
  fibonacci_server

  ${catkin_LIBRARIES}
)

add_dependencies(
  fibonacci_server
  ${actionlib_tutorials_EXPORTED_TARGETS}
)

#find_package(catkin REQUIRED COMPONENTS actionlib std_msgs message_generation) 
#add_action_files(DIRECTORY action FILES Averaging.action)
#generate_messages(DEPENDENCIES std_msgs actionlib_msgs)

add_executable(averaging_client src/averaging_client.cpp)
target_link_libraries(averaging_client ${catkin_LIBRARIES})

add_executable(averaging_server src/averaging_server.cpp)
target_link_libraries(averaging_server ${catkin_LIBRARIES})



