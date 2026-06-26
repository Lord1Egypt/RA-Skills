# Official ROS1/Noetic Sources

Use these sources as primary references when implementing or validating ROS1 Noetic behavior.

## Core docs

1. ROS Noetic docs index (official)
   - http://docs.ros.org/en/noetic/

2. `roscpp` API docs (official)
   - http://docs.ros.org/en/noetic/api/roscpp/html/

3. `rosbag` package docs (official)
   - http://docs.ros.org/en/noetic/api/rosbag/html/index.html

4. ROS package index (official)
   - `roscpp`: https://index.ros.org/p/roscpp/
   - `rospy`: https://index.ros.org/p/rospy/
   - `catkin`: https://index.ros.org/p/catkin/
   - `roslaunch`: https://index.ros.org/p/roslaunch/
   - `rosbag`: https://index.ros.org/p/rosbag/
   - `rosservice`: https://index.ros.org/p/rosservice/
   - `rostopic`: https://index.ros.org/p/rostopic/
   - `tf`: https://index.ros.org/p/tf/
   - `tf2_ros`: https://index.ros.org/p/tf2_ros/
   - `actionlib`: https://index.ros.org/p/actionlib/
   - `rosbridge_server`: https://index.ros.org/p/rosbridge_server/
   - `rosdep`: https://index.ros.org/p/rosdep/

## ROS wiki pages reviewed via browser (official)

- https://wiki.ros.org/noetic/Installation/Ubuntu
- https://wiki.ros.org/ROS/Tutorials
- https://wiki.ros.org/ROS/Concepts
- https://wiki.ros.org/Names
- https://wiki.ros.org/roscpp/Tutorials
- https://wiki.ros.org/rospy/Tutorials
- https://wiki.ros.org/catkin/Tutorials
- https://wiki.ros.org/roslaunch
- https://wiki.ros.org/tf/Tutorials
- https://wiki.ros.org/rosbag/Commandline
- https://wiki.ros.org/actionlib
- https://wiki.ros.org/rosbridge_suite
- https://wiki.ros.org/rosdep

## Access guidance

The ROS wiki may present anti-bot JavaScript challenges in automated fetch contexts.

If blocked:

1. keep `docs.ros.org` + `index.ros.org` as reliable machine-readable sources
2. use whatever browsing or browser-automation tools the host runtime actually exposes
3. if no browsing tools are available, rely on machine-readable docs and be explicit about the gap

Do not conclude "docs unavailable" before attempting browser-based access.

## Safety note for command examples

Official docs may show setup commands such as package installation, `sudo`, or machine initialization.

- Ask for confirmation before running those commands in a user environment.
- Treat `sudo rosdep init` as a one-time machine setup step, not a routine workspace command.
- Treat robot-motion examples as simulation-first unless the user clearly approved real hardware motion.

## Practical interpretation for OpenClaw + ROS1

- Use docs.ros.org API pages for interface-level correctness.
- Use index.ros.org pages for package status / maintenance / dependencies.
- Use wiki pages for procedural tutorials, architecture notes, and operational caveats.
- For rosbridge/OpenClaw usage, prefer interface docs plus your own deployment contract over generic tutorial assumptions.
