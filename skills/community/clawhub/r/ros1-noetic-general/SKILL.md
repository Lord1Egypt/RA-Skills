---
name: ros1-noetic-general
description: General bilingual ROS1 Noetic skill for ROS questions and ROS project operations across robot dogs, mobile robots, manipulators, perception pipelines, simulation, and OpenClaw integrations. Trigger whenever the user mentions ROS, ROS1, Noetic, catkin, roslaunch, rosrun, roscore, rostopic, rosservice, rospy, roscpp, tf, tf2, rosbag, launch files, workspace, package.xml, CMakeLists.txt, rosbridge, or asks in Chinese or English to start/build/check/debug/stop a ROS project or robot, such as "启动 ROS", "启动机器狗", "编译 ROS 项目", "检查 catkin 工作区", "run roslaunch", "build this ROS package", or "debug this ROS node". For general ROS knowledge questions, provide broad ROS guidance first; for requests involving local files, local workspaces, commands, builds, launch/run actions, monitoring, health checks, or stopping runtime targets, use this skill's local scripts and workflows. If the user explicitly says "使用 rosskill", "用 ros skill", or "use rosskill", treat that as a strong signal to use this skill.
---

# ROS1 Noetic General

Use this skill for **project-agnostic ROS1 Noetic work**, not only quadruped tasks.

Typical trigger phrasing includes requests like:

- "启动机器狗"
- "启动 ROS 程序"
- "启动 ROS"
- "帮我看一下 ROS"
- "帮我编译一下这个 ROS 项目"
- "检查这个 catkin 工作区"
- "帮我把这个 launch 跑起来"
- "看看这个 ROS 节点为什么没起来"
- "build this ROS package"
- "start this ROS launch"
- "check this ROS workspace"
- "debug this ROS node"
- "use rosskill"

Routing rule inside this skill:

- If the request is mainly **general ROS knowledge** (concepts, terminology, architecture, best practices), answer with ROS guidance first.
- If the request touches **local files, local workspace state, local commands, build/start/launch/run/monitor/stop actions, or runtime diagnostics**, use this skill's scripts and execution workflow.
- If the user explicitly says **`使用 rosskill`**, **`用 ros skill`**, or **`use rosskill`**, strongly prefer this skill even when the request could also be answered more generally.

When the request mentions **OpenClaw**, **rosbridge**, **websocket ROS control**, or **remote intent mapping**, load `references/ros1-openclaw-adapter.md` early.

## Workflow

1. Resolve execution context and bundled resource paths.
2. Validate ROS1 environment and active graph.
3. Classify request into a project profile.
4. Execute profile-specific checklist.
5. Apply safe rollout and verification.
6. Report result with reproducible commands.

## Step 1: Resolve execution context first

Bundled scripts live inside this skill directory. Do **not** assume the current shell directory is the skill root.

- Resolve `scripts/...` and `references/...` relative to this `SKILL.md` file before using them.
- If you execute a bundled script, prefer an absolute path to the script.
- If the host runtime already provides equivalent ROS inspection commands, it is fine to use those directly.

Example pattern:

```zsh
SKILL_DIR="<absolute-path-to-this-skill>"
zsh "$SKILL_DIR/scripts/ros1_shell_detect.sh"
zsh "$SKILL_DIR/scripts/ros1_env_check.sh"
```

## Step 2: Validate environment

Run:

```zsh
zsh "$SKILL_DIR/scripts/ros1_shell_detect.sh"
zsh "$SKILL_DIR/scripts/ros1_env_check.sh"
zsh "$SKILL_DIR/scripts/ros1_graph_probe.sh" topic
```

If ROS commands are missing, use the shell detector output to decide whether the machine expects `setup.bash` or `setup.zsh`, then source ROS first.

Typical pattern:

```zsh
source /opt/ros/noetic/setup.zsh
```

If workspace overlays exist, source base first and overlays second.

## Step 3: Choose project profile

- **A. Bringup/Build**: catkin workspace, package dependencies, launch files.
- **B. Runtime Debug**: topics/services/actions, tf tree, node health.
- **C. Motion Control**: velocity/joint commands with feedback checks.
- **D. Data Pipeline**: rosbag record/playback, offline analysis.
- **E. OpenClaw Integration**: rosbridge websocket adaptation and intent mapping.
- **F. Architecture/Performance**: nodelets, callback-threading, message_filters, dynamic_reconfigure.
- **G. Migration Planning**: ROS1 legacy maintenance and ROS1→ROS2 transition strategy.

Read detailed commands from `references/project-profiles.md`.

For full ROS1 coverage (core graph, launch, tf/tf2, actions, bags, diagnostics, networking), load `references/ros1-full-scope.md`.

## Step 4: Execute by profile

