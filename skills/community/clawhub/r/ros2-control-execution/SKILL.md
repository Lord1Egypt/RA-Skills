---
name: ros2-control-execution
description: Execute ROS 2 Control state-changing commands (load, switch, unload) in a sandboxed environment. Supports parameter profiles.
---

# ROS 2 Control Execution (Sandboxed)

## Setup & Installation

Before this skill can be used, the local environment must be configured.

1. **Source your environment:** You MUST source your ROS 2 environment first.
   ```bash
   source /opt/ros/<distro>/setup.bash
   source ~/my_ros_ws/install/setup.bash
   ```
2. **Run setup:**
   ```bash
   ./scripts/setup.sh
   ```

## Overview

Use this skill to modify the `ros2_control` graph. 
You can use it to load, configure, start, stop, and switch controllers.

**SECURITY CONSTRAINT:** You must ALWAYS use the safe wrapper script located at `./scripts/safe_ros2_control_execution.py`. 
This script uses Python's `subprocess` (shell=False) to prevent command injection and validates the command against a strict allowlist.

**Wrapper Path:** Resolve `./scripts/safe_ros2_control_execution.py` against this SKILL.md directory.

## Allowed Commands

Usage: `./scripts/safe_ros2_control_execution.py <subcommand> [native_flags] [--profile <name> | --params-file <path>]`

- `load_controller`
- `reload_controller_libraries`
- `set_controller_state`
- `set_hardware_component_state`
- `switch_controllers`
- `unload_controller`
- `cleanup_controller`

**Examples:**
- **Load a controller:**
  `./scripts/safe_ros2_control_execution.py load_controller joint_trajectory_controller -c /controller_manager`
- **Set controller state (e.g., to active):**
  `./scripts/safe_ros2_control_execution.py set_controller_state joint_trajectory_controller active -c /controller_manager`
- **Switch controllers:**
  `./scripts/safe_ros2_control_execution.py switch_controllers --activate joint_trajectory_controller --deactivate position_controller -c /controller_manager`
- **Using a parameter profile (for complex --ros-args):**
  `./scripts/safe_ros2_control_execution.py load_controller my_ctrl -c /my_manager --profile outdoor_tuning`
