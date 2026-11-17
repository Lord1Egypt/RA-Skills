# base — 底盘驱动

## 能力
机器人移动控制（前进、后退、转向、停止），通过发布速度指令到 `/cmd_vel`。

## 启动
```bash
ros2launch xrrobot_bringup xrrobot_base.launch.py
```

## ROS2 接口

### Topic — 控制底盘运动
```
话题名：/cmd_vel
类型：  geometry_msgs/msg/Twist

linear.x  > 0 → 前进   < 0 → 后退   （麦轮全向底盘）
linear.y  ≠ 0 → 左右横移
angular.z > 0 → 左转   < 0 → 右转
```

### CLI 调用方式

```bash
# 前进
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.3, y: 0.0}, angular: {z: 0.0}}" --once

# 后退
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: -0.3, y: 0.0}, angular: {z: 0.0}}" --once

# 左转
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0}, angular: {z: 0.5}}" --once

# 右转
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0}, angular: {z: -0.5}}" --once

# 横移
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.3}, angular: {z: 0.0}}" --once

# 停
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0}, angular: {z: 0.0}}" --once

# 不要持续发布非零速度；所有运动都必须设置有限时长并在结束后停止。
```

也可以用 `xr-call` 封装好的命令（带超时控制）：
```bash
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call move --direction forward --duration-sec 2 --speed-mps 0.3
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call turn --direction left --duration-sec 1
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call stop
```

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `xrrobot_base.launch.py` |
| 前置 | 无 |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ camera | 独立节点 |
| ✅ lidar | 独立节点 |
| ❌ joy | 手柄也是 `/cmd_vel` 控制源；没有 twist_mux 仲裁时不得同时控制 |
| ❌ navigation | Nav2 会接管 /cmd_vel，冲突 |
| ❌ autopilot | 自动驾驶独占底盘 |
| ❌ lanekeeping | 巡线独占底盘 |
| ❌ follower | 跟随独占底盘 |

⚠️ 多个发布者同时发 `/cmd_vel` 会争用控制。如果 joy / navigation / autopilot / lanekeeping / follower 已启动，不要再单独发 move 指令。
