---
name: rdk-x5-camera
description: "配置并启动 RDK X5 上的 MIPI CSI 摄像头、USB 摄像头或双目深度摄像头（RealSense/ZED/Orbbec），通过 Web 浏览器预览实时画面。Use when the user wants to start a camera, preview video, capture images, or troubleshoot camera connection issues on RDK X5. Do NOT use for AI inference on camera feeds (use rdk-x5-ai-detect), audio/video encoding (use rdk-x5-media), or GPIO hardware (use rdk-x5-gpio)."
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - ros2
    compatibility:
      platform: rdk-x5
---

# RDK X5 Camera — 摄像头配置与图像采集

## 已适配摄像头

| 类型 | 型号 | 接口 |
|------|------|------|
| MIPI CSI | IMX219, IMX415, IMX477, OV5647, F37, GC4663 | CAM 0/1 |
| MIPI 双目 | SC230ai, SC132gs | CAM 0 + 1 |
| USB | 任何 UVC 兼容（MJPEG/YUYV） | /dev/videoX |
| 深度相机 | Intel RealSense, ZED, Orbbec Gemini | USB 3.0 |

## 操作步骤

### 1. 启动 MIPI 摄像头

> ⚠️ **严禁带电插拔 MIPI 摄像头**，否则烧坏模组。先断电再接线。

```bash
source /opt/tros/humble/setup.bash

# 单路 MIPI
ros2 launch mipi_cam mipi_cam.launch.py

# 双路 MIPI（需两个 CSI 接口都接上）
ros2 launch mipi_cam mipi_cam_dual_channel.launch.py

# 第二路需要 remap topic
ros2 run mipi_cam mipi_cam --ros-args --remap /image_raw:=/image_raw_alias
```

### 2. 启动 USB 摄像头

```bash
source /opt/tros/humble/setup.bash

# Step 1: 确认设备节点
ls /dev/video*
v4l2-ctl --list-devices

# Step 2: MJPEG 模式（推荐，低 CPU 占用）
ros2 launch hobot_usb_cam hobot_usb_cam.launch.py \
  usb_video_device:=/dev/video0

# Step 2 备选: YUYV→RGB 模式（兼容性更广）
ros2 launch hobot_usb_cam hobot_usb_cam.launch.py \
  usb_video_device:=/dev/video0 \
  usb_pixel_format:=yuyv2rgb \
  usb_image_width:=640 usb_image_height:=480
```

### 3. 启动双目深度摄像头

**RealSense:**
```bash
sudo apt-get install ros-humble-librealsense2* ros-humble-realsense2-* -y
ros2 launch realsense2_camera rs_launch.py \
  enable_rgbd:=true enable_sync:=true \
  align_depth.enable:=true enable_color:=true enable_depth:=true
```

**ZED:**
```bash
source /opt/tros/humble/setup.bash
ros2 launch hobot_zed_cam pub_stereo_imgs.launch.py need_rectify:=true
```

### 4. Web 浏览器预览

```bash
source /opt/tros/humble/setup.bash

# 编码 + WebSocket
ros2 launch hobot_codec hobot_codec_encode.launch.py &
ros2 launch websocket websocket.launch.py \
  websocket_image_topic:=/image_jpeg \
  websocket_only_show_image:=true
```
浏览器访问 `http://<RDK_IP>:8000` 查看画面。

### 5. ISP 图像调参

```bash
cd /app/multimedia_samples/tuning_tool
make && sudo ./run_tuning.sh
```
用于调整白平衡、曝光、降噪等 ISP 参数（C 源码需先编译）。

### 6. 停止所有摄像头服务

```bash
pkill -f "ros2.*cam" ; pkill -f "ros2.*websocket" ; pkill -f "ros2.*codec"
```

## 排查故障

| 现象 | 原因 | 解决 |
|------|------|------|
| `/dev/video*` 无设备 | USB 未识别或 MIPI 未接好 | 检查物理连接；`dmesg \| tail` 查看内核日志 |
| 启动报 `Open camera failed` | 设备节点错误或被占用 | `fuser /dev/video0` 查看占用进程，`kill` 后重试 |
| Web 页面无画面 | WebSocket 未启动或端口被占 | 确认 websocket 节点运行中：`ros2 node list` |
| MIPI 画面全黑 | 排线松动或型号不匹配 | 断电重新插拔排线；检查 `dmesg` 中 sensor probe 日志 |
| USB 帧率低 | YUYV 模式 CPU 占用高 | 切换为 MJPEG 模式，或降低分辨率 |
