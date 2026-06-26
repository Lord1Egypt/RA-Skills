---
name: rdk-x5-app
description: "运行 RDK X5 /app 目录下的预装示例程序：12 个 Python AI 推理 demo（YOLO/分类/分割/Web展示）、40pin GPIO 示例、C++ 多媒体示例（编解码/RTSP/VIO）、查看 34 个预装 BPU 模型。Use when the user wants to run pre-installed /app demos, test Python AI samples, compile C++ multimedia examples, or browse the model library. Do NOT use for TROS ROS2 launch commands (use rdk-x5-tros), camera hardware setup (use rdk-x5-camera), or custom AI inference (use rdk-x5-ai-detect)."
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    compatibility:
      platform: rdk-x5
---

# RDK X5 App — /app 预装示例

## 目录结构

```
/app/
├── pydev_demo/         # 12 个 Python AI demo
│   ├── 01_basic_sample/ ~ 12_yolov5s_v6_v7_sample/
│   └── models/          # 34 个 BPU 模型 (.bin)
├── 40pin_samples/       # GPIO/I2C/SPI/PWM/UART 示例
├── cdev_demo/           # 8 个 C++ 多媒体示例
└── multimedia_samples/  # 底层 C 示例
```

## Python AI 示例

### 图像分类（01_basic_sample）
```bash
cd /app/pydev_demo/01_basic_sample
python3 test_mobilenetv1.py     # MobileNetV1
python3 test_resnet18.py        # ResNet18
python3 test_googlenet.py       # GoogleNet
```

### 语义分割（04_segment_sample）
```bash
cd /app/pydev_demo/04_segment_sample
python3 test_segment.py
```

### Web 摄像头展示（05）
```bash
cd /app/pydev_demo/05_web_display_camera_sample
bash start_nginx.sh
python3 mipi_camera_web.py
```
浏览器 `http://<RDK_IP>:8080` 查看。

### YOLO 系列检测
```bash
cd /app/pydev_demo/06_yolov3_sample && python3 test_yolov3.py
cd /app/pydev_demo/07_yolov5_sample && python3 test_yolov5.py
cd /app/pydev_demo/09_yolov5x_sample && python3 test_yolov5x.py
cd /app/pydev_demo/12_yolov5s_v6_v7_sample && python3 test_yolov5s_v6.py
```

### 其他检测
```bash
cd /app/pydev_demo/10_ssd_mobilenetv1_sample && python3 test_ssd_mobilenetv1.py
cd /app/pydev_demo/11_centernet_sample && python3 test_centernet.py
```

### RTSP 流解码（08）
```bash
cd /app/pydev_demo/08_decode_rtsp_stream
python3 test_decode_rtsp.py "rtsp://admin:password@192.168.1.64:554/stream1"
```

## 40pin GPIO 示例

```bash
cd /app/40pin_samples
sudo python3 simple_out.py          # GPIO 输出
sudo python3 simple_input.py        # GPIO 输入
sudo python3 simple_pwm.py          # PWM
sudo python3 button_event.py        # 按钮事件
sudo python3 button_led.py          # 按钮控 LED
sudo python3 test_i2c.py            # I2C
sudo python3 test_spi.py            # SPI
sudo python3 test_serial.py         # UART
```

## C++ 多媒体示例

编译并运行：
```bash
cd /app/cdev_demo/<demo_name>
make && ./<executable>
```

| 目录 | 功能 | 可执行文件 |
|------|------|-----------|
| bpu | BPU C++ 推理 | `bpu_demo` |
| v4l2 | V4L2 摄像头 | `v4l2_demo` |
| vio2display | VIO 到显示 | `vio2display` |
| vio2encoder | VIO 到编码 | `vio2encoder` |
| decode2display | 解码显示 | `decoder2display` |
| rtsp2display | RTSP 显示 | `rtsp2display` |
| vio_capture | VIO 采集 | `capture` |
| vps | 视频处理 | 见目录 |

## 模型库速查

路径：`/app/pydev_demo/models/`（34 个 .bin 文件）

| 类别 | 模型 |
|------|------|
| 分类 | mobilenetv1, mobilenetv2, resnet18, googlenet, efficientnasnet_m/s, efficientnet_lite0~4, vargconvnet |
| 检测 | yolov2, yolov3, yolov5s/5x/5s_v6/v7, yolov8, yolov10, yolov11m, yolov12n, ssd_mobilenetv1, centernet, fcos, fcos_efficientnetb2/b3 |
| 分割 | yolov8_seg, deeplabv3plus (efficientnetb0/m1), fastscnn, mobilenet_unet, stdc |

所有模型为 NV12 格式，专为 BPU 优化。

## ⚠️ 必须使用系统 Python

RDK X5 的 `hobot_dnn` 等硬件库安装在系统 Python (`/usr/bin/python3.10`)，**不在 conda 环境中**。

```bash
# ✅ 正确 — 使用系统 Python
/usr/bin/python3.10 /app/pydev_demo/01_basic_sample/test_resnet18.py

# ❌ 错误 — conda 环境没有 hobot_dnn，会报 ModuleNotFoundError
python /app/pydev_demo/01_basic_sample/test_resnet18.py
```

## 排查故障

| 现象 | 原因 | 解决 |
|------|------|------|
| `ModuleNotFoundError: hobot_dnn` | 使用了 conda 或 venv Python | 改用 `/usr/bin/python3.10` 运行 |
| `make` 编译失败 | 缺少头文件或库 | `sudo apt install libhbm-dev` 检查依赖 |
| Web 展示无画面 | nginx 未启动 | `bash start_nginx.sh` |
| 模型文件找不到 | 路径错误 | 确认模型在 `/app/pydev_demo/models/` |
