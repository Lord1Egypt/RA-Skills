---
name: soarm-control
description: Control the robotic arm through the OpenClaw SOARM API. Use this skill when reading current joint state, moving by joint angles, moving by XYZ coordinates, or handling SOARM robot-control requests.
---

# 🦐 SOARM Control Skill

Use the existing SOARM API to control the robotic arm directly.

## ⚙️ Configuration Notes

**Default Local Setup (when on same machine):**
- API Base URL: `http://127.0.0.1:8000`

## 🔍 Key APIs & Examples

### Read Current State

```bash
curl -sS http://127.0.0.1:8000/joints
```

Returns current joint values and XYZ end-effector position.

---

### Move To a Position By Joint Angles

```bash
curl -sS -X POST http://127.0.0.1:8000/move/joints \
  -H 'Content-Type: application/json' \
  -d '{"angles":[0,0,0,0,0,0]}'
```

**Parameter Notes:**
- Joints order: `shoulder_pan`, `shoulder_lift`, `elbow_flex`, `wrist_flex`, `wrist_roll`, `gripper`
- First 5 joints use **degrees (deg)**
- Gripper uses **0-100** range

**Fixed Positions:**

| Name | shoulder_pan | shoulder_lift | elbow_flex | wrist_flex | wrist_roll | gripper |
|---|---:|---:|---:|---:|---:|---:|
| `initial` | 0 | -104 | 95 | 65 | -95 | 10 |
| `top_down` | 0 | -50 | 30 | 90 | -95 | 70 |

**Examples:**

Return to `initial`:

```bash
curl -sS -X POST http://127.0.0.1:8000/move/joints \
  -H 'Content-Type: application/json' \
  -d '{"angles":[0,-104,95,65,-95,10]}'
```

Return to `top_down`:

```bash
curl -sS -X POST http://127.0.0.1:8000/move/joints \
  -H 'Content-Type: application/json' \
  -d '{"angles":[0,-50,30,90,-95,70]}'
```

---

### Move By XYZ Coordinates

```bash
curl -sS -X POST http://127.0.0.1:8000/move/xyz \
  -H 'Content-Type: application/json' \
  -d '{"x":0.2,"y":0.0,"z":0.2}'
```

**Parameter Notes:**
- `x`: forward/backward (positive = forward)
- `y`: left/right (positive = left)  
- `z`: up/down (positive = up)
- Values in **meters**

---

### Trigger a Pick Task

```bash
curl -sS -X POST http://127.0.0.1:8000/pick
```

Returns:

- `ok`: true if the task was accepted
- `message`: `抓取任务已启动`
- Returns HTTP `409` if another pick task is already running


---

## 🐙 Quick Commands I Can Run

### Return to initial position
```bash
curl -sS -X POST http://localhost:8000/move/joints \
  -H 'Content-Type: application/json' \
  -d '{"angles":[0,-104,95,65,-95,10]}'
```

### Return to top-down position
```bash
curl -sS -X POST http://localhost:8000/move/joints \
  -H 'Content-Type: application/json' \
  -d '{"angles":[0,-50,30,90,-95,70]}'
```

### Read current position
```bash
curl -sS http://localhost:8000/joints
```

---

## 🛠️ Setup Notes
When pairing your SOARM device with OpenClaw:

1. **Organize the skill directory** 

    ```bash
    ├── references
    │   └── so101_new_calib.urdf  # download from TheRobotStudio 
    ├── scripts
    │   ├── best.pt  # yolo11n model
    │   ├── control_soarm_joints.py
    │   ├── move_soarm_to_xyz_pinocchio.py
    │   ├── read_soarm_joints.py
    │   ├── soarm_api.py
    │   └── start_server.sh
    └── SKILL.md
    ```
2. **Perpare lerobot env**
3. **Launch the server**
    ```bash
    ~/.openclaw/workspace/skills/soarm-control 
    bash scripts/start_server.sh
    ```

---

