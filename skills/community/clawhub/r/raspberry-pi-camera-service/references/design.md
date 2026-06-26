# 树莓派摄像头 HTTP 服务设计文档

## 1. 概述

本服务旨在为树莓派提供一个简单、高效的摄像头录制和转换服务。通过 HTTP API 接口，客户端可以远程控制摄像头录制视频，并将原始 H264 流转换为 MP4 或 GIF 格式。

### 1.1 核心理念

- **简单易用**：提供 RESTful API 接口，易于集成
- **心跳机制**：客户端必须定期发送心跳来维持录制会话，超时自动停止
- **单客户端限制**：同一时间只能有一个客户端进行录制
- **自动保护**：服务端自主监控心跳状态，防止资源泄漏
- **双摄像头支持**：自动检测并支持 CSI (Picamera2) 和 USB (FFmpeg) 摄像头
- **高效转换**：H264 到 MP4 采用零拷贝封装，GIF 转换使用高质量调色板

### 1.2 解决的问题

| 问题 | 解决方案 |
|------|---------|
| 远程摄像头控制 | 提供标准化 HTTP API |
| 多摄像头兼容 | 自动检测 CSI/USB 并适配 |
| 格式转换复杂 | 内置 H264→MP4/GIF 转换 |
| 客户端崩溃导致资源泄漏 | 心跳机制 + 自动超时清理 |
| 资源竞争 | 单客户端锁定机制 |
| 大文件传输 | 支持范围请求（断点续传） |

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    树莓派摄像头 HTTP 服务                    │
│  ┌──────────────┐     HTTP API      ┌──────────────────┐   │
│  │   客户端      │ ◀──────────────▶ │   服务端          │   │
│  │ (任何HTTP客户端)│   RESTful API   │ (FastAPI + Picamera2/FFmpeg)│   │
│  └──────────────┘                   └──────────────────┘   │
│         │                                    │              │
│         ▼                                    ▼              │
│    发送指令/下载 ◀────────────────────────▶ 录制视频/转换    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 核心组件

#### 📹 摄像头管理器 (CameraManager)
- 统一接口管理 CSI 和 USB 摄像头
- 自动检测可用摄像头类型
- 统一输出 H264 格式

#### 🔁 格式转换器 (FFmpegConverter)
- 异步 H264 到 MP4 转换（零拷贝封装）
- 异步 H264 到 GIF 转换（高质量调色板）
- 超时保护和错误处理

#### 🌐 HTTP 服务 (FastAPI)
- RESTful API 接口
- 并发控制（单任务锁定）
- 文件管理（上传、下载、删除、列表）

#### 💓 心跳会话管理 (RecordingSession)
- **会话生命周期管理**：创建、续期、过期、清理
- **心跳超时监控**：后台任务定期检查，超时自动停止
- **单客户端保护**：全局锁确保只有一个活跃会话
- **自动资源清理**：心跳超时后自动释放摄像头和文件资源

#### 💻 客户端 SDK (CameraClient)
- Python 客户端库
- 上下文管理器支持
- 便捷录制方法（record_video, record_gif）
- **自动心跳线程**：录制期间自动发送心跳（可选）
- **手动心跳控制**：支持手动发送心跳和延长超时时间

## 3. 核心组件

### 3.1 RecordingSession（心跳会话管理）

#### 会话状态
- `session_id`: 唯一会话ID（UUID）
- `client_id`: 客户端标识
- `created_at`: 会话创建时间
- `last_heartbeat`: 最后心跳时间戳
- `heartbeat_timeout`: 心跳超时时间（秒）
- `is_active`: 会话是否活跃
- `recording_file`: 录制文件路径

#### 心跳机制
- **心跳超时**：默认30秒，可配置（5-300秒）
- **心跳检查间隔**：每5秒检查一次
- **自动清理**：心跳超时自动停止录制并释放资源
- **后台监控**：独立的异步任务监控所有活跃会话

#### 主要接口
- `update_heartbeat(extend_timeout)`: 更新心跳时间，可选延长超时
- `is_expired()`: 检查会话是否过期
- `get_remaining_time()`: 获取剩余心跳时间

### 3.2 CameraManager（摄像头管理器）

## 3. 核心组件

### 3.1 CameraManager（摄像头管理器）

#### 摄像头类型
- `csi`：树莓派 CSI 摄像头，使用 Picamera2 硬件编码
- `usb`：USB 摄像头，使用 FFmpeg 软件编码
- 自动回退：CSI 不可用时自动切换到 USB

