---
name: workrally-image
slug: workrally-image
displayName: WorkRally 图片生成（SkillPay）
display_name: WorkRally 图片生成（SkillPay）
display_name_en: WorkRally Image Generation (SkillPay)
description: 生成静态图片的付费创作 Skill。当用户要文生图、图生图（基于参考图改图/换风格/续作），或做海报、插画、壁纸、头像、配图、logo 等时命中。例：「画一张橘猫」「做张产品海报」「参考这张图改动漫风」「出张壁纸」。
description_zh: 付费图片生成 Skill，支持文生图与图生图，适用于海报、插画、壁纸、头像、配图、logo 等创作场景。
description_en: Paid image generation skill for text-to-image and image-to-image, covering posters, illustrations, wallpapers, avatars, and logos.
tags: [图片生成, 文生图, 图生图, 画图, 改图, 海报, 插画, 壁纸, 头像, 配图, AIGC]
version: 1.1.1
license: MIT-0
author: WorkRally Team
homepage: https://workrally.qq.com
user-invocable: true
capability: image_generation
pricing:
  model: per_call
  amount_fen: 36
---

# WorkRally 图片生成

根据用户的文字描述，或用户提供的参考图加文字描述，调用 WorkRally 平台生成**图片**。每次生成需用户完成一次支付授权，扣款后返回生成结果。

## 触发规则（精准命中）

**命中本 Skill 的创作意图**：

- **生成图片**（`product_id: image-generation`）：用户想要一张/几张图片，或想基于参考图继续生成/改图。
  例：「画一只……」「生成一张……」「做一张海报 / 插画 / 壁纸 / 头像 / 配图 / logo」「参考这张图生成……」「把这张图改成……风格」

**不触发**的情况：

- 纯文字问答、查询、文案/文字修改、对已有内容的纯文字点评等与"生成新的图片"无关的请求
- **视频 / 动画 / 短片 / 动态画面**等创作意图 —— 应使用 `workrally-video` Skill

## 付费前置检查

调用本 Skill 前，必须检查当前 Agent 是否已安装支付能力（`weixinpay` extension）：

- ✅ **已安装**：可继续提供付费创作服务
- ❌ **未安装**：向用户提示「当前 Agent 暂不支持付费创作能力」，终止流程

## 服务与定价

| 产品ID | 服务内容 | 单价 |
|--------|----------|------|
| `image-generation` | WorkRally图片生成 | 0.36 元/次 |

> 价格以 SkillHub 后台配置为准。命中创作意图后，向用户展示服务名称和价格，由用户确认后进入付费流程。
>
> **生成规格由云端设定**：图片为 1K 规格，每次生成 1 张，调用方无需指定 `model` / `resolution`。

## 使用并获取付费服务

用户确认使用后，按以下步骤完成付费内容获取：

### 步骤 1：发起付费请求

调用云端服务 API：

```http
POST https://workrally.qq.com/zenstudio/api/agent-pay/invoke
Content-Type: application/json

{
  "product_id": "image-generation",
  "prompt": "<用户描述的画面内容>",
  "input_images": ["<可选：data:image/jpeg;base64,在此填入Base64>"]
}
```

> `prompt` 是必填项，**≤500 字**（超长会被 `INVALID_FIELD` 拒绝、不扣费）。**不要直接透传用户原话**；调用前先按下方「提示词优化」将需求编译成自然语言制作指令，再传优化后的提示词。
> `input_images` 是可选项。用户提供本地参考图并要求图生图/改图时，以 `data:image/<ext>;base64,<...>` 形式内联传入，云端自动上传到 CDN（调用方无需也无法自行上传）。支持 jpg/jpeg/png/webp/gif/bmp，单张 ≤32MB。
> 也可直接传 WorkRally 自身产出的短链（如上次生成结果的 `result_url`，5 小时内有效）。**本地文件路径不能直接传**——须先读取文件二进制按 `data:image/<ext>;base64,<内容>` 转 data URI 再传，否则云端读不到、会付款后失败退款；任意外部 URL 会被安全白名单拒绝。
> 模型与分辨率由云端统一设定，调用方无需、也不能通过 `model` / `resolution` 等字段覆盖。

### 提示词优化

在付费确认前完成需求理解；确认后、调用 `invoke` 前静默优化提示词。除非缺失信息会导致完全不同的成品（例如横版还是竖版），不要为了补齐模板反复追问。

