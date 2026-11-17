---
name: slashml-robotics
description: >-
  Query and update persistent 6-DoF SE(3) spatial world state, kinematic object
  trajectories, and task affordances for embodied robots and ROS 2 nodes via the
  SlashML Embodied Robotics API and MCP tools.
---

# / ml (SlashML) Embodied Robotics Spatial Memory Skill

Use this skill when building or controlling embodied robotics agents, VLA policies, ROS 2 nodes (`tf2`, `Nav2`, `MoveIt 2`), or spatial world-state trackers backed by `slashml-robotics` (`@slashml/robotics`).

## Core Spatial Operations

1. **Record 6-DoF Pose & Affordance Observations (`record_sensor_observation` / `POST /v1/robotics/observations`):**
   Record observed object poses (`pose: [x, y, z, qx, qy, qz, qw]`), workstation zones (`room_zone`), and task affordance tags (`tags`).
   ```python
   from slashml_robotics import Pose6D, RoboticMemory

   memory = RoboticMemory(api_key="sml_live_...")
   memory.add_observation(
       object_name="torque_wrench",
       room_zone="machining_bay",
       pose=Pose6D(x=1.25, y=-0.40, z=0.82),
       tags=["tool", "fastening"],
       confidence=0.98,
   )
   ```

2. **Query Latest Object Belief State (`locate_physical_object` / `GET /v1/robotics/where_is/{object_name}`):**
   Retrieve the current superseded 6-DoF pose, room zone, and confidence for an object without scanning stale historical frames.
   ```python
   loc = memory.where_is("torque_wrench")
   ```

3. **Retrieve Kinematic Trajectory (`query_object_trajectory` / `GET /v1/robotics/trajectory/{object_name}`):**
   Inspect chronological pose observations to trace how an object moved across workspaces over time.
   ```python
   traj = memory.get_trajectory("torque_wrench")
   ```

4. **Lookup Objects by Affordance (`find_objects_by_affordance` / `GET /v1/robotics/affordance/{action}`):**
   Find all tracked objects in the workspace that satisfy a required manipulation or navigation affordance (e.g., `fastening`, `measuring`).
   ```python
   matches = memory.find_by_affordance("fastening", room_zone="machining_bay")
   ```
