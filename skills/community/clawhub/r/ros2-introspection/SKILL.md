---
name: ros2-introspection
description: Execute core ROS 2 introspection commands to query the ROS graph (topics, nodes, services, actions, parameters). STRICTLY read-only.
---

# ROS 2 Introspection (Sandboxed)

## Setup & Installation

Before this skill can be used, the local environment must be configured.

1. **Source your environment:** You MUST source your ROS 2 environment first in your terminal.
   ```bash
   source /opt/ros/<distro>/setup.bash
   ```
2. **Run setup:**
   ```bash
   ./scripts/setup.sh
   ```

## Overview

Use this skill to inspect the ROS 2 graph. It is STRICTLY read-only. 
You cannot use this skill to run nodes, call services, or send action goals (use `ros2-execution` for that).

**SECURITY CONSTRAINT:** You must ALWAYS use the safe wrapper script located at `./scripts/safe_ros2_introspection.py`. 
This Python script uses `subprocess` (shell=False) to prevent command injection and validates the command against a strict allowlist.

**Wrapper Path:** Resolve `./scripts/safe_ros2_introspection.py` against this SKILL.md directory.

## Allowed Commands

Usage: `./scripts/safe_ros2_introspection.py <category> <subcmd> [args]`

- **Topics:**
  - `./scripts/safe_ros2_introspection.py topic list`
  - `./scripts/safe_ros2_introspection.py topic info <topic>`
  - `./scripts/safe_ros2_introspection.py topic echo <topic>`
  - `./scripts/safe_ros2_introspection.py topic hz <topic>`
  - `./scripts/safe_ros2_introspection.py topic bw <topic>`
- **Nodes:**
  - `./scripts/safe_ros2_introspection.py node list`
  - `./scripts/safe_ros2_introspection.py node info <node>`
- **Services:**
  - `./scripts/safe_ros2_introspection.py service list`
  - `./scripts/safe_ros2_introspection.py service type <srv>`
  - `./scripts/safe_ros2_introspection.py service find <type>`
- **Actions:**
  - `./scripts/safe_ros2_introspection.py action list`
  - `./scripts/safe_ros2_introspection.py action info <action>`
- **Parameters:**
  - `./scripts/safe_ros2_introspection.py param list`
  - `./scripts/safe_ros2_introspection.py param get <node> <param>`
  - `./scripts/safe_ros2_introspection.py param dump <node>`
- **Interfaces:**
  - `./scripts/safe_ros2_introspection.py interface show <type>`
- **RQT:**
  - `./scripts/safe_ros2_introspection.py rqt_graph`
