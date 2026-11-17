# XRRobot ROS2 机器人控制 Skill

> 此 skill 供运行 OpenClaw agent 的 XRRobot 主机使用。
> 通过本地 `exec` 执行 ROS 2 命令并控制机器人。

---

## 概述

机器人硬件：麦轮全向底盘 + 机械臂 + 奥比中光大白深度相机 + 激光雷达  
ROS 2 版本：Jazzy  
源码目录：`~/colcon_ws/src`  
工作区：`~/colcon_ws`

**所有命令都在本机执行**，无需 SSH。

---

## 安全前置

凡是会引起机器人底盘移动、机械臂运动、夹爪动作、自动导航、自动驾驶、跟随、抓取的操作，都必须先满足以下条件：

- 机器人周围已清场，人员、线缆、易碎物不在运动范围内
- 操作人员在现场可见机器人状态，并能随时介入停止
- 在执行会真实运动的命令前，先向用户明确说明“机器人可能立即开始运动”
- 对抓取、导航、自动驾驶、跟随这类连续动作，除非用户已经明确要求立即执行，否则先确认一次再执行
- Web 服务仅建议在可信局域网内使用；采集画面、训练数据、部署模型前先确认不会泄露敏感内容

如果用户只是想查看状态、列模型、看检测结果、dry-run 检测，不要默认升级成真实运动或抓取动作。

---

## 模式切换（推荐用 xrmode）

xrmode 是 `xrrobot-runtime-tools` 提供的模式切换 CLI。

### 前置 source

```bash
source /opt/ros/jazzy/setup.bash && source "$HOME/colcon_ws/install/setup.bash"
```

### xrmode 支持的动作

| 动作 | 命令 | 说明 |
|------|------|------|
| 手动模式 | `xrmode manual` | 底盘 + 手柄 + 相机 + web_video_server |
| 建图模式 | `xrmode mapping` | 激光 SLAM 建图（Cartographer） |
| 导航模式 | `xrmode navigation` | Nav2 激光导航 |
| 停止模式 | `xrmode stop` | 停止当前模式 |
| 查询状态 | `xrmode status` | 获取当前模式 JSON |
| 保存地图 | `xrmode save` | 保存当前地图（需 mapping 模式下） |

### 状态 JSON 关键字段

```json
{
  "stage": "idle | starting | running | ready | degraded | stopped | error | exited",
  "mode": "manual | mapping | navigation | none",
  "ready": true,
  "missing_nodes": [],
  "missing_topics": [],
  "stale_topics": [],
  "recommended_action": "",
  "runtime_services": {
    "rosbridge": { "enabled": true, "running": true, "pid": 1234 }
  }
}
```

**关键规则**：只有 `stage=ready` 才表示模式真正可用。`running` 只是进程已拉起，不等于就绪。

---

## 完整指令表

### 模式切换

```bash
# source 一次，后续省略
source /opt/ros/jazzy/setup.bash && source "$HOME/colcon_ws/install/setup.bash"

# 查状态
xrmode status

# 停当前模式
xrmode stop

# 切模式
xrmode manual
xrmode mapping
xrmode navigation

# 保存地图（mapping 模式下）
xrmode save
```

### ros2launch 直接启动

```bash
# 先杀已有进程
ros2kill

# 激光建图（Cartographer）
ros2launch xrrobot_bringup xrrobot_map_slam.launch.py

# 激光导航（Nav2）
ros2launch xrrobot_bringup xrrobot_map_navigation.launch.py

# 保存地图
ros2launch xrrobot_bringup xrrobot_save_map.launch.py

# 纯底盘（用于抓取场景）
ros2launch xrrobot_bringup xrrobot_base.launch.py

# 视觉建图（RTAB-Map）
ros2launch xrrobot_bringup xrrobot_visual_slam.launch.py

# 视觉导航
ros2launch xrrobot_bringup xrrobot_visual_slam_navigation.launch.py

# 自动驾驶跑圈
ros2launch xrrobot_autopilot xrrobot_autopilot_drive.launch.py

# 自动驾驶数据采集
ros2launch xrrobot_autopilot xrrobot_autopilot_collect.launch.py

# 自动驾驶训练
ros2launch xrrobot_autopilot xrrobot_autopilot_train.launch.py

# 车道保持/巡线
ros2launch xrrobot_lanekeeping xrrobot_lanekeeping.launch.py

# 雷达跟随
ros2launch xrrobot_follower laser_follower.launch.py

# 雷达警戒
ros2launch xrrobot_follower radar_guard.launch.py

# 群组控制
ros2launch xrrobot_bringup xrrobot_cmd_vel_fleet.launch.py

# 视觉抓取（深度摄像头）
ros2launch xrrobot_vision_grasp vision_grasp.launch.py

# 任务编排器（导航→抓取→搬运）
ros2launch xrrobot_task_orchestrator xrrobot_task_orchestrator.launch.py

# YOLO Studio（采集/训练/部署）
ros2launch xrrobot_yolo_studio xrrobot_yolo_studio.launch.py

# 视觉面板（MediaPipe 姿态/手势/人脸/ArUco）
ros2launch xrrobot_vision vision_dashboard.launch.py
```

### Web 服务端口

启动对应功能后，在浏览器访问：

