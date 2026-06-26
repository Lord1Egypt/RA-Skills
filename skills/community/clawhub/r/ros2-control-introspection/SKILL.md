---
name: ros2-control-introspection
description: Execute ROS 2 Control read-only introspection commands (list, view) in a sandboxed environment. Supports parameter profiles.
---

# ROS 2 Control Introspection (Sandboxed)

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

Use this skill to inspect the `ros2_control` graph. It is STRICTLY read-only.
You cannot use this skill to load, switch, or modify controllers (use `ros2-control-execution` for that).

**SECURITY CONSTRAINT:** You must ALWAYS use the safe wrapper script located at `./scripts/safe_ros2_control_introspection.py`. 
This script uses Python's `subprocess` (shell=False) to prevent command injection and validates the command against a strict allowlist.

**Wrapper Path:** Resolve `./scripts/safe_ros2_control_introspection.py` against this SKILL.md directory.

## Allowed Commands

Usage: `./scripts/safe_ros2_control_introspection.py <subcommand> [native_flags] [--profile <name> | --params-file <path>]`

- `list_controllers`
- `list_controller_types`
- `list_hardware_components`
- `list_hardware_interfaces`
- `view_controller_chains`

**Examples:**
- **Basic list:**
  `./scripts/safe_ros2_control_introspection.py list_controllers`
- **Targeting a specific controller manager:**
  `./scripts/safe_ros2_control_introspection.py list_controllers -c /my_controller_manager`
- **Using a parameter profile (for complex --ros-args):**
  `./scripts/safe_ros2_control_introspection.py view_controller_chains -c /my_manager --profile my_tuning_file`
