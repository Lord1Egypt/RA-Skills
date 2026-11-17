# 创建视频任务 · create

> a7w 插件 `wan` 的接口 `create` · 平台官方文档

---

`POST /api/v1/apps/wan/create`

# Wan 视频生成 · 创建任务

提交 Wan 模型族视频任务。用户只对接平台统一接口；平台会按 `model` 选择对应能力，并负责参数过滤、任务入库、扣点冻结和轮询转存。

<details>
<summary>基本信息</summary>

| 字段 | 内容 |
| --- | --- |
| 类型 | 应用 API |
| 应用编码 | `wan` |
| API 编码 | `create` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/wan/create` |
| 调用模式 | 异步 |
| 计费方式 | 按生成时长计费，单价来自租户价格矩阵 |

</details>

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 请求路径

```http
POST /api/v1/apps/wan/create
```

提交成功后返回平台 `task_id`。请使用 `GET /api/v1/apps/wan/query?task_id={task_id}` 查询结果，或在请求中传 `callback_url` 接收任务完成/失败回调。

## 模型能力

| model | 场景 | 必填参数 | 说明 |
| --- | --- | --- | --- |
| `wan2.7` | 文生视频 | `model`, `prompt` | 不需要素材输入 |
| `wan2.7-r2v` | 角色/参考图生视频 | `model`, `prompt`, `image_with_roles` | 传参考图和图片角色 |
| `wan2.7-videoedit` | 视频编辑 | `model`, `prompt`, `video_urls` | 传待编辑视频 URL，按含视频输入档计费 |

## 业务参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 示例 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `model` | string | 是 | `wan2.7` | `wan2.7` / `wan2.7-r2v` / `wan2.7-videoedit` | `wan2.7` | Wan 模型版本，也是能力选择开关 |
| `prompt` | string | 是 | - | - | `一辆复古跑车沿着海岸公路行驶，电影感光影` | 视频画面、动作、镜头、风格描述 |
| `resolution` | string | 否 | `720p` | `720p` / `1080p` | `720p` | 输出分辨率，同时参与价格矩阵匹配 |
| `duration` | integer | 否 | `5` | `wan2.7`/`wan2.7-r2v`: `2-15`；`wan2.7-videoedit`: `2-10` | `5` | 生成视频时长，单位秒；平台按该值乘以单价扣点 |
| `size` | string | 否 | - | `16:9` / `9:16` / `1:1` / `4:3` / `3:4` | `16:9` | 视频画幅比例 |
| `image_with_roles` | array | `wan2.7-r2v` 必填 | - | 最多 2 张；`role`: `reference_image` / `first_frame` / `last_frame` | `[{"url":"https://example.com/role.png","role":"reference_image"}]` | 参考图列表；每项至少传 `url` |
| `image_urls` | array | 否 | - | `wan2.7` 最多 2 张；`wan2.7-videoedit` 最多 4 张 | `["https://example.com/reference.png"]` | 参考图片 URL 列表 |
| `video_urls` | array | `wan2.7-videoedit` 必填 | - | 最多 1 段 | `["https://example.com/input.mp4"]` | 待编辑视频 URL 列表；传入后按 `with_video` 档位计费 |
| `audio_url` | string | 否 | - | HTTP/HTTPS URL | `https://example.com/audio.mp3` | 参考音频 URL |
| `negative_prompt` | string | 否 | - | - | `低清晰度、畸形、闪烁` | 不希望出现在画面中的内容 |
| `prompt_extend` | boolean | 否 | - | `true` / `false` | `false` | 是否启用提示词扩展 |
| `seed` | integer | 否 | - | `0-2147483647` | `42` | 随机种子，用于尽量复现结果 |
| `watermark` | boolean | 否 | - | `true` / `false` | `false` | 是否添加水印 |
| `callback_url` | string | 否 | - | HTTPS URL | `https://your-domain.com/webhook/wan` | 任务完成或失败时的平台回调地址 |
| `metadata` | object | 否 | - | `audio_setting`: `auto` / `origin` | `{"biz_id":"order_1001","audio_setting":"auto"}` | 业务透传字段；视频编辑可指定音频处理方式 |

## 请求示例

### 文生视频

```json
{
  "model": "wan2.7",
  "prompt": "一辆复古跑车沿着海岸公路行驶，电影感光影，镜头缓慢推进",
  "resolution": "720p",
  "duration": 5,
  "seed": 42
}
```

### 角色/参考图生视频

```json
{
  "model": "wan2.7-r2v",
  "prompt": "让参考图中的人物在城市街头自然行走，保持人物身份一致",
  "resolution": "1080p",
  "duration": 5,
  "image_with_roles": [
    {
      "url": "https://example.com/role.png",
      "role": "reference_image"
    }
  ]
}
```

### 视频编辑

```json
{
  "model": "wan2.7-videoedit",
  "prompt": "将视频改成赛博朋克夜景风格，增强霓虹灯和雨夜反光",
  "resolution": "720p",
  "duration": 5,
  "video_urls": [
    "https://example.com/input.mp4"
  ]
}
```

