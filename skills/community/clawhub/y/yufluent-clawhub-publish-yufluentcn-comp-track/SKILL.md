---
name: yufluentcn-comp-track
description: >-
  竞品 Listing 快照对比分析，通过粘贴竞品文案进行多维度对标（标题/五点/描述/关键词），
  输出差异化建议与机会点。经 Yufluent 云端 Harness 执行。Use for 竞品分析、
  competitor snapshot、对标、竞品对比.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [competitor, analysis, amazon, shopify, tiktok, benchmarking, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 竞品追踪

单条竞品 Listing 快照对比 — 将你的产品与竞品文案进行多维度对标，输出差异化建议。**ClawHub / OpenClaw 用户使用云端模式** — Harness 在 Yufluent 服务端执行，本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

本技能基于你**手动粘贴**的竞品文案进行分析，**不**抓取平台商品页。

## 快速开始（3 步，60 秒）

1. **注册获取 API 密钥** → https://claw.changzhiai.com/login （新用户即送体验积分，无需绑卡）
2. **设置环境变量**：export TOKENAPI_KEY=*** 或写入 .env 文件
3. **运行**：参照下方 Examples 示例执行 python scripts/run.py ...

> 还没注册？前往 https://claw.changzhiai.com/login 免费获取密钥。

## OpenClaw 与 Yufluent（必读）

OpenClaw 对话与技能调用**共用同一 `tk-*`**。接入见 https://claw.changzhiai.com/app/openclaw。

| 层 | 走哪里 | 干什么 |
|----|--------|--------|
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 收集竞品文案、调 `run.py`、解读对比结果 |
| **对比正式输出** | `POST /v1/skills/comp-track/run`（同一 tk-*） | Harness → 竞品对比报告 |

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整竞品对比报告。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/comp-track/run`）获取输出。
3. 对话模型仅用于：帮助整理竞品文案、确认平台与语言、解释对比结果、建议下一步。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

## Instructions（Agent 工作流）

1. **确认平台**：`amazon` | `shopify` | `tiktok`；语言 `zh|en|...`。
2. **收集输入**：
   - `--our-product`（必填）：我方产品名
   - `--competitor`（必填）：竞品文案或 `.txt` 文件路径
   - `--our-listing`（可选）：我方 Listing 文案或文件路径
3. **调用（必须 — 云端）**：
   ```bash
   python scripts/run.py \
     --our-product "无线蓝牙耳机" \
     --competitor "竞品标题: ..." \
     --platform amazon \
     --lang zh
   ```
   - 支持 `--competitor` 传入 `.txt` 文件路径
   - 可选 `--our-listing` 传入我方 Listing 做双方对比
4. **交付**：将输出报告交给用户，建议下一步联动其他技能（如 `yufluentcn-ecommerce-listing`）。
5. **计费**：402 余额不足；401 密钥无效。

## 输出说明

Harness 从以下维度对比输出：

| 维度 | 说明 |
|------|------|
| **标题** | 关键词布局、长度、卖点排序 |
| **五点/Bullets** | 覆盖场景、差异化亮点 |
| **描述** | 叙事结构、SEO 关键词密度 |
| **差异化建议** | 我方可抓住的机会点与改进方向 |

## 与其他技能联动

| 需求 | 技能 |
|------|------|
| 竞品标题关键词 → Listing 优化 | `yufluentcn-ecommerce-listing` |
| 竞品关键词 → SEO 补词 | `yufluentcn-seo-pro` |
| 多条竞品 CSV 批量对比 | `yufluentcn-comp-scrape` |
| 竞品差评 → 我方卖点反击 | `yufluentcn-review-intel` |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取 |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

## 触发词

- "竞品分析"
- "跟竞品对比一下"
- "对标这个链接"
- "竞品标题分析"
- "我的 Listing 和竞品比怎么样"
- "competitor analysis"

## Examples

**Amazon — 单条对标**

```bash
python scripts/run.py \
  --our-product "便携式咖啡机" \
  --competitor "标题: Mini Espresso Maker Portable... 五点: ..." \
  --platform amazon \
  --lang zh
```

**Shopify — 带我方文案对比**

```bash
python scripts/run.py \
  --our-product "Nordic Wooden Dining Chair" \
  --competitor competitor.txt \
  --our-listing our-listing.txt \
  --platform shopify \
  --lang en
```

**TikTok — 竞品文案**

```bash
python scripts/run.py \
  --our-product "美妆精华液" \
  --competitor "商品标题: ... 描述: ..." \
  --platform tiktok \
  --lang zh
```

## 合规声明

- 仅分析用户手动粘贴的竞品文案，不抓取平台数据
- 对比结论仅供参考，不构成平台排名或流量承诺
- 不引用竞品商标做虚假关联

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v1.0.0 | 2026-06-13 | 规范 SKILL.md：补充 Agent 规则、Instructions、触发词、示例、版本记录 |
| v0.1.0 | — | 初始竞品快照对比技能 |
