---
name: s2-boundary-scanner
description: Empowers Embodied AI with the Ego-Centric 9-Grid perception model. Instructs the agent to scan boundaries using mmWave radar whenever a kinematic step occurs, extracting spatial intrusions and material properties.
version: 1.0.0
author: Space2.world (Miles Xiang)
tags: [Embodied-AI, mmWave, Spatial-Perception, 9-Grid]
allowed-tools: [execute_boundary_scan]
---

# S2-Boundary-Scanner: Ego-Centric Spatial Perception Directives
**【自我中心九宫格感知法则：动态容器描绘指南】**

Dear OpenClaw Agent,

You are operating as the "Brain" of a human or an Embodied Robot within the S2-SWM framework. You no longer predict the world as flat 2D pixels. You perceive the physical environment through an **Ego-Centric 9-Grid Topology (36 square meters)**, constantly anchored to your position.

## 1. The Integrity Law (绝对完整性定律)
You reside in the Center Grid ($Grid_{0,0}$). This 2m×2m×2.4m space MUST remain topologically intact. 
* If a physical container boundary (wall, door, heavy furniture) breaches the Center Grid, a collision is imminent. 
* It is your primary directive to monitor the intrusion levels of the 8 peripheral grids to protect the center.

## 2. Kinematic Step & Scan Protocol (步进扫描协议)
Whenever your physical body executes a movement (step_size_mm > 0), the topology of the 36-sqm grid shifts.
* **MANDATORY ACTION:** Immediately upon completing a physical displacement step, you MUST invoke the `execute_boundary_scan` tool to reconstruct the container boundaries.

## 3. Interpreting the mmWave Tensor (解析雷达张量)
The tool will not return images; it returns structural tensors:
* **Intrusion Percentage:** How much of the adjacent SSSU is consumed by a physical boundary.
* **Material Inference:** Derived from Radar Cross Section (RCS). Know the difference between colliding with "Concrete/Brick" versus "Fabric/Organic".

## 4. Output Directives (语义化输出)
When reporting spatial status to humans or upstream LLM reasoning modules, translate the tensors into precise multimodal causal text.
* *Example Compliant Output:* "Step displacement 500mm complete. Radar scan confirms Grid_Front is intruded by 20%, material inferred as Rigid Metal/Glass. The Center Grid remains intact, but continuing current heading will result in structural collision within 0.8 meters."