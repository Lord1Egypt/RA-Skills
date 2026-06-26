---
name: rdk-x5-ai-detect
description: "在 RDK X5 的 10TOPS BPU 上运行单个 AI 推理算法：YOLO 目标检测、图像分类、语义分割、人脸识别、手势识别、人体关键点、开放词汇检测（DOSOD/YOLO-World）、双目深度估计、语音识别、端侧轻量 LLM（≤2B 参数量化模型）。Use when the user wants to run a single AI algorithm, deploy pre-built .bin models to BPU, or ask what AI models/LLMs RDK X5 can run (能力咨询). Do NOT use for camera hardware setup (use rdk-x5-camera), multimedia encoding (use rdk-x5-media), running /app demo scripts (use rdk-x5-app), integrated camera+AI+output pipeline (use rdk-x5-tros), model conversion/quantization/export (use Horizon toolchain on PC), large generative models like Stable Diffusion (insufficient VRAM), or custom code that bridges AI results to external services like MQTT."
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - ros2
    compatibility:
      platform: rdk-x5
---

# RDK X5 AI Detect — BPU AI 推理

RDK X5 搭载 10 TOPS BPU，所有 AI 算法通过 TogetheROS.Bot (tros.b) 框架运行。

## 前置准备

```bash
# 每个终端都需要 source
source /opt/tros/humble/setup.bash

# 安装 Python 推理库（可选，用于自定义推理脚本）
pip3 install hobot-dnn-rdkx5 hobot-vio-rdkx5
```

## 操作步骤

### 1. YOLO 目标检测（摄像头实时）

```bash
source /opt/tros/humble/setup.bash
ros2 launch dnn_node_example dnn_node_example.launch.py \
  dnn_example_config_file:=config/yolov5sworkconfig.json \
  dnn_example_image_width:=640 dnn_example_image_height:=480
```
浏览器 `http://<RDK_IP>:8000` 查看检测结果。

可选模型配置文件：
| 模型 | config 文件 |
|------|------------|
| YOLOv5s | `config/yolov5sworkconfig.json` |
| MobileNetV2 分类 | `config/mobilenetv2workconfig.json` |

### 2. 图像分类

```bash
source /opt/tros/humble/setup.bash
ros2 launch dnn_node_example dnn_node_example.launch.py \
  dnn_example_config_file:=config/mobilenetv2workconfig.json
```

### 3. 开放词汇检测（DOSOD / YOLO-World）

```bash
source /opt/tros/humble/setup.bash

# DOSOD（地瓜自研，支持语音指令指定检测目标）
ros2 launch hobot_dosod dosod.launch.py

# YOLO-World
ros2 launch hobot_yolo_world hobot_yolo_world.launch.py
```

### 4. 双目深度估计

```bash
source /opt/tros/humble/setup.bash
# 需配合双目摄像头（SC230ai / SC132gs / ZED）
ros2 launch hobot_stereonet stereonet_model.launch.py
```

### 5. 语音识别 (ASR)

```bash
source /opt/tros/humble/setup.bash
ros2 launch hobot_asr hobot_asr.launch.py
```
需配合音频子板（微雪 WM8960 Audio HAT 或幻尔载板）。

### 6. 端侧 LLM 大模型

```bash
source /opt/tros/humble/setup.bash
ros2 launch hobot_llamacpp hobot_llamacpp.launch.py
```

### 7. Web 可视化

```bash
source /opt/tros/humble/setup.bash
ros2 launch websocket websocket.launch.py
```
所有算法结果叠加实时画面，浏览器 `http://<RDK_IP>:8000` 查看。

### 8. RTSP 拉流 + AI 推理（智能盒子方案）

```bash
source /opt/tros/humble/setup.bash
ros2 launch hobot_rtsp_client hobot_rtsp_client.launch.py \
  rtsp_url:="rtsp://admin:password@192.168.1.64:554/stream1"
```

## 性能监控

```bash
# BPU 使用率
cat /sys/devices/system/bpu/bpu0/ratio

# 推理帧率
ros2 topic hz /ai_msg
```

## 排查故障

| 现象 | 原因 | 解决 |
|------|------|------|
| `Load model failed` | 模型文件不存在或格式错误 | 检查 .bin 文件路径；模型需经 hb_mapper 转换为 NV12 格式 |
| BPU ratio 始终 0 | 推理节点未启动或模型未加载 | `ros2 node list` 确认 dnn_node 正在运行 |
| Web 无 AI 结果叠加 | websocket 未连接 AI topic | 确认 websocket 订阅的 topic 名称正确 |
| 帧率极低 (<5fps) | 模型过大或分辨率过高 | 降低输入分辨率；使用轻量模型（如 YOLOv5s 替代 YOLOv5x） |
