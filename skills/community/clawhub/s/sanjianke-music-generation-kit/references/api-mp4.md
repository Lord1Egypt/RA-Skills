# 导出 MP4 · mp4

> a7w 插件 `music_generation` 的接口 `mp4` · 平台官方文档

---

`POST /api/v1/apps/music_generation/mp4`

# 音乐生成 · 导出 MP4

基于音频 ID 获取视频文件链接。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `mp4` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/music_generation/mp4` |
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
            "video_url": "https://example.com/music/video.mp4",
            "data": {
                "video_url": "https://example.com/music/video.mp4"
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

- 结算口径：按次固定价 20 点（租户价）
- 标准价：`fixed_price=20.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=20.00` / `tenant_points_per_1k_input=0.0000`
