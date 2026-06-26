# CameraClient 使用指南

`client.py` 提供了树莓派摄像头服务的 Python 客户端，支持录制视频（MP4/GIF/H264）和拍照（JPEG）。

## 📖 API 文档

### 初始化客户端

```python
client = CameraClient(
    base_url="http://localhost:27793",  # 服务地址
    timeout=30,                          # API 超时时间（秒）
    heartbeat_enabled=True               # 是否启用自动心跳
)
```

### 核心方法

#### 1. `record_video()` - 录制视频（便捷方法）

```python
result = client.record_video(
    duration=5,              # 录制时长（秒）
    task_name="my_video",    # 任务名称
    output_format="mp4"      # 格式: h264, mp4, gif
)
```

**返回值**:
```python
{
    'success': True,
    'video_path': '/tmp/videos/xxx.mp4',  # 视频路径
    'h264_path': '/tmp/videos/xxx.h264',  # H264 路径
    'format': 'mp4',
    'file_size_bytes': 123456,
    'message': '录制完成，MP4 转换中（后台处理）'
}
```

#### 2. `record_gif()` - 录制 GIF（便捷方法）

```python
result = client.record_gif(
    duration=3,           # 录制时长（秒）
    width=320,            # 宽度（像素）
    fps=10,               # 帧率
    quality=5,            # 质量（1-10）
    loop=True             # 是否循环
)
```

#### 3. `capture()` - 拍照（JPEG）

```python
result = client.capture(
    task_name="snapshot"     # 任务名称，用于文件名
)
```

**返回值**:
```python
{
    'success': True,
    'image_path': '/tmp/videos/xxx.jpg',   # 图片路径
    'filename': 'xxx.jpg',
    'file_size_bytes': 123456,
    'message': '拍照成功'
}
```

**注意**: 拍照与录像互斥，如果正在录制中会返回错误。

#### 5. `start_recording()` - 开始录制（细粒度控制）

```python
result = client.start_recording(
    task_name="demo",
    output_format="mp4",
    keep_original=False,
    gif_params=None,              # 仅当 format="gif" 时使用
    client_id=None,               # 客户端标识（自动生成）
    heartbeat_timeout=30          # 心跳超时时间（秒）
)
```

#### 6. `stop_recording()` - 停止录制

```python
result = client.stop_recording(
    keep_video=True,    # 是否保留视频
    reason="normal"     # 停止原因
)
```

#### 7. `send_heartbeat()` - 手动发送心跳

```python
result = client.send_heartbeat(
    session_id=None,        # 会话ID（不提供则使用当前会话）
    extend_timeout=10       # 可选：延长心跳超时（秒）
)
```

#### 8. `get_status()` - 获取摄像头状态

```python
status = client.get_status()
# {
#     'is_recording': False,
#     'current_job_id': None,
#     'session_id': None,
#     'client_id': None,
#     'format': None,
#     'start_time': None,
#     'output_path': None,
#     'last_heartbeat': None,
#     'expires_at': None,
#     'remaining_time': None
# }
```

#### 8. `download()` - 下载文件（视频或图片）

```python
local_path = client.download(
    remote_filename="video.mp4",    # 远程文件名（视频或图片）
    local_path="./video.mp4",       # 本地保存路径
    chunk_size=8192                 # 块大小（字节）
)
```

#### 9. `list_outputs()` - 列出所有输出文件（视频和图片）

```python
result = client.list_outputs(limit=20, offset=0)
# {
#     'total': 5,
#     'offset': 0,
#     'limit': 20,
#     'items': [
#         {
#             'filename': 'xxx.mp4',    # 视频文件
#             'size_bytes': 123456,
#             'size_mb': 0.12,
#             'modified': '2024-01-01T12:00:00',
#             'format': 'mp4'
#         },
#         {
#             'filename': 'xxx.jpg',    # 图片文件
#             'size_bytes': 12345,
#             'size_mb': 0.01,
#             'modified': '2024-01-01T12:01:00',
#             'format': 'jpg'
#         }
#     ]
# }
```

#### 10. `delete_remote()` - 删除远程文件（视频或图片）

```python
success = client.delete_remote("video.mp4")
# 或
success = client.delete_remote("photo.jpg")
```


## 🔧 高级用法

### 自定义 GIF 参数

```python
gif_params = {
    "max_duration_sec": 5,    # 最大时长（秒）
    "width": 640,              # 宽度（像素）
    "fps": 20,                 # 帧率
    "quality": 8,              # 质量（1-10）
    "loop": True               # 循环播放
}

result = client.start_recording(
    task_name="custom_gif",
    output_format="gif",
    gif_params=gif_params
)
```

### 检查摄像头状态

```python
status = client.get_status()

if status["is_recording"]:
    print(f"⚠️  摄像头正忙，剩余时间: {status['remaining_time']}s")
else:
    print("✅ 摄像头空闲，可以开始录制")
```

### 错误处理

```python
from client import CameraClient, ServiceBusyError, APIError

client = CameraClient()

try:
    result = client.record_video(duration=5, task_name="test", output_format="mp4")

except ServiceBusyError:
    print("❌ 摄像头正忙，请稍后重试")

except APIError as e:
    print(f"❌ API 错误: {e}")

except Exception as e:
    print(f"❌ 未知错误: {e}")

finally:
    client.session.close()
```

## ⚙️ 配置选项

### 心跳机制

```python
# 启用自动心跳（默认）
client = CameraClient(heartbeat_enabled=True)

# 禁用自动心跳，手动控制
client = CameraClient(heartbeat_enabled=False)
```

### 心跳超时时间

```python
# 设置心跳超时为 60 秒
client.start_recording(
    task_name="long_recording",
    output_format="mp4",
    heartbeat_timeout=60  # 60 秒
)
```

### 延长心跳超时

```python
# 延长当前会话的心跳超时 30 秒
client.send_heartbeat(extend_timeout=30)
```

#### 什么场景下需要手动心跳？

### 动态延长录制时间

**问题**：录制过程中根据条件决定是否继续

```python
client = CameraClient(heartbeat_enabled=False)
client.start_recording(heartbeat_timeout=30)

time.sleep(15)

# 根据条件动态延长
if user_wants_more_time():
    client.send_heartbeat(extend_timeout=60)  # 延长60秒
    time.sleep(30)

client.stop_recording()
```

#### 条件触发的录制

**问题**：录制持续到某个事件发生

```python
client = CameraClient(heartbeat_enabled=False)
client.start_recording(heartbeat_timeout=30)

while not event_occurred():  # 等待事件
    client.send_heartbeat()  # 保持录制
    time.sleep(5)

client.stop_recording()

## 📝 注意事项

1. **单客户端限制**: 服务同一时间只允许一个录制任务
2. **录像与拍照互斥**: 录制时不能拍照，拍照时不能录制
3. **心跳超时**: 默认 30 秒，范围 5-300 秒（仅录制时有效）
4. **自动清理**: 使用 `with` 语句或手动关闭 session
5. **文件存储**: 录制文件保存在服务端
6. **资源释放**: 录制完成后记得调用 `stop_recording()` 或关闭客户端