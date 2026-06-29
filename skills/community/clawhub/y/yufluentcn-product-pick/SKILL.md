---
name: yufluentcn-product-pick
description: >-
  选品分析：亚马逊/TikTok Shop/速卖通多平台 BSR、销量、价格、评论、利润与竞争度 AI 打分，
  筛选蓝海、规避红海与侵权风险。经 Yufluent 云端 Harness 执行。
  Use for 选品、蓝海、BSR、备货决策、product research、选品分析.
version: 1.0.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [product-research, sourcing, blue-ocean, bsr, amazon, tiktok, aliexpress, inventory, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 选品分析

帮助老板与运营**用数据做备货决策**：多平台（Amazon / TikTok Shop / 速卖通）BSR、销量信号、价格、评论、利润与竞争度综合打分，输出 go / watch / no-go 与 IP 风险提示。

**ClawHub / OpenClaw 云端模式** — Harness `product_pick` 在 Yufluent 服务端执行；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

⚠️ **合规** — 市场数据应来自 Browser Service 已授权页面提取、用户手动粘贴或已授权 API 导出；本技能**不**未授权爬取平台。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login
2. **设置环境变量**：`export TOKENAPI_KEY=***` 或写入 `.env`
3. **运行**：见下方 Examples

## OpenClaw 与 Yufluent（必读）

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话 + Browser** | `browser_*` 工具 + 同一 `tk-*` | 在授权页面提取 BSR/价格/评论，整理为结构化文本 |
| **选品正式报告** | `POST /v1/skills/product-pick/run` | Harness → 蓝海打分与备货建议 JSON |

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整选品决策报告。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/product-pick/run`）获取输出。
3. **推荐工作流（自动 Browser）**：说「自动选品 / browser选品 / 选品分析 + 品类名」→ Agent 触发 workflow `browser-to-product-pick`（Amazon SERP → Listing 抓取 → 本技能打分）。已有数据时直接 `run_skill(product-pick)` 或 workflow 内提供 `product_candidates` 则跳过 Browser。
4. **手动 Browser 工作流**：`browser_navigate` → `browser_extract` → 将结果填入 `--product-candidates` → `run.py`。
5. 对话模型仅用于：澄清选品方向、解释打分、建议补数据。
6. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

## 自动选品流程（Agent 编排）

> **workflow_id**：`browser-to-product-pick`（manifest 内置，可 `run_workflow` 一键触发；等价于下方 Step 1–4 的自动化子集，默认抓 Top 5 Listing 详情）。  
> **auto_discover**：Agent 无现成 `product_candidates` 时，**必须**按下列步骤抓取后再 `run.py`，禁止跳过 Browser 直接编造数据。

**触发词**：`自动选品` / `browser选品` / `帮我选品 + 品类名` / `选品分析 + 品类名`

| Step | 动作 | 说明 |
|------|------|------|
| **1** | `browser_navigate` → Amazon SERP | URL：`https://www.amazon.com/s?k={niche}`；`browser_extract(schema=amazon_serp)` |
| **2** | 对 SERP 中 **Top 20** 非 sponsored ASIN | 逐个 `browser_navigate` → `browser_extract(schema=amazon_listing)`，取 BSR / 价格 / 评分 / 评论数 |
| **3** | 整理 `--product-candidates` | 合并为 CSV/JSON，列建议：`platform,asin,title,bsr,price,rating,review_count,url`；写入 `working_notes` |
| **4** | **必须**调用 Harness | `python scripts/run.py --niche "{品类}" --product-candidates ./data.json --data-source browser_extract --lang zh`（或 `POST /v1/skills/product-pick/run`） |
| **5** | 解读交付 | 向老板说明 `blue_ocean_score`、`competition_score`、`ip_risk`、`capital_impact`、`verdict`（go / watch / no-go） |

**快捷路径**（已配置 Browser Service）：

```text
run_workflow(workflow_id="browser-to-product-pick", payload={ "niche": "便携榨汁杯", "max_capital": "50000", "lang": "zh" })
```

若 payload 已含 `product_candidates`，workflow 跳过 Step 1–3，直接 Step 4。

## Instructions（Agent 工作流）

1. **澄清选品方向**：`--niche`（细分品类 / 场景）。
2. **采集市场数据**（任选其一）：
   - Browser：`browser_navigate` + `browser_extract`（amazon_listing / amazon_serp 等 schema）
   - 用户粘贴多平台表格或 JSON
   - 已授权 API 导出（`--data-source api_snapshot`）
3. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --niche "便携榨汁杯" \
     --product-candidates @market_data.txt \
     --platforms "amazon,tiktok,aliexpress" \
     --unit-cost "到岸 ¥35" \
     --target-margin "30%" \
     --max-capital "¥50000" \
     --lang zh
   ```
4. **解读**：向老板说明 `blue_ocean_score`、`ip_risk`、`capital_impact` 与 `verdict`。

## 与其他技能联动

| 需求 | 技能 |
|------|------|
| 单条竞品快照 | `yufluentcn-comp-track` |
| 批量竞品 CSV 对比 | `yufluentcn-comp-scrape` |
| 评论痛点深挖 | `yufluentcn-review-intel` |
| 关键词 / 搜索量 | `yufluentcn-seo-pro` |
| 备货与补货 | `yufluentcn-inventory-pilot` |
| 合规 / 认证 | `yufluentcn-compliance-guard` |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "选品分析"
- "蓝海选品"
- "这个品类能不能做"
- "BSR 选品"
- "备货决策"
- "自动选品"
- "browser选品"
- "product research"

## Examples

**CLI 自动发现（`--discover`，需 Browser Service）**

```bash
# Amazon 搜索 SERP → Top N Listing 详情 → Harness 打分
python scripts/run.py \
  --niche "便携榨汁杯" \
  --discover \
  --discover-source amazon_serp \
  --search-query "portable juicer" \
  --max-candidates 20 \
  --lang zh

# Amazon 畅销排序搜索
python scripts/run.py --niche "瑜伽垫" --discover --discover-source amazon_bs

# TikTok Shop 搜索页发现（依赖页面结构，可能回退为快照行）
python scripts/run.py --niche "手机支架" --discover --discover-source tiktok_trending
```

环境变量：`BROWSER_SERVICE_URL`（默认 `http://127.0.0.1:9222`）

**Browser 提取后分析**

```bash
python scripts/run.py \
  --niche "宠物自动喂食器" \
  --product-candidates ./browser_extract.json \
  --data-source browser_extract \
  --platforms "amazon,tiktok" \
  --max-capital "80000" \
  --lang zh
```

**手动粘贴多平台数据**

```bash
python scripts/run.py \
  --niche "瑜伽阻力带" \
  --product-candidates "platform,title,bsr,price,reviews,rating
amazon,Set A,#1200,\$19.99,850,4.3
tiktok,Set B,月销2k+,¥89,320,4.1" \
  --data-source manual \
  --unit-cost "¥12 到岸" \
  --target-margin "35%" \
  --lang zh
```

## 合规声明

- 仅分析用户提供或 Browser Service 已授权提取的数据
- 不指导绕过平台 ToS 的爬虫
- 利润与销量为估算，IP 风险须人工复核
- 不构成采购或投资建议

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.2 | 2026-06-25 | run.py 增加 --discover / --discover-source / --search-query / --max-candidates |
| v1.0.1 | 2026-06-25 | 增加「自动选品流程（Agent 编排）」与 auto_discover / browser-to-product-pick 说明 |
| v1.0.0 | 2026-06-25 | 初始选品分析技能：多平台打分、蓝海/红海/IP/资金占用 |
