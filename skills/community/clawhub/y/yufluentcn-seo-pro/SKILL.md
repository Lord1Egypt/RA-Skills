---
name: yufluentcn-seo-pro
description: >-
  跨境电商 SEO 关键词研究 — 亚马逊关键词+Backend、COSMO/Rufus 语义场景、Shopify 站内+Meta、TikTok 搜索+
话题标签，经 Yufluent 云端 Harness 输出结构化投放建议。Cross-border ecommerce
keyword research & SEO placement reports for Amazon (search stack/backend/semantic), Shopify
(on-page+meta) & TikTok Shop (search+hashtags). Use for 关键词研究、SEO、Amazon 搜索、
COSMO、Rufus、search terms、长尾词、Backend Keywords、Meta title、TikTok 话题标签.
version: 1.2.0
author: 元畅 · Yufluent
metadata:
  category: ecommerce
  tags: [seo, keywords, amazon, cosmo, rufus, shopify, tiktok, listing, yufluent, b2b]
  billing: yufluent
  languages: [zh, en, es, de, fr, ja]
  homepage: https://claw.changzhiai.com
  license: MIT
  openclaw: '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY","install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
---

# SEO 关键词研究与投放建议

跨境电商 **Amazon / Shopify / TikTok Shop** 关键词扩展与字段投放建议。**ClawHub / OpenClaw 云端模式** — Harness 在 Yufluent 服务端执行，输出结构化 **JSON 报告**；本机只需 `TOKENAPI_KEY`（`tk-*`）与 `requests`。

本技能 **不**连接 Seller Central、不拉取实时搜索量/排名 API；报告基于 Harness 平台规则 + 你提供的种子词/竞品词，由云端业务模型生成，**须人工对照后台数据复核后再上架**。

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
| **OpenClaw 对话** | Yufluent `/v1/chat/completions`（同一 tk-*） | 理解意图、收集种子词/竞品词、调 `run.py`、解读 JSON |
| **SEO 正式输出** | `POST /v1/skills/seo-pro/run`（同一 tk-*） | Harness `seo_keywords` → 关键词 JSON 报告 |

**Agent 硬性规则：**

1. **禁止**用对话模型自行编造完整关键词矩阵（含 priority / placement / reason 的 JSON）。
2. **必须**通过 `python scripts/run.py ...`（或 `POST /v1/skills/seo-pro/run`）获取输出。
3. 对话模型负责：按下方「关键词策略」补全输入、解释报告、建议下一步（如转 `yufluentcn-ecommerce-listing`）。
4. 只需 `TOKENAPI_KEY`，**不要**要求用户另配厂商 LLM Key。

---

## 方法论总览（TokenApi SEO 框架）

跨境 Listing SEO 的目标不是「堆词」，而是 **让买家搜索意图与产品事实在平台允许的位置对齐**。

```text
买家意图 → 词库分层（核心/长尾/防御）→ 平台投放位 → Listing 正文 → 人工审核上架
```

### 1. 搜索意图分层

在收集种子词前，先判断用户处于哪类意图（可混合）：

| 意图类型 | 买家状态 | 词的特征 | 典型用途 |
|----------|----------|----------|----------|
| **交易型** | 准备购买 | 品类+属性+规格（如 `wireless earbuds noise cancelling`） | 标题、核心 bullet |
| **商业型** | 对比选购 | `best` / `for running` / `vs` / 场景词 | 五点、描述前段 |
| **信息型** | 了解品类 | `how to` / `what is` | 描述、A+、博客（Shopify） |

**原则**：标题与首屏 bullet 优先 **交易型 + 高相关核心词**；长尾与场景词进 bullets / 描述 / Backend（Amazon）或集合标签（Shopify）。

### 2. 词库三层结构（输出应对齐）

Harness 报告将词分为（命名因平台略有差异）：

| 层级 | 定义 | 数量预期 | 优先级倾向 |
|------|------|----------|------------|
| **核心词 (primary)** | 与 SKU 直接对应、搜索量概念上的「大类词」 | 5–10 | 高 → 标题 |
| **长尾词 (long_tail)** | 属性/场景/人群/痛点组合 | 10–20 | 中 → bullets / 描述 |
| **防御/规避 (avoid)** | 低相关、违规、易误导、竞品品牌 | 若干 | 标注勿用 |

Amazon 另输出 **`backend_keywords`**（仅 Search Terms 字段，不重复标题已用词）。

### 3. 相关性三角（扩词前自检）

每个候选词需同时满足：

1. **产品事实**：材质、功能、尺寸、适用场景与实物一致。  
2. **搜索意图**：买家搜这个词时，你的详情页能回答他的问题。  
3. **平台规则**：不侵权、不夸大、不用未授权品牌/医疗宣称（见各平台 policy）。

任一不满足 → 进入 `avoid_keywords` 或降优先级。

### 4. 平台差异（方法论，非实时数据）

