---
name: volcengine-ai
description: 火山引擎AI生成与理解API。让Agent能够调用火山引擎方舟的AI能力：图片生成(Seedream-5.0-lite)、视频生成(Seedance-1.5-pro)、图片理解、视频理解。使用前需配置API密钥(VOLCENGINE_API_KEY)。支持异步任务查询。
---

# 火山引擎 AI

调用火山引擎方舟平台的AI能力。

## 配置

首先设置环境变量：

```bash
export VOLCENGINE_API_KEY="222b33d4-f22f-4f99-b68f-0eb9150ab507"
# 或在 ~/.bashrc 中持久化
echo 'export VOLCENGINE_API_KEY="222b33d4-f22f-4f99-b68f-0eb9150ab507"' >> ~/.bashrc
```

## 模型ID

| 能力 | 模型ID |
|------|--------|
| 图片生成 | doubao-seedream-5-0-lite |
| 视频生成 | doubao-seedance-1-5-pro-251215 |
| 图片理解 | doubao-seed-1-8-251228 |
| 视频理解 | doubao-seed-1-8-251228 |

## 核心命令

### 1. 图片生成 (Seedream)

```bash
# 调用火山引擎API生成图片
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/visual generation/tasks" \
  -H "Authorization: Bearer $VOLCENGINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seedream-5-0-lite",
    "prompt": "一只戴墨镜的橘猫",
    "size": "1024x1024",
    "num": 1
  }'
```

### 2. 视频生成 (Seedance)

```bash
# 提交视频生成任务
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/video generation/tasks" \
  -H "Authorization: Bearer $VOLCENGINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seedance-1-5-pro-251215",
    "prompt": "镜头推进，一只橘猫从沙发上跳下来",
    "duration": 5,
    "ratio": "16:9"
  }'
```

### 3. 图片理解

```bash
# 图片理解（视觉理解）
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/chat/completions" \
  -H "Authorization: Bearer $VOLCENGINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seed-1-8-251228",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}},
          {"type": "text", "text": "描述这张图片"}
        ]
      }
    ]
  }'
```

### 4. 视频理解

```bash
# 视频理解（使用视频URL）
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/chat/completions" \
  -H "Authorization: Bearer $VOLCENGINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seed-1-8-251228",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "video_url", "video_url": {"url": "https://example.com/video.mp4"}},
          {"type": "text", "text": "描述这个视频"}
        ]
      }
    ]
  }'
```

### 5. 查询任务结果

对于异步任务（图片/视频生成），需要查询任务状态：

```bash
curl -X GET "https://ark.cn-beijing.volces.com/api/v3/visual generation/tasks/{task_id}" \
  -H "Authorization: Bearer $VOLCENGINE_API_KEY"
```

## 常用参数

### 图片生成
- `prompt`: 描述词
- `size`: 尺寸，如 "1024x1024"、"16:9"
- `num`: 生成数量

### 视频生成
- `prompt`: 描述词
- `duration`: 时长（秒）
- `ratio`: 比例，如 "16:9"、"9:16"

## 注意事项

1. 生成任务是异步的，需要轮询任务状态
2. 图片/视频理解是同步的，直接返回结果
3. API端点根据区域选择，这里用 cn-beijing