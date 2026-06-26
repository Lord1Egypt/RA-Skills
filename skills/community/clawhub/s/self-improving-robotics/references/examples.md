# Entry Examples

Concrete examples of well-formatted robotics entries with full metadata.

## Learning: Localization Drift in Dynamic Environment

```markdown
## [LRN-20250415-001] localization_drift

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: localization

### Summary
Robot loses localization confidence in crowded aisle transitions where moving humans dominate lidar returns

### Details
In warehouse aisle transitions, AMCL particle spread grows quickly when dynamic obstacles obscure static map features.
Localization covariance spikes from 0.03 m to 0.42 m within 6 seconds and planner oscillates between paths.
Failure reproduces in shift-change windows with high pedestrian traffic.

### Suggested Action
Enable dynamic object filtering for localization input, increase recovery behavior threshold, and gate global replans when covariance exceeds safety bound.

### Metadata
- Source: field_test
- Platform: differential_drive_base_v3
- Related Files: config/localization/amcl.yaml, launch/nav_stack.launch.py
- Tags: localization, amcl, dynamic-environment, covariance
- Pattern-Key: localization_drift.dynamic_aisle

---
```

## Robotics Issue: Planner Failure in Narrow Passage

```markdown
## [ROB-20250415-001] narrow_passage_planner_failure

**Logged**: 2025-04-15T11:10:00Z
**Priority**: high
**Status**: pending
**Area**: planning

### Summary
Planner repeatedly fails to produce feasible trajectory through narrow service corridor

### Error Output
```
[planner_server]: planner failed: no valid path found
[behavior_tree]: recovery count exceeded; aborting mission segment
```

### Root Cause
Inflation radius and footprint padding consume corridor width; effective free space < minimum turning envelope.
Costmap update lag during obstacle-rich scene causes stale obstacle cells.

### Fix
Reduce inflation radius for corridor profile, switch to narrow-passage profile, and trigger constrained-path planner fallback.

### Prevention
- Add corridor benchmark in simulation CI
- Validate footprint/inflation consistency during map updates
- Add runtime monitor for repeated planner recovery loops

### Context
- Trigger: field_test
- Environment: hospital basement corridor
- Mission Segment: station_B_to_station_C

### Metadata
- Reproducible: yes
- Related Files: config/planning/local_costmap.yaml, config/planning/planner_profiles.yaml
- See Also: LRN-20250418-002

---
```

## Robotics Issue: Oscillatory Control Behavior

```markdown
## [ROB-20250415-002] heading_control_oscillation

**Logged**: 2025-04-15T14:00:00Z
**Priority**: critical
**Status**: in_progress
**Area**: control

### Summary
Heading controller exhibits 2.8 Hz oscillation during low-speed docking approach

### Error Output
```
controller: heading_error alternates +/-0.19 rad
cmd_vel.angular.z saturating at +/-0.75 rad/s
watchdog warning: repeated velocity saturation
```

### Root Cause
PID derivative term amplifies quantization noise from low-rate yaw estimate and integral anti-windup is disabled.

### Fix
Lower D gain, enable derivative low-pass filter, add anti-windup clamp, retune at target docking speed.

### Prevention
- Add closed-loop frequency response check in tuning runbook
- Require anti-windup validation before release
- Record gain sets by payload and floor friction condition

### Context
- Trigger: hil_test
- Controller: heading_pid_v2
- Speed: 0.18 m/s

### Metadata
- Reproducible: yes
- Related Files: control/pid_heading.yaml, control/docking_controller.cpp
- Tags: pid, oscillation, tuning, docking

---
```

## Learning: Sensor Fusion Timestamp Mismatch

```markdown
## [LRN-20250416-001] sensor_fusion_error

**Logged**: 2025-04-16T09:20:00Z
**Priority**: high
**Status**: pending
**Area**: perception

### Summary
Camera-lidar-imu timestamp skew causes intermittent map ghosting and pose jumps

### Details
Fusion pipeline shows camera frames arriving 85-120 ms late relative to lidar and IMU.
Kalman filter update order becomes inconsistent, introducing transient pose discontinuities.
Issue appears after NTP service restart on edge compute module.

### Suggested Action
Enforce hardware timestamp source, add clock-drift monitor, and reject packets exceeding sync budget.

### Metadata
- Source: hardware_diagnostics
- Related Files: perception/fusion/time_sync.yaml, scripts/monitor_clock_skew.py
- Tags: sensor-fusion, timestamp, desync, kalman
- Pattern-Key: sensor_fusion_error.clock_skew

---
```

## Robotics Issue: Hardware Interface CAN Timeout

