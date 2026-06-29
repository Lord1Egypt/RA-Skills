---
name: yufluentcn-b2b-assist
description: >-
  B2B 外贸询盘回复与 RFQ 报价助手，经 Yufluent 云端 Harness 执行。
  支持 FOB/CIF 报价单、MOQ 谈判、交期回复、公司简介等专业外贸场景。
  Use for 询盘回复、RFQ、FOB/CIF 报价、外贸报价、B2B inquiry.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [b2b, inquiry, rfq, quotation, fob, cif, trade, import-export, yufluent]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# B2B 询盘助手

外贸 **B2B 询盘回复与 RFQ 报价** 专用技能。**ClawHub / OpenClaw 云端模式** — Harness `b2b_inquiry` 在 Yufluent 服务端执行；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 收集询盘原文与报价要素、调 `run.py`、提交人工审核 |
| **询盘回复正式输出** | `POST /v1/skills/b2b-assist/run`（同一 tk-*） | Harness → 专业询盘回复或报价单 |

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整 B2B 报价单或商务回复（尤其是含价格承诺、交期保证的条款）。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/b2b-assist/run`）获取输出。
3. 对话模型仅用于：收集询盘原文与报价要素（MOQ、FOB/CIF、交期、付款方式）、确认语言、提醒审核。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

## Instructions（Agent 工作流）

1. **确认语言**：`--lang`，默认 `en`（外贸通用英语）。
2. **收集输入**（尽量一次问齐）：
   - `--message`（必填）：买家询盘原文或 `.txt` 文件路径
   - `--product`：产品名称
   - `--moq`：最小起订量
   - `--fob-price` / `--cif-price`：FOB/CIF 报价
   - `--lead-time`：交期（如 `30 days`）
   - `--payment-terms`：付款方式（如 `T/T 30% deposit`）
   - `--company-profile`：公司简介（可选）
   - `--inquiry-type`：`rfq` / `general`（默认 `rfq`）
3. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --message "Please quote 500 units FOB Shenzhen" \
     --product "Bluetooth Speaker" \
     --moq 500 \
     --fob-price "USD 12.50" \
     --lead-time "30 days" \
     --payment-terms "T/T 30% deposit, 70% before shipment" \
     --lang en
   ```
   - API：`POST {TOKENAPI_BASE_URL}/skills/b2b-assist/run`
4. **交付**：将回复正文（JSON 包含邮件正文 + 报价摘要）交给用户，提醒核实价格/条款后发送。
5. **计费**：402 余额不足；401 密钥无效。

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "帮我回这封询盘"
- "写个 RFQ 报价"
- "B2B 回复"
- "外贸报价"
- "FOB 报价单"
- "回复买家询价"
- "inquiry reply"

## Examples

**RFQ 报价回复**

```bash
python scripts/run.py \
  --message "We are interested in your Bluetooth speakers. Please quote 500 units with FOB Shenzhen price." \
  --product "Portable Bluetooth Speaker X1" \
  --moq 500 \
  --fob-price "USD 12.50" \
  --lead-time "25-30 days" \
  --payment-terms "T/T 30% deposit, 70% before shipment" \
  --lang en
```

**一般询盘回复（无报价）**

```bash
python scripts/run.py \
  --message "Do you offer OEM service for wireless earbuds?" \
  --product "TWS Wireless Earbuds" \
  --inquiry-type general \
  --company-profile "10-year OEM manufacturer, ISO 9001 certified" \
  --lang en
```

**从文件读取询盘**

```bash
python scripts/run.py \
  --message ./inquiry.txt \
  --product "LED Strip Light" \
  --moq 1000 \
  --fob-price "USD 3.00" \
  --lang en
```

## 合规声明

- 最终报价须由业务员核实成本、汇率与产能后签发
- 不虚构公司资质、认证或交期承诺
- 注意目标市场进出口规定与制裁名单

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.0.0 | 2026-06-13 | 规范 SKILL.md：补充 Agent 规则、Instructions、触发词、示例、合规、版本记录 |
| v0.1.0 | — | 初始 B2B 询盘回复技能 |
