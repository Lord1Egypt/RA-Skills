# 听懂了 API 文档 (v1)

## 基础信息

- **Base URL**: `http://111.229.22.145:8092/api/v1`
- **协议**: HTTP（后续支持 HTTPS）
- **编码**: UTF-8
- **Content-Type**: `application/json`

## 端点列表

### 1. 健康检查

```
GET /health
```

**响应**：
```json
{
  "service": "tingdongle-api",
  "version": "v1",
  "status": "ok",
  "timestamp": "2026-08-20T10:33:21.885807"
}
```

### 2. 提交播客生成任务

```
POST /podcast/submit
```

**请求体**：
```json
{
  "content": "https://mp.weixin.qq.com/s/xxxxx",
  "content_type": "url",
  "style": "conversational",
  "duration": "medium",
  "user_id": "user_001"
}
```

**参数说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 是 | 文章链接或文本内容 |
| content_type | string | 否 | `url` 或 `text`（默认 url） |
| style | string | 否 | `conversational`/`summary`/`deep_dive` |
| duration | string | 否 | `short`/`medium`/`long`（暂无效） |
| user_id | string | 否 | 用户标识 |

**响应**：
```json
{
  "task_id": "td_20260820_103528_d9ea7fd1",
  "status": "pending",
  "message": "任务已提交",
  "estimated_time": 60,
  "check_url": "/api/v1/podcast/td_20260820_103528_d9ea7fd1"
}
```

### 3. 查询任务状态

```
GET /podcast/{task_id}
```

**响应（处理中）**：
```json
{
  "task_id": "td_20260820_103528_d9ea7fd1",
  "status": "analyzing",
  "progress": "AI分析中...",
  "title": "文章标题",
  "source": "公众号名称",
  "content_length": 2406,
  "created_at": "2026-08-20T10:35:28.348046"
}
```

**响应（已完成）**：
```json
{
  "task_id": "td_20260820_103528_d9ea7fd1",
  "status": "completed",
  "progress": "完成",
  "title": "文章标题",
  "source": "公众号名称",
  "content_length": 2406,
  "analysis_length": 1195,
  "audio_url": "http://111.229.22.145:8092/tingdongle/audio/13178f73201e.mp3",
  "completed_at": "2026-08-20T10:36:16.535727"
}
```

**响应（失败）**：
```json
{
  "task_id": "td_20260820_103330_d69627a3",
  "status": "failed",
  "error": "shutil is not defined",
  "created_at": "2026-08-20T10:33:30.930067"
}
```

### 4. 查询额度

```
GET /quota?user_id=xxx
```

**响应**：
```json
{
  "free_quota": 10,
  "used": 0,
  "remaining": 10,
  "reset_at": "每月1日"
}
```

## 状态码说明

| 状态 | 含义 |
|------|------|
| pending | 已提交，等待处理 |
| fetching | 正在抓取文章内容 |
| analyzing | AI 分析中 |
| synthesizing | 语音合成中 |
| completed | 完成 |
| failed | 失败 |

## 音频访问

音频文件通过以下 URL 访问：

```
GET http://111.229.22.145:8092/tingdongle/audio/{article_id}.mp3
```

示例：
```
http://111.229.22.145:8092/tingdongle/audio/13178f73201e.mp3
```

## 错误码

| HTTP 状态 | 错误信息 | 说明 |
|-----------|---------|------|
| 400 | content 不能为空 | 请求参数错误 |
| 400 | content_type 必须是 url 或 text | 类型不支持 |
| 400 | 文本输入暂不支持 | 功能未开放 |
| 404 | 任务不存在 | task_id 错误 |
| 500 | 服务器内部错误 | 后端异常 |
