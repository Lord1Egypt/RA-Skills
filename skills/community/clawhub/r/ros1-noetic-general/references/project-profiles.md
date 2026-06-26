# ROS1 Noetic Project Profiles

Use this file to choose commands/checklists based on project type.

Assume bundled helper scripts are resolved relative to the skill directory, not the user's project cwd.

Terms used below:

- `bringup`: the path from sourced environment to a runnable ROS graph
- `rosbridge`: a websocket-facing bridge for topic/service/parameter access into ROS

## A) Bringup / Build Profile

### Goals

- Build catkin workspace reliably
- Launch nodes with deterministic config

### Checklist

1. Confirm ROS environment sourced.
2. Detect the preferred shell and setup file first.
3. Confirm workspace root and `src/` layout.
4. Confirm with the user before dependency installation or any `sudo` command.
5. Install dependencies (`rosdep`) if needed.
6. Build (`catkin_make`, `catkin build`, or project-specific command).
7. Validate launch files.
8. If the target should remain running for OpenClaw, start it with state/log capture and run a health check before declaring success.

### Commands

```zsh
# workspace example
zsh "<skill_dir>/scripts/ros1_shell_detect.sh"
zsh "<skill_dir>/scripts/ros1_workspace_probe.sh" --path <ws_root>
zsh "<skill_dir>/scripts/ros1_bringup_check.sh" --workspace <ws_root>

# then source and build with the detected shell/setup files
# source /opt/ros/noetic/setup.zsh
cd <ws_root>
# catkin_make
# source devel/setup.zsh

# install deps only after user approval
# rosdep install --from-paths src --ignore-src -r -y

# validate package and launch visibility
rospack list | head
roslaunch --help
zsh "<skill_dir>/scripts/ros1_launch_discover.sh" --path <ws_root>

# start a long-running target and keep a state handle for later stop/check actions
zsh "<skill_dir>/scripts/ros1_start_target.sh" --workspace <ws_root> --package <pkg> --launch <file.launch>
zsh "<skill_dir>/scripts/ros1_runtime_health_check.sh" --state-file <state.env> --expect-topic /rosout
```

## B) Runtime Debug Profile

### Goals

- Explain why graph behavior differs from expectations

### Checklist

1. Node existence and namespace check.
2. Topic type/rate consistency.
3. Service/action availability.
4. TF frame chain sanity.

### Commands

```zsh
rosnode list
rostopic list
rostopic type <topic>
rostopic hz <topic>
rosservice list

# tf diagnostics (if installed in environment)
# rosrun tf view_frames
# rosrun tf tf_echo <from> <to>
```

## C) Motion Control Profile

### Goals

- Execute movement safely with measurable completion

### Checklist

1. Verify command topic (e.g., `/cmd_vel` or joint command topics).
2. Verify feedback telemetry (odometry/joint states).
3. Apply conservative speed and timeout.
4. Issue explicit stop at end and on error.

### Commands

```zsh
zsh "<skill_dir>/scripts/ros1_interface_check.sh" topic /cmd_vel geometry_msgs/Twist
rostopic echo -n 1 /odom

# example closed-loop move
python3 "<skill_dir>/scripts/move_forward_by_odom.py" --cmd-topic /cmd_vel --odom-topic /odom --distance 1.0
```

## C2) Manipulator / Joint-Control Variant

### Goals

- Execute joint-space or controller-service operations safely

### Checklist

1. Confirm `/joint_states` is updating.
2. Confirm target controller topic/service exists and type matches.
3. Apply bounded increments and timeout.
4. Verify final joint tolerance before reporting success.

### Commands

```zsh
rostopic echo -n 1 /joint_states
# Example type check (replace with your actual control interface)
# zsh "<skill_dir>/scripts/ros1_interface_check.sh" topic /arm_controller/command <msg_type>
```

## D) Data Pipeline Profile

### Goals

- Capture/replay data for debugging or evaluation

### Checklist

1. Select minimal topic set.
2. Record with clear naming and timestamps.
3. Capture metadata (`rosbag info`).
4. Replay with expected clock settings.

### Commands

```zsh
rosbag record /cmd_vel /odom
rosbag info <file.bag>
rosbag play <file.bag>
```

## E) OpenClaw Integration Profile (ROS1)

### Goals

- Bridge OpenClaw intents to ROS1 operations

### Checklist

1. Start `rosbridge_server` websocket.
2. Validate websocket endpoint accessibility from the OpenClaw side.
3. Whitelist the ROS topics/services/actions OpenClaw may use.
4. Map intent -> ROS operation (topic/service/action) with deterministic payload templates.
5. Subscribe to telemetry/status before sending commands.
6. Add emergency stop path, timeout fallback, and disconnect handling.

### Commands

```zsh
roslaunch rosbridge_server rosbridge_websocket.launch
# default websocket endpoint: ws://<host>:9090
```

### Rosbridge message templates

Topic publish:

```json
{"op":"advertise","topic":"/cmd_vel","type":"geometry_msgs/Twist"}
{"op":"publish","topic":"/cmd_vel","msg":{"linear":{"x":0.2,"y":0.0,"z":0.0},"angular":{"x":0.0,"y":0.0,"z":0.0}}}
```

Telemetry subscribe:

```json
{"op":"subscribe","topic":"/odom","type":"nav_msgs/Odometry","throttle_rate":200}
```

Service call:

```json
{"op":"call_service","service":"/start_task","args":{"mode":"inspect"}}
```

Action pattern:

- Prefer a ROS-side adapter node when possible.
- If direct actionlib bridging is required, treat the action as a set of ROS topics (`goal`, `feedback`, `result`, `status`, `cancel`) and verify the exact message types before sending anything.

## Notes

- Choose profile first, then run only relevant checks.
- Keep outputs reproducible: include exact commands and measured values.
- For long-running processes, return `state_file`, `log_file`, and the next recommended health or stop command.
- For architecture/performance tuning (nodelets, callback threading, dynamic_reconfigure), see `ros1-engineering-patterns.md`.
- For migration planning, use `ros1-engineering-patterns.md` migration checklist with `ros1-full-scope.md` interface inventory rules.
- For OpenClaw work, always describe the approved control surface explicitly: endpoint, allowed interfaces, stop path, and observed telemetry.
