# 语音转文字 · stt

> a7w 插件 `voice_tts` 的接口 `stt` · 平台官方文档

---

`POST /api/v1/apps/voice_tts/stt`

## 语音转文字

### 接口地址
`POST /api/v1/apps/voice_tts/stt`

### 功能说明
将音频文件中的语音内容识别并转写为文本。支持多种语言自动检测。

### 请求方式
- **方式一**（推荐）：JSON Body 传入 `audio_url` 音频链接
- **方式二**：multipart/form-data 上传 `audio` 文件字段

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| audio_url | string | 否 | 音频文件URL（与文件上传二选一） |
| language | string | 否 | 语言代码(zh/en/ja等)，不填自动检测 |
| ignore_timestamps | boolean | 否 | 是否忽略时间戳，默认true |

### 响应示例
```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "text": "识别出的文本内容",
    "duration": 12.5,
    "language": "zh"
  }
}
```

### 注意事项
- 支持 mp3/wav/ogg 格式
- 单个文件建议不超过 50MB
- 语音长度建议不超过 30 分钟

## 参数（平台 schema 原文）

```json
{
  "language": {
    "type": "string",
    "required": "",
    "description": "识别语言，不传则自动检测"
  },
  "audio_url": {
    "type": "string",
    "required": "",
    "description": "音频文件URL（与文件上传二选一）"
  },
  "ignore_timestamps": {
    "type": "boolean",
    "required": "",
    "description": "是否忽略精确时间戳，默认 true"
  }
}
```

## 计费

- 结算口径：按次固定价 30 点（租户价）
- 标准价：`fixed_price=30.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=30.00` / `tenant_points_per_1k_input=0.0000`
