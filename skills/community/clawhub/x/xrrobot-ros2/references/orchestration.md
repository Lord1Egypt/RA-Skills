# _orchestration — 组合规划指南

> 这不是一个独立能力，而是教 agent 如何组合其他技能实现复杂任务。

---

## 目标位置从哪来

| 你听到用户说…… | 你怎么做 |
|----------------|---------|
| "去A点/去一号位/去起点" | **先查点位** → `{baseDir}/scripts/rosx {baseDir}/scripts/xr-call list-waypoints`，确认存在后再用 `navigate --waypoint A` |
| "导航到坐标 (1.0, 2.0)" | 直接调 Nav2 action |
| "导航到 X 位置" 但你没听过这个点位名 | **问用户** |
| 用户没说去哪 | **问用户** |

**核心原则**：不知道就问。不要猜位置。

---

## 节点运行状态检查

```bash
ros2 node list                    # 查看所有运行节点
ros2 topic list                   # 查看所有活跃话题
ros2 topic info /xxx              # 看话题是否有 publisher
ros2 service list                 # 查看所有服务
ros2 action list                  # 查看所有 action server
```

### 判断表

| 要启动的能力 | 检查什么 | 存在则跳过 |
|-------------|---------|-----------|
| `xrrobot_camera.launch.py` | `/camera/color/image_raw` 有 publisher | ✅ |
| `xrrobot_lidar.launch.py` | `/scan` 有 publisher | ✅ |
| `xrrobot_base.launch.py` | 检查预期底盘节点和 `/cmd_vel` subscriber；仅看到 publisher 不能证明底盘就绪 | ✅ |
| `xrrobot_map_navigation.launch.py` | `nav2` 节点 | ⚠️ 含 base+雷达 |
| `vision_grasp.launch.py` | `xrrobot_vision_grasp` 服务 | ✅ |

---

## 步骤执行结果解析

### 导航（NavigateToPose action）
结果状态：`SUCCEEDED` → 到达 / `ABORTED` → 失败
失败时告诉用户："导航失败，检查地图和路径"

### 检测目标（ObserveTarget service）
- `error_code=0, success=true` → ✅ 发现目标，有 3D 坐标
- `error_code=5` (TARGET_NOT_FOUND) → ❌ 没找到
- `error_code=6` (DEPTH_INVALID) → ❌ 深度数据无效（物体太远/太近）

### 执行抓取（DetectAndGrasp action）
- `execution_success=true` → ✅ 抓取成功
- `planning_success=false, error_code=8` (IK_UNREACHABLE) → ❌ 机械臂够不到
- `error_code=5` (TARGET_NOT_FOUND) → ❌ 没检测到目标
- `error_code=4` (SERVO_FEEDBACK_INVALID) → ❌ 机械臂舵机掉线
- `error_code=7` (NOT_AT_HOME) → ❌ 机械臂不在待命位

### 设置夹爪（SetGripper service）
- `success=true` → ✅ 夹爪已开/闭
- `success=false` → ❌ 操作失败

### 列出 YOLO 模型
- `model_names` 为空 → 没有可用模型，只能用画框模式
- `active_model_classes` → 检查用户说的物体能否被识别

---

## 导航模式下抓取的特殊处理（对准车身）

导航到目标点后，抓取前可能需要**对准车身**，让物体进入机械臂工作范围。

**什么时候需要对准？**

| 条件 | 判断依据 | 操作 |
|------|---------|------|
| 已在 navigation 模式 | 当前模式为 navigation | ✅ 需要对准 |
| 手动控制模式 | 当前模式为 manual | ❌ 不需要 |
| 物体在工作空间内 | observe_target 的 x 在 0.05~0.45m | ✅ 直接抓 |
| 物体超出工作空间 | x > 0.45 或 y > 0.25 | ✅ 需要对准 |

**如何调用对准？**

