---
name: raspberry-pi-camera-service
description: "提供使用摄像头拍照, 录制视频或直接生成gif的能力。何时触发: 需要拍照时, 需要观察一段时间当前视野时, 需要关注某件事情的进展时."
---

# Raspberry Pi Camera Service Skill

## 概述

树莓派摄像头服务提供基于HTTP的树莓派摄像头硬件（CSI或USB）控制，具备以下高级功能：

- 多格式视频录制（H264、MP4、GIF）
- 带心跳监控的会话管理
- 自动超时保护
- 后台转换任务
- 视频文件管理（列表、下载、删除）

## 架构

该服务由三个主要组件组成：

1. **摄像头管理器（Camera Manager）** - 处理底层摄像头硬件（通过Picamera2使用CSI接口，通过FFmpeg使用USB接口）
2. **转换器（Converter）** - 使用FFmpeg将原始H264转换为其他格式（MP4、GIF）
3. **服务（Service）** - 使用FastAPI构建的HTTP API服务器，具备会话管理功能

## 客户端
客户端SDK会在服务端部署时自动安装到本地

## 服务端部署
可通过执行 `python -c "from camera_client import CameraClient"`来判断服务是否被成功部署  
如果发现服务还未部署，则立刻阅读 `references/deploy_service.md` 进行部署

### 快速开始

#### 拍照
```python
from camera_client import CameraClient

with CameraClient() as client:
    result = client.capture(task_name="snapshot")
    print(f"✅ {result['image_path']}")
```

#### 录制 MP4 视频

```python
from camera_client import CameraClient

client = CameraClient()

try:
    # 录制 5 秒的 1080p 视频
    result = client.record_video(
        duration=5,
        task_name="demo_video",
        output_format="mp4"
    )

    print(f"录制完成: {result['video_path']}")
    print(f"文件大小: {result['file_size_bytes'] / 1024 / 1024:.2f} MB")

finally:
    client.session.close()
```

#### 录制 GIF 动图

```python
from camera_client import CameraClient

client = CameraClient()

try:
    # 录制 3 秒的高质量 GIF
    result = client.record_gif(
        duration=3,
        width=480,        # 480 像素宽
        fps=15,           # 15 帧/秒
        quality=7,        # 高质量
        loop=True         # 循环播放
    )

    print(f"GIF 录制完成: {result['video_path']}")

finally:
    client.session.close()
```

#### 手动控制录制流程

```python
from camera_client import CameraClient
import time

client = CameraClient()

try:
    # 1. 开始录制
    result = client.start_recording(
        task_name="manual_control",
        output_format="mp4",
        heartbeat_timeout=30
    )

    # 2. 录制中（等待 6 秒）
    time.sleep(6)

    # 3. 停止录制
    result = client.stop_recording(keep_video=True)

    print(f"✅ 完成: {result['video_path']}")

finally:
    client.session.close()
```

#### 手动心跳控制

```python
from camera_client import CameraClient
import time

# 禁用自动心跳
client = CameraClient(heartbeat_enabled=False)

try:
    # 开始录制（心跳超时 15 秒）
    client.start_recording(
        task_name="manual_heartbeat",
        output_format="h264",
        heartbeat_timeout=15
    )

    # 每 5 秒手动发送一次心跳
    for i in range(3):
        time.sleep(5)
        client.send_heartbeat()

    # 停止录制
    result = client.stop_recording(keep_video=True)

finally:
    client.session.close()
```

如果碰到了问题而需要了解更多细节，请阅读`references/client_usage.md`

## 会话管理

- 每个录制会话都会分配一个唯一的 `session_id`（会话ID）
- 心跳机制可防止客户端断开连接时的资源泄漏
- 若未收到心跳信号，自动超时将停止录制
- 客户端支持启用自动心跳功能

## 支持格式

1. **H264** - 原始H264流（硬件编码，速度最快）
2. **MP4** - 封装在MP4容器中的H264（后台转换）
3. **GIF** - 从视频片段生成的动画GIF，支持可配置参数（后台转换）

## 硬件支持

- **CSI摄像头** - 通过Picamera2提供主要支持（树莓派摄像头模块）
- **USB摄像头** - 通过FFmpeg提供备用支持（标准UVC摄像头）
- 若CSI摄像头不可用，自动检测并回退到USB摄像头

## 错误处理

- 服务繁忙 (423) - 其他客户端正在录制
- API错误 (4xx/5xx) - 无效请求或服务器错误
- 客户端断开连接时自动清理
- 资源管理以防止资源泄漏

## 特别注意

如果你不确定录制时长（根据条件录制），一定要阅读`references/client_usage.md` 
比如你需要录制 **从舵机开始转动到舵机转动结束** 的视频，此时舵机开始转动前，要请求服务开始录制，然后一直到舵机转动结束，再结束录制。**期间要维持心跳**