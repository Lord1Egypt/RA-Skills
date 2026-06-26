# ROS1 Noetic Full Scope (General)

This reference is a **project-agnostic ROS1 Noetic capability map** distilled from official ROS Wiki / docs.ros.org / index.ros.org pages.

For concrete implementation patterns (node design, callback threading, nodelets, dynamic_reconfigure, migration tactics), also read: `ros1-engineering-patterns.md`.

## 1) Core architecture and graph concepts

From ROS Concepts and Names documentation:

- Node: executable ROS process
- Master (`roscore`): registration/lookup for graph resources
- Parameter server: key-value config store
- Topic: asynchronous pub/sub transport
- Service: request/reply RPC
- Action: preemptable long-running task (goal/feedback/result)
- Bag: record/replay ROS message streams
- Names and remapping: namespace-scoped composition primitive

## 2) Names, namespace, remapping (must-know)

### Name kinds

- relative: `camera/image_raw`
- global: `/camera/image_raw`
- private: `~rate`

### Resolution and remapping checks

```zsh
rosnode info <node>
rosparam list
rosparam get <param>
```

Rules:

- avoid hard-coded global names unless required
- prefer relative/private names inside reusable nodes
- use launch remapping to integrate subsystems safely

## 3) Workspace, package, build, dependencies

### Catkin lifecycle

```zsh
source /opt/ros/noetic/setup.zsh
mkdir -p <ws>/src
cd <ws>
catkin_make
source devel/setup.zsh
```

### rosdep workflow

```zsh
# one-time init, only with user approval
# sudo rosdep init

# update as normal user (no sudo)
rosdep update

# install workspace deps only after user approval
# rosdep install --from-paths src --ignore-src -r -y
```

Notes:

- ROS wiki explicitly warns: do **not** run `rosdep update` with sudo
- `rosdep init` is machine-level setup, not a routine per-workspace step
- prefer apt installation paths for Noetic tooling where available

## 4) Launch system and orchestration

`roslaunch` responsibilities:

- start multi-node systems
- apply params/remaps/namespaces
- support local + remote machine launch (SSH)

Core references include `roslaunch/XML`, architecture docs, and command-line tools.

Useful commands:

```zsh
roslaunch --help
roslaunch <pkg> <file.launch>
```

### Launch file quality gate

Use catkin launch checks in CI/tests:

- `find_package(roslaunch REQUIRED)`
- `roslaunch_add_file_check(launch)`

## 5) Runtime graph diagnostics

### Nodes

```zsh
rosnode list
rosnode info <node>
```

### Topics

```zsh
rostopic list
rostopic type <topic>
rostopic hz <topic>
rostopic echo -n 1 <topic>
```

### Services

```zsh
rosservice list
rosservice type <service>
rosservice info <service>
```

### Parameters

```zsh
rosparam list
rosparam get <param>
rosparam set <param> <value>
```

## 6) Client library coverage

### roscpp (C++)

Key APIs from official docs:

- `ros::init`
- `ros::NodeHandle`
- `ros::param`, `ros::service`, `ros::master`, `ros::names`

### rospy (Python)

Focus areas from official tutorials:

- publisher/subscriber
- service/client
- parameter operations
- logging to rosout
- timer/rate patterns

## 7) TF / tf2 coverage

From tf tutorials and concepts:

- broadcaster/listener patterns (C++ + Python)
- time-aware transform lookup
- frame graph debugging
- robot setup with robot_state_publisher

Diagnostics:

```zsh
rosrun tf view_frames
rosrun tf tf_echo <from_frame> <to_frame>
```

Prefer tf2 for new development where possible (tf remains common in ROS1 stacks).

## 8) Actionlib coverage

Actionlib provides preemptable task semantics.

- goal states: pending/active/succeeded/aborted/preempted/etc.
- interfaces: `SimpleActionClient` / `SimpleActionServer`
- verify goal/result types and timeout/cancel logic

Action namespace inspection pattern:

- `/<name>/goal`
- `/<name>/feedback`
- `/<name>/result`
- `/<name>/status`
- `/<name>/cancel`

## 9) rosbag full workflow

From official commandline docs:

- `record`, `info`, `play`
- `check`, `fix`, `filter`
- `compress`, `decompress`, `reindex`

Examples:

```zsh
rosbag record /topic_a /topic_b
rosbag info my.bag
rosbag play my.bag --clock
```

Operational tips:

- for high-bandwidth data, record on data-source machine
- keep bag metadata (scenario, topic set, clock mode)
- prefer selective recording over `-a` unless explicitly needed

## 10) Multi-machine ROS1

For distributed setups:

- keep network/DNS/hostnames consistent
- configure `ROS_MASTER_URI` and host/IP identity carefully
- validate cross-machine topic visibility before application debug

## 11) OpenClaw ↔ ROS1 adaptation (rosbridge mode)

Use `rosbridge_suite` when OpenClaw must control ROS1 through websocket.

- protocol supports topic pub/sub, services, params
- default endpoint commonly `ws://<host>:9090`
- prefer a narrow approved interface surface instead of exposing the full graph
- subscribe to telemetry before sending commands
- prefer a ROS-side adapter node for complex task semantics or action workflows

Start pattern:

```zsh
source /opt/ros/noetic/setup.zsh
roslaunch rosbridge_server rosbridge_websocket.launch
```

Message templates:

```json
{"op":"advertise","topic":"/cmd_vel","type":"geometry_msgs/Twist"}
{"op":"publish","topic":"/cmd_vel","msg":{"linear":{"x":0.2,"y":0.0,"z":0.0},"angular":{"x":0.0,"y":0.0,"z":0.0}}}
{"op":"subscribe","topic":"/odom","type":"nav_msgs/Odometry","throttle_rate":200}
{"op":"call_service","service":"/start_task","args":{"mode":"inspect"}}
```

Action note:

- rosbridge is straightforward for topics/services
- for actionlib, prefer an existing ROS-side adapter or explicitly manage `goal` / `feedback` / `result` / `status` / `cancel` topics after type checks

## 12) Safety baseline (mandatory)

- conservative default speed/step values
- explicit timeout for each long operation
- stop/neutral command on success and failure paths
- reject execution when telemetry is stale/missing
- report measured result (distance/yaw/state), not only intent
- ask for confirmation before real-hardware motion
- treat websocket disconnect as a failure that still requires stop-state verification

## 13) Coverage checklist before claiming “done”

- [ ] Build + dependency path validated (catkin + rosdep)
- [ ] Launch and namespace/remap behavior validated
- [ ] Topic/service/action interfaces type-checked
- [ ] TF frame chain and timestamps validated
- [ ] rosbag record/replay path validated
- [ ] rosbridge path validated when OpenClaw integration is required
- [ ] approved OpenClaw control surface documented (endpoint + allowed interfaces + stop path)
- [ ] safety stop + timeout semantics validated