| 平台 | 排序/曝光逻辑（简化） | 本技能报告侧重 |
|------|----------------------|----------------|
| **Amazon** | 关键词排名（A9/A10 式信号）+ COSMO 语义 + Rufus 发现；标题权重高 | 标题 / 五点 / Backend + 场景意图自然语言 |
| **Shopify** | 谷歌自然搜索 + 站内结构；Meta 影响 CTR | `meta_title` / `meta_description` + 集合标签 + 博客选题 |
| **TikTok Shop** | 站内搜索 + 内容场域；标签与短视频 Hook | `search_keywords` + `hashtag` + `video_hook_keywords` |

同一产品在三平台 **词可翻译/本地化，但不可机械照搬**（例如 Amazon Backend 字节限制与 TikTok 话题习惯不同）。

### 5. 推荐工作流（与 Listing 协同）

```text
1) yufluentcn-seo-pro  →  JSON 关键词报告（含 semantic_intents / buyer_questions）
2) 人工删改 / 对照广告&搜索词报告（可选）
3) yufluentcn-ecommerce-listing  →  将高优先级词 + suggested_copy / answer_hint 写入标题/五点/描述
4) 上架后 2–4 周  →  用搜索词/业务报告迭代第二轮 seo-pro
```

**先 SEO 后 Listing** 可避免正文写完后反复改标题；若用户只要 Listing，仍建议至少提供 3–5 个种子词。

---

## 关键词策略说明（Agent 收集输入用）

### 种子关键词 (`--keywords` / `seed_keywords`) 怎么写

| 做法 | 说明 |
|------|------|
| **最少 3 个、建议 5–12 个** | 逗号分隔；中英文混排时注明目标 `lang` |
| **结构** | 1 个品类词 + 2–3 个核心属性 + 1–2 个场景/人群词 |
| **示例（耳机）** | `无线耳机, 降噪, 蓝牙5.3, 运动, 长续航` |
| **避免** | 仅品牌名、仅形容词（`好用的`）、与 SKU 无关的大词 |

种子词 = 扩词 **锚点**；过宽则报告发散，过窄则长尾不足。

### 竞品/类目参考词 (`--competitor-keywords`)

用于模拟「类目头部 Listing 在覆盖什么意图」，**不是**让你抄袭竞品品牌名。

| 来源 | 示例写法 |
|------|----------|
| 竞品标题拆词 | `running shoes women cushioned, marathon` |
| 类目畅销榜前 10 标题高频词 | 粘贴逗号分隔 |
| 广告搜索词报告（手动） | 高转化 query 摘录 |

未提供时 Harness 填「（未提供）」—— 报告仍可用，但长尾与差异化会偏弱。**有竞品词时务必传入。**

### 目标市场 (`--market` / `target_market`)

影响 **语言、拼写、场景与合规**（如美国/英国拼写、电压、认证表述）：

- 示例：`美国`、`UK`、`东南亚-越南`、`德语区`  
- 与 `--lang` 配合：`lang=de` + `market=德国` 优于仅设 lang。

### 优先级（报告内 高/中/低）判定逻辑

Harness 按下列 **启发式** 标注（非实时搜索量）：

| 优先级 | 条件（同时参考） | 建议 placement |
|--------|------------------|----------------|
| **高** | 核心品类/主属性；交易意图强；适合标题前 80 字符 | `title` |
| **中** | 长尾、场景、兼容词；可进 bullet 或描述 | `bullets` / `description` |
| **低** | 边缘场景、复现词、仅 Backend 有价值的变体 | `backend`（Amazon）或集合标签 |

Agent 向用户解释报告时，应说明：**「高」= 建议优先人工验证后写入标题**，仍需结合卖家后台搜索词报告做最终取舍。

### 字段投放策略（Amazon：关键词 + 语义意图）

| 字段 | 策略要点 |
|------|----------|
| **标题** | 核心高优先级词靠前；不堆砌重复词；遵守类目字数；含 1 个清晰场景或人群 |
| **五点** | 每点 1–2 个长尾；覆盖场景/人群/差异化；完整句子便于 COSMO/Rufus 理解 |
| **描述** | 补充同义词与场景叙事；回答买家可能追问的参数/兼容问题 |
| **Backend Search Terms** | 标题/五点 **未出现** 的拼写变体、外语、适用型号；**不**重复、不加标点堆砌 |

### 字段投放策略（Shopify）

| 字段 | 策略要点 |
|------|----------|
| **Title / H1** | 与 `meta_title` 语义一致，控制约 60 字符内可读 |
| **Meta description** | 含 1–2 个核心词 + 明确 CTA；约 150–160 字符 |
| **Collection tags** | 用于集合页与筛选，偏类目与场景 |
| **Blog ideas** | 承接信息型意图，导流产品集合页 |

### 字段投放策略（TikTok Shop）

| 字段 | 策略要点 |
|------|----------|
| **Search keywords** | 商品卡与搜索场景；偏口语、短词组 |
| **Hashtags** | 3–8 个：品类 + 场景 + 活动（无空格） |
| **Video hook keywords** | 短视频前 3 秒口播/字幕用词，与主图一致 |

### `avoid_keywords` 常见类别

- 竞品注册商标、未授权品牌词  
- 平台禁售/受限宣称（疗效、绝对化「第一/best」需有依据）  
- 与 SKU 无关的泛流量词（易拉低转化）  
- 已在标题重复多次的词（Amazon Backend 不必再填）

