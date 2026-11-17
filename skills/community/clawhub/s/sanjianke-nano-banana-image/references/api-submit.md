# 创建图片任务 · submit

> a7w 插件 `nano_banana` 的接口 `submit` · 平台官方文档

---

`POST /api/v1/apps/nano_banana/submit`

# nano-banana · 创建图片任务

提交图片生成或编辑任务。接口返回平台 `task_id`，客户端通过查询接口或统一任务查询接口获取结果。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `nano_banana` |
| API 编码 | `submit` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/nano_banana/submit` |
| 调用模式 | 异步 |
| 默认模型 | `nano-banana` |
| 默认分辨率 | `1K` |

## 鉴权

```http
POST /api/v1/apps/nano_banana/submit
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 请求参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 格式 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `prompt` | string | 是 | - | - | 图片内容、主体、风格、构图和细节描述 |
| `action` | string | 否 | `generate` | `generate` / `edit` | `generate` 为文生图，`edit` 为基于参考图编辑 |
| `model` | string | 否 | `nano-banana` | 见下方模型表 | 模型规格，影响价格和可用分辨率 |
| `image_urls` | array | `edit` 必填 | - | HTTP/HTTPS URL 数组 | 参考图片列表，文生图可不传 |
| `resolution` | string | 否 | `1K` | `1K` / `2K` / `4K` | 官方高清模型按该字段分档计费 |
| `aspect_ratio` | string | 否 | `auto` | `auto` / `1:1` / `16:9` / `9:16` / `4:3` / `3:4` / `3:2` / `2:3` / `5:4` / `4:5` / `21:9` | 图片宽高比 |
| `callback_url` | string | 否 | - | HTTPS URL | 任务完成或失败时由平台主动通知 |

## 模型和价格摘要

文档只展示汇总档位，避免一次展开过多 SKU。完整实时价格以当前租户配置和价格查询接口为准。

| 模型 | 分辨率 | 价格摘要 | 说明 |
| --- | --- | ---: | --- |
| `nano-banana` | `1K` | 24 点/次 | 普通模型，默认规格 |
| `nano-banana-2` | `1K` | 38 点/次 | 普通模型升级版 |
| `nano-banana-2-lite` | `1K` | 24 点/次 | 普通轻量规格 |
| `nano-banana-pro` | `1K` | 45 点/次 | 普通专业规格 |
| `nano-banana:official` | `1K` | 28.03 点/次 | 官方模型 |
| `nano-banana-2-lite:official` | `1K` | 28.03 点/次 | 官方轻量规格 |
| `nano-banana-2:official` | `1K` / `2K` / `4K` | 35.76 点/次起 | 官方高清，按分辨率计费 |
| `nano-banana-pro:official` | `1K` / `2K` / `4K` | 61.52 点/次起 | 官方高清专业规格，按分辨率计费 |

## 请求示例

### 文生图

```json
{
  "prompt": "A clean product photo of a yellow banana-shaped speaker on a white table.",
  "model": "nano-banana",
  "aspect_ratio": "1:1"
}
```

### 图生图编辑

```json
{
  "action": "edit",
  "prompt": "Change the background to a bright kitchen and keep the product shape unchanged.",
  "model": "nano-banana-2:official",
  "resolution": "2K",
  "image_urls": ["https://example.com/reference.png"]
}
```

### 官方高清

```json
{
  "prompt": "A cinematic poster of a futuristic banana cafe, detailed lighting, sharp focus.",
  "model": "nano-banana-pro:official",
  "resolution": "4K",
  "aspect_ratio": "16:9",
  "callback_url": "https://example.com/api/ai/callback"
}
```

## 成功响应

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "task_id": "task_xxxxxxxxxxxx",
    "status": "pending",
    "app": "nano_banana",
    "api": "submit",
    "frozen_points": 24
  }
}
```

返回后可用 `data.task_id` 调用 `/api/v1/apps/nano_banana/query` 或 `/api/v1/tasks/{task_id}` 查询任务。

## 失败响应

```json
{
  "code": 0,
  "msg": "当前请求未命中可用计费规格，请检查模型、分辨率是否在支持范围内。",
  "data": [],
  "show": 1
}
```

常见错误包括：`prompt` 为空、`action` 无效、`model` 不支持、普通模型传入非 `1K` 分辨率、点数不足、API Key 无权限。

## 价格查询

查询当前租户对该 API 的完整规格价格：

```http
GET /api/v1/pricing?type=app_api&app_code=nano_banana&api_code=submit
Authorization: Bearer <YOUR_API_KEY>
```

提交前查询某个参数组合命中的价格：

```http
POST /api/v1/pricing/batch
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

```json
{
  "items": [
    {
      "type": "app_api",
      "app_code": "nano_banana",
      "api_code": "submit",
      "params": {
        "model": "nano-banana-pro:official",
        "resolution": "4K"
      }
    }
  ]
}
```

实际扣点以任务创建时冻结的价格快照为准，后续价格调整不会改写历史任务。

## 参数（平台 schema 原文）

```json
{
  "model": {
    "type": "string",
    "default": "nano-banana",
    "example": "nano-banana",
    "options": "nano-banana / nano-banana-2 / nano-banana-2-lite / nano-banana-pro / nano-banana:official / nano-banana-2-lite:official / nano-banana-2:official / nano-banana-pro:official",
    "description": "模型规格。普通模型适合常规生成，官方模型适合更高一致性和高清档位。"
  },
  "action": {
    "type": "string",
    "default": "generate",
    "example": "generate",
    "options": "generate / edit",
    "description": "任务类型。generate 为文生图，edit 为基于参考图编辑。"
  },
  "prompt": {
    "type": "string",
    "example": "A clean product photo of a yellow banana-shaped speaker on a white table.",
    "description": "图片内容、风格、主体和细节描述。"
  },
  "image_urls": {
    "type": "array",
    "example": [
      "https://example.com/reference.png"
    ],
    "description": "参考图片 URL 列表。action=edit 时必填。"
  },
  "resolution": {
    "type": "string",
    "default": "1K",
    "example": "1K",
    "options": "1K / 2K / 4K",
    "description": "输出分辨率。官方高清模型按 1K、2K、4K 分档计费。"
  },
  "aspect_ratio": {
    "type": "string",
    "example": "1:1",
    "options": "auto / 1:1 / 16:9 / 9:16 / 4:3 / 3:4 / 3:2 / 2:3 / 5:4 / 4:5 / 21:9",
    "description": "图片宽高比。"
  },
  "callback_url": {
    "type": "string",
    "example": "https://example.com/api/ai/callback",
    "description": "任务完成或失败时由平台主动通知的 HTTPS 地址。"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
