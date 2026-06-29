---
name: yufluentcn-chat-assist
description: >-
  跨境电商智能客服回复助手 — 亚马逊 / Shopify / TikTok 买家消息专业回复草稿，
经 Yufluent 云端 Harness + messaging-guard 合规护栏执行。Cross-border buyer
message reply assistant for Amazon, Shopify & TikTok Shop with platform policies.
Use for 客服回复、买家消息、物流查询、退款咨询、差评沟通、order inquiry.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [customer-service, messaging, amazon, shopify, tiktok, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 跨境客服回复助手

为 **Amazon / Shopify / TikTok Shop** 买家站内信/客服消息生成 **可直接粘贴发送的回复正文**。**ClawHub / OpenClaw 云端模式** — Harness `chat_reply` + `messaging-guard` 在 Yufluent 服务端执行；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

本技能 **不**连接卖家后台、不自动发送消息、不查询真实物流 API；`order_context` 由你提供摘要，模型不会虚构已核实的状态。

---

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw 。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 收集买家原文与订单上下文、调 `run.py`、人工微调后发送 |
| **客服正式输出** | `POST /v1/skills/chat-assist/run`（同一 tk-*） | Harness + 平台规则 → 回复正文 |

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整客服回复（尤其是含退款/赔偿承诺的句子）。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/chat-assist/run`）获取输出。
3. 对话模型仅用于：确认平台与语言、收集 `message` / `order_context`、提醒卖家审核、建议转人工场景。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

---

## Instructions（Agent 工作流）

1. **确认平台**：`amazon` | `shopify` | `tiktok`（决定模板与 messaging 规则）。  
2. **确认回复语言 `--lang`**：默认与买家消息一致；卖家指定时用 `zh|en|es|de|fr|ja`。  
3. **收集输入**：  
   - `message`（必填）：买家原文，**原样粘贴**，不要改写成第三人称。  
   - `order_context`（强烈建议）：订单号、物流单号、当前状态摘要、卖家授权政策（如「可补发」）。  
   - `product`（可选）：SKU/品名，便于对齐 Listing。  
4. **调用（必须 — 云端）**：  
   ```bash
   python scripts/run.py \
     --message "Where is my package? Order #123-4567890" \
     --platform amazon \
     --lang en \
     --product "Wireless Earbuds Pro" \
     --order-context "Shipped 2026-05-20, tracking 1Z999, in transit US"
   ```  
5. **交付**：将 stdout **回复正文**交给卖家；提醒删除不实承诺、按平台按钮发送。  
6. **计费**：402 余额不足；401 密钥无效。

---

## 买家消息输入格式

| 字段 | CLI / API | 说明 |
|------|-----------|------|
| **买家消息** | `--message` / `message` | **必填**；支持多行；保留买家原语言 |
| **订单/物流** | `--order-context` / `order_context` | 建议格式见下表 |
| **产品** | `--product` / `product` | 关联 ASIN/SKU 或商品名 |
| **平台** | `--platform` | `amazon` \| `shopify` \| `tiktok`，默认 `amazon` |
| **语言** | `--lang` | 输出语言；未指定时 Harness 结合买家消息与 locale |

### `order_context` 推荐写法（一行或短段落）

```text
Order #123-4567890 | Shipped 2026-05-20 | Tracking 1Z999AA10123456784 | In transit to US
```

| 片段 | 示例 |
|------|------|
| 订单号 | `Order #123-4567890` |
| 物流状态 | `Delivered` / `In transit` / `Delayed — carrier investigation` |
| 卖家授权 | `Seller authorized: replacement once` / `No refund without return` |

未提供时 Harness 填「（买家未提供订单号）」—— 回复会以「为您核实」为主，**避免**编造物流细节。

### 常见场景（Agent 推断平台与语气）

| 场景 | 回复策略要点 |
|------|----------------|
| **物流查询** | 共情 + 说明已记录单号 + 引导查 tracking / 承诺跟进时效（不承诺具体送达日） |
| **未收到/丢件** | 请照片/地址确认 + 转核实 + 按授权提及补发/退款流程 |
| **质量/损坏** | 致歉 + 要订单号与照片 + 不预判责任 |
| **退款/退货** | 引用平台 RMA 步骤；无授权时 **不**承诺金额 |
| **售前咨询** | 规格/库存中性说明 + 链到 Listing（Amazon 避免站外营销外链） |
| **差评/威胁** | 保持专业；**不**要求改评；引导站内解决 |

---

## 输出说明

- **纯文本回复正文**（非 JSON）：无标题、无「以下是回复」类前缀。  
- 长度通常 **2–5 句**（由 `messaging-guard` 约束）。  
- 须 **人工审核** 后再在 Seller Central / Shopify Inbox / TikTok 商家后台发送。

---

## 平台差异（简要）

| 平台 | 注意 |
|------|------|
| **Amazon** | Buyer-Seller Messaging；避免站外联系与营销外链 |
| **Shopify** | 可提及店铺政策，勿编造条款原文 |
| **TikTok Shop** | 注意 SLA 表述，避免绝对送达日期 |

---

## 与其他技能联动

| 需求 | 技能 |
|------|------|
| 批量评论洞察后再回信 | `yufluentcn-review-intel` → 本技能 |
| 改 Listing 减少售前咨询 | `yufluentcn-ecommerce-listing` |
| 关键词/描述与买家问法对齐 | `yufluentcn-seo-pro` |
| 独立站运营话术策略 | `yufluentcn-shopify-operator` |

---

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*` |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

---

## 触发词

- "回复这条买家消息"  
- "客服怎么回" / "写个英文回复"  
- "订单到哪了" / "refund request"  
- "包裹破损怎么回"  
- "TikTok 买家催发货"

---

## Examples

**Amazon — 物流（英文）**

```bash
python scripts/run.py \
  --message "Where is my order? It's been 10 days." \
  --platform amazon \
  --lang en \
  --order-context "Order #111-2223333, shipped May 18, tracking in transit" \
  --product "USB-C Hub 7-in-1"
```

**Shopify — 退款咨询（中文）**

```bash
python scripts/run.py \
  --message "想退货，不喜欢颜色" \
  --platform shopify \
  --lang zh \
  --order-context "Order #1042, delivered May 20, 30-day return policy applies" \
  --product "北欧实木餐椅"
```

**TikTok — 售前（英文）**

```bash
python scripts/run.py \
  --message "Does this fit iPhone 15?" \
  --platform tiktok \
  --lang en \
  --product "MagSafe Phone Case"
```

---

## 合规声明

- 回复须符合各平台 **Buyer-Seller Messaging** 与当地消费者法规。  
- **不得**索要站外联系方式、引导删改差评、未经授权承诺退款/赔偿。  
- 卖家对发送内容负最终责任；本技能输出仅为草稿。  

Harness 合规护栏：`harness/scenes/chat_reply/policies/messaging-guard.md`

---

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v0.3.0 | 2026-05-28 | 按 ad-optimize 结构扩展：工作流、输入格式、场景表、示例与合规 |
| v0.2.0 | — | Harness `chat_reply` 三平台模板 |
| v0.1.0 | — | 初始云端薄客户端 |
