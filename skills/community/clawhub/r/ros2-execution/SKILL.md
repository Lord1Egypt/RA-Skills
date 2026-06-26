---
name: ros2-execution
description: Execute ROS 2 commands (run, launch, call) in a sandboxed, allowlisted environment. Supports parameter profiles.
---

# ROS 2 Execution (Sandboxed)

## Setup & Installation

Before this skill can be used, the local environment must be configured. 
The setup script dynamically discovers your ROS paths and approved workspaces. **You can re-run the setup script at any time if you add new workspaces.**

1. **Source your environment:** You MUST source your ROS 2 environment and any local workspaces *first* in your terminal.
   ```bash
   source /opt/ros/<distro>/setup.bash
   source ~/my_ros_ws/install/setup.bash
   ```
2. **Run setup:**
   ```bash
   ./scripts/setup.sh
   ```
3. **Whitelist Packages:** Edit `config/packages.json` to explicitly allow the packages you want the agent to execute.
4. **Parameter Profiles (Optional):** Create YAML parameter files in `~/.openclaw/workspace/ros_profiles/` for quick execution using the `--profile` flag.

## Overview

Use this skill to execute ROS 2 commands. 

**SECURITY CONSTRAINT:** You must ALWAYS use the safe wrapper script located at `./scripts/safe_ros2_execution.py`. 
This script performs strict security checks using Python's `subprocess` (no raw shell execution, preventing injection) and validates:
1. The command type (must be run/launch/call).
2. The package is in an approved workspace.
3. The package is explicitly allowlisted.

**Wrapper Path:** Resolve `./scripts/safe_ros2_execution.py` against this SKILL.md directory.

## Allowed Commands

Usage: `./scripts/safe_ros2_execution.py <command> <package> <target> [--profile <name> | --params-file <path>] [extra_args]`

- **Run a node:** 
  `./scripts/safe_ros2_execution.py run <pkg> <node>`
- **Run a node with a Parameter Profile:** 
  `./scripts/safe_ros2_execution.py run <pkg> <node> --profile outdoor`
  *(Loads from `~/.openclaw/workspace/ros_profiles/outdoor.yaml`)*
- **Run a node with a specific Params File:** 
  `./scripts/safe_ros2_execution.py run <pkg> <node> --params-file /tmp/temp_params.yaml`
- **Launch a file:** 
  `./scripts/safe_ros2_execution.py launch <pkg> <launch_file>`
- **Call a service:** 
  `./scripts/safe_ros2_execution.py service_call <pkg> <srv_name> <srv_type> <args>`
- **Send an action goal:** 
  `./scripts/safe_ros2_execution.py action_send_goal <pkg> <action_name> <action_type> <args>`

## Handling Parameters (--ros-args)
Avoid passing complex strings (like nested arrays or JSON dictionaries) directly in the command arguments. Instead:
1. Write the parameters to a temporary YAML file.
2. Use the `--params-file /path/to/file.yaml` flag to safely load them.
3. For recurring setups, save the YAML file to `~/.openclaw/workspace/ros_profiles/<name>.yaml` and use `--profile <name>`.
