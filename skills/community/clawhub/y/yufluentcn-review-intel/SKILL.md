---
name: yufluentcn-review-intel
description: >-
  跨境电商评论分析雷达 — 买家评论情感聚类、差评归因、改进建议与回复模板，
经 Yufluent 云端 Harness 输出结构化 JSON 洞察。Cross-border review intelligence:
sentiment themes, complaints, praises & action items via cloud Harness.
Use for 评论分析、差评聚类、VOC、review insights、改进建议、回复模板.
version: 1.1.2
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [reviews, sentiment, voc, amazon, shopify, tiktok, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# 评论分析与改进洞察

对 **Amazon / Shopify / TikTok Shop** 买家评论做情感归纳、主题聚类、改进建议与回复话术草稿。**ClawHub / OpenClaw 云端模式** — Harness `review_analyze` 输出结构化 **JSON**；本机只需 `TOKENAPI_KEY`（`tk-*`）。

本技能 **不**抓取平台评论 API、不自动回复买家；须使用你已合法获得的评论文本。

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
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 整理评论格式、调 `run.py`、解读 JSON |
| **分析正式输出** | `POST /v1/skills/review-intel/run`（同一 tk-*） | Harness → 洞察 JSON |

**Agent 硬性规则：**

1. **禁止**用对话模型自行撰写完整评论分析报告（themes / action_items 等 JSON）。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/review-intel/run`）获取输出。
3. 对话模型负责：把用户粘贴内容 **规范成标准分隔格式**、缺参时追问、解释结果。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

---

## 评论输入格式（必读）

Harness 将 `--reviews` / API `reviews` 字段视为 **一条或多条买家评论正文**。多条评论之间用 **独立一行的分隔符 `---`** 分开（上下各空一行推荐）。

### 标准格式（推荐）

```text
[可选元数据行]
评论正文第 1 条，可多行书写。

---
[可选元数据行]
评论正文第 2 条。

---
评论正文第 3 条。
```

**规则：**

| 规则 | 说明 |
|------|------|
| **分隔符** | 仅使用单独一行的 `---`（前后换行）；不要用 `***`、`===` 或仅逗号分隔 |
| **单条评论** | 可不写分隔符，整段视为 1 条 |
| **条数建议** | 至少 **3 条** 才有聚类意义；推荐 **10–50 条**；API 单次总长 ≤ **8000 字符** |
| **语言** | 与 `--lang` 一致；可混多种语言但分析质量下降 |
| **勿含** | 买家姓名、电话、地址等 PII；竞品商号诽谤（可打码） |
| **勿用** | 评论正文中间出现单独一行 `---`（会与分隔符冲突） |

### 可选元数据行（建议 Agent 帮用户整理）

每条评论 **第一行** 可写结构化前缀，正文从下一行开始：

```text
[2024-06-01] [★★☆☆☆ 2/5] [verified]
电池续航太差，用两天就没电了。
```

| 前缀片段 | 含义 |
|----------|------|
| `[YYYY-MM-DD]` | 评论日期（可选） |
| `[★★★★☆ 4/5]` 或 `[4/5]` | 星级（可选） |
| `[verified]` | 已验证购买（可选） |

元数据 **不强制**；无星级时 Harness 仍可从正文判断情感。

### CLI：内联 vs 文件

| 方式 | 用法 |
|------|------|
| **内联** | `--reviews "第一条\n\n---\n\n第二条"`（PowerShell 建议用文件） |
| **文件** | `--reviews reviews.txt` — 若路径存在则 **整文件 UTF-8 读取** |

```powershell
# 推荐：先写入 reviews.txt，再调用
python scripts/run.py --reviews reviews.txt --product "蓝牙耳机" --platform amazon --lang zh
```

### HTTP API

```json
{
  "reviews": "第一条评论\n\n---\n\n第二条评论",
  "product": "蓝牙耳机",
  "platform": "amazon",
  "lang": "zh"
}
```

- 字段名：`reviews`（必填字符串）；Harness 内部亦接受 `reviews_text` / `text`（集成用）。
- `product`：强烈建议填写，便于主题与 SKU 对齐。
- 不支持单次请求上传多文件；请合并为一个字符串。

### 从平台导出后如何粘贴

**Amazon（卖家后台 / 第三方导出）**

- 每行一条时：Agent 应在每条之间插入 `\n---\n` 再调用。
- CSV：取「Review Text」列，忽略 Order ID 等 PII 列。

**Shopify / 应用评论插件**

- 导出 CSV 的 `body` / `content` 列，同样用 `---` 拼接。

**TikTok Shop**

- 短评可多条 `---` 分隔；带图评论仅粘贴文字部分。

### 反例（会导致条数错误或分析偏差）

```text
❌ 用逗号拼接：好评，好评，差评
❌ 用编号但不分隔：1. xxx 2. yyy  （应改为 --- 分隔）
❌ 分隔符写进正文：这家店---太差了  （换措辞或拆成两条）
❌ 只给星级没有文字：★★★★★  （至少补一句摘要）
```

---

## 方法论简述

1. **VOC 聚合**：从多条评论提炼 recurring themes，而非逐条摘要。  
2. **情感 + 主题**：`overall_sentiment` 与 `themes[]` 分开看；混合评分常见。  
3. **可执行改进**：`action_items` 按 产品 / 物流 / 描述 / 客服 归类，带优先级。  
4. **回复模板**：`reply_templates` 为草稿，**须人工审核**后发送，遵守平台沟通政策。  
5. **后续联动**：痛点短语可喂给 `yufluentcn-seo-pro`（长尾词）或 `yufluentcn-ecommerce-listing`（卖点优化）。

---

## Instructions（Agent 工作流）

1. **确认平台与语言**：`platform`：`amazon` | `shopify` | `tiktok`；`lang`：`zh|en|es|de|fr|ja`。  
2. **整理评论为标准 `---` 格式**（见上）；不足 3 条时提示用户补充或说明「样本较少，结论仅供参考」。  
3. **调用（必须 — 云端）**：  
   ```bash
   python scripts/run.py \
     --reviews reviews.txt \
     --product "主动降噪蓝牙耳机" \
     --platform amazon \
     --lang zh \
     -o review-insights.json
   ```  
4. **解读 JSON**：向用户展示 `top_complaints`、`action_items`（高优先级）、可选 `reply_templates`。  
5. **计费**：402 余额不足；401 密钥无效。

---

## 输出结构（JSON）

| 字段 | 说明 |
|------|------|
| `overall_sentiment` | `positive` \| `mixed` \| `negative` |
| `sentiment_score` | 数值（模型估计，非平台官方） |
| `themes[]` | `theme`, `count`, `sentiment`, `examples[]` |
| `top_complaints` | 主要抱怨点列表 |
| `top_praises` | 主要好评点列表 |
| `action_items[]` | `priority`, `area`, `suggestion` |
| `reply_templates[]` | `for_theme`, `tone`, `text`（草稿） |

---

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TOKENAPI_KEY` | 是 | `tk-*` |
| `TOKENAPI_BASE_URL` | 否 | 默认 `http://localhost:8080/v1` |

---

## 与其他技能联动

| 需求 | 技能 |
|------|------|
| 痛点转关键词 | `yufluentcn-seo-pro` |
| 改 Listing 卖点/描述 | `yufluentcn-ecommerce-listing` |
| 差评回复（买家消息） | `yufluentcn-chat-assist` |
| 对比竞品差评差异 | 先 `yufluentcn-comp-track`，再本技能 |

---

## 触发词

- "分析这些评论" / "差评原因"  
- "评论里大家抱怨什么"  
- "VOC 洞察" / "改进建议"  
- "帮我写回复差评的模板"

---

## Examples

**文件输入（推荐）**

`reviews.txt`：

```text
[★★★★☆ 4/5]
音质不错，但佩戴久了耳朵疼。

---
[★★☆☆☆ 2/5]
降噪效果不如宣传，地铁里还是能听见。

---
[★★★★★ 5/5]
续航超预期，一周充一次够用。
```

```bash
python scripts/run.py --reviews reviews.txt --product "ANC蓝牙耳机" --platform amazon --lang zh -o out.json
```

**API 内联两条**

```bash
python scripts/run.py --reviews "物流太慢\n\n---\n\n做工很好" --product "手机壳" --platform shopify --lang zh
```

---

## 合规

- 仅分析你有权使用的评论数据。  
- 回复模板不得承诺平台外赔偿、不得泄露其他买家信息。  
- 分析结果供内部改进，不构成法律或质量鉴定。  

卖家操作说明见 [docs/技能-评论分析客户指南.md](../../docs/技能-评论分析客户指南.md)。

---

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v0.3.0 | 2026-05-28 | 明确评论输入格式（`---` 分隔）、元数据行、CLI/文件/API |
| v0.2.0 | — | Harness `review_analyze` JSON 洞察 |
| v0.1.0 | — | 初始云端薄客户端 |