| 功能 | 端口 | 地址 |
|------|------|------|
| 视频流 | 8080 | `http://<机器人IP>:8080/stream_viewer?topic=/camera/color/image_raw` |
| YOLO Studio | 8091 | `http://<机器人IP>:8091` |
| 车道保持 | 8765 | `http://<机器人IP>:8765` |
| 视觉面板 | 8792 | `http://<机器人IP>:8792` |
| 群组控制 | 8790 | `http://<机器人IP>:8790` |
| 视觉抓取 | 8795 | `http://<机器人IP>:8795` |
| 任务编排 | 8796 | `http://<机器人IP>:8796` |

---

## 用户意图 → 执行规划

### 模式切换

**"切到手动模式 / 我要遥控"**
```
→ xrmode stop
→ xrmode manual
→ xrmode status 等待 stage=ready
```

**"开始建图 / 扫描环境"**
```
→ xrmode stop  
→ xrmode mapping
→ 等待 stage=ready
→ 告知用户 http://<IP>:8080 看画面
```

**"开始导航 / 去XX点"**
```
→ xrmode stop
→ xrmode navigation
→ 等待 stage=ready
→ 注意：导航点需通过 RViz2 或 APP 设置
```

**"保存地图"**
```
→ 先 xrmode status 确认在 mapping 模式
→ xrmode save
→ 看返回的 yaml 路径
```

**"停下来 / 急停"**
```
→ xrmode stop
→ 立即向用户说明：如果机器人仍在运动，现场人员需要立刻采取人工安全措施
→ 不要把“手写 ros2 topic pub /cmd_vel ...”当成默认急停方案
→ 停止后用 xrmode status 确认当前模式已退出或不再处于 ready
```

### 查询状态

**"检查机器人状态 / 当前什么情况"**
```
→ xrmode status
→ 解析 JSON，汇报 stage + mode + 异常
```

**"雷达正常吗 / 前面有障碍物吗"**
```
→ xrmode status 看 stale_topics 中 /scan 是否超时
```

**"看看摄像头画面"**
```
→ 用户需要浏览器访问 http://<IP>:8080/stream_viewer?topic=/camera/color/image_raw
```

### 高级功能

**"开始自动驾驶跑圈"**
```
→ 先提醒用户：机器人启动后可能立即开始自主运动，先确认场地清空、赛道正确、有人现场看护
→ ros2launch xrrobot_autopilot xrrobot_autopilot_drive.launch.py
```

**"开始巡线 / 车道保持"**
```
→ ros2launch xrrobot_lanekeeping xrrobot_lanekeeping.launch.py
→ 告知用户访问 http://<IP>:8765
```

**"启动跟随"**
```
→ 先提醒用户：机器人启动后可能立即跟随前方目标移动，请先清空前方区域并保持人工看护
→ ros2launch xrrobot_follower laser_follower.launch.py
→ 确认后再让用户站到雷达前方
```

**"启动警戒"**
```
→ 先提醒用户：该模式会持续监测并可能触发告警，确保部署区域和阈值符合预期
→ ros2launch xrrobot_follower radar_guard.launch.py
→ 1m 内触发报警
```

**"训练YOLO模型"**
```
→ 先提醒用户：Web 服务建议只在可信局域网访问，采集画面和训练数据可能包含敏感信息
→ ros2launch xrrobot_yolo_studio xrrobot_yolo_studio.launch.py
→ 告知用户访问 http://<IP>:8091
```

**"启动YOLO识别 / 用某个YOLO模型开始识别 / 发布识别结果"**
```
→ 先提醒用户：识别服务建议只在可信局域网中使用；若后续接入控车链路，先单独验证模型效果
→ 先自动检索 xrrobot_yolo_studio 下的 data/models、data/runs、config 中的 .pt/.onnx
→ 只有一个候选时，直接用它作为 model_path
→ 多个候选时，列出模型给用户选择
→ 没有候选时，再追问模型路径
→ ros2launch xrrobot_yolo_studio xrrobot_yolo_detection.launch.py model_path:=<模型路径>
→ 如相机已在其他模块启动，则加 launch_camera:=false image_topic:=/camera/color/image_raw
→ 说明结果发布到 /xrrobot_yolo_studio/detection_results
```

**"启动视觉抓取"**
```
→ ros2launch xrrobot_bringup xrrobot_base.launch.py（需先启动）
→ 另开终端: ros2launch xrrobot_vision_grasp vision_grasp.launch.py
→ 告知用户访问 http://<IP>:8795
```

**"去A点抓物体放到B点 / 任务编排"**
```
→ 导航 launch 已包含底盘和雷达，不要重复启动 base：
  1. ros2launch xrrobot_bringup xrrobot_map_navigation.launch.py
  2. ros2launch xrrobot_vision_grasp vision_grasp.launch.py
  3. ros2launch xrrobot_task_orchestrator xrrobot_task_orchestrator.launch.py
→ 告知用户访问 http://<IP>:8796 加载工作流
```

---

## 重要规则

1. **模式切换独占**：进入新模式前必须先 `xrmode stop` 或 `ros2kill`
2. **等待 ready**：`stage=ready` 才算模式真正就绪
3. **不要混用**：如果之前用 `ros2launch` 启动，先 `ros2kill` 再用 `xrmode`；反之亦然
4. **多步骤任务要多终端**：复杂场景需同时运行多个 `ros2launch`，需提醒用户在机器人上另开终端

---

## 排查

| 问题 | 方法 |
|------|------|
| 模式切不过去 | `xrmode status` 看 `missing_nodes` / `stage` |
| 雷达没数据 | status 中 `stale_topics` 含 `/scan` |
| 看不到画面 | 检查 `http://<IP>:8080` 是否可访问 |
