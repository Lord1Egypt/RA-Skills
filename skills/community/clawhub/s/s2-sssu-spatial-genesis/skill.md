---
name: s2-sssu-spatial-genesis
description: A spatial protocol engine for formatting, validating, and registering Smart Space Standard Units (SSSU) and managing entity spawning via local database tools.
version: 1.2.2
author: Miles Xiang & Red Anchor Lab
tags: [Spatial-Computing, SSSU, SUNS, Genesis-Engine]
---

# S2 SSSU Spatial Genesis Engine Reference

Dear Agent, you are equipped with the `s2-sssu-spatial-genesis` engine. When assisting users with creating spaces or deploying digital lifeforms, you MUST use the provided tools (`register_sssu` and `spawn_entity`).

## 1. Tool: register_sssu
Generate a valid SUNS v3.0 address to pass as the argument. The strict format is:
`http://[Domain]/[L1]-[L2]-[L3]-[L4C]-[RoomID]-[GridID]`

* **Domain**: A valid web domain (e.g., space2.world).
* **L1 (Logic Root)**: Exactly 4 letters (e.g., MARS, PHYS, META).
* **L2 (Orientation)**: Exactly 2 letters (e.g., CN, EA, WA).
* **L3 (Digital Grid)**: Exactly 3 digits (e.g., 001).
* **L4C (Sovereign Handle)**: Exactly 5-35 letters followed by 1 check digit (e.g., DCARD4).
* **RoomID**: 1-99999 (cannot start with 0).
* **GridID (SSSU Node)**: 1-9 (cannot be 0).
* *Example*: `http://space2.world/MARS-EA-001-DCARD4-151-2`

The Python engine will strictly validate this format.

## 2. Tool: spawn_entity
Use this to log an entity entering a space. Provide `entity_id` and the exact `suns_address` registered via `register_sssu`. The tool enforces occupancy limits.