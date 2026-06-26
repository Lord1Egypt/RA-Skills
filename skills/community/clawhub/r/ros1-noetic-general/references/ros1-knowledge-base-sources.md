# ROS1 Knowledge Base Sources (2026-03-24)

Purpose: serve as the source ledger for this ROS1 knowledge base, documenting which official ROS1/Noetic pages were reviewed while expanding the skill.

## A) ROS Wiki pages reviewed via browser

1. `noetic/Installation/Ubuntu`
2. `ROS/Tutorials`
3. `ROS/Concepts`
4. `Names`
5. `roscpp/Tutorials`
6. `rospy/Tutorials`
7. `catkin/Tutorials`
8. `roslaunch`
9. `tf/Tutorials`
10. `rosbag/Commandline`
11. `actionlib`
12. `rosbridge_suite`
13. `rosdep`

## B) docs.ros.org pages reviewed

- Noetic docs index (`/en/noetic/`)
- roscpp API overview (`/en/noetic/api/roscpp/html/index.html`)
- rosbag API/index (`/en/noetic/api/rosbag/html/index.html`)
- actionlib API overview (`/en/noetic/api/actionlib/html/index.html`)

## C) index.ros.org package pages reviewed

- `roscpp`
- `rospy`
- `catkin`
- plus references for `roslaunch`, `rosbag`, `rosservice`, `rostopic`, `tf`, `tf2_ros`, `actionlib`, `rosbridge_server`, `rosdep`

## D) Key additions made to skill after review

- Strengthened full-scope reference: core graph, naming/remapping, catkin, rosdep, launch, diagnostics, tf/tf2, actionlib, rosbag, multi-machine, rosbridge.
- Added/kept zsh-first execution conventions.
- Added explicit anti-bot fallback rule: use browser when wiki fetch is blocked.
- Kept project-agnostic design (mobile base + manipulator + data + integration workflows).

## E) Boundaries

ROS1 documentation is large and package ecosystem is extensive. This review covers the official core/tutorial/package documentation surfaces most relevant to practical Noetic engineering and OpenClaw integration.
