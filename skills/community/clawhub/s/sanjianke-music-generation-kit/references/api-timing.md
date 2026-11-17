# 歌词时间轴 · timing

> a7w 插件 `music_generation` 的接口 `timing` · 平台官方文档

---

`POST /api/v1/apps/music_generation/timing`

# 音乐生成 · 歌词时间轴

基于音频 ID 获取歌词与音频时间轴信息。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `timing` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/music_generation/timing` |
| 调用模式 | 同步 |
| 计费方式 | 免费 |

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 业务参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 示例 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `audio_id` | string | 是 | - | - | `audio_xxxxxxxxxxxx` | 音频 ID，用于定位已生成或已上传的音频片段。 |
| `callback_url` | string | 否 | - | - | - | 任务完成或失败时由平台主动通知的 HTTPS 地址；同步接口可不传。 |

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
            "data": {
                "aligned_words": [
                    {
                        "word": "Morning",
                        "start_s": 18.431,
                        "end_s": 18.989,
                        "success": true
                    }
                ],
                "segments": [
                    {
                        "text": "Morning on the street",
                        "start_s": 18.431,
                        "end_s": 21.383
                    }
                ],
                "waveform_data": [
                    0.05253,
                    0.09595,
                    0.08009
                ]
            }
        },
        "usage": {
            "points_cost": 0,
            "actual_points": 0
        }
    }
}
```

### 失败示例

```json
{
    "code": 0,
    "msg": "任务处理失败，请稍后重试",
    "data": null
}
```

## 参数（平台 schema 原文）

```json
{
  "audio_id": {
    "type": "string",
    "example": "audio_xxxxxxxxxxxx",
    "description": "音频 ID，用于定位已生成或已上传的音频片段。"
  },
  "callback_url": {
    "type": "string",
    "description": "任务完成或失败时由平台主动通知的 HTTPS 地址；同步接口可不传。"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
