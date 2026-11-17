# grasp — 视觉抓取

## 能力
通过深度摄像头识别并抓取物体。支持两种视觉模式：
- **ROI 模式**：用户在网页上画框指定抓取目标
- **YOLO 模式**：用 YOLO 模型自动识别目标类别并抓取

## 启动
```bash
# 需要先确保底盘+相机在跑
ros2launch xrrobot_bringup xrrobot_base.launch.py

# 另开终端，启动抓取
ros2launch xrrobot_vision_grasp vision_grasp.launch.py
```

Web 界面：`http://<机器人IP>:8795`

---

## 安全前置

视觉抓取会引起机械臂、夹爪，必要时还会引起底盘运动。执行前必须先满足：

- 机械臂和夹爪运动范围内无人、无易碎物、无线缆缠绕
- 目标物体允许被抓取，且周边没有不希望碰撞的物体
- 操作人员在现场可直接观察机器人，并可随时介入停止
- 默认先做“只检测不抓取”或 `dry_run: true`，确认目标和位姿正确后再执行真实抓取

如果用户没有明确要求立刻真实抓取，不要直接执行 `dry_run: false`。

---

## 完整使用流程

### 第一步：检查可用 YOLO 模型及类名
```bash
ros2 service call /xrrobot_vision_grasp/list_yolo_models \
  xrrobot_vision_grasp_interfaces/srv/ListYoloModels "{}"
```
返回示例：
```json
{ "model_names": ["yolov8n.pt", "yolov8s_cup.pt"],
  "active_model": "yolov8n.pt",
  "model_status": "ready",
  "active_model_classes": ["person","bicycle","car","cup","bottle",...] }
```

**关键**：拿到类名列表后，如果用户说要抓的物体不在里面，要告诉用户这个模型只能识别什么。

### 第二步：让用户选择模型和类别
```
我："当前有这些模型：
   yolov8n.pt → 可识别：person, bicycle, car, cup, bottle, ...
   yolov8s_cup.pt → 可识别：cup, bottle
   你要用哪个，抓什么？"
用户："用 cup 模型，抓杯子"
```

### 第三步：切换视觉模式（如果需要）
```bash
# 切到 YOLO 模式
ros2 service call /xrrobot_vision_grasp/set_mode \
  xrrobot_vision_grasp_interfaces/srv/SetVisionMode "{mode: 'yolo'}"
```

### 第四步：观测目标（检测不抓取）
```bash
ros2 service call /xrrobot_vision_grasp/observe_target \
  xrrobot_vision_grasp_interfaces/srv/ObserveTarget \
  "{target_classes: ['cup'], model_name: 'yolov8s_cup.pt', selection_policy: 0}"
```
返回目标详情：深度、3D 坐标、置信度。适合先"看一眼"再决定抓不抓。

### 第五步：先做 dry-run 验证
```bash
ros2 action send_goal /xrrobot_vision_grasp/detect_and_grasp \
  xrrobot_vision_grasp_interfaces/action/DetectAndGrasp \
  "{target_classes: ['cup'], model_name: 'yolov8s_cup.pt',
    selection_policy: 0, dry_run: true, detection_timeout_sec: 15.0}"
```

### 第六步：用户确认后再执行真实抓取

只有在用户明确同意、且现场确认安全后，才执行：

```bash
ros2 action send_goal /xrrobot_vision_grasp/detect_and_grasp \
  xrrobot_vision_grasp_interfaces/action/DetectAndGrasp \
  "{target_classes: ['cup'], model_name: 'yolov8s_cup.pt',
    selection_policy: 0, dry_run: false, detection_timeout_sec: 15.0}"
```

---

## 用户意图 → 执行策略

**"抓个杯子"**
```
1. list_yolo_models → 拿模型列表 + 每个模型的类名
2. 展示给用户：这些模型能识别什么
3. 用户选模型 + 目标类
4. 切 YOLO 模式
5. observe_target 检测
6. 先用 dry_run 检查目标是否正确
7. 用户明确确认后，再 detect_and_grasp 执行真实抓取
```

