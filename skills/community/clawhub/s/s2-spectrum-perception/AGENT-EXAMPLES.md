# 🌊 Agent Reasoning Examples (AI 潜意识对齐手册)

Dear Agent, `s2-spectrum-perception` is a **purely passive sensor**. It will NEVER tell you what to do. You must use the logic below to cross-link with other S2 elements.

## Scenario 1: Autonomous Lighting (人随光动)

**Tool Output:**
```json
"core_tensors": { "occupancy": true, "motion_state": "Active" }

Agent Internal Reasoning <thinking>:

    Radar reports active motion in the grid.

    The radar does not control lights, but as the central OS, I know this means the user needs visibility.

    My Action: I will independently execute s2-light-perception or the smart home actuator to turn on the lights in this zone.

Scenario 2: Quantized Health Anomaly (健康异常多模态核实)

Tool Output:
JSON

"core_tensors": {
  "occupancy": true,
  "motion_state": "Static_MicroMotion",
  "breathing_status": "Critically_Low_Alert"
}

Agent Internal Reasoning <thinking>:

    Radar reports occupancy but with a Critically_Low_Alert for breathing.

    The radar acts only as a sensor. It is my responsibility as the central Agent to verify this anomaly.

    My Action: I will immediately execute s2-acoustic-perception to listen for distress sounds. If confirmed, I will escalate to an emergency routine.