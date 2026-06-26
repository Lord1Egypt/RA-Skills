---
name: spark-image
version: 1.0.0
description: 提供图片生成能力：输入文本描述生成图片，可附加风格提示词。支持 1-4 张图片生成，按图片尺寸对应点数计费。Authorization 使用本系统发放的 Bearer Token。
triggers: 生成图片, 画一张图, text to image, 文生图, AI绘图, 油画风格, 水彩画, 动漫风, 国画, 科幻风, 唯美风格, 制作图片, 画图, 生成图片
metadata: {"openclaw":{"emoji":"🎨","homepage":"https://image.open-idea.net","primaryEnv":"IMAGE_GATEWAY_API_KEY","requires":{"env":["IMAGE_GATEWAY_API_KEY"]}}}
---

# Spark Image Skill 图片生成技能

文本生成图片服务，基于火山引擎图片生成 API。Base URL: **https://image.open-idea.net/api/v1**，`Authorization: Bearer <Key>`。

## Install

```
openclaw skills install spark-image
```

## Setup

- **`IMAGE_GATEWAY_API_KEY`**：[image.open-idea.net](https://image.open-idea.net) 登录后在「API Key」页创建，Bearer 调 `/api/v1`。[API-KEY.md](./references/API-KEY.md)

## Privacy

图片生成时，提示词文本将发送至第三方服务 **image.open-idea.net**（火山引擎 API）。请勿上传敏感或保密内容。

## Output

成功响应后对用户展示：业务正文（图片或生成结果）+ 计费行。

图片以 `<img src="data:image/png;base64,...">` 渲染给用户，或提供下载链接。若返回多张图，则逐张渲染。**勿**贴长 base64 原文。

计费行：
```
本次扣费: {charged} CNY, 余额: {balance} CNY
```

HTTP 头字段：`X-Mengguyu-Billing-Charged` · `X-Mengguyu-Billing-Balance` · `X-Mengguyu-Billing-Currency`

**禁止**对用户输出：完整 JSON、路由说明、模型名、token、Key 等内部信息。

## Usage

### 生成图片

```
POST /image
Body: { "prompt": "描述文字", "width": 2048, "height": 2048, "style": "油画风格，厚涂笔触", "image_count": 1 }
```

响应：`data.images[]`（1-4 张 base64 PNG）+ `data.points_used`

说明：
- 当前公开接口仅支持 2K 及以上推荐尺寸组合。
- `image_count` 支持 `1-4`。
- 多图请求会逐张生成并聚合返回，通常比单图耗时更长。

### 可用尺寸与点数

| 尺寸 | 点数 |
|------|------|
| 2048x2048 | 56 |
| 2304x1728 | 54 |
| 1728x2304 | 54 |
| 2848x1600 | 61 |
| 1600x2848 | 61 |
| 2496x1664 | 56 |
| 1664x2496 | 56 |
| 3136x1344 | 57 |

详见 [IMAGE-GENERATION.md](./references/IMAGE-GENERATION.md) 和 [HTTP-REQUESTS.md](./references/HTTP-REQUESTS.md)。

## references/

| 文件 | 用途 |
|------|------|
| [HTTP-REQUESTS.md](./references/HTTP-REQUESTS.md) | 全接口 curl、计费头 |
| [IMAGE-GENERATION.md](./references/IMAGE-GENERATION.md) | 图片生成详细说明 |
| [BEHAVIOR-RULES.md](./references/BEHAVIOR-RULES.md) | 行为规范、重试、确认 |
| [API-KEY.md](./references/API-KEY.md) | Key 配置 |