#### 主要接口
- `init_camera(width, height, fps)`：初始化摄像头
- `start_recording(execution_id, task_name)`：开始录制 H264
- `stop_recording()`：停止录制并返回文件信息
- `delete_recording()`：删除当前录制文件
- `release()`：释放摄像头资源

### 3.2 FFmpegConverter（格式转换器）

#### 转换功能
- **H264 → MP4**：极速封装，不重新编码，保留原始质量
- **H264 → GIF**：提取指定时长，高质量调色板，支持自定义参数

#### 主要接口
- `h264_to_mp4(h264_path, framerate, delete_original)`：异步转换为 MP4
- `h264_to_gif(h264_path, duration, fps, width)`：异步转换为 GIF

### 3.3 HTTP API 服务

#### 主要端点
- `GET /`：服务信息
- `GET /status`：获取当前录制状态
- `POST /start`：开始录制
- `POST /stop/{session_id}`：停止录制并转换
- `PUT /heartbeat/{session_id}`：发送心跳续期会话
- `GET /videos/{filename}`：下载视频文件
- `DELETE /videos/{filename}`：删除视频文件
- `GET /videos/`：列出所有视频文件

#### 请求/响应模型
- `StartRequest`：开始录制请求参数（包含 `heartbeat_timeout`）
- `StopRequest`：停止录制请求参数
- `HeartbeatRequest`：心跳请求参数（可选 `extend_timeout`）
- `StartResponse`：开始录制响应（包含 `session_id`, `heartbeat_timeout`）
- `StopResponse`：停止录制响应
- `JobInfo`：当前任务信息（包含会话详细信息）

### 3.4 CameraClient（客户端 SDK）

#### 主要方法
- `start_recording(task_name, output_format, heartbeat_timeout, ...)`：开始录制，返回 `session_id`
- `stop_recording(keep_video, reason)`：停止录制
- `send_heartbeat(session_id, extend_timeout)`：手动发送心跳
- `record_video(duration, task_name, output_format)`：便捷录制视频
- `record_gif(duration, width, fps, **kwargs)`：便捷录制 GIF
- `download(remote_filename, local_path)`：下载文件
- `delete_remote(filename)`：删除远程文件
- `list_videos(limit, offset)`：列出视频文件

#### 自动心跳支持
- **自动模式**：`heartbeat_enabled=True`（默认），启动录制后自动发送心跳
- **心跳间隔**：默认10秒（约等于超时时间的1/3）
- **手动模式**：`heartbeat_enabled=False`，需手动调用 `send_heartbeat()`

## 4. 心跳机制协议

### 4.1 心跳流程

```
客户端                          服务端
  |                              |
  |-- POST /start ------------->|  创建会话，返回 session_id
  |                              |  启动后台心跳监控
  |<--------------------------|  {session_id, heartbeat_timeout: 30}
  |                              |
  |-- PUT /heartbeat/{id} ----->|  发送心跳（每10秒）
  |                              |  更新 last_heartbeat
  |<--------------------------|  {remaining_time: 30}
  |                              |
  |-- PUT /heartbeat/{id} ----->|  继续发送心跳
  |                              |
  |   (停止发送心跳)              |
  |                              |
  |                              |  后台监控检测到超时（30秒）
  |                              |  自动停止录制
  |                              |  释放资源
```

### 4.2 开始录制 (`POST /start`)

**请求参数**：
```json
{
  "client_id": "string",
  "task_name": "string",
  "output_format": "h264|mp4|gif",
  "keep_original": "boolean",
  "heartbeat_timeout": "integer",  // 5-300 秒
  "gif_params": {
    "fps": "integer",
    "max_duration_sec": "integer",
    "width": "integer",
    "quality": "integer",
    "loop": "boolean"
  }
}
```

**响应**：
```json
{
  "success": "boolean",
  "session_id": "string",          // 会话唯一标识
  "execution_id": "string",        // 兼容旧版（session_id 前8位）
  "message": "string",
  "confirmed_format": "h264|mp4|gif",
  "h264_path": "string",
  "heartbeat_timeout": "integer"   // 心跳超时时间（秒）
}
```

### 4.3 发送心跳 (`PUT /heartbeat/{session_id}`)

**请求参数**（可选）：
```json
{
  "extend_timeout": "integer"  // 可选：延长心跳超时时间（5-300秒）
}
```

**响应**：
```json
{
  "success": "boolean",
  "session_id": "string",
  "last_heartbeat": "ISO8601 timestamp",
  "expires_at": "ISO8601 timestamp",
  "remaining_time": "integer"  // 剩余心跳时间（秒）
}
```

