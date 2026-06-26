# Doubao Seedance API 参考

基于火山引擎方舟平台的视频生成 API。

## API 端点

- **创建任务**: `POST /video/generations`
- **查询任务**: `GET /video/generations/{task_id}`
- **任务列表**: `GET /video/generations`
- **取消/删除**: `DELETE /video/generations/{task_id}`

## 请求参数

### 创建任务

```json
{
  "model": "doubao-seedance-1.5",
  "prompt": "视频描述",
  "first_frame": "图片URL或base64",
  "last_frame": "图片URL或base64",
  "reference_image": "参考图URL",
  "audio_enabled": false,
  "aspect_ratio": "16:9",
  "duration": 5
}
```

### 响应

```json
{
  "id": "task_xxx",
  "status": "pending",
  "created_at": 1234567890
}
```

### 任务状态

- `pending` - 等待中
- `processing` - 处理中
- `completed` - 已完成
- `failed` - 失败

### 完成响应

```json
{
  "id": "task_xxx",
  "status": "completed",
  "video_url": "https://xxx.mp4",
  "duration": 5,
  "aspect_ratio": "16:9"
}
```

## 鉴权

使用 Bearer Token：

```
Authorization: Bearer YOUR_API_KEY
```

## 限制

- 视频时长：1-10秒
- 支持比例：1:1, 16:9, 9:16, 4:3, 3:4
- 生成时间：约30秒-5分钟
