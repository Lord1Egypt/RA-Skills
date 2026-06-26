# Robot Embodiment Reference

## Supported Configurations (π0)

| Platform | Arms | Config DoF | Action Dim | Cameras |
|---|---|---|---|---|
| UR5e (single arm) | 1 | 6 + gripper | 7 | 2 |
| UR5e (bimanual) | 2 | 12 + 2 grippers | 14 | 3 |
| Franka | 1 | 7 + gripper | 8 | 2 |
| Bimanual Trossen | 2 | 12 + 2 grippers | 14 | 3 |
| Bimanual ARX/AgileX | 2 | 12 + 2 grippers | 14 | 3 |
| Mobile Trossen/ARX | 2 + nonholonomic base | 14 config, 16 action | 16 | 3 |
| Mobile Fibocom | 2 + holonomic base | 14 config, 17 action | 17 | 3 |

**Max action dimension: 17** — all smaller action spaces are zero-padded to match.

## Multi-Embodiment Design Principles

- **Single model, all robots** — one set of weights controls 7+ configurations
- **Zero-padding** — smaller action spaces padded to 17-dim; model learns to ignore padding
- **No embodiment ID token** — embodiment-specific behavior emerges from data, not explicit conditioning
- **Cross-embodiment transfer** — training on diverse robots helps generalization within each robot type

## Camera Setup

- 2 cameras: typically wrist + overhead (single-arm)
- 3 cameras: wrist + overhead + side (bimanual/mobile)
- All cameras provide RGB images; no depth required for π0

## Action Space Definition

Action = joint positions (or velocities) + gripper commands

For mobile robots, action includes:
- Base velocity commands (nonholonomic: 2D; holonomic: 3D)
- Arm joint positions
- Gripper commands
