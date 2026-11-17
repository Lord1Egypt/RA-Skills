# 优化音乐风格 · style

> a7w 插件 `music_generation` 的接口 `style` · 平台官方文档

---

`POST /api/v1/apps/music_generation/style`

# 音乐生成 · 优化音乐风格

根据提示词生成更完整的音乐风格描述。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `style` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/music_generation/style` |
| 调用模式 | 同步 |
| 计费方式 | 固定价 14 点/次 |

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 业务参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 示例 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `prompt` | string | 是 | - | - | `warm electronic pop with female vocal` | 需要优化的风格提示词。 |

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
                "upsampled_tags": "Ultra-soft electronic pop at 84 BPM, bright synth arpeggios, muted kick, airy pad chords."
            }
        },
        "usage": {
            "points_cost": 14,
            "actual_points": 14
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
  "prompt": {
    "type": "string",
    "example": "warm electronic pop with female vocal",
    "description": "需要优化的风格提示词。"
  }
}
```

## 计费

- 结算口径：按次固定价 14 点（租户价）
- 标准价：`fixed_price=14.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=14.00` / `tenant_points_per_1k_input=0.0000`
