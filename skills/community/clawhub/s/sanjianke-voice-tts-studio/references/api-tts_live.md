# 文字转语音（Live·异步） · tts_live

> a7w 插件 `voice_tts` 的接口 `tts_live` · 平台官方文档

---

`POST /api/v1/apps/voice_tts/tts_live`

## 文字转语音（WebSocket Live · 异步）

### 接口地址
`POST /api/v1/apps/voice_tts/tts_live`

### 功能说明
使用 Fish Audio **WebSocket `wss://…/v1/tts/live`** 流式合成，适合长文本；**提交后立即返回 `task_id`**，实际合成在后台 **独立 Worker** 中执行，避免 HTTP 网关超时。

### 轮询
`GET /api/v1/tasks/{task_id}` 直至 `status` 为 `completed`，结果中 `result.audio_url` 为音频地址。

### 回调
可选 `callback_url`，与 `tts_async` 行为一致。

### Worker 部署
服务器需执行：
`php think fish_tts:worker`（常驻）或 `php think fish_tts:worker --once`（crontab 每分钟）。

### 依赖
Composer 已包含 `rybakit/msgpack`、`textalk/websocket`；服务端需能访问 `wss://api.fish.audio`。

## 参数（平台 schema 原文）

```json
{
  "text": {
    "type": "string",
    "required": "1",
    "description": "待合成文本（WebSocket 流式上游，适合长文本）"
  },
  "model": {
    "type": "string",
    "required": "",
    "description": "TTS 模型：s1 / s2-pro，默认 s2-pro"
  },
  "top_p": {
    "type": "number",
    "required": "",
    "description": "Top-P"
  },
  "format": {
    "type": "string",
    "required": "",
    "description": "wav / pcm / mp3 / opus，默认 mp3"
  },
  "latency": {
    "type": "string",
    "required": "",
    "description": "low / normal / balanced"
  },
  "prosody": {
    "type": "object",
    "required": "",
    "description": "语调：speed、volume、normalize_loudness（仅 s2-pro）"
  },
  "normalize": {
    "type": "boolean",
    "required": "",
    "description": "文本规范化，默认 true"
  },
  "mp3_bitrate": {
    "type": "integer",
    "required": "",
    "description": "MP3 比特率：64 / 128 / 192"
  },
  "sample_rate": {
    "type": "integer",
    "required": "",
    "description": "采样率"
  },
  "temperature": {
    "type": "number",
    "required": "",
    "description": "生成温度"
  },
  "callback_url": {
    "type": "string",
    "required": "",
    "description": "回调 URL；不传则 GET /api/v1/tasks/{task_id} 轮询"
  },
  "chunk_length": {
    "type": "integer",
    "required": "",
    "description": "文本分块长度 100~300，默认 300"
  },
  "opus_bitrate": {
    "type": "integer",
    "required": "",
    "description": "Opus 比特率"
  },
  "reference_id": {
    "type": "string",
    "required": "",
    "description": "音色模型ID。单说话人传 string；多说话人可传 string[]（仅 s2-pro）"
  },
  "max_new_tokens": {
    "type": "integer",
    "required": "",
    "description": "每分块最大音频 token"
  },
  "min_chunk_length": {
    "type": "integer",
    "required": "",
    "description": "最小分块长度 0~100"
  },
  "repetition_penalty": {
    "type": "number",
    "required": "",
    "description": "重复惩罚"
  },
  "early_stop_threshold": {
    "type": "number",
    "required": "",
    "description": "提前停止阈值，0~1"
  },
  "condition_on_previous_chunks": {
    "type": "boolean",
    "required": "",
    "description": "是否利用前一段音频作为上下文"
  }
}
```

## 计费

- 结算口径：输入 50 点/1k tokens（租户价）
- 标准价：`fixed_price=0.0000` / `input_price=50.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=50.0000`
