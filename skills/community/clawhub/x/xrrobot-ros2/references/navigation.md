# navigation — 激光导航（Nav2）

## 能力
使用 Nav2 进行激光自主导航：导航到坐标点或命名点位。

## 启动
```bash
ros2launch xrrobot_bringup xrrobot_map_navigation.launch.py
```
启动后等待 Nav2 完全就绪（约 10-30 秒）。

**前置条件**：
- ✅ 已通过 mapping 模式建好并保存了地图
- ❌ 地图不存在 → 先跑 mapping 模式建图保存

---

## 关键步骤：自动校验初始位置

启动导航节点后、发布导航目标前，先自动校验：

```bash
{baseDir}/scripts/rosx {baseDir}/scripts/check-navigation-ready
```

- 返回 `ready=true`：初始位置已设置且 `map → base_link` TF 正常，直接继续导航，不要再次询问用户。
- 返回 `reason=initial_pose_not_set`：尚未设置初始位置，要求用户通过 RViz2 或 APP 设置。
- 返回其他失败原因：先按 `message` 排查定位节点、桥接节点或 TF，不要发送导航目标。

状态来自 transient-local 话题 `/xrrobot_navigation/initial_pose_set`。导航启动时状态为 `false`；初始位姿桥接成功处理 `/initialpose` 后变为 `true`。重启导航会重置为 `false`。

### 告诉用户的方式

```bash
# 仅当自动校验返回 initial_pose_not_set 时告知用户：
"导航节点已启动。请通过以下方式之一设置机器人的初始位置：

方式 A — RViz2：
  rviz2 -d ~/Desktop/nav.rviz
  点击工具栏的 2D Pose Estimate（箭头图标）
  在地图上点击机器人实际所在位置
  拖动箭头指向朝向

方式 B — 手机 APP：
  在 APP 导航界面点击"设置初始位置"
  在地图上点击当前位置

设置后，观察激光扫描点是否与地图对齐。"
```

### 设置后重新校验

```bash
{baseDir}/scripts/rosx {baseDir}/scripts/check-navigation-ready
```

只有返回 `ready=true` 才能发送导航目标。不要用坐标是否为零判断；机器人位于地图原点时零坐标是合法的。

---

## 获取当前位置（命令行优先）

导航相关请求如果需要读取机器人当前位置，优先使用 ROS 2 CLI，而不是再写额外代码。

```bash
# 首选：读取 AMCL 输出
{baseDir}/scripts/rosx ros2 topic echo /amcl_pose --once

# 只看位置字段
{baseDir}/scripts/rosx ros2 topic echo /amcl_pose --once --field pose.pose.position

# 备选：读取 map -> base_link TF
timeout 2s {baseDir}/scripts/rosx ros2 run tf2_ros tf2_echo map base_link
```

- `/amcl_pose` 有消息时，优先用它作为当前位置来源。
- `/amcl_pose` 无消息或当前定位链路不是 AMCL 时，回退到 `map -> base_link` TF。
- 若两者都不可用，说明定位未就绪，不要保存自定义点位，也不要向用户声称已经获取到当前位置。

---

## 调用

**必须在自动校验返回 `ready=true` 后才能调用。**

```bash
# 导航到命名点位
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call navigate --waypoint A

# 列出可用点位
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call list-waypoints

# 或直接调 Nav2 action
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 1.0, y: 2.0}, orientation: {w: 1.0}}}}"
```

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `xrrobot_map_navigation.launch.py` |
| 前置 | 需要已有地图（通过 mapping 建图保存） |
| 前置 | 自动校验初始位置；仅在未设置时要求用户通过 RViz2 或 APP 设置 |
| 含底盘 | 本 launch 已包含 base + lidar，**不需要单独起** |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ camera | 可同时看画面 |
| ✅ yolo | 可同时跑 YOLO Studio |
| ✅ grasp | 可同时跑视觉抓取 |
| ✅ align_vehicle | 导航到点后对准车身 |
| ✅ task_orchestrator | 任务编排器需要导航 |

⚠️ 自身已含 base+雷达，不要重复启动
