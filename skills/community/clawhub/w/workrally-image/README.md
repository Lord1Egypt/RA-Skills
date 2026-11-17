# WorkRally 图片生成 Skill

WorkRally 图片生成 Skill：根据用户的文字描述或参考图，调用 WorkRally 平台生成**图片**。
付费类型 Skill，对接微信支付 Agent 支付（X402 V1.3）协议——用户每次生成完成一次支付授权，扣款后返回结果。

> 视频生成请使用 [`workrally-video`](../workrally-video/README.md) Skill。

## 能力

| 产品 | product_id | 服务 | 单价 |
|------|-----------|------|------|
| 图片生成 | `image-generation` | 根据文字描述或参考图生成图片 | 0.36 元/次 |

> 价格以 SkillHub 后台配置为准。规格为 1K，由云端统一设定。

## 何时触发

当用户表达**生成图片**的创作意图时触发，例如：
- 「画一只橘猫」「生成一张产品海报」
- 「做张插画 / 壁纸 / logo 配图」「我想要一张关于……的图」
- 「参考这张图生成……」「把这张图改成……风格」

视频 / 动画 / 短片等意图不触发，应走 `workrally-video` Skill。纯问答、查询、文字修改等也不触发。
详见 [`SKILL.md`](SKILL.md) 的「触发规则」。

## 调用流程（概览）

1. **invoke** — `POST /zenstudio/api/agent-pay/invoke`，传 `product_id: "image-generation"` + `prompt`，图生图时加 `input_images`，返回 402 + `payment_code`
2. 用户用 `payment_code` 完成微信支付授权
3. **content** — `POST /zenstudio/api/agent-pay/content`，传同一 `payment_id` 轮询取结果（`generating` → `delivered` + `result_url`）

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
2. 上传本目录（`SKILL.md` + `references/`）作为 Skill 包，建议注册名为 `WorkRally图片生成`
3. 在平台后台配置 `image-generation` 产品价格
4. 审核通过后即可在 Agent 中触发
