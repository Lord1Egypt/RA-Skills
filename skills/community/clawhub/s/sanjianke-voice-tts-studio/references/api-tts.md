# 文字转语音 · tts

> a7w 插件 `voice_tts` 的接口 `tts` · 平台官方文档

---

`POST /api/v1/apps/voice_tts/tts`

## 文字转语音（同步）

### 接口地址
`POST /api/v1/apps/voice_tts/tts`

### 功能说明
将文本内容同步合成为语音音频文件。请求后直接返回结果，适合短文本（建议 500 字符内）。长文本请使用异步接口 `tts_async`。

### 调用模式
**同步接口** - 请求后直接返回合成结果（含音频URL），无需轮询。

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 待合成文本，建议不超过500字符 |
| reference_id | string | 否 | 音色模型ID（克隆音色返回的 model_id） |
| model | string | 否 | 合成引擎：speech-1.5 / speech-1.5-turbo |
| format | string | 否 | 输出格式：mp3(默认)/wav/ogg/opus/pcm |
| sample_rate | integer | 否 | 采样率：8000/16000/22050/44100(默认) |
| chunk_length | integer | 否 | 分块长度，默认200 |
| normalize | boolean | 否 | 文本规范化，默认true |
| mp3_bitrate | integer | 否 | MP3比特率，默认128 |
| temperature | number | 否 | 生成温度 0~1，默认0.7 |
| top_p | number | 否 | Top-P采样 0~1，默认0.8 |

### 响应示例
```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "audio_url": "https://your-domain.com/uploads/ai_app/202604/tts_xxxxxxxx.mp3",
    "format": "mp3"
  }
}
```

### 注意事项
- 同步接口适合短文本（500字符内），长文本请使用 `tts_async` 异步接口
- 未指定 reference_id 时使用系统默认音色
- 未指定 model 时使用平台配置的默认模型

## 参数（平台 schema 原文）

```json
{
  "text": {
    "type": "string",
    "required": "1",
    "description": "待合成文本，同步接口建议不超过 500 字符"
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
