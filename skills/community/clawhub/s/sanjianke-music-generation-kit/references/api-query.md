# 查询音乐任务 · query

> a7w 插件 `music_generation` 的接口 `query` · 平台官方文档

---

`POST /api/v1/apps/music_generation/query`

# 音乐生成 · 查询音乐任务

按平台任务 ID 查询任务状态与结果。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `query` |
| 请求方式 | `GET` |
| 请求路径 | `/api/v1/apps/music_generation/query` |
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
| `task_id` | string | 是 | - | - | `task_xxxxxxxxxxxx` | 创建任务后返回的平台任务 ID。 |

## 响应说明

同步返回处理结果。媒体类结果可能包含 `audio_url`、`video_url`、`file_url`、`image_url`、`audio_id`、`persona_id` 等字段，具体以接口实际结果为准。

### 处理中示例

```json
{
    "code": 1,
    "msg": "success",
    "data": {
        "result": {
            "status": "processing"
        },
        "usage": {
            "points_cost": 0,
            "actual_points": 0
        }
    }
}
```

### 完成示例

```json
{
    "code": 1,
    "msg": "success",
    "data": {
        "result": {
            "task_id": "task_xxxxxxxxxxxx",
            "status": "completed",
            "audio_url": "https://example.com/music/audio.mp3",
            "file_url": "https://example.com/music/audio.wav",
            "data": [
                {
                    "id": "audio_xxxxxxxxxxxx",
                    "title": "Morning API",
                    "audio_url": "https://example.com/music/audio.mp3"
                }
            ]
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
  "task_id": {
    "type": "string",
    "example": "task_xxxxxxxxxxxx",
    "description": "创建任务后返回的平台任务 ID。"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
