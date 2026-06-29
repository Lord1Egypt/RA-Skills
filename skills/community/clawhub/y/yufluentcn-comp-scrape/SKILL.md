---
name: yufluentcn-comp-scrape
description: >-
  竞品批量对比分析，基于用户上传的 CSV 导出或已授权 API 快照，非未授权爬虫。
  经 Yufluent 云端 Harness 执行。Use for 竞品批量、CSV 对比、competitor export、
  批量对标.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [competitor, batch, csv, amazon, shopify, tiktok, benchmarking, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 竞品批量对比

基于用户**上传的 CSV 导出或已授权 API 快照**进行批量竞品对比分析。**ClawHub / OpenClaw 云端模式** — Harness `comp_scrape` 在 Yufluent 服务端执行；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

⚠️ **非未授权爬虫** — 本技能仅分析你手动导出或授权的数据，不抓取平台页面。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 收集 CSV/数据、调 `run.py`、解读对比报告 |
| **批量对比正式输出** | `POST /v1/skills/comp-scrape/run`（同一 tk-*） | Harness → 批量竞品对比报告 |

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整批量竞品对比报告。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/comp-scrape/run`）获取输出。
3. 对话模型仅用于：帮助整理竞品 CSV 格式、确认平台与语言、解释报告、建议下一步。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

## Instructions（Agent 工作流）

1. **确认数据来源**：`--source-type` 为 `csv_export`（默认）或 `api_snapshot`。
2. **收集输入**：
   - `--our-product`（必填）：我方产品名
   - `--competitor-data`（必填）：CSV 内容或 `.csv`/`.txt` 文件路径
   - `--platform`：`amazon` | `shopify` | `tiktok`
3. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --our-product "蓝牙耳机" \
     --competitor-data "title,price\nComp A,29.99\nComp B,35.00" \
     --platform amazon \
     --lang zh
   ```
   - 文件模式：`--competitor-data ./competitors.csv`
   - API：`POST {TOKENAPI_BASE_URL}/skills/comp-scrape/run`
4. **计费**：402 余额不足；401 密钥无效。

## 与其他技能联动

| 需求 | 技能 |
|------|------|
| 单条竞品快照对比 | `yufluentcn-comp-track` |
| 批量对比 → Listing 优化 | `yufluentcn-ecommerce-listing` |
| 竞品关键词提取 → SEO | `yufluentcn-seo-pro` |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "竞品批量对比"
- "CSV 导入竞品分析"
- "批量对标"
- "这些竞品帮我分析"
- "competitor batch"

## Examples

**CSV 内联**

```bash
python scripts/run.py \
  --our-product "蓝牙耳机" \
  --competitor-data "title,price,rating\nComp A,29.99,4.2\nComp B,35.00,4.5" \
  --platform amazon \
  --lang zh
```

**从 CSV 文件读取**

```bash
python scripts/run.py \
  --our-product "USB-C Hub" \
  --competitor-data ./competitors.csv \
  --platform amazon \
  --lang en
```

**授权 API 快照模式**

```bash
python scripts/run.py \
  --our-product "瑜伽垫" \
  --competitor-data ./api-export.json \
  --source-type api_snapshot \
  --platform shopify \
  --lang zh
```

## 合规声明

- 仅分析用户自行导出或已授权的数据，不抓取平台页面
- 不抓取竞品评论、不代写虚假对比
- 对比结论仅供参考，不构成流量承诺

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.0.0 | 2026-06-13 | 规范 SKILL.md：补充 Agent 规则、Instructions、触发词、示例、合规声明、版本记录 |
| v0.1.0 | — | 初始竞品批量对比技能 |
