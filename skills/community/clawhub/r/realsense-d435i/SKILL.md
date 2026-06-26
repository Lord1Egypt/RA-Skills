---
name: realsense-d435i
description: Intel RealSense D435i 深度相机操作技能。适用：深度照片、3D点云、IMU数据、RGBD视频录制。自动按日期分目录存储。
---

# RealSense D435i Skill

Intel RealSense D435i 深度相机的拍摄脚本，支持深度照片、3D点云、IMU数据、RGBD视频。

## 依赖

- **硬件**: Intel RealSense D435i
- **系统**: Linux（需要 V4L2 支持）
- **Python**: 3.x（测试于 3.8）
- **依赖库**: `opencv-python` / `opencv-python-headless`、`numpy`、`pyrealsense2`
- **系统工具**: `ffmpeg`（用于视频编码）、`rs-enumerate-devices`（可选）

安装依赖：
```bash
pip install opencv-python-headless numpy pyrealsense2
```

## 快速开始

```bash
# 深度拍照
python3 scripts/realsense_capture.py --mode depth

# 3D 点云
python3 scripts/realsense_capture.py --mode pointcloud

# IMU 数据（5秒）
python3 scripts/realsense_capture.py --mode imu --duration 5

# RGBD 视频（5秒）
python3 scripts/realsense_capture.py --mode rgbd --duration 5
```

## 输出目录

数据默认保存到 `data/`（脚本同目录下），按内容类型和日期分目录：

```
data/
├── photos/
│   └── YYYY-MM-DD/
│       ├── rgb/         RGB 照片
│       └── depth/       深度照片（伪彩色 + 原始 PNG）
├── videos/
│   └── YYYY-MM-DD/
│       ├── rgb/         RGB 视频
│       └── depth/       深度视频（伪彩色）
├── pointcloud/
│   └── YYYY-MM-DD/     3D 点云（PLY）
└── imu/
    └── YYYY-MM-DD/     IMU 数据（CSV）
```

指定其他路径：
```bash
python3 scripts/realsense_capture.py --mode depth --output /path/to/storage/
```

## 输出文件说明

| 模式 | 文件 | 说明 |
|------|------|------|
| depth | `depth_colorized_*.jpg` | 伪彩色深度图（近=红，远=蓝） |
| depth | `rgb_*.jpg` | 对齐后的 RGB 照片 |
| depth | `depth_raw_*.png` | 原始 16 位深度数据（需专门工具查看） |
| rgbd | `rgb_*.mp4` | RGB 彩色视频 |
| rgbd | `depth_*.mp4` | 伪彩色深度视频 |
| pointcloud | `pointcloud_*.ply` | 3D 点云（可用 MeshLab / CloudCompare 打开） |
| imu | `imu_*.csv` | 加速度计 + 陀螺仪原始数据 |

## 设备节点

USB 设备节点在拔插后可能变化，可通过以下方式确认：
```bash
rs-enumerate-devices
# 或
ffmpeg -f v4l2 -list_formats all -i /dev/video0
```

当前测试节点（参考）：
- `/dev/video0` → Depth（gray16le）
- `/dev/video2` → Infrared
- `/dev/video4` → RGB（yuyv422）

## USB 带宽限制

D435i 使用 USB 2.1，同时启用 Depth + RGB 时建议：
- ✅ 640×480 @ 30fps（推荐）
- ⚠️ 1280×720 @ 6fps（勉强可用）

1080p RGB 建议单独录制（无 Depth 同时）。

## 查看点云文件

PLY 文件需要专门工具：
- [MeshLab](https://www.meshlab.net/downloads)（推荐，免费）
- [CloudCompare](https://www.dashcamviewer.com/)
- 在线查看：https://3dviewer.net/

## 配置说明

- Python 解释器：脚本开头 shebang 为 `#!/usr/bin/env python3`，系统会自动找到
- 如果遇到 `ModuleNotFoundError`，确认依赖已安装：`pip install opencv-python-headless numpy pyrealsense2`
- 视频编码依赖 `ffmpeg`，确保已安装