**"杯子"不在模型类名里**
```
→ 告知用户："这个模型能识别的是：[类名列表]，没有'杯子'。
   要不要换一个模型，或者用画框模式在网页上手动框选？"
```

**"帮我看看前面有什么物体"**
```
1. list_yolo_models → 确定用什么模型
2. observe_target 检测（不抓取）
3. 返回检测到的所有物体名称给用户
```

---

## ROS2 接口

### Action — 一步检测+抓取
```
服务名：/xrrobot_vision_grasp/detect_and_grasp
类型：  xrrobot_vision_grasp_interfaces/action/DetectAndGrasp

Goal 参数：
  string[] target_classes      ← 要抓的目标类名，如 ["cup", "bottle"]
  string model_name            ← YOLO 模型名（空=自动选默认）
  uint8 selection_policy       ← 0=最高置信度 1=最靠近中心 2=类优先级
  bool dry_run                 ← true=只模拟不实际抓
  float32 detection_timeout_sec

Feedback 阶段（stage 字段）：
  1 = SWITCHING_MODE   2 = LOADING_MODEL   3 = WAITING_FRAME
  4 = DETECTING        5 = TARGET_ACQUIRED 6 = PLANNING
  7 = EXECUTING        8 = VERIFYING
```

### Service — 设置视觉模式
```
名：/xrrobot_vision_grasp/set_mode
请求：{mode: "roi"} 或 {mode: "yolo"}
返回：{success, active_mode}
```

### Service — 设置夹爪
```
名：/xrrobot_vision_grasp/set_gripper
请求：{action: "open"} 或 {action: "close"}
返回：{success, message}
```

### Service — 对准车身（导航模式下使用）
```
服务名：/xrrobot_task_orchestrator/align_vehicle
类型：  xrrobot_task_orchestrator_interfaces/srv/AlignVehicle

请求：
  float32 target_x           ← 前方距离 (m)，来自 observe_target 的 arm_base_target_point
  float32 target_y           ← 横向偏移 (m)
  float32 target_z           ← 高度
  float32 distance_min       ← 最小可接受距离（默认 0.15）
  float32 distance_max       ← 最大可接受距离（默认 0.30）
  float32 lateral_tolerance  ← 横向容忍度（默认 0.02）
  float32 timeout_sec        ← 超时（默认 15）

返回：
  bool success
  string message
  float32 final_distance_m
```

说明：
- 只在 navigation 模式下需要，手动控制时不需要
- 调用前先通过 observe_target 拿到 arm_base_target_point
- 将 target_x, target_y 传入本服务
- 返回 success=true 表示车身已对准到最佳抓取位置

### Service — 观测目标（检测不抓）
```
名：/xrrobot_vision_grasp/observe_target
请求：{target_classes, model_name, selection_policy}
返回：{success, detection_count, target: {class_name, depth_m, camera_point, arm_base_target_point}}
```

### Service — 列出可用 YOLO 模型（含类名）
```
服务名：/xrrobot_vision_grasp/list_yolo_models
类型：  xrrobot_vision_grasp_interfaces/srv/ListYoloModels
返回：  string[] model_names
        string active_model
        string model_status
        string[] active_model_classes   ← 当前已加载模型的可用类名
```

### Topic — 抓取状态
```
话题：/xrrobot_vision_grasp/status
字段：state(0=idle/1=busy/2=error), vision_mode, active_model, camera_ready, model_ready
```

### 机械臂关节控制
```
话题：/xrrobot_arm/joint_commands     类型：sensor_msgs/JointState
反馈：/xrrobot_arm/joint_states_feedback
关节顺序：gripper1, wrist_roll, wrist_flex, elbow_flex, shoulder_lift, shoulder_pan
舵机状态：/xrrobot_arm/servo_feedback_valid
卸力：    /xrrobot_arm_bridge/torque_off (Empty)
```

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `xrrobot_base.launch.py` + `vision_grasp.launch.py` |
| 前置 | 需要底盘驱动 + 摄像头在线 |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ navigation | 导航+抓取是典型组合场景 |
| ✅ task_orchestrator | 任务编排器调度导航→抓取工作流 |