```bash
# 1. 先观测目标拿到坐标
ros2 service call /xrrobot_vision_grasp/observe_target \
  xrrobot_vision_grasp_interfaces/srv/ObserveTarget \
  "{target_classes: ['cup'], selection_policy: 0}"

# 2. 看 arm_base_target_point 的坐标
#    point.x → 前方距离
#    point.y → 横向偏移
#    point.z → 高度

# 3. 调用对准（只在 navigation 模式下使用）
ros2 service call /xrrobot_task_orchestrator/align_vehicle \
  xrrobot_task_orchestrator_interfaces/srv/AlignVehicle \
  "{target_x: 0.35, target_y: -0.05, target_z: 0.0,
    distance_min: 0.15, distance_max: 0.30,
    lateral_tolerance: 0.02, timeout_sec: 15.0}"

# 4. 返回 success=true → 对准完成，可以抓取
#    返回 success=false → 对准超时，告知用户
```

**对准成功后的抓取**

```bash
ros2 action send_goal /xrrobot_vision_grasp/detect_and_grasp \
  xrrobot_vision_grasp_interfaces/action/DetectAndGrasp \
  "{target_classes: ['cup'], dry_run: false}"
```
## 决策流程

```
用户请求
  │
  ▼
① 拆解任务 → 列出需要的子能力
  │
  ▼
② 检查 launch 依赖和兼容性
  │
  ▼
③ 涉及位置？查点位或问用户
  │
  ▼
④ 涉及抓取？查模型类名
  │
  ▼
⑤ 导航模式下抓取？需要判断对准
  ├── 物体在工作空间内 → 直接抓
  └── 超出范围 → 告知用户或推荐编排器
  │
  ▼
⑥ 逐步骤执行，每步解析结果
  └── 成功 → 继续
  └── 失败 → 告知原因
```

---

## 复合模式示例

### 导航+抓取（简单场景，检测到可直接抓）

```bash
# 阶段1：导航到A
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: 'map'}, ...}}"
# → SUCCEEDED？

# 阶段2：查模型
ros2 service call /xrrobot_vision_grasp/list_yolo_models \
  xrrobot_vision_grasp_interfaces/srv/ListYoloModels "{}"
# → active_model_classes 含用户要抓的物体？

# 阶段3：检测并确认距离
ros2 service call /xrrobot_vision_grasp/observe_target \
  xrrobot_vision_grasp_interfaces/srv/ObserveTarget \
  "{target_classes: ['cup'], selection_policy: 0}"
# → 看 arm_base_target_point.x
#   0.05~0.45 → 可抓  |  >0.45 → 太远

# 阶段4：执行抓取
ros2 action send_goal /xrrobot_vision_grasp/detect_and_grasp \
  xrrobot_vision_grasp_interfaces/action/DetectAndGrasp \
  "{target_classes: ['cup'], dry_run: false}"
# → execution_success？
```

### 复杂多步工作流（推荐编排器）

```bash
ros2kill

ros2launch xrrobot_bringup xrrobot_map_navigation.launch.py &
ros2launch xrrobot_bringup xrrobot_camera.launch.py &
ros2launch xrrobot_vision_grasp vision_grasp.launch.py &
ros2launch xrrobot_task_orchestrator xrrobot_task_orchestrator.launch.py &

# 打开 http://<IP>:8796 加载工作流
# 编排器自动处理：导航→对准→抓取→放置
```

### 手动控制+抓取（不用对准）

```bash
ros2kill

ros2launch xrrobot_bringup xrrobot_base.launch.py &
ros2launch xrrobot_bringup xrrobot_camera.launch.py &
ros2launch xrrobot_vision_grasp vision_grasp.launch.py &

# 用户遥控车身到合适位置
# 直接抓取
```

---

## 互斥表

| 组合 | 说明 |
|------|------|
| navigation + camera | ✅ |
| navigation + grasp | ✅ 导航+对准+抓取 |
| mapping + camera | ✅ |
| base + camera | ✅；手柄与其他 `/cmd_vel` 控制源仍互斥 |
| mapping + navigation | ❌ |
| autopilot + 任何 | ❌ |

---

## 排查

| 问题 | 方法 |
|------|------|
| 节点没启动 | `ros2 node list` |
| 话题没数据 | `ros2 topic info /xxx` |
| 抓取报 BUSY | `ros2 topic echo /xrrobot_vision_grasp/status --once` |
| 模型不识别 | `list_yolo_models` 看 `active_model_classes` |
| 够不到 | 看 `observe_target` 返回的 arm_base_target_point |
| 舵机掉线 | `/xrrobot_arm/servo_feedback_valid` = false |