### 4.4 停止录制 (`POST /stop/{session_id}`)

**说明**：支持使用完整 `session_id` 或旧版 `execution_id`（前8位）

**请求参数**：
```json
{
  "keep_video": "boolean",
  "reason": "string"
}
```

**响应**：
```json
{
  "success": "boolean",
  "execution_id": "string",
  "video_path": "string",
  "h264_path": "string|null",
  "format": "h264|mp4|gif|deleted",
  "file_size_bytes": "integer",
  "message": "string"
}
```

### 4.5 状态查询 (`GET /status`)

**响应**：
```json
{
  "is_recording": "boolean",
  "current_job_id": "string|null",
  "session_id": "string|null",       // 新增
  "client_id": "string|null",
  "format": "string|null",
  "start_time": "string|null",
  "output_path": "string|null",
  "last_heartbeat": "string|null",   // 新增：最后心跳时间
  "expires_at": "string|null",       // 新增：过期时间
  "remaining_time": "integer|null"   // 新增：剩余心跳时间
}
```

## 5. 心跳机制与并发控制

### 5.1 心跳超时机制

- **默认超时时间**：30秒
- **可配置范围**：5-300秒
- **检查间隔**：每5秒检查一次活跃会话
- **自动清理**：心跳超时后自动停止录制，释放摄像头和文件资源
- **日志记录**：超时事件会被记录到日志中

### 5.2 单客户端限制

- **全局锁**：使用 `asyncio.Lock` 确保同一时间只有一个录制任务
- **会话互斥**：开始录制时检查锁状态，如果被占用返回 423 Locked
- **资源独占**：录制期间摄像头资源被独占，其他客户端必须等待

### 5.3 后台监控任务

```python
async def _monitor_heartbeats():
    """后台任务：每5秒检查一次活跃会话的心跳超时"""
    while True:
        session = state.get_active_session()
        if session and session.is_expired():
            logger.warning(f"会话 {session.session_id} 心跳超时，自动停止")
            await _auto_stop_session("心跳超时")
        await asyncio.sleep(HEARTBEAT_CHECK_INTERVAL)  # 5秒
```

### 5.4 自动清理流程

1. 检测到心跳超时
2. 停止摄像头录制
3. 保留录制文件（不删除）
4. 清理会话状态
5. 释放摄像头资源
6. 释放全局锁
7. 记录日志

## 4. API 协议

### 4.1 开始录制 (`POST /start`)

**请求参数**：
```json
{
  "client_id": "string",
  "task_name": "string",
  "output_format": "h264|mp4|gif",
  "keep_original": "boolean",
  "gif_params": {
    "fps": "integer",
    "max_duration_sec": "integer",
    "width": "integer",
    "quality": "integer",
    "loop": "boolean"
  }
}
```

**响应**：
```json
{
  "success": "boolean",
  "execution_id": "string",
  "message": "string",
  "confirmed_format": "h264|mp4|gif",
  "h264_path": "string"
}
```

### 4.2 停止录制 (`POST /stop/{execution_id}`)

**请求参数**：
```json
{
  "keep_video": "boolean",
  "reason": "string"
}
```

**响应**：
```json
{
  "success": "boolean",
  "execution_id": "string",
  "video_path": "string",
  "h264_path": "string|null",
  "format": "h264|mp4|gif|deleted",
  "file_size_bytes": "integer",
  "message": "string"
}
```

## 5. 并发控制机制

- **单任务锁定**：使用 `asyncio.Lock` 确保同时只有一个录制任务
- **错误状态**：录制失败时自动清理资源
- **服务关闭**：优雅关闭，强制停止未完成的录制任务

## 6. 文件管理

### 6.1 文件存储
- 临时目录：`/tmp/videos`
- 文件命名：`{timestamp}_{execution_id}_{task_name}.{ext}`
- 支持格式：`.h264`, `.mp4`, `.gif`

### 6.2 文件操作
- **下载**：支持范围请求（断点续传）
- **删除**：安全的文件名验证，防止目录遍历
- **列表**：分页查询，按修改时间排序

## 7. 错误处理策略

| 错误类型 | HTTP 状态码 | 处理方式 |
|---------|------------|----------|
| 服务正忙 | 423 Locked | 返回占用信息 |
| 文件不存在 | 404 Not Found | 返回文件不存在 |
| 非法文件名 | 400 Bad Request | 防止目录遍历 |
| 内部错误 | 500 Internal Server Error | 详细错误日志 |
| 摄像头初始化失败 | 500 Internal Server Error | 自动清理资源 |


## 9. 使用示例

