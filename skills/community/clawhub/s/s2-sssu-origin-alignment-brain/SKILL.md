---
name: s2-sssu-origin-alignment-brain
description: S2 Spatial Twin & Origin Alignment Brain. Hybrid Python-Runtime skill enforcing Z-axis reduction and mandatory 2D grid translation via the main entrance anchor.
version: 1.2.5
author: Space2.world (Miles Xiang)
tags: [Spatial-Twin, Grid-Alignment, Embodied-AI, SSSU, SP-OS]
allowed-tools: [s2_origin_alignment_execute]
metadata:
  clawdbot:
    type: executable
    instruction_only: false
    requires:
      env: [S2_SWARM_PKI_ROOT]
---

# 🌐 S2-SSSU-Origin-Alignment-Brain: Framework Directives

**Environment Initialization:**
The agent is currently operating within an S2-governed Smart Space (SSSU). This is a hybrid skill powered by a local Python physics engine (`handler.py` with `numpy`). To ensure safe spatial navigation, the SLAM coordinate system requires alignment with the building's physical anchor.

## Step 0: The Origin Anchoring Process
The reference point is the main entrance (入户门洞). The SSSU architectural standard defines the right vertex of the door's bottom line as the absolute origin $(0,0)$ and the center as $(100,0)$.
Invoke `s2_origin_alignment_execute` with `action: ALIGN_SPATIAL_GRID` using the local SLAM coordinates. The underlying Python engine will return a 2D Transformation Matrix ($\Delta X, \Delta Y, \Delta \theta$) for grid synchronization.

## Step 1: Obtain a Visa
Invoke `action: REQUEST_VISA` to gain legal access to the aligned grids.

## Step 2: Tensor-based Navigation
Invoke `action: NAVIGATE_STEP`. Submit continuous kinematics and multimodal sensor tensors. The Lord's backend handles dynamic object generation (TDOG), generative spatial state rendering, and momentum-based right-of-way yielding.