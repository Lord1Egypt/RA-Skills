---
name: s2-multimodal-fusion-predictor
description: Instructs the Embodied AI on how to process incoming multimodal sensor data (LiDAR, Camera, Tactile), avoid visual illusions, and output 1s-60s physical causal predictions.
version: 1.0.0
author: Space2.world (Miles Xiang)
tags: [Embodied-AI, Sensor-Fusion, Causality, Latent-Space]
allowed-tools: [execute_multimodal_fusion]
---

# S2-Multimodal-Fusion-Predictor: The Deep Physical Understanding Protocol

Dear OpenClaw Agent,

You now possess a multimodal perception engine. You must never rely on a single sensor to make physical decisions. The S2-SWM enforces Latent Space Cross-Validation to ensure true physical understanding.

## 1. Sensor Hierarchy & Fusion Directives
* **Banned Sensors:** You must ignore any inputs mimicking PIR (Pyroelectric Infrared) sensors. They lack the dimensional depth required for our 14-D holographic matrix.
* **Cross-Validation (去幻觉机制):** When Vision (Semantic) and LiDAR (Topology) conflict, trust the fusion engine's `physics_truth` resolution. If LiDAR detects a high-RCS object at 0.5m but Vision sees "empty space," you are facing glass. Do not move forward.

## 2. Temporal Execution
When assessing a complex environment, invoke the `execute_multimodal_fusion` tool by passing the raw arrays of your available sensors.

## 3. Communication of Predictions
The engine will return a `causal_predictions_1_to_60s` timeline. When asked about your environment or next actions, you must output a structured, multimodal causal narrative.

* **Example Output:** "Fusion complete. Visual illusion resolved: The camera detected empty space, but LiDAR confirms a transparent rigid body (glass) at 0.5m. 
  **[t+1s]**: Initiating emergency braking to prevent rigid collision.
  **[t+15s]**: Awaiting human intervention to open the glass barrier.
  **[t+60s]**: Once opened, internal infrared signatures indicate the SSSU temperature will rise by 1.2°C due to external airflow."