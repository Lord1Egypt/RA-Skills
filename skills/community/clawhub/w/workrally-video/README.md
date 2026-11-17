# WorkRally 视频生成 Skill

WorkRally 视频生成 Skill：根据用户的文字描述或单张参考图，调用 WorkRally 平台生成**视频**。
付费类型 Skill，对接微信支付 Agent 支付（X402 V1.3）协议——用户每次生成完成一次支付授权，扣款后返回结果。

> 图片生成请使用 [`workrally-image`](../workrally-image/README.md) Skill。

## 能力

| 产品 | product_id | 服务 | 单价 |
|------|-----------|------|------|
| 视频生成 | `video-generation` | 根据文字描述或单张参考图生成视频 | 6.88 元/次 |

> 价格以 SkillHub 后台配置为准。规格为 720p，默认 10 秒。

## 何时触发

当用户表达**生成视频 / 动画**的创作意图时触发，例如：
- 「生成一段……的视频」「生成一个……的动画」
- 「做个……的短片」「把这个画面变成视频」
- 「把这张图动起来」「基于这张图生成一段视频」
- 「来个……的动态画面」

图片 / 插画 / 壁纸等意图不触发，应走 `workrally-image` Skill。纯问答、查询、文字修改等也不触发。
详见 [`SKILL.md`](SKILL.md) 的「触发规则」。

## 调用流程（概览）

1. **invoke** — `POST /zenstudio/api/agent-pay/invoke`，传 `product_id: "video-generation"` + `prompt`，可选 `duration` / `single_image_url`，返回 402 + `payment_code`
2. 用户用 `payment_code` 完成微信支付授权
3. **content** — `POST /zenstudio/api/agent-pay/content`，传同一 `payment_id` 轮询取结果（`generating` → `delivered` + `result_url`）。**视频生成耗时较长**，单条通常 1-3 分钟，需长轮询

完整字段、状态机与重试规则见 SKILL.md 与 references/。

## 目录内容

| 文件 | 说明 |
|------|------|
| [`SKILL.md`](SKILL.md) | Skill 主文档（给 Agent 读）：触发规则、调用步骤、状态处理 |
| [`references/pricing.md`](references/pricing.md) | 产品定价与 `product_id` 映射 |
| [`references/invoke-flow.md`](references/invoke-flow.md) | 完整调用时序图与字段说明 |
| [`references/troubleshooting.md`](references/troubleshooting.md) | 错误码、超时、重试规则 |

## 上架（SkillHub）

1. 在 SkillHub 平台创建开发者账号，获取 `partner_mch_id` + `pub_key_id`
2. 上传本目录（`SKILL.md` + `references/`）作为 Skill 包，建议注册名为 `WorkRally视频生成`
3. 在平台后台配置 `video-generation` 产品价格
4. 审核通过后即可在 Agent 中触发
