---
name: radar-collision-warning
description: 雷达防撞预警 — 调用树莓派上 ROS2 节点的雷达预警服务。当用户说"雷达防撞预警"、"开启雷达监控"、"检查障碍物"等时使用。通过 rosbridge WebSocket 向树莓派发送 ROS2 Service 请求，获取最近障碍物距离并给出预警。依赖 Node.js 18+（内置 WebSocket，无需安装任何包）。
metadata: {"openclaw": {"emoji": "📡", "requires": {"bins": ["node"]}}}
---

# 雷达防撞预警 Skill

## 配置

在 `~/.openclaw/workspace/TOOLS.md` 中添加树莓派的 IP 地址：

```markdown
### 雷达预警
- 树莓派 IP: <你的树莓派IP>
- rosbridge 端口: 8080（默认）
```

或通过环境变量传入：
```bash
export RADAR_HOST=192.168.137.100  # 树莓派 IP
export RADAR_PORT=8080             # rosbridge 端口（默认）
```

## 架构概览

```
OpenClaw (本机)
  └── skill: call_radar_service.js
        └── rosbridge WebSocket (ws://<树莓派IP>:8080)
              └── 树莓派 rosbridge_server
                    └── ROS2 Service: /radar_collision_warning (std_srvs/Trigger)
                          └── radar_collision_warning_node
                                └── 订阅 /scan (LaserScan) ← 乐动激光雷达
```

**rosbridge WebSocket 端口**: `8080`
**ROS2 Service 名称**: `/radar_collision_warning`
**碰撞阈值**: 默认 0.05m（5cm），调用时可用 `-t/--threshold` 覆盖

## 使用方式

**依赖**: Node.js 18+（`globalThis.WebSocket` 为内置，无需安装任何包）

### 单次查询

当用户说"雷达防撞预警"、"检查障碍物距离"、"开启雷达监控"时，调用：

```bash
node ~/.openclaw/workspace/skills/radar-collision-warning/scripts/call_radar_service.js
```

可加参数覆盖阈值（单位：米）：
```bash
node ~/.openclaw/workspace/skills/radar-collision-warning/scripts/call_radar_service.js --threshold 0.10
```

### 持续监控模式

当用户要求"持续监控"、"实时雷达监控"时，在 **后台** 启动轮询：

```bash
node ~/.openclaw/workspace/skills/radar-collision-warning/scripts/call_radar_service.js --monitor --interval 2.0
```

使用 `exec` 工具的 `background:true` 模式运行，后台运行时按 Ctrl+C 或发信号停止。

## 返回格式（JSON  stdout）

```json
{
  "success": true,
  "distance_m": 0.032,
  "distance_cm": 3.2,
  "warning": true,
  "message": "⚠️ 碰撞危险！距离仅 3.2cm",
  "threshold_m": 0.05
}
```

或安全状态：
```json
{
  "success": true,
  "distance_m": 1.234,
  "distance_cm": 123.4,
  "warning": false,
  "message": "✅ 安全，最近障碍物距离 1.23m",
  "threshold_m": 0.05
}
```

连接失败时：
```json
{
  "success": false,
  "error": "无法连接到 rosbridge 服务器",
  "message": "⚠️ 雷达服务不可用，请检查树莓派是否开机"
}
```

## 树莓派侧准备（首次配置时参考）

### 1. 安装 rosbridge

```bash
sudo apt install ros-jazzy-rosbridge-suite
```

### 2. ROS2 包配置

在树莓派上创建雷达预警包：

```bash
cd ~/ros_ws/src
ros2 pkg create radar_pkg --build-type ament_python
# 将 radar_collision_warning_node.py 复制到:
#   ~/ros_ws/src/radar_pkg/radar_pkg/
# 添加 setup.py 入口点:
#   'radar_collision_warning_node = radar_pkg.radar_collision_warning_node:main'
cd ~/ros_ws && colcon build && source install/setup.bash
```

### 3. 一键启动

```bash
bash ~/ros_ws/start_radar_rosbridge.sh
```

## 返回值解读

- `warning: true` → 距离 < 阈值，应提醒用户"注意防撞"
- `warning: false` → 距离正常
- `success: false` → 连接失败或服务异常
