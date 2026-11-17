# TingDong 后端 API 文档

## 服务器信息

- **Base URL**: `http://111.229.22.145:8092`
- **技术栈**: Flask + SQLite + 智谱 GLM-4 + Edge-TTS + Playwright
- **部署**: Gunicorn (单 worker + 4 线程) + Nginx 反向代理

## API 端点

### 1. 健康检查

```
GET /health
```

**响应**:
```json
{
  "status": "ok",
  "version": "2.0.0",
  "queue_size": 0
}
```

---

### 2. 提交播客生成任务

```
POST /api/podcast/submit
```

**请求体**:
```json
{
  "content": "文章链接或文本内容",
  "content_type": "url",
  "style": "conversational",
  "duration": "medium",
  "voice": "zh-CN-XiaoxiaoNeural"
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `content` | string | 是 | 文章 URL 或纯文本 |
| `content_type` | string | 否 | `url`(默认) / `text` |
| `style` | string | 否 | `conversational`(默认) / `summary` / `deep_dive` |
| `duration` | string | 否 | `short`(~5min) / `medium`(~10min, 默认) / `long`(~20min) |
| `voice` | string | 否 | Edge-TTS 语音标识，默认中文女声 |

**响应**:
```json
{
  "task_id": "td_20260820_abc123",
  "status": "pending",
  "estimated_time": 60
}
```

---

### 3. 查询任务状态

```
POST /api/podcast/status
```

**请求体**:
```json
{
  "task_id": "td_20260820_abc123"
}
```

**响应 - 处理中**:
```json
{
  "task_id": "td_20260820_abc123",
  "status": "processing",
  "progress": "正在生成播客脚本...",
  "percent": 45
}
```

**响应 - 完成**:
```json
{
  "task_id": "td_20260820_abc123",
  "status": "completed",
  "audio_url": "http://111.229.22.145:8092/audio/td_20260820_abc123.mp3",
  "title": "AI Agent 正在重构软件交互",
  "duration": 720,
  "source": "机器之心"
}
```

**响应 - 失败**:
```json
{
  "task_id": "td_20260820_abc123",
  "status": "failed",
  "error": "内容抓取失败：链接无法访问"
}
```

---

### 4. 语音列表（可选）

```
GET /api/voices
```

**响应**:
```json
{
  "voices": [
    {"id": "zh-CN-XiaoxiaoNeural", "name": "晓晓", "gender": "female", "locale": "zh-CN"},
    {"id": "zh-CN-YunxiNeural", "name": "云希", "gender": "male", "locale": "zh-CN"},
    {"id": "zh-CN-XiaoyiNeural", "name": "晓伊", "gender": "female", "locale": "zh-CN"}
  ]
}
```

---

## 错误码

| HTTP 状态 | 含义 |
|-----------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 任务不存在 |
| 429 | 队列已满，请稍后重试 |
| 500 | 服务端错误 |

## 注意事项

1. **队列机制**：后端使用 SQLite 持久化队列，支持并发但建议合理控制请求频率
2. **超时设置**：内容抓取 + AI 分析 + TTS 合成总耗时 30-120 秒，建议轮询间隔 5 秒
3. **音频保留**：生成的音频文件保留 7 天，之后自动清理
4. **微信文章**：Playwright 抓取需额外 10-20 秒启动时间