## 成功响应

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "task_id": "task_xxxxxxxxxxxx",
    "status": "queued",
    "app": "wan",
    "api": "create"
  }
}
```

## 计费说明

计费公式：`duration × 当前租户价格矩阵单价`。

价格矩阵按 `model + resolution + 输入类型` 匹配。`wan2.7-videoedit` 因传入 `video_urls`，会使用 `with_video` 档位；其它未传视频输入的场景使用 `without_video` 档位。平台会在提交任务时冻结点数，任务完成后按实际计费结果结算。

## 失败响应

```json
{
  "error": {
    "message": "点数余额不足",
    "type": "insufficient_points",
    "code": "insufficient_points"
  }
}
```

### 常见错误码

| HTTP | code | 含义 |
| --- | --- | --- |
| 400 | `missing_model` / `missing_prompt` | 必填参数缺失 |
| 400 | `unsupported_model` | `model` 不在当前 Wan 版本规格中 |
| 400 | `missing_image_with_roles` | `wan2.7-r2v` 未传参考图 |
| 400 | `missing_video_urls` | `wan2.7-videoedit` 未传视频素材 |
| 401 | `auth_failed` | API Key 缺失或无效 |
| 402 | `insufficient_points` | 点数余额不足 |
| 403 | `permission_denied` | 当前 API Key 无权调用该应用 |
| 429 | `queue_limit_exceeded` | 排队任务已达上限 |
| 5xx | `server_error` / `task_error` | 平台服务异常或任务处理失败 |

## 参数（平台 schema 原文）

```json
{
  "seed": {
    "type": "integer",
    "options": "0-2147483647",
    "description": "随机种子，用于结果复现。范围：0-2147483647。"
  },
  "size": {
    "type": "string",
    "example": "16:9",
    "options": "16:9 / 9:16 / 1:1 / 4:3 / 3:4",
    "description": "视频画幅比例。"
  },
  "model": {
    "type": "string",
    "example": "wan2.7",
    "options": "wan2.7 / wan2.7-r2v / wan2.7-videoedit",
    "description": "Wan 模型版本。不同版本支持的素材输入略有差异。"
  },
  "prompt": {
    "type": "string",
    "example": "一辆复古跑车沿着海岸公路行驶，电影感光影",
    "description": "视频画面与运动描述。"
  },
  "duration": {
    "type": "integer",
    "default": "5",
    "example": "5",
    "options": "wan2.7 / wan2.7-r2v: 2-15；wan2.7-videoedit: 2-10",
    "description": "生成视频时长，单位秒。wan2.7、wan2.7-r2v 支持 2-15；wan2.7-videoedit 支持 2-10。"
  },
  "metadata": {
    "type": "object",
    "example": {
      "biz_id": "order_1001",
      "audio_setting": "auto"
    },
    "children": {
      "biz_id": {
        "type": "string",
        "description": "业务侧自定义 ID"
      },
      "audio_setting": {
        "type": "string",
        "options": "auto / origin",
        "description": "音频处理方式，主要用于视频编辑场景。"
      }
    },
    "description": "附加业务信息。wan2.7-videoedit 可在 metadata.audio_setting 中选择音频处理方式。"
  },
  "audio_url": {
    "type": "string",
    "example": "https://example.com/audio.mp3",
    "description": "参考音频 URL。需要音频驱动生成时传入。"
  },
  "watermark": {
    "type": "boolean",
    "example": "",
    "options": "true / false",
    "description": "是否添加水印。"
  },
  "image_urls": {
    "type": "array",
    "example": [
      "https://example.com/reference.png"
    ],
    "description": "参考图片 URL 列表。wan2.7 最多 2 张；wan2.7-videoedit 最多 4 张。"
  },
  "resolution": {
    "type": "string",
    "default": "720p",
    "example": "720p",
    "options": "720p / 1080p",
    "description": "输出分辨率。"
  },
  "video_urls": {
    "type": "array",
    "example": [
      "https://example.com/input.mp4"
    ],
    "description": "视频素材地址列表，最多 1 段。wan2.7-videoedit 必填，并按含视频输入档计费。"
  },
  "callback_url": {
    "type": "string",
    "example": "https://your-domain.com/webhook/wan",
    "description": "任务完成或失败时由平台主动通知的 HTTPS 地址。"
  },
  "prompt_extend": {
    "type": "boolean",
    "example": "",
    "options": "true / false",
    "description": "是否启用提示词扩展。"
  },
  "negative_prompt": {
    "type": "string",
    "description": "不希望出现在画面中的内容。"
  },
  "image_with_roles": {
    "type": "array",
    "example": [
      {
        "url": "https://example.com/role.png",
        "role": "reference_image"
      }
    ],
    "children": {
      "url": {
        "type": "string",
        "required": "1",
        "description": "图片地址，支持 http/https"
      },
      "role": {
        "type": "string",
        "options": "reference_image / first_frame / last_frame",
        "description": "图片角色。wan2.7-r2v 可用 reference_image / first_frame；首尾帧场景可用 first_frame / last_frame。"
      }
    },
    "description": "角色或参考图列表。wan2.7-r2v 必填，最多 2 张。"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
- 分档：`models`={'720p': {'with_video': 47.81, 'without_video': 47.81}, '1080p': {'with_video': 78.91, 'without_video': 78.91}}
