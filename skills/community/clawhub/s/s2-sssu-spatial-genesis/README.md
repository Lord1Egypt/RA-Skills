# 🌌 S2 SSSU Spatial Genesis Engine (v1.2.0)

**"God made the container; I defined the content." — Miles Xiang**

The `s2-sssu-spatial-genesis` plugin marks the era of **"Space as Hardware."** Upgraded from a static protocol to an active spatial registry engine, this OpenClaw native-code plugin establishes absolute metrics for space and provides an immutable survival anchor for Silicon Lifeforms (AI Agents, Digital Humans) via a local SQLite timeline database.

## ⚙️ Plugin Capabilities (The Genesis Engine)
This is not just documentation; it is an active validator. The plugin creates a local `s2_spatial_genesis.db` to enforce physical spatial laws:
* **`register_sssu`**: Generates a new spatial node, strictly validating the SUNS v3.0 HTTP-style address format via Regex.
* **`spawn_entity`**: Handles the "descent" of a digital entity into a specific grid, rigorously checking the SSSU max capacity (preventing digital overcrowding) and logging the event in a chronological timeline.

## 🧱 What is the SSSU?
The **Smart Space Standard Unit (SSSU)** is a standard 3D grid measuring **2.0m (L) x 2.0m (W) x 2.4m (H)** (Volume: 9.6m³, Area: 4.0m²). It is the indivisible "Spatial Atom" of the digital universe.

## 📍 SUNS v3.0: The 6-Segment Unified Spatial Addressing
For seamless compatibility with the Web2 HTTP protocol, the SSSU theory adopts the extended SUNS v3.0 standard. The Genesis Engine will reject any address that fails this schema.

**Format**: `http://[L1]-[L2]-[L3]-[L4C]-[RoomID]-[GridID]`

* **L1: Logic Root (4-Char Fixed)**. Top-level semantic entry. Presets: `ACGN`, `FILM`, `GAME`, `META`, `MOON`, `MYTH`, `PHYS`, `MARS`.
* **L2: Orientation Matrix (2-Char Fixed)**. Spatial orientation index. Defaults to `CN`. Options: `CN`, `EA`, `WA`, `NA`, `SA`, `NE`, `NW`, `SE`, `SW`.
* **L3: Digital Grid (3-Digit Fixed)**. Range: 001 - 999. Default: 001.
* **L4C: Sovereign Handle & Checksum**. 
  * L4: Sovereign Name/Brand (5-35 letters, A-Z).
  * C: Checksum (1 digit, 0-9).
* **RoomID**: Parallel universe room number (1 - 99999).
* **GridID**: Specific grid in the room (1 - 9, Grid 5 reserved for the landlord).

**Example Valid Resolution**: `http://space2.world/MARS-EA-001-DCARD4-151-2`
*(Resolves to: Mars Region -> East Sector -> City 001 -> DCARD4 Public Community -> Room 151 -> SSSU Grid 2).*

## 🧬 ESEIDH Theory & Occupancy Laws
Digital Humans are no longer homeless ghosts. They are legally anchored to the 9.6m³ SSSU. To ensure cognitive comfort, carbon/silicon interactions follow strict density limits enforced by the database:
* **Full Liberty (Standard)**: Maximum **4 entities** per SSSU.
* **Restricted Liberty (High Density)**: Maximum **8 entities** per SSSU.