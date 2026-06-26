---
name: rdk-x5-media
description: "RDK X5 多媒体处理：音频录制/播放（arecord/aplay/PulseAudio）、hobot_codec 视频编解码、RTSP 拉流/推流、HDMI 分辨率配置、MIPI LCD 触摸屏适配、VNC 远程桌面服务端安装与配置。Use when the user wants to record or play audio, encode/decode video, configure HDMI output, set up LCD screen, use RTSP streaming to view camera on PC, set up VNC desktop server, or stream camera video to remote viewer. Do NOT use for VNC 连接失败排查 (use rdk-x5-network), running AI algorithms (use rdk-x5-ai-detect), camera hardware setup (use rdk-x5-camera), or system backup (use rdk-x5-system)."
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - arecord
        - ffmpeg
    compatibility:
      platform: rdk-x5
---

# RDK X5 Media — 多媒体处理

## 操作步骤

### 1. 音频配置

```bash
# 选择音频设备（PulseAudio 通道同步，v3.4.1+）
sudo srpi-config
# → Audio Options

# 查看设备
aplay -l        # 播放设备
arecord -l      # 录音设备
```

支持音频子板：微雪 WM8960 Audio HAT、幻尔载板。

### 2. 音频录制与播放

```bash
# 录音（16kHz 单声道 16bit 5秒）
arecord -D plughw:0,0 -f S16_LE -r 16000 -c 1 -d 5 test.wav

# 播放
aplay test.wav

# PulseAudio 方式
parecord --rate=16000 --channels=1 test.wav
paplay test.wav
```

### 3. 视频编解码（hobot_codec）

```bash
source /opt/tros/humble/setup.bash

# NV12 → MJPEG 编码
ros2 launch hobot_codec hobot_codec_encode.launch.py

# RGB → MJPEG（USB 摄像头 YUYV 模式）
ros2 launch hobot_codec hobot_codec_encode.launch.py \
  codec_in_mode:=ros codec_in_format:=rgb8 \
  codec_sub_topic:=/image codec_pub_topic:=/image_mjpeg
```
ISP/VIO/编解码模块在 v3.4.1 经过大规模稳定性修复。

### 4. RTSP 拉流 + AI 推理

```bash
source /opt/tros/humble/setup.bash
ros2 launch hobot_rtsp_client hobot_rtsp_client.launch.py \
  rtsp_url:="rtsp://admin:password@192.168.1.64:554/stream1"
```
浏览器 `http://<RDK_IP>:8000` 查看结果。

### 5. WebSocket 实时预览

```bash
source /opt/tros/humble/setup.bash
ros2 launch websocket websocket.launch.py \
  websocket_image_topic:=/image_jpeg websocket_only_show_image:=true
```

### 6. HDMI 显示配置

```bash
xrandr                                           # 查看当前分辨率
xrandr --output HDMI-1 --mode 1920x1080          # 设置分辨率
```
v3.4.1 已优化多分辨率兼容性，v3.1.1 修复竖屏黑屏问题。

### 7. MIPI LCD 触摸屏

```bash
sudo srpi-config
# → Display Options → MIPI Screen
```

已适配型号：11.9寸微雪宽屏（v3.4.1）、7款微雪 MIPI DSI 屏（v3.0.1+）。
- 支持双击和长按操作，长按模拟右键
- v3.4.1 修复触摸坐标漂移

### 8. VNC 远程桌面

```bash
sudo srpi-config
# → Interface Options → VNC → Enable
```

## 常用命令

```bash
v4l2-ctl --list-devices                          # 列出视频设备
v4l2-ctl -d /dev/video0 --list-formats-ext       # 查看格式
v4l2-ctl -d /dev/video0 --set-fmt-video=width=1920,height=1080,pixelformat=MJPG \
  --stream-mmap --stream-to=frame.jpg --stream-count=1    # 截图
```

## 排查故障

| 现象 | 原因 | 解决 |
|------|------|------|
| `arecord` 无设备 | 音频子板未接或未配置 | `srpi-config` → Audio 选择设备 |
| HDMI 无输出 | 分辨率不兼容 | 换低分辨率显示器测试；检查 `xrandr` |
| LCD 触摸偏移 | 型号未正确选择 | `srpi-config` 重新选择屏幕型号 |
| websocket 页面空白 | codec 未启动或 topic 不匹配 | 确认 `hobot_codec` 节点运行中 |
