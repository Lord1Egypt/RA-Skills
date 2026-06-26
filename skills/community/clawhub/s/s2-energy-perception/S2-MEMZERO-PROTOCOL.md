# ⚡ S2 Energy Perception: Memzero Protocol / 空间记忆协议

## 1. The Spatial Hierarchy (严格空间层级)
The Energy data must strictly adhere to the following addressing:
* **Residence (住宅)**: The root node.
* **Room (房间)**: E.g., `living_room`, `master_bedroom`. Minimum 1 per residence.
* **Space (标准空间)**: E.g., `x1_y1` to `x3_y3`. Minimum 1, Maximum 9 per room. Default is `x1_y1`. All user devices are registered at THIS level.

## 2. Dimensional Tensors (核心维度张量)
| Tensor Key | Type | Description |
|------------|------|-------------|
| `total_estimated_power_w` | Float | The sum of Watts for all devices in this specific grid. |
| `carbon_footprint_kg_per_hour` | Float | Computed CO2 emissions based on grid factor (0.5810). |
| `device_topology` | Array | List of devices `[{"name", "type", "power_w", "smart"}]`. |

## 3. Agent Assignment Protocol (智能体策略分配原则)
For every device mapped in the `device_topology`, the Central OS must mentally assign an Agent topology:
- `smart: True` -> Assign to **Active Control Agent** (Can cut power/adjust state).
- `smart: False` -> Assign to **Passive Notification Agent** (Can only alert the user via Digital Human UI).