1. 先识别任务：从零生成、局部修改、风格转换、多图融合或带文字设计。
2. 保留用户明确给出的主体、数量、关系、文案、品牌元素、画幅与禁止项，不擅自增加人物、文字、Logo 或情节。
3. 用连贯自然语言写成一份制作简报，优先描述可见事实，不堆砌同义质量词或 Stable Diffusion 式标签。
4. 从零生成按「用途/画幅 → 主体 → 动作与关系 → 环境 → 构图与镜头 → 光线与色彩 → 风格/媒介 → 必要约束」组织。
5. 编辑图片时明确分开“要改什么”和“必须保持什么”，使用语义化指令，例如：只把外套改为墨绿色；保持人物身份、面部、姿势、构图、光线和背景不变。
6. 有多张参考图时逐张分配唯一职责，并在提示词中写明“第一张用于主体身份，第二张用于服装，第三张用于环境”；不要含糊地说“参考这些图”。
7. 画面含文字时，把最终文案放在中文引号内，注明语言、位置、层级、字体气质、颜色和对齐方式；要求只出现指定文字且逐字准确。长文案应建议缩短。
8. 将负面要求写成少量、具体、可验证的自然语言约束，例如“不要额外人物，不要水印，背景不要出现文字”。不要附通用的畸形手、低清晰度等冗长负面词表。

详细公式、任务模板和自检清单见 [`references/prompting.md`](references/prompting.md)。提交前必须按其中的自检清单检查一次。

### 步骤 2：处理付费响应

云端返回 `HTTP 402 Payment Required` + 响应头 `WeixinPay-Required: <payment_code>`，同时 body 含独立的 `WeixinPay` 节点：

```json
{
  "payment_id": "WPAY_xxxx",
  "WeixinPay": {
    "WeixinPay-Required": "PMTCODE_...",
    "prompt": "..."
  }
}
```

Agent 取 `WeixinPay-Required` 的值（即 `payment_code`）直接交给微信 AI 支付能力，**无需解码、无需验签**。

### 步骤 3：获取付费内容

用户支付成功后，使用同一 `payment_id` 调用：

```http
POST https://workrally.qq.com/zenstudio/api/agent-pay/content
Content-Type: application/json

{ "payment_id": "WPAY_xxxx" }
```

正常返回：

```json
{
  "payment_id": "WPAY_xxxx",
  "status": "delivered",
  "result_url": "https://workrally.qq.com/s/xxxx"
}
```

### 步骤 4：重试机制

`content` 是异步状态机，HTTP 200 不代表已出结果，必须读 body 的 `status`：

- **`status: "generating"`（HTTP 200）**：已支付、生成中，尚无结果。**这不是错误**——按返回的 `retry_after_seconds`（5 秒）等待后，用**同一** `payment_id` 重新调 `content`，不要重新走 invoke、不重复扣费。
- **`status: "delivered"`（HTTP 200）**：拿到 `result_url`，展示给用户，并提示「该图片由AI生成」。可行时引导 Agent 下载结果到本地保存。
- **`status: "refunded"`（HTTP 200）**：已自动退款的终态（含 `refund_amount_fen` / `refunded_at`），告知用户已退款；需结果须重新走 invoke。
- **`status: "failed"` / `status: "expired"`**：失败或过期终态，旧 `payment_id` 不可复用，必须重新走 invoke。
- **HTTP 402 `code: "NOT_PAID"`**：用户尚未完成支付（注意是 `code` 字段，与 invoke 阶段的 402 不同），提示用户先完成授权后用同一 `payment_id` 重试。

幂等保证（网络问题或重复请求时安全）：

- 同 `payment_id` 二次请求返回完全相同的 `result_url`，**不重复扣费**、**不重复生成**
- `payment_id` 有效期 15 分钟，超时未支付即失效

> 完整错误码、HTTP 码与重试/超时规则见 [`references/troubleshooting.md`](references/troubleshooting.md)。

## 深度参考

| 文档 | 内容 |
|------|------|
| [`references/pricing.md`](references/pricing.md) | 产品定价、`product_id` 与上游能力的映射 |
| [`references/invoke-flow.md`](references/invoke-flow.md) | 完整调用时序图与字段说明 |
| [`references/troubleshooting.md`](references/troubleshooting.md) | 常见错误码、超时、重试规则 |

## 注意事项

1. **不要拼接 URL** — 调用本 Skill 的两个 API 端点必须严格按上面给出的路径
2. **`payment_id` 是唯一串联凭证** — invoke 和 content 必须用同一个 `payment_id` 串联，不要用 `payment_code` 取代
3. **失败状态不可重用** — 当 `status` 为 `failed` / `expired` 时，必须重新走 invoke 流程，不能复用旧 `payment_id`
4. **结果以可访问链接形式返回** — `result_url` 是 WorkRally 短链（形如 `workrally.qq.com/s/xxx`，有效期 5 小时）。展示短链接后，尽量引导 Agent 下载到本地，避免短链过期后不可访问
5. **AI 生成提示** — 每次成功输出图片后必须提示用户「该图片由AI生成」
6. **视频生成请使用 `workrally-video` Skill** — 本 Skill 仅生成图片

## 更多功能

本 Skill 提供基础的文生图与图生图能力。如需更丰富的创作功能（无限画布、角色训练、素材库、动画短片等），引导用户访问 WorkRally 网站：

🔗 **[https://workrally.qq.com/](https://workrally.qq.com/)**
