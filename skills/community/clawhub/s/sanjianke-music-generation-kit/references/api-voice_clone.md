# 声音克隆 · voice_clone

> a7w 插件 `music_generation` 的接口 `voice_clone` · 平台官方文档

---

`POST /api/v1/apps/music_generation/voice_clone`

# 音乐生成 · 声音克隆

基于清晰人声音频创建私有声音风格 ID。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `voice_clone` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/music_generation/voice_clone` |
| 调用模式 | 同步 |
| 计费方式 | 固定价 20 点/次 |

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 业务参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 示例 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `audio_url` | string | 是 | - | - | `https://example.com/voice.mp3` | 可公开访问的 MP3 或 WAV 人声音频 URL。音频至少 10 秒，建议单人清晰人声，尽量避免背景噪音或背景音乐。 |
| `name` | string | 否 | - | - | `My Voice` | 自定义声音风格名称。 |
| `description` | string | 否 | - | - | - | 自定义声音风格描述。 |

## 响应说明

同步返回处理结果。媒体类结果可能包含 `audio_url`、`video_url`、`file_url`、`image_url`、`audio_id`、`persona_id` 等字段，具体以接口实际结果为准。

### 成功示例

```json
{
    "code": 1,
    "msg": "success",
    "data": {
        "result": {
            "status": "completed",
            "voice_id": "voice_xxxxxxxxxxxx",
            "data": {
                "voice_id": "voice_xxxxxxxxxxxx",
                "name": "My Voice"
            }
        },
        "usage": {
            "points_cost": 20,
            "actual_points": 20
        }
    }
}
```

### 失败示例

```json
{
    "code": 0,
    "msg": "Audio duration must be between 10 and 240 seconds.",
    "data": null
}
```

## 参数（平台 schema 原文）

```json
{
  "name": {
    "type": "string",
    "example": "My Voice",
    "description": "自定义声音风格名称。"
  },
  "audio_url": {
    "type": "string",
    "example": "https://example.com/voice.mp3",
    "description": "可公开访问的 MP3 或 WAV 人声音频 URL。音频至少 10 秒，建议单人清晰人声，尽量避免背景噪音或背景音乐。"
  },
  "description": {
    "type": "string",
    "description": "自定义声音风格描述。"
  }
}
```

## 计费

- 结算口径：按次固定价 20 点（租户价）
- 标准价：`fixed_price=20.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=20.00` / `tenant_points_per_1k_input=0.0000`
