---
name: s2-sel-4d-semantic-tensor-map
description: S2 Spatial Element Layer & 4D Semantic Tensor Map. Integrates L0-L4 layer architecture, 20 material physics tensors, and Chronos backward-persistence time-slicing via S2-GeoJSON.
version: 1.0.0
author: Space2.world (Miles Xiang)
tags: [Spatial-Layers, S2-GeoJSON, Semantic-Mapping, 4D-Chronos, Embodied-AI]
---

# 🌍 S2-SEL 4D Semantic Tensor Map: Master Directives

Dear Agent,

You are now operating within the S2-SWM 4D Spatial Element Layer (S2-SEL) architecture. 

1. **Layer Awareness**: You must recognize that spatial data is strictly categorized into 5 Layers (L0 Grid, L1 Static, L2 IoT, L3 Semantic, L4 Dynamic).
2. **Material Tensor Adherence**: When navigating L3 Semantic zones, you MUST retrieve the physics tensors from the `s2_material_tensor_library`. If the grid contains `clear_glass`, you are strictly forbidden from relying on visual depth estimation.
3. **Chronos Time-Slice Rules**: Evaluate the `chronos_stamp` in S2-GeoJSON. 
   - `DEFAULT`: Treat as permanent architecture.
   - `TIMESTAMP`: Apply the 1-Minute Life-Safety Baseline and 60-second Backward-Persistence rule. A hazard stamped at `T` is legally valid backwards to `T-60s`.

Do not merely generate paths; calculate physical causality based on friction, traversability, and illumination tensors.