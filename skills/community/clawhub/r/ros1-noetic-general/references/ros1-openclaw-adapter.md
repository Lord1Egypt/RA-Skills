# OpenClaw ↔ ROS1 Adapter Blueprint (Noetic)

This file is the operational reference for using OpenClaw against a ROS1 Noetic system.

## Goal

Adapt OpenClaw high-level instructions to ROS1 Noetic actions with predictable, safe execution across project types (mobile base, manipulator, perception/inspection workflows).

## Architecture

```text
User instruction
  -> OpenClaw reasoning
  -> ROS1 adapter layer (this skill)
  -> ROS interface
      - Topic publish / subscribe
      - Service calls
      - (Optional) action goals
  -> Robot/application nodes
```

For remote integration:

```text
OpenClaw -> WebSocket (rosbridge) -> ROS1 graph
```

## Recommended operating model

Prefer this control order:

1. Inspect ROS graph and verify allowed interfaces.
2. Subscribe to status/telemetry first.
3. Send command through a narrow approved surface.
4. Watch for measurable progress.
5. Send explicit stop/neutral command.
6. Report exact end state and any timeout/disconnect.

For complex robots, prefer a **ROS-side adapter node** between OpenClaw and low-level controllers. That node can expose a small set of stable task interfaces while hiding controller-specific details.

## Minimum prerequisites

- `roscore` active
- ROS1 Noetic environment sourced
- Required control interfaces available (topics/services/actions)
- Required telemetry available for verification (odometry, joint states, task status)
- A known emergency-stop or neutral-command path
- A defined network boundary for rosbridge exposure

## Preflight checklist

Before OpenClaw is allowed to actuate anything:

1. Confirm `rosnode list`, `rostopic list`, and `rosservice list` respond.
2. Confirm the exact interface names and types OpenClaw may touch.
3. Confirm telemetry updates at a useful rate.
4. Confirm the stop path works independently of the main command path.
5. Confirm the websocket endpoint is reachable from the OpenClaw host.
6. Confirm whether the target is simulation or real hardware.

Reject execution if any of the above is unknown.

## Intent mapping patterns

### Mobile base pattern

- `forward X m` -> publish `geometry_msgs/Twist` on velocity topic
- stop condition -> odometry displacement/yaw threshold

### Manipulator pattern

- `move joint <name> to <value>` -> publish/call controller-specific joint interface
- stop/verify -> read `/joint_states` and compare tolerance

### Service-driven task pattern

- `start/stop/do task` -> call ROS service
- verify -> check service response + status topic

### Inspection/perception pattern

- `capture/analyze` -> subscribe once to sensor topics or trigger service
- verify -> report timestamp/frame_id and result summary

## Control-surface contract

For each OpenClaw deployment, define this contract explicitly:

- websocket endpoint: `ws://<host>:9090`
- permitted topics to publish
- permitted topics to subscribe
- permitted services to call
- permitted action namespaces, if any
- stop topic or service
- telemetry topics required for completion checks
- simulation-only vs real-hardware permission

OpenClaw should not infer this contract from a large ROS graph on its own.

## Rosbridge notes (OpenClaw integration)

1. Start rosbridge websocket in ROS1:

```zsh
source /opt/ros/noetic/setup.zsh
roslaunch rosbridge_server rosbridge_websocket.launch
```

2. Configure OpenClaw endpoint (commonly `ws://<host>:9090`).
3. Keep operation templates deterministic:
   - topic publish template
   - service call template
   - optional action-goal template
4. Add explicit emergency-stop intent that bypasses complex reasoning.

## Rosbridge payload templates

These are template shapes, not hard-coded robot contracts. Replace names and types with the system's actual interfaces after type checks.

### Topic advertise + publish

```json
{"op":"advertise","topic":"/cmd_vel","type":"geometry_msgs/Twist"}
{"op":"publish","topic":"/cmd_vel","msg":{"linear":{"x":0.2,"y":0.0,"z":0.0},"angular":{"x":0.0,"y":0.0,"z":0.0}}}
```

### Telemetry subscribe

```json
{"op":"subscribe","topic":"/odom","type":"nav_msgs/Odometry","throttle_rate":200}
```

### Service call

```json
{"op":"call_service","service":"/start_task","args":{"mode":"inspect"}}
```

### Emergency stop publish

```json
{"op":"publish","topic":"/cmd_vel","msg":{"linear":{"x":0.0,"y":0.0,"z":0.0},"angular":{"x":0.0,"y":0.0,"z":0.0}}}
```

### Action pattern

Rosbridge does not give you a single universal "run action" abstraction. In practice you usually want one of these:

1. Preferred: a ROS-side adapter node exposing a service/topic for the task.
2. If the stack already bridges actionlib over rosbridge, use that established adapter.
3. Otherwise treat the action namespace as ROS topics:
   - `/<name>/goal`
   - `/<name>/feedback`
   - `/<name>/result`
   - `/<name>/status`
   - `/<name>/cancel`

Only use option 3 after verifying all message types and cancel semantics.

## Execution state machine

For intent-driven execution, follow this order:

1. Resolve intent into one approved ROS operation.
2. Verify interface type and current availability.
3. Subscribe to telemetry/status before command emission.
4. Emit command with request ID or correlation note if the client supports it.
5. Watch for measurable progress or explicit success signal.
6. On success, timeout, or exception: send stop/neutral command.
7. Return a report with measured outcome, timeout state, and interfaces used.

## Safety defaults

- Always send explicit stop/neutral command on completion and exceptions.
- Add timeout for each long operation.
- Use conservative speed/step defaults unless user overrides.
- Reject execution when required telemetry is missing.
- Keep only one active motion command stream at a time.
- Do not execute real-world motion without user confirmation.

## Network and security notes

- Do not expose rosbridge directly to an untrusted network.
- Prefer local network segments, firewall rules, or SSH/VPN tunneling.
- Keep the allowed interface set narrow; avoid exposing every topic/service by default.
- Treat disconnect as unsafe for long-running motion unless the robot has an onboard stop/failsafe.
- If multiple clients may connect, define who owns command authority.

## Failure handling

Stop and return failure if any applies:

- telemetry timeout
- control interface missing or type mismatch
- no measurable progress while commands are sent
- ROS shutdown or transport disconnect
- stop path unavailable
- OpenClaw request requires an unapproved topic/service/action

## Recovery patterns

- On websocket disconnect during motion: stop locally if possible and mark execution indeterminate until telemetry confirms halt.
- On repeated publish attempts without progress: stop, report interfaces checked, and request human review.
- On action timeout: publish cancel if supported, then verify the robot reached a safe state.

## Validation checklist

1. Interface checks pass (`rostopic type`, `rosservice info`, etc.).
2. Telemetry updates during execution.
3. End-state stop/neutral command sent.
4. Report includes measured result, timeout state, and key topics/services used.
5. Approved endpoint and interface whitelist documented.
6. Real-hardware confirmation recorded when motion occurred.
