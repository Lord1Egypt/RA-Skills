# 创建视频任务 · submit

> a7w 插件 `grok_video` 的接口 `submit` · 平台官方文档

---

`POST /api/v1/apps/grok_video/submit`

# Grok 视频生成 - 创建任务

`POST /api/v1/apps/grok_video/submit`

创建接口始终异步返回。提交成功后立即获得平台 `task_id`。

## 请求头

| 名称 | 值 |
| --- | --- |
| `Authorization` | `Bearer YOUR_API_KEY` |
| `Content-Type` | `application/json` |

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | `grok-imagine-video-1.5-fast` 或 `grok-imagine-video-1.5` |
| `prompt` | string | 条件必填 | 快速生成未传 `image_urls` 时必填 |
| `duration` | integer | 否 | 默认 8。快速生成范围 1-30；标准生成范围 1-15 |
| `image_urls` | array | 条件必填 | 输入图片地址列表。第一张作为主图，其余图片作为参考图；标准生成至少需要一张 |
| `resolution` | string | 否 | 默认 `480p`。可选 `480p`、`720p`、`1080p` |
| `aspect_ratio` | string | 否 | 可选 `1:1`、`16:9`、`9:16`、`4:3`、`3:4`、`3:2`、`2:3` |
| `callback_url` | string | 否 | 接收任务终态通知的地址 |

## 规则说明

- `grok-imagine-video-1.5-fast`：至少提供 `prompt` 或 `image_urls` 其中一项；不传图片时可直接文生视频。
- `grok-imagine-video-1.5`：仅支持标准生成视频，必须提供至少一张 `image_urls` 图片。
- `image_urls` 的第一张图片作为主图，后续图片自动作为参考图处理。
- 快速生成按次计费；标准生成按输出秒计费。不同分辨率对应不同价格。

## 请求示例

```json
{
  "model": "grok-imagine-video-1.5-fast",
  "prompt": "A cinematic city street at sunset, smooth camera movement.",
  "duration": 8,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "callback_url": "https://example.com/api/video-callback"
}
```

## 多图参考示例

```json
{
  "model": "grok-imagine-video-1.5",
  "image_urls": [
    "https://example.com/main.jpg",
    "https://example.com/style.jpg",
    "https://example.com/character.jpg"
  ],
  "duration": 8,
  "resolution": "720p",
  "aspect_ratio": "16:9"
}
```

## 成功响应示例

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "task_id": "task_xxxxxxxxxxxx",
    "status": "pending"
  }
}
```

## 回调说明

传入 `callback_url` 后，平台会在任务成功或失败时向该地址发送 JSON POST 请求。回调中包含平台 `task_id`、终态 `status`；成功结果的 `result` 中包含 `video_url`。回调接收方应返回 2xx 状态码。

## 参数（平台 schema 原文）

```json
{
  "model": {
    "type": "string",
    "default": "grok-imagine-video-1.5-fast",
    "options": "grok-imagine-video-1.5-fast / grok-imagine-video-1.5",
    "description": "视频模型规格。"
  },
  "prompt": {
    "type": "string",
    "description": "视频内容描述。快速生成在未提供 image_urls 时必填。"
  },
  "duration": {
    "type": "integer",
    "default": "8",
    "options": "1-30",
    "description": "视频时长（秒）。快速生成支持 1-30，标准生成支持 1-15。"
  },
  "image_urls": {
    "type": "array",
    "example": [
      "https://example.com/main.jpg",
      "https://example.com/style.jpg"
    ],
    "description": "输入图片地址列表。第一张作为主图，其余图片作为参考图；标准生成模型至少需要一张。"
  },
  "resolution": {
    "type": "string",
    "default": "480p",
    "options": "480p / 720p / 1080p",
    "description": "输出分辨率，影响价格。"
  },
  "aspect_ratio": {
    "type": "string",
    "options": "1:1 / 16:9 / 9:16 / 4:3 / 3:4 / 3:2 / 2:3",
    "description": "视频宽高比。"
  },
  "callback_url": {
    "type": "string",
    "description": "任务完成或失败时由平台主动通知的 HTTPS 地址。"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