---

## Instructions（Agent 工作流）

1. **确认平台**：`amazon` | `shopify` | `tiktok`。  
2. **按「关键词策略」收集**：  
   - `product`（必填）  
   - `keywords` / 种子词（必填，逗号分隔）  
   - `competitor_keywords`（强烈建议）  
   - `market`（跨境时建议）  
   - `use_case` / 目标人群或场景（Amazon 强烈建议，如 `通勤降噪, 运动跑步`）  
   - `lang`：`zh|en|es|de|fr|ja`  
3. **调用（必须 — 云端）**：  
   ```bash
   python scripts/run.py \
     --product "主动降噪蓝牙耳机" \
     --keywords "无线耳机,降噪,蓝牙5.3,运动,通勤" \
     --competitor-keywords "anc earbuds, wireless earphones sports" \
     --use-case "通勤降噪, 运动跑步" \
     --platform amazon \
     --market "美国" \
     --lang zh \
     -o seo-report.json
   ```  
4. **交付**：将 JSON 保存或格式化展示；提醒用户对照 **Brand Analytics / 广告搜索词 / Shopify Search** 做二次筛选。  
5. **下一步**：_offer `yufluentcn-ecommerce-listing`，把 `primary_keywords` 中高优先级词及 `semantic_intents[].suggested_copy`、`buyer_questions[].answer_hint` 写入 Listing 上下文。  
6. **计费**：402 余额不足；401 密钥无效。

---

## 输出结构（JSON）

平台不同，字段略有差异；均为 **合法 JSON**（无 markdown 代码块包裹）。

### Amazon

- `primary_keywords[]`：`keyword`, `priority`, `placement`, `reason`  
- `long_tail_keywords[]`  
- `semantic_intents[]`：`intent`, `suggested_copy`, `placement`, `priority`（COSMO 场景句）  
- `buyer_questions[]`：`question`, `answer_hint`, `placement`（Rufus 问答覆盖）  
- `backend_keywords[]`  
- `avoid_keywords[]`  
- `summary`

> Amazon 默认走 Harness 模板 **amazon-seo-v2**（含语义字段）；显式 `template_version: v1` 可回退旧版词表模板。

Harness 会对 SEO JSON 输出 **质量分（0–10）** 并写入 run 记录，维度含词库深度、种子词覆盖、Backend 去重、COSMO/Rufus 语义覆盖等。

### Shopify

- `primary_keywords[]`  
- `collection_tags[]`  
- `meta_title_suggestion`, `meta_description_suggestion`  
- `blog_content_ideas[]`  
- `summary`

### TikTok Shop

- `search_keywords[]`  
- `hashtag_suggestions[]`  
- `video_hook_keywords[]`  
- `summary`

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
| 将关键词写入完整 Listing | `yufluentcn-ecommerce-listing` |
| 评论中的痛点转长尾词 | `yufluentcn-review-intel` → 再 `seo-pro` |
| 竞品标题拆词 | `yufluentcn-comp-track` → 提取词再 `seo-pro` |
| 落地页广告用语一致 | `yufluentcn-ad-optimize`（与 SEO 词分开迭代） |

---

## 触发词

- "关键词研究" / "SEO 优化"  
- "Amazon 搜索" / "COSMO" / "Rufus" / "Backend Search Terms"  
- "Shopify meta title"  
- "TikTok 话题标签"  
- "长尾词扩展"  
- "标题埋词怎么布局"

---

## Examples

**Amazon — 3C 配件**

```bash
python scripts/run.py \
  --product "USB-C 多口充电坞 65W" \
  --keywords "充电坞,USB-C,氮化镓,多设备,旅行" \
  --competitor-keywords "gan charger, usb c charging station" \
  --platform amazon \
  --market "美国" \
  --lang en \
  -o amazon-seo.json
```

**Shopify — 家居**

```bash
python scripts/run.py \
  --product "北欧实木餐椅" \
  --keywords "餐椅,实木,北欧,餐厅家具" \
  --platform shopify \
  --market "德国" \
  --lang de
```

**TikTok Shop — 美妆**

```bash
python scripts/run.py \
  --product "维生素C精华液" \
  --keywords "精华,维C,提亮,护肤" \
  --competitor-keywords "vitamin c serum, brightening" \
  --platform tiktok \
  --lang zh
```

---

## 合规声明

- 报告仅供参考，不构成平台排名或流量承诺。  
- 禁止建议侵权、虚假宣传或未授权品牌词。  
- 上架前须符合目标市场广告与品类合规要求。  

更完整的卖家操作说明见 [docs/技能-SEO关键词客户指南.md](../../docs/技能-SEO关键词客户指南.md)。

---

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1.0 | 2026-06-14 | SKILL.md added quickstart registration guide; 401/402 error messages now in Chinese with register links |
| v0.3.0 | 2026-05-28 | 补充方法论、关键词策略、平台投放与工作流 |
| v0.2.0 | — | Harness `seo_keywords` 三平台 JSON 报告 |
| v0.1.0 | — | 初始云端薄客户端 |
