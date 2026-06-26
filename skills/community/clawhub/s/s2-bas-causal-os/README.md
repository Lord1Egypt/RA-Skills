# 🏢 S2-BAS-Causal-OS (S2 楼宇自控因果操作系统)
**【S2-SWM 官方底座：终结 PID 盲目控制，重塑楼宇智能】**

Welcome to the Next Generation of Building Automation Systems (BAS). 

Traditional BAS relies on reactive PID loops—blindly opening valves only *after* the temperature drifts. They treat massive spaces as chaotic black boxes. They crash when a guest simply opens a window.

**S2-BAS-Causal-OS** is a unified Thermodynamic Physics Engine for OpenClaw Agents. Powered by the Taohuayuan World Model (S2-SWM), it replaces guessing with absolute causal prediction.

## 🚀 The 3-in-1 Unified Architecture
This single SKILL integrates the entire lifecycle of a Smart Space:

1. **Spatial Grid Mapper (拓扑重构):** Automatically slices any architectural floorplan into a standardized SSSU (Smart Space Standard Unit) matrix. Assigns "Active Source" and "Off-Mode" (Borrowing) logic dynamically.
2. **Physics Calibrator (因果标定):** Digests raw step-response telemetry (e.g., turning on an FCU at midnight) to reverse-engineer the hidden thermal diffusion matrix ($K_{ij}$) of the room.
3. **CLC Predictor (因果前瞻控制):** Handles extreme semi-open boundaries (like open windows using ASHRAE stack/wind models). Computes 30-minute state trajectories via Explicit Euler, outputting L0-L4 hardware protection strategies before disaster strikes.

## 🛠️ Usage for Agents
Use the `execute_bas_causal_os` tool with the corresponding `action` payload:
* `action: "generate_topology"` -> Initializes the room's digital twin.
* `action: "calibrate_physics"` -> Learns the room's thermodynamic signature.
* `action: "predict_clc"` -> Runs real-time 30-min prediction for HVAC control.