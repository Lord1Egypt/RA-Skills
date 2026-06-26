---
name: rdk-x5-tros
description: "使用 RDK X5 上的 TogetheROS.Bot (tros.b) Humble 框架：启动 43 个预装 ROS2 算法包、管理 ROS2 话题/节点/服务、构建摄像头+AI+输出（Web/语音/HDMI）集成 pipeline、创建自定义 ROS2 工作空间。Use when the user mentions ROS2, TROS, ros2 launch, topic/node/service, or wants to build an integrated multi-component pipeline combining camera + AI + any output (集成/pipeline/全链路). Also use when user combines camera + AI + display/audio in one request. Do NOT use for camera-only hardware setup (use rdk-x5-camera), /app demo scripts (use rdk-x5-app), standalone AI inference without ROS2 (use rdk-x5-ai-detect), GPIO/I2C hardware (use rdk-x5-gpio), or system management (use rdk-x5-system)."
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - ros2
        - colcon
    compatibility:
      platform: rdk-x5
---

# RDK X5 TROS — TogetheROS.Bot 机器人开发

所有 tros 包安装在 `/opt/tros/humble/`，共 43 个包、136 个 launch 文件。

## 前置准备

```bash
# 每个终端必须 source
source /opt/tros/humble/setup.bash
```

## 预装包速查表

### 感知算法（17 个）
| 包名 | 功能 |
|------|------|
| dnn_node_example | YOLO/分类/分割通用推理 |
| mono2d_body_detection | 人体 2D 检测 |
| mono3d_indoor_detection | 室内 3D 检测 |
| face_age_detection | 人脸年龄检测 |
| face_landmarks_detection | 人脸关键点 |
| hand_gesture_detection | 手势检测 |
| hand_lmk_detection | 手部关键点 |
| hobot_falldown_detection | 跌倒检测 |
| hobot_dosod | 开放词汇检测 (DOSOD) |
| hobot_yolo_world | YOLO-World 开放词汇 |
| parking_perception | 停车场感知 |
| mono_mobilesam | MobileSAM 分割 |
| mono_edgesam | EdgeSAM 轻量分割 |
| elevation_net | 高程估计 |
| mono_pwcnet | 光流估计 |
| reid | 行人重识别 |
| clip_manage | CLIP 图文匹配 |

### 传感器驱动（6 个）
| 包名 | 功能 |
|------|------|
| mipi_cam | MIPI 摄像头 |
| hobot_usb_cam | USB 摄像头 |
| hobot_zed_cam | ZED 双目 |
| hobot_stereonet | 双目深度估计 |
| imu_sensor | IMU |
| hobot_audio | 音频采集 |

### 处理与输出（8 个）
| 包名 | 功能 |
|------|------|
| hobot_codec | 图像编解码 |
| hobot_cv | 硬件加速图像处理 |
| hobot_hdmi | HDMI 显示 |
| hobot_image_publisher | 图片发布（测试） |
| hobot_visualization | 可视化叠加 |
| websocket | Web 展示 (port 8000) |
| hobot_rtsp_client | RTSP 拉流 |
| hobot_vio | 视频 IO |

### 应用方案（6 个）
| 包名 | 功能 |
|------|------|
| hobot_llamacpp | 端侧 LLM 大模型 |
| audio_control | 语音控制 |
| audio_tracking | 声源追踪 |
| body_tracking | 人体追踪 |
| gesture_control | 手势控制 |
| parking_search | 智能车位搜索 |

### 工具包（6 个）
hobot_shm（零拷贝共享内存）、tros_lowpass_filter、tros_perception_fusion、dstereo_occnet 等。

## 常用 Pipeline

### 摄像头 + YOLO + Web
```bash
ros2 launch dnn_node_example dnn_node_example.launch.py \
  dnn_example_config_file:=config/yolov5sworkconfig.json \
  dnn_example_image_width:=640 dnn_example_image_height:=480
```

### 人脸关键点 + Web
```bash
ros2 launch face_landmarks_detection body_det_face_landmarks_det.launch.py
```

### DOSOD 开放词汇
```bash
ros2 launch hobot_dosod dosod.launch.py
```

### SAM 分割
```bash
ros2 launch mono_mobilesam sam.launch.py
```

### LLM 大模型
```bash
ros2 launch hobot_llamacpp hobot_llamacpp.launch.py
```

## ROS2 管理命令

```bash
ros2 topic list                    # 所有话题
ros2 topic hz /image_raw           # 话题频率
ros2 topic echo /ai_msg --no-arr  # 打印数据
ros2 node list                     # 运行中节点
ros2 node info /mipi_cam           # 节点详情
ros2 service list                  # 服务列表
ros2 param list                    # 参数列表
```

### 查看 launch 文件

```bash
ls /opt/tros/humble/share/<package_name>/launch/
```

## 自定义开发

```bash
mkdir -p ~/tros_ws/src && cd ~/tros_ws/src
ros2 pkg create my_node --build-type ament_python --dependencies rclpy
cd ~/tros_ws && colcon build
source install/setup.bash
ros2 run my_node my_node
```

## 排查故障

| 现象 | 原因 | 解决 |
|------|------|------|
| `Package not found` | 未 source 环境 | `source /opt/tros/humble/setup.bash` |
| 节点启动后立即退出 | 依赖节点未启动（如缺摄像头） | 先启动摄像头节点，再启动算法节点 |
| topic 无数据 | 节点间 topic 名称不匹配 | `ros2 topic list` 检查；用 `--remap` 对齐 |
| 共享内存报错 | hobot_shm 配置问题 | 检查 `/dev/shm` 空间：`df -h /dev/shm` |
