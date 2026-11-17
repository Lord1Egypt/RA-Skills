# 变更日志

## 0.3.2（2026-08-17）

**X402 协议代码级实现**——修复安全审核被拒「缺少必要的支付服务」。

- 新增后端 `src/pay.ts` 模块：完整实现微信 Native 下单 → X402 AI 预下单（SHA256withRSA 签名，5 行签名串，Base64 双层 body）→ HTTP 402 + `WeixinPay-Required` 头 → 回调验签解密（AES-256-GCM）→ 退款 全链路
- `src/server.ts` 集成支付闸门：首次请求无 `X-PAYMENT` → 创建订单返回 402；重试带 `X-PAYMENT` → 验证 `payment_code` 放行；新增 `POST /cloud/api/pay/notify`（回调）、`GET /cloud/api/pay/status/:outTradeNo`（查询）、`POST /cloud/api/pay/refund/:outTradeNo`（退款）三个端点
- `src/db.ts` 新增 `payments` 表（out_trade_no / payment_code / status / transaction_id 等）
- SKILL.md X402 章节按官方教程全面重写：替换 v0.3.1 的理论占位（`X-PAYMENT-CHALLENGE`/`order_id`）为真实协议字段（`WeixinPay-Required`/`payment_code`/`code_url`/`preorder`）
- 关键词索引更新：覆盖 `WeixinPay-Required`、`payment_code`、`preorder`、`SHA256withRSA`、`SKILLHUB-SHA256-RSA2048`、`AUTH_AND_PAY`、`code_url` 等 24 个关键词

## 0.3.1（2026-08-16）

**首发 Pay Skill 收费版**（¥9.9/次）。

- SKILL.md frontmatter 新增 `pricing` 块：`model=per_call / amount_fen=990 / currency=CNY / unit=次`，声明计费单元、扣费时机、失败/退款规则
- description 内补充计费单元语义，让 Agent 在用户沟通中可如实告知
- 后端 v0.3.1 同版本联动（市场首页缩略图墙、页脚备案号、OG 分享卡片）
- 上架材料：3 张真实生产环境截图（云市场首页 / 档口详情 / 微信分享卡片占位）随发布包提交

## 0.3.0（2026-08-16）

与后端 ruancy-cloud-market v0.3.0 对齐，首次按 15-Skill 发布规范整理为可上架包。

- SKILL.md 补 frontmatter（slug `tenyuan-cloud-shop`），新增触发场景与关键约束小节（示意图如实标注、不承诺交易、后端不可达时如实降级）
- 新增 `references/api.md`：完整后端 API 契约（创建档口 / 上传二维码 / 获取分享素材 / 档口页 / 错误形态与应对）
- `agents/openai.yaml` 补齐二维码与分享素材端点、降级与如实转述规则
- 新增 `scripts/validate_package.py` 包体校验（必需文件、零二进制、版本一致性、必备声明语句）及其负向测试
- 后端本版本的对应能力：分享链接区（完整 URL + 复制/系统分享）、店主微信二维码上传与展示、页脚返回阮策AI·云市场、资源 URL 域名自适应（库存相对路径）

## 0.2.0（2026-08-16）

- 对应后端 v0.2：OpenAI TTS 口播音频生成

## 0.1.0（2026-08-16）

- 首版：一句话/一张图创建云铺档口页
