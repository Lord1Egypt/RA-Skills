# 文字转语音（异步） · tts_async

> a7w 插件 `voice_tts` 的接口 `tts_async` · 平台官方文档

---

`POST /api/v1/apps/voice_tts/tts_async`

## 文字转语音（异步）

### 接口地址
`POST /api/v1/apps/voice_tts/tts_async`

### 功能说明
将文本内容异步合成为语音音频文件。适合长文本，提交后立即返回 `task_id`，通过回调或轮询获取结果。

### 调用模式
**异步接口** - 提交后返回 task_id。
- 传 `callback_url`：任务完成后自动回调
- 不传 `callback_url`：通过 `GET /api/v1/tasks/{task_id}` 轮询

### 提交响应示例
```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "task_id": "tsk_xxxxxxxxxxxx",
    "status": "pending",
    "app": "voice_tts",
    "api": "tts_async"
  }
}
```

## 参数（平台 schema 原文）

```json
{
  "text": {
    "type": "string",
    "required": "1",
    "description": "待合成文本，适合长文本（最大约 10000 字符）"
  },
  "model": {
    "type": "string",
    "required": "",
    "description": "TTS 模型，可选 s1 / s2-pro，默认 s2-pro"
  },
  "top_p": {
    "type": "number",
    "required": "",
    "description": "Top-P 采样，0~1，默认 0.7"
  },
  "format": {
    "type": "string",
    "required": "",
    "description": "输出格式：wav / pcm / mp3 / opus，默认 mp3"
  },
  "latency": {
    "type": "string",
    "required": "",
    "description": "延迟模式：low / normal / balanced"
  },
  "prosody": {
    "type": "object",
    "required": "",
    "description": "语调控制对象：speed、volume、normalize_loudness"
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
    "description": "采样率按格式限制"
  },
  "temperature": {
    "type": "number",
    "required": "",
    "description": "生成温度，0~1，默认 0.7"
  },
  "callback_url": {
    "type": "string",
    "required": "",
    "description": "回调通知URL；不传则通过任务接口轮询"
  },
  "chunk_length": {
    "type": "integer",
    "required": "",
    "description": "文本分块长度，范围 100~300，默认 300"
  },
  "opus_bitrate": {
    "type": "integer",
    "required": "",
    "description": "Opus 比特率：-1000 / 24 / 32 / 48 / 64"
  },
  "reference_id": {
    "type": "string",
    "required": "",
    "description": "音色模型ID。单说话人传 string；多说话人模式可传 string[]（仅 s2-pro）"
  },
  "max_new_tokens": {
    "type": "integer",
    "required": "",
    "description": "每个分块最多生成音频 token，默认 1024"
  },
  "min_chunk_length": {
    "type": "integer",
    "required": "",
    "description": "最小分块长度，范围 0~100，默认 50"
  },
  "repetition_penalty": {
    "type": "number",
    "required": "",
    "description": "重复惩罚，默认 1.2"
  },
  "early_stop_threshold": {
    "type": "number",
    "required": "",
    "description": "提前停止阈值，范围 0~1，默认 1"
  },
  "condition_on_previous_chunks": {
    "type": "boolean",
    "required": "",
    "description": "是否利用前一段音频作为上下文，默认 true"
  }
}
```

## 计费

- 结算口径：输入 50 点/1k tokens（租户价）
- 标准价：`fixed_price=0.0200` / `input_price=50.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=50.0000`
