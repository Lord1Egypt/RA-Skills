---
name: yufluentcn-record-outcome
description: >-
  Yufluent 效果回传辅助包：将 Listing / SEO 等技能返回的 run_id 与卖家
  反馈的销量、点击、曝光登记到 Yufluent 效果闭环。不走 /v1/skills/*/run，
  仅 POST /v1/agent/outcomes（与 OpenClaw 对话共用 tk-*）。
  Use for 效果回传、run_id 登记、上架后销量记录、效果追踪.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [tracking, analytics, outcome, run-id, yufluent]
  billing: yufluent
  languages: [zh, en]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 效果回传

将此前 Listing / SEO / 广告等技能返回的 **`run_id`** 与卖家反馈的销量、点击、曝光等登记到 Yufluent 效果闭环，用于后续模型优化和效果归因。

**注意**：本技能不走 `POST /v1/skills/*/run`，仅走 `POST /v1/agent/outcomes`（与 OpenClaw 对话共用同一 `tk-*`）。不调用 Harness 生成内容。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与本技能**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 识别 run_id、收集效果数据、调 `run.py` |
| **效果登记** | `POST /v1/agent/outcomes`（同一 tk-*） | 登记效果到 Yufluent |

**Agent 硬性规则：**

- **禁止**用对话模型自行构造 `POST /v1/agent/outcomes` 请求或编造效果数据。
- **必须**通过 `python scripts/run.py ...` 登记效果。
- 只需 `TOKENAPI_KEY`，不要另配 Key

## Instructions（Agent 工作流）

1. **触发时机**：用户说「Listing 上架了」「这周卖了 20 单」且对话里出现过 `run_id=hr_xxx`。
2. **收集参数**：
   - `--run-id`（必填）：之前技能输出中的 run_id
   - `--event`：事件类型（默认 `published`，可选 `sale`）
   - `--orders` / `--impressions` / `--clicks`：效果数据
   - `--notes`：备注如 "Amazon US 首周"
3. **调用**：
   ```bash
   python scripts/run.py \
     --run-id "hr_abc123" \
     --event sale \
     --orders 20 \
     --notes "Amazon US 首周"
   ```
4. **无需计费**：仅登记，不消耗 Harness Token。

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--run-id` | 是 | 技能返回的 run_id（如 `hr_abc123`） |
| `--event` | 否 | 事件类型：`published` / `sale` / `promoted`，默认 `published` |
| `--orders` | 否 | 订单数 |
| `--impressions` | 否 | 曝光量 |
| `--clicks` | 否 | 点击量 |
| `--revenue-cny` | 否 | 收入（元） |
| `--external-id` | 否 | 平台 ASIN / SKU |
| `--notes` | 否 | 备注说明 |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "帮我记录效果"
- "上架后有销量了"
- "run_id 回传"
- "效果登记"
- "Listing 出单了"
- "登记一下"

## Examples

**商品上架回传**

```bash
python scripts/run.py \
  --run-id "hr_abc123" \
  --event published \
  --external-id "B0XXXXXXX" \
  --notes "Amazon US 上架"
```

**销量回传**

```bash
python scripts/run.py \
  --run-id "hr_abc123" \
  --event sale \
  --orders 20 \
  --revenue-cny 15000 \
  --impressions 5000 \
  --clicks 320 \
  --notes "首周数据"
```

## 工作原理

```text
跑 Listing/SEO 技能 → 输出 run_id → 过段时间有销量 → 调 record-outcome 回传
                                                    ↓
                                            Yufluent 累计效果数据
                                                    ↓
                                        后续模型优化 / 归因分析
```

## 合规声明

- 仅登记用户主动提供的数据，不抓取平台后台
- 不自动获取 ASIN、订单号或任何卖家敏感数据

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.0.0 | 2026-06-13 | 规范 SKILL.md：补充 Agent 规则、Instructions、触发词、示例、环境变量、合规、版本记录 |
| v0.1.0 | — | 初始效果回传辅助包 |
