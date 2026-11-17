---
name: workrally-video
slug: workrally-video
displayName: WorkRally 视频生成（SkillPay）
display_name: WorkRally 视频生成（SkillPay）
display_name_en: WorkRally Video Generation (SkillPay)
description: 生成视频的付费创作 Skill。当用户要文生视频、图生视频（把单张参考图做成动态），或做动画、短片、动态画面、产品演示等时命中。例：「生成一段城市夜景视频」「做个产品演示动画」「把这张图动起来」。
description_zh: 付费视频生成 Skill，支持文生视频与图生视频，适用于动画、短片、动态画面、产品演示等创作场景。
description_en: Paid video generation skill for text-to-video and image-to-video, covering animation, short films, motion clips, and product demos.
tags: [视频生成, 文生视频, 图生视频, 做视频, 动画, 短片, 动态画面, AIGC]
version: 1.1.1
license: MIT-0
author: WorkRally Team
homepage: https://workrally.qq.com
user-invocable: true
capability: video_generation
pricing:
  model: per_call
  amount_fen: 688
---

# WorkRally 视频生成

根据用户的文字描述，或用户提供的单张参考图加文字描述，调用 WorkRally 平台生成**视频**。每次生成需用户完成一次支付授权，扣款后返回生成结果。

## 触发规则（精准命中）

**命中本 Skill 的创作意图**：

- **生成视频**（`product_id: video-generation`）：用户想要一段视频 / 动画，或想把一张图做成动态视频。
  例：「生成一段……的视频」「做个……的动画 / 短片」「把……做成视频」「把这张图动起来」「来个……的动态画面」

**不触发**的情况：

- 纯文字问答、查询、文案/文字修改、对已有内容的纯文字点评等与"生成新的视频"无关的请求
- **图片 / 插画 / 壁纸 / 头像**等创作意图 —— 应使用 `workrally-image` Skill

## 付费前置检查

调用本 Skill 前，必须检查当前 Agent 是否已安装支付能力（`weixinpay` extension）：

- ✅ **已安装**：可继续提供付费创作服务
- ❌ **未安装**：向用户提示「当前 Agent 暂不支持付费创作能力」，终止流程

## 服务与定价

| 产品ID | 服务内容 | 单价 |
|--------|----------|------|
| `video-generation` | WorkRally视频生成 | 6.88 元/次 |

> 价格以 SkillHub 后台配置为准。命中创作意图后，向用户展示服务名称和价格，由用户确认后进入付费流程。
>
> **生成规格由云端设定**：视频为 720p，默认 10 秒；如果用户在提示词中明确指定秒数，可传 `duration`。每次生成 1 条。

## 使用并获取付费服务

用户确认使用后，按以下步骤完成付费内容获取：

### 步骤 1：发起付费请求

调用云端服务 API：

```http
POST https://workrally.qq.com/zenstudio/api/agent-pay/invoke
Content-Type: application/json

{
  "product_id": "video-generation",
  "prompt": "<用户描述的视频内容>",
  "duration": 10,
  "single_image_url": "<可选：data:image/jpeg;base64,在此填入Base64>"
}
```

> `prompt` 是必填项，**≤500 字**（超长会被 `INVALID_FIELD` 拒绝、不扣费）。**不要直接透传用户原话**；调用前先按下方「提示词优化」将需求编译成可执行镜头指令，再传优化后的提示词。
> `duration` 仅在用户明确指定秒数时传入；未指定时省略或传 10。
> `single_image_url` 是可选项。用户要求把本地图片做成视频时，以 `data:image/<ext>;base64,<...>` 形式内联传入，云端自动上传到 CDN（调用方无需也无法自行上传）；没有参考图时省略。支持 jpg/jpeg/png/webp/gif/bmp，≤32MB。
> 也可直接传 WorkRally 自身产出的短链（如上次生成图片结果的 `result_url`，5 小时内有效）。**本地文件路径不能直接传**——须先读取文件二进制按 `data:image/<ext>;base64,<内容>` 转 data URI 再传，否则云端读不到、会付款后失败退款；任意外部 URL 会被安全白名单拒绝。
> 模型与分辨率由云端统一设定，调用方无需、也不能通过 `model` 覆盖。

### 提示词优化

在付费确认前完成需求理解；确认后、调用 `invoke` 前静默优化提示词。优先生成目标清楚、动作有限、镜头可执行的短片，不要用堆满形容词的长提示词压垮主要动作。

1. 先识别模式：文生视频或单图生视频，并以接口实际支持的文本和单张参考图为边界，不编造多图、参考视频或参考音频输入。
2. 锁定一个主要主体、一条主要动作线和一种镜头运动。用户明确要求多主体或多镜头时才增加，并保持动作因果清楚。
3. 按「主体与场景 → 按时间发生的动作 → 镜头 → 光线/风格 → 声音（需要时）→ 连续性约束」组织成自然语言。
4. 动作必须使用可见、可拍摄的动词，写清起始状态、过程和结束状态；避免“很有感觉、充满故事性”等抽象指令。
5. 用户指定时长或内容较复杂时，使用时间段编排，例如“0–3 秒……；3–7 秒……；7–10 秒……”。默认 10 秒建议最多 2–3 个连续动作节拍。
6. 镜头语言使用一种主运动（固定、缓慢推进、横向跟拍、环绕、拉远、手持跟随等），必要时补充景别和视角；避免同时要求推、拉、摇、移、环绕。
7. 图生视频时把输入图视为首帧和视觉锚点，明确哪些元素必须保持：人物身份、服装、物体形状、Logo、色彩和场景布局；只描述希望发生的运动，不重新发明整张图。
8. 约束要短而具体：主体外观前后一致、动作连续、物体不变形、镜头不跳切、背景不闪烁。不要附通用负面词大全。
9. 若用户要求对白或音效，写出说话者、准确台词、语气和环境声；未要求声音时不要擅自加入对白、旁白或歌词。

详细公式、模板和自检清单见 [`references/prompting.md`](references/prompting.md)。提交前必须按其中的自检清单检查一次。

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
- **`status: "delivered"`（HTTP 200）**：拿到 `result_url`，展示给用户，并提示「该视频由AI生成」。可行时引导 Agent 下载结果到本地保存。
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
5. **图片生成请使用 `workrally-image` Skill** — 本 Skill 仅生成视频
6. **AI 生成提示** — 每次成功输出视频后必须提示用户「该视频由AI生成」
7. **视频生成耗时较长** — 单条视频通常需要 1-3 分钟（具体视模型与队列情况），调用方需做好长轮询和用户预期管理

## 更多功能

本 Skill 仅提供基础的文生视频能力。如需更丰富的创作功能（无限画布、角色训练、素材库、动画短片等），引导用户访问 WorkRally 网站：

🔗 **[https://workrally.qq.com/](https://workrally.qq.com/)**
