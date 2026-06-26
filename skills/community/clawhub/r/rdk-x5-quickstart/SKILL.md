---
name: rdk-x5-quickstart
description: "RDK X5 新手快速入门：从开箱到第一个 AI 应用的完整流程，包括首次烧录镜像、首次启动、首次连接网络、运行第一个 YOLO 检测 demo。Use when the user is a beginner, first-time user, just unboxed the board, asks '怎么开始/入门/第一次', or needs the initial image flashing guide. Do NOT use for re-flashing an existing board or firmware upgrade (use rdk-x5-system), advanced system management (use rdk-x5-system), specific AI algorithms (use rdk-x5-ai-detect), or TROS development (use rdk-x5-tros)."
license: MIT-0
metadata:
  openclaw:
    compatibility:
      platform: rdk-x5
---

# RDK X5 Quickstart — 快速入门

从开箱到运行第一个 AI 应用。

## Step 1: 烧录系统镜像

1. 从 [地瓜机器人官网](https://developer.d-robotics.cc/) 下载最新 RDK OS 镜像
2. 使用 balenaEtcher 或 `dd` 烧录到 microSD 卡（≥16GB）：
```bash
sudo dd if=rdk_os_image.img of=/dev/sdX bs=4M status=progress && sync
```
3. 插入 SD 卡到 RDK X5

## Step 2: 首次启动

1. 接上电源（Type-C 5V/3A 或 12V DC）
2. 默认账号：`root` / `root` 或 `sunrise` / `sunrise`
3. 系统启动后自动获取 IP（有线 DHCP）

## Step 3: 连接网络

```bash
# 查看 IP（有线）
ip addr show eth0

# 连接 WiFi
sudo nmcli device wifi connect "你的WiFi名" password "你的密码"

# 确认联网
ping -c 2 baidu.com
```

## Step 4: 确认系统版本

```bash
rdkos_info
cat /etc/version
```

## Step 5: 更新系统（推荐）

```bash
sudo apt update && sudo apt upgrade -y
```

## Step 6: 运行第一个 AI Demo

### 方式 A: Python 脚本（最简单）
```bash
cd /app/pydev_demo/07_yolov5_sample
python3 test_yolov5.py
```
终端输出检测结果。

### 方式 B: TROS + 摄像头 + Web 展示（推荐）

1. 接上 USB 或 MIPI 摄像头
2. 运行：
```bash
source /opt/tros/humble/setup.bash
ros2 launch dnn_node_example dnn_node_example.launch.py \
  dnn_example_config_file:=config/yolov5sworkconfig.json \
  dnn_example_image_width:=640 dnn_example_image_height:=480
```
3. 浏览器打开 `http://<RDK_IP>:8000` 查看实时检测画面

## Step 7: 下一步探索

| 想做什么 | 使用哪个 Skill |
|---------|---------------|
| 管理摄像头 | rdk-x5-camera |
| 运行更多 AI 算法 | rdk-x5-ai-detect |
| 控制 GPIO/舵机 | rdk-x5-gpio |
| 监控系统状态 | rdk-x5-monitor |
| 使用 ROS2 开发 | rdk-x5-tros |
| 运行 /app 示例 | rdk-x5-app |
| 系统备份/升级 | rdk-x5-system |

## 排查故障

| 现象 | 原因 | 解决 |
|------|------|------|
| 无法启动（无串口输出） | SD 卡未正确烧录 | 重新烧录镜像；换一张 SD 卡 |
| 启动后无法 SSH | IP 未知 | 用串口登录查看 IP；或连接显示器 |
| `apt update` 失败 | 无网络或 DNS 问题 | `ping 8.8.8.8`；检查网线/WiFi |
| 摄像头无画面 | 未接摄像头或设备节点错误 | `ls /dev/video*` 确认设备存在 |