### A) Bringup/Build

- `bringup` means bringing a ROS system up far enough to run: source ROS, identify workspace, build if needed, find launch files, start nodes, and confirm the graph is healthy.
- Verify workspace structure and package discoverability.
- Detect workspace/build strategy first with `scripts/ros1_workspace_probe.sh`.
- Run `scripts/ros1_bringup_check.sh` before starting or rebuilding a project.
- For OpenClaw-style tool use, prefer the runtime loop: `ros1_start_target.sh` -> `ros1_runtime_health_check.sh` -> `ros1_stop_target.sh`.
- Build with the detected catkin command and stop on first error.
- Discover and validate launch files before runtime.

Minimal runtime loop example:

```zsh
zsh "$SKILL_DIR/scripts/ros1_start_target.sh" \
  --workspace /path/to/ws \
  --package my_pkg \
  --launch demo.launch

zsh "$SKILL_DIR/scripts/ros1_runtime_health_check.sh" \
  --state-file /tmp/ros1_skill_runtime/<run>/state.env \
  --expect-topic /rosout

zsh "$SKILL_DIR/scripts/ros1_stop_target.sh" \
  --state-file /tmp/ros1_skill_runtime/<run>/state.env
```

### B) Runtime Debug

- Confirm graph visibility (`rosnode list`, `rostopic list`).
- Check type/rate/bandwidth for critical topics.
- Verify tf availability and frame consistency.

### C) Motion Control

- Verify command topic type and active subscribers.
- Validate critical interface types explicitly with `scripts/ros1_interface_check.sh`.
- Prefer closed-loop motion if distance/angle is requested.
- Keep conservative defaults and always send explicit stop.

Use interface/type checks first, then run motion script (mobile base profile):

```zsh
zsh "$SKILL_DIR/scripts/ros1_interface_check.sh" topic /cmd_vel geometry_msgs/Twist
python3 "$SKILL_DIR/scripts/move_forward_by_odom.py" \
  --cmd-topic /cmd_vel \
  --odom-topic /odom \
  --distance 1.0 \
  --speed 0.2
```

### D) Data Pipeline

- Record minimal required topics (avoid “record all” unless requested).
- Confirm clock/time behavior in playback scenarios.
- Document bag metadata and replay command for reproducibility.

### E) OpenClaw Integration (ROS1)

- `rosbridge` is the websocket bridge that lets OpenClaw or other external clients publish/subscribe/call into a ROS graph without writing native `rospy` / `roscpp` code.
- Start ROS1 rosbridge websocket.
- Preflight the ROS graph before exposing any endpoint to OpenClaw.
- Map high-level intents to ROS1 topic/service/action operations with explicit templates.
- Enforce safety stop semantics, timeout, and disconnect behavior for every motion intent.

See `references/ros1-openclaw-adapter.md`.

### F) Architecture / Performance

- Enforce single-responsibility node boundaries.
- Choose queue sizes intentionally for high-rate sensor topics.
- Use `message_filters` for sensor-time synchronization.
- Apply callback threading patterns (`MultiThreadedSpinner` / worker queue).
- Use nodelets for large intra-process data when zero-copy matters.
- Use `dynamic_reconfigure` for runtime tuning instead of hard-coded constants.

See `references/ros1-engineering-patterns.md`.

### G) Migration Planning (ROS1 → ROS2)

- Capture current ROS1 interfaces (topics/services/actions/params) before migration.
- Prefer staged migration from leaf nodes inward.
- Use bridge period planning where mixed ROS1/ROS2 runtime is required.

See `references/ros1-engineering-patterns.md` migration section.

## Step 5: Safety and quality gates

- Never leave a robot/controller moving on function exit.
- Add timeout for every long-running command.
- Fail fast when telemetry is stale or missing.
- Report exact measured outcome (not only “success”).
- When starting long-running processes, persist pid/log/state metadata so later health checks and stop actions can use the same handle.
- Ask for confirmation before commands that install packages, require `sudo`, change system configuration, or move hardware in the real world.
- Prefer dry-run inspection before any destructive or stateful ROS action.

## Step 6: References

- Official ROS docs and package index links: `references/official-docs.md`
- Full ROS1 capability map and command matrix: `references/ros1-full-scope.md`
- Engineering patterns & migration playbook: `references/ros1-engineering-patterns.md`
- Project-profile checklists and command templates: `references/project-profiles.md`
- OpenClaw↔ROS1 adapter blueprint: `references/ros1-openclaw-adapter.md`
- ROS1 knowledge-base sources ledger (official pages reviewed): `references/ros1-knowledge-base-sources.md`

If official sites block simple fetches, use whatever browsing or browser-automation tools the host runtime actually exposes. Do not assume tool names that the host has not provided.