```markdown
## [ROB-20250416-002] can_bus_timeout_on_motor_driver

**Logged**: 2025-04-16T13:45:00Z
**Priority**: critical
**Status**: pending
**Area**: hardware_integration

### Summary
Motor driver reports CAN timeout bursts leading to command dropouts and motion stutter

### Error Output
```
[motor_driver]: CAN timeout on node 0x12
[hardware_interface]: dropped packets=47 in 60s
[safety]: emergency stop asserted due to command watchdog
```

### Root Cause
CAN bus utilization exceeds 82% under high telemetry mode; arbitration delays exceed driver timeout window.

### Fix
Reduce non-critical telemetry publish rate, increase timeout guard band, and split diagnostics onto secondary bus.

### Prevention
- Add CAN utilization alarm at 70%
- Include high-load bus saturation test in HIL suite
- Track dropped packet trend by firmware version

### Context
- Trigger: telemetry_alert
- Firmware: motor_fw_3.2.1
- Bus Speed: 500 kbps

### Metadata
- Reproducible: yes
- Related Files: hardware/can_interface.yaml, firmware/motor_driver/config.h

---
```

## Robotics Issue: Unexpected Safety Stop Trigger

```markdown
## [ROB-20250417-001] unexpected_emergency_brake

**Logged**: 2025-04-17T08:10:00Z
**Priority**: critical
**Status**: resolved
**Area**: safety

### Summary
Emergency brake triggers without obstacle due to stale safety lidar sector mask after mode switch

### Error Output
```
[safety_monitor]: emergency stop triggered zone=front-left
[diagnostics]: mode switched AUTONOMOUS -> MANUAL -> AUTONOMOUS in 1.2s
[safety_monitor]: sector mask timestamp stale by 310 ms
```

### Root Cause
Safety monitor reuses previous sector mask during rapid mode transition before first fresh scan arrives.

### Fix
Reset sector mask state on mode transition and block motion until fresh safety scan arrives.

### Prevention
- Add mode-transition safety regression test
- Require freshness check on all safety-critical sensor inputs
- Add explicit safety state machine transition audit logs

### Context
- Trigger: safety_event
- Environment: loading dock
- Mode Transition: manual override event

### Metadata
- Reproducible: yes
- Related Files: safety/safety_monitor.cpp, safety/state_machine.yaml
- Tags: emergency-stop, safety, stale-data

### Resolution
- **Resolved**: 2025-04-17T12:55:00Z
- **Commit/PR**: #214
- **Notes**: Added scan-freshness gate and validated in 50 transition cycles

---
```

## Learning: Sim-to-Real Domain Gap

```markdown
## [LRN-20250418-001] sim_to_real_gap

**Logged**: 2025-04-18T15:30:00Z
**Priority**: high
**Status**: pending
**Area**: simulation

### Summary
Navigation policy succeeds in sim but fails on glossy floors due to wheel slip not represented in simulator

### Details
Simulation assumes constant traction and perfect odometry; real robot experiences slip during turns and acceleration.
Policy over-trusts odometry and underweights IMU correction, causing cumulative heading error.

### Suggested Action
Expand domain randomization with variable friction, wheel slip noise, and sensor latency distributions.
Add real-log replay loop before deployment approval.

### Metadata
- Source: postmortem
- Related Files: sim/worlds/warehouse.world, sim/randomization/friction_profiles.yaml
- Tags: sim2real, wheel-slip, domain-randomization
- Pattern-Key: sim_to_real_gap.floor_friction

---
```

## Learning: Thermal Throttling and Battery Sag

```markdown
## [LRN-20250419-001] power_thermal_constraint

**Logged**: 2025-04-19T11:40:00Z
**Priority**: high
**Status**: in_progress
**Area**: hardware_integration

### Summary
Compute module throttles and battery rail sags under sustained perception load, reducing control loop rate

### Details
During high-resolution perception mode, CPU reaches 92C and throttles from 2.1 GHz to 1.3 GHz.
Battery voltage dips below 21.0 V during peak motor demand, causing intermittent brownout warnings.
Control loop misses deadlines and planner update latency doubles.

### Suggested Action
Introduce thermal-aware workload scheduler, cap perception frame rate under high temperature, and adjust power distribution policy.

### Metadata
- Source: telemetry_alert
- Related Files: runtime/performance_manager.py, power/pdu_limits.yaml
- Tags: thermal, battery-sag, brownout, realtime
- Pattern-Key: power_thermal_constraint.compute_load

---
```

## Feature Request: Unified Robotics Incident Replay Tool

```markdown
## [FEAT-20250420-001] synchronized_incident_replay

**Logged**: 2025-04-20T10:00:00Z
**Priority**: medium
**Status**: pending
**Area**: simulation

### Requested Capability
Single command tool to replay synchronized camera/lidar/imu/odom/control logs with timeline scrubbing and safety-event overlays.

### User Context
Current debugging flow requires multiple tools and manual timestamp alignment, slowing postmortems and making root cause analysis inconsistent.

### Complexity Estimate
complex

### Suggested Implementation
1. Build unified log index with normalized timestamps
2. Provide synchronized playback UI and CLI export mode
3. Overlay planner states, control outputs, and safety flags
4. Add one-click export of incident bundle for review and learning logs

### Metadata
- Frequency: recurring
- Related Features: telemetry dashboards, rosbag tooling, postmortem automation

---
```
