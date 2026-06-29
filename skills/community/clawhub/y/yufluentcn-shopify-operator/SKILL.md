---
name: yufluentcn-shopify-operator
description: >-
  Shopify 独立站全店运营教练 — 六阶段指导型技能（选品→寻源→上架→装修→社媒→监控），
经 Yufluent 云端 Harness 执行。Full-store Shopify operations coach covering
sourcing → supplier → listing → decoration → social → monitoring.
Use for 全店运营、独立站、选品扩品、供应链、上架优化、店铺装修、社媒、监控复盘。
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [shopify, dtc, operations, coaching, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# Shopify 全店运营教练

Shopify 独立站 **全生命周期运营** 指导技能：覆盖新店从 0 到 1，也覆盖已开业店铺的扩品、优化、营销与复盘。**ClawHub / OpenClaw 用户使用云端模式** — Harness 在 Yufluent 服务端执行，本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw 。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 理解意图、选 stage、收集 context、调 `run.py`、整理回复 |
| **运营方案正式输出** | `POST /v1/skills/shopify-operator/run`（同一 tk-*） | Harness + 阶段策略 → Markdown 运营方案 |

```text
用户 → OpenClaw（yufluent provider）→ python scripts/run.py → Yufluent API → Harness → 运营方案
```

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整运营方案（选品表、供应商表、装修方案、社媒日历、监控模板等长文）。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/shopify-operator/run`）获取输出，并将 stdout 作为交付物。
3. 对话模型仅用于：确认店铺阶段、收集 niche / store_url / context、解释结果、建议下一步或联动其他技能。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

## Instructions（Agent 工作流）

1. **判断店铺状态**：新店（未上线 / 密码页）还是老店（已有 SKU 与流量）。老店可跳过 sourcing，直接进入 listing / decoration / monitoring。
2. **选择 stage**（见下表）；用户未说明时，根据问题推断，或默认 `monitoring`（复盘类）/ `sourcing`（从零开店类）。
3. **收集上下文**（尽量一次问清）：
   - `message`（必填）：本轮具体问题
   - `niche`：细分品类 / 主营类目
   - `store_url`：店铺 URL（老店强烈建议提供）
   - `context`：月 GMV 区间、SKU 数、痛点、已尝试动作等
4. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --stage monitoring \
     --message "店铺转化率 0.8%，想优化低转化 SKU" \
     --niche "宠物用品" \
     --store-url "https://xxx.myshopify.com" \
     --context "月 GMV 约 $8k，共 42 SKU" \
     --lang zh
   ```
   - API：`POST {TOKENAPI_BASE_URL}/skills/shopify-operator/run`
5. **交付**：将 Markdown 正文转给用户；结尾通常含「下一步请你确认/提供」清单，引导用户补充数据或进入下一阶段。
6. **计费**：402 余额不足；401 密钥无效。

### 六阶段（stage）

| stage | 适用场景 | 输出类型 |
|-------|----------|----------|
| `sourcing` | 新店选品、老店扩品 / 换季选品 | 调研表结构、参数建议、短名单模板 |
| `supplier` | 已确认 SKU，需寻源与毛利测算 | 1688/阿里寻源检查表、毛利公式 |
| `listing` | 批量上新、低转化 SKU 文案优化 | 上架清单、素材需求；可联动 listing 技能 |
| `decoration` | 新店装修、老店改版、集合页优化 | 视觉规范、Banner/集合页文案、shot list |
| `social` | 日常发帖、活动预热、2 周内容规划 | 帖文草稿、内容日历（**不**代发） |
| `monitoring` | 周/月复盘、竞品跟踪、指标诊断 | cron 说明、日志模板、优化检查表 |

阶段可用数字 `1`–`6` 或别名（如 `research` → `sourcing`）。

### 与其他技能联动

| 需求 | 技能 | 说明 |
|------|------|------|
| 生成 Shopify 产品 JSON 文案 | `yufluentcn-ecommerce-listing` | stage=listing 时可在方案中建议用户另跑 |
| SEO 关键词布局 | `yufluentcn-seo-pro` | 扩品或 listing 优化前后 |
| 竞品 Listing 对标 | `yufluentcn-comp-track` | monitoring 阶段发现竞品异动时 |
| 评论洞察 / 差评归因 | `yufluentcn-review-intel` | 低转化或高退货 SKU 诊断 |
| 买家消息回复 | `yufluentcn-chat-assist` | 日常客服，非本技能范围 |

本技能 **不**调用 Jungle Scout / 1688 API、不代发社媒、不直连 Shopify Admin。

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

模型档位由平台 Harness 自动选择，无需卖家配置。

## 触发词

- "Shopify 全店运营"
- "独立站怎么从选品做到上架"
- "老店转化率低怎么优化"
- "帮我做两周社媒内容日历"
- "扩品调研表"
- "供应商毛利怎么算"
- "店铺装修方案"
- "竞品监控模板"
- "Shopify 运营复盘"

## Examples

**新店 — 选品**

```bash
python scripts/run.py \
  --stage sourcing \
  -m "我想做宠物用品独立站，请给调研表结构" \
  --niche "宠物用品" \
  --lang zh
```

**老店 — 监控复盘**

```bash
python scripts/run.py \
  --stage monitoring \
  -m "弃购率偏高，请给本周优化检查表" \
  --store-url "https://pawmart.myshopify.com" \
  --context "月 GMV $12k，主力 SKU 3 个" \
  --lang zh
```

**扩品 — 供应商**

```bash
python scripts/run.py \
  --stage supplier \
  -m "已确认这 3 个 SKU，请给寻源表与毛利模板" \
  --niche "宠物牵引绳" \
  --lang zh
```

## 文件结构（ClawHub 包）

```
yufluentcn-shopify-operator/
  SKILL.md
  README.md
  .env.example
  requirements.txt
  scripts/
    run.py
    yufluent_api.py
    cloud_cli.py
```

桌面客户端体验见仓库 `clients/yufluentcn-assistant/`。

## 合规声明

- 方案与文案需人工审核后执行；遵守 Shopify 及目标市场法规
- 不虚构 ASIN、供应商链接、已发布帖子 URL 或后台已修改状态
- 图片与描述须与实物一致，禁止误导性宣传

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v0.3.0 | 2026-05-28 | 定位升级为「全店运营」；完善 Agent 工作流、阶段说明与技能联动 |
| v0.2.0 | 2026-05-24 | OpenClaw 双模型；六阶段云端教练 |
| v0.1.0 | 2026-05-21 | 从 DIDagent 迁移流程与 Prompt |
