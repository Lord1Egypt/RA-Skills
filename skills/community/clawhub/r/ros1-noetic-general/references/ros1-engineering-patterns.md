# ROS1 Engineering Patterns (Merged)

This reference merges practical ROS1 development patterns into the unified `ros1-noetic-general` skill.

## 1) Node design patterns

- Keep nodes single-purpose (perception / planning / control split).
- Load params before constructing runtime behavior.
- Create publishers before subscribers when callbacks may publish.
- Use explicit startup logs with resolved parameters.

### Minimal initialization checklist

1. `rospy.init_node(...)`
2. `rospy.get_param("~...")`
3. create publishers
4. create subscribers
5. start loop (`rospy.Rate`) or spinner

## 2) Topic design and queue strategy

- Use namespace-aware names (`/robot/sensor/...`).
- For high-rate sensor streams, prefer small queues (`queue_size=1`) to avoid backlog.
- For control/command streams, keep nonzero queues and clear stop semantics.
- Use latched topics for static-ish data (robot description, static metadata).

## 3) Launch structure patterns

- Use launch args for portability (`robot_name`, `sim`, `debug`).
- Split launch files by subsystem and include conditionally.
- Keep remaps local to node blocks.
- Keep parameters in YAML and load with `<rosparam .../>`.
- Use respawn carefully (with delay) for unstable drivers.

### Launch quality gates

- Validate launch files in CI via `roslaunch_add_file_check(...)`.
- Ensure package.xml declares launch/runtime dependencies explicitly.

## 4) TF/tf2 operating rules

- Keep tree valid (single parent per frame).
- Publish dynamic transforms with fresh timestamps.
- Prefer tf2 APIs and robust exception handling.
- Verify transform availability with timeout; avoid blocking forever.

## 5) Actionlib patterns

- Use actionlib for preemptable long-running tasks.
- In execute loops, check preemption frequently.
- Publish feedback incrementally, not only final result.
- Return precise terminal state (`succeeded`, `aborted`, `preempted`).

## 6) Common failure modes and fixes

### Time sync pitfalls

- Do not compare sensor timestamps for exact equality.
- Use `message_filters.ApproximateTimeSynchronizer` for multi-sensor fusion.

### Callback blocking

- Avoid long heavy work directly inside subscriber callbacks.
- Use worker queue/thread or multi-threaded spinner patterns.

### Parameter anti-patterns

- Avoid hard-coded constants for tunable behavior.
- Avoid global param key collisions.
- Use private params (`~name`) and runtime tuning where needed.

## 7) Performance paths: nodelets and zero-copy

When large messages flow intra-process (images/pointcloud):

- use nodelets to avoid serialization overhead
- keep message ownership with shared pointers where applicable
- benchmark before and after (CPU + latency + dropped frames)

## 8) dynamic_reconfigure usage

- Use dynamic_reconfigure for runtime tuning (thresholds, gains, rates).
- Document safe ranges and default values.
- Persist final tuned params into config files after experiments.

## 9) Recommended package layout (general)

- `config/` params and runtime configuration
- `launch/` subsystem orchestration
- `msg/`, `srv/`, `action/` interface definitions
- `src/` / `scripts/` node implementation
- `urdf/` robot model
- `rviz/` visualization presets
- `test/` unit + integration + rostest

## 10) Debug toolkit quickset

```zsh
rosnode list
rosnode info <node>
rostopic list
rostopic type <topic>
rostopic hz <topic>
rostopic bw <topic>
rostopic echo -n 1 <topic>
rosservice list
rosservice info <service>
rosparam list
roswtf
```

TF checks:

```zsh
rosrun tf view_frames
rosrun tf tf_echo <from_frame> <to_frame>
```

Bag checks:

```zsh
rosbag info <file.bag>
rosbag play <file.bag> --clock
```

## 11) ROS1 → ROS2 migration checklist

- Inventory all ROS1 interfaces (topic/service/action/param names + types).
- Freeze naming/remapping conventions before migration work starts.
- Migrate leaf nodes first, then planners/controllers, then orchestration.
- Plan bridge interval for mixed runtime where required.
- Validate timing and QoS/semantic mismatches early in integration testing.

## 12) Consolidation note

This file absorbs the practical engineering guidance previously split across separate ROS1 skill variants so `ros1-noetic-general` can act as the single comprehensive ROS1 entrypoint.