### 9.1 服务端启动
```bash
python main.py
# 默认监听 0.0.0.0:27793
```

### 9.2 Python 客户端使用（自动心跳）

```python
from sdk.client import CameraClient

# 初始化客户端（自动心跳默认启用）
client = CameraClient("http://raspberry-pi-ip:27793")

# 开始录制（设置心跳超时30秒）
result = client.start_recording(
    task_name="test_video",
    output_format="mp4",
    heartbeat_timeout=30  # 心跳超时时间
)

print(f"Session ID: {result['session_id']}")
print(f"Heartbeat Timeout: {result['heartbeat_timeout']}s")

# SDK 会自动在后台发送心跳，无需手动管理
# 录制持续进行...

# 停止录制
stop_result = client.stop_recording(keep_video=True)
print(f"视频文件: {stop_result['video_path']}")
```

### 9.3 Python 客户端使用（手动心跳）

```python
from sdk.client import CameraClient
import time

# 初始化客户端（禁用自动心跳）
client = CameraClient("http://raspberry-pi-ip:27793", heartbeat_enabled=False)

# 开始录制
result = client.start_recording(
    task_name="manual_heartbeat",
    output_format="h264",
    heartbeat_timeout=15  # 设置较短的超时时间
)

session_id = result["session_id"]

# 手动发送心跳（每5秒一次）
for i in range(3):
    time.sleep(5)
    heartbeat = client.send_heartbeat(session_id)
    print(f"Heartbeat {i+1}: 剩余时间 {heartbeat['remaining_time']}s")

# 停止录制
client.stop_recording(keep_video=True)
```

### 9.4 直接 HTTP 调用

```bash
# 1. 开始录制
curl -X POST http://raspberry-pi:27793/start \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "http_test",
    "output_format": "gif",
    "heartbeat_timeout": 30
  }'

# 假设返回:
# {
#   "success": true,
#   "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
#   "execution_id": "a1b2c3d4",
#   "heartbeat_timeout": 30
# }

# 2. 定期发送心跳（每10秒一次）
SESSION_ID="a1b2c3d4-e5f6-7890-abcd-ef1234567890"

while true; do
  curl -X PUT http://raspberry-pi:27793/heartbeat/$SESSION_ID
  sleep 10
done

# 3. 停止录制（在另一个终端或脚本中）
curl -X POST http://raspberry-pi:27793/stop/$SESSION_ID \
  -H "Content-Type: application/json" \
  -d '{"keep_video": true}'

# 4. 下载文件
curl http://raspberry-pi:27793/videos/20240101_120000_a1b2c3d4.gif -o output.gif
```

### 9.5 心跳超时自动清理示例

```python
from sdk.client import CameraClient
import time

client = CameraClient("http://raspberry-pi-ip:27793", heartbeat_enabled=False)

# 开始录制但不发送心跳（模拟客户端崩溃）
result = client.start_recording(
    task_name="timeout_test",
    output_format="h264",
    heartbeat_timeout=10  # 设置10秒超时
)

print("录制开始，但不发送心跳...")
print("等待心跳超时自动清理...")

# 等待15秒（超过10秒超时时间）
time.sleep(15)

# 检查状态（应该已经自动停止）
status = client.get_status()
print(f"录制状态: {status['is_recording']}")  # 应该是 False
print("✅ 心跳超时后服务端已自动清理资源")
```

## 10. 技术约束

### 10.1 硬件要求
- **CSI 摄像头**：树莓派官方 CSI 摄像头
- **USB 摄像头**：支持 H264 或 MJPEG 格式的 USB 摄像头
- **存储空间**：足够的临时存储空间（/tmp/videos）

### 10.2 软件依赖
- Python 3.7+
- FastAPI
- Uvicorn
- Picamera2 (可选，用于 CSI)
- FFmpeg (必需，用于 USB 和格式转换)
- Requests (用于客户端 SDK)

### 10.3 心跳机制约束
- **默认心跳超时**：30秒
- **最小心跳超时**：5秒
- **最大心跳超时**：300秒（5分钟）
- **心跳检查间隔**：5秒
- **自动心跳间隔**：约10秒（超时时间的1/3）
- **单会话限制**：同一时间只能有一个活跃录制会话

### 10.4 性能限制
- **并发**：单任务录制（避免资源竞争）
- **转换超时**：MP4 转换 60 秒，GIF 转换 120 秒
- **文件大小**：受限于可用磁盘空间
- **网络带宽**：大文件下载可能较慢
- **心跳开销**：后台监控任务每5秒检查一次，开销极小