---
name: twitter-ai-kol-fetcher
description: "抓取 Twitter AI 领域 KOL 最新动态、识别热门话题、生成专业内参。触发条件：\"抓取 Twitter\"、\"AI 领域最新动态\"、\"每天 AI 动态\"、\"写内参\"、\"AI 内参\"。"
---

# Twitter AI KOL Fetcher

抓取 Twitter AI 领域动态，识别热门话题，自动生成专业内参报告。

**内参风格参考：中关村两院《美国对中国"关键软件"出口管制的影响研判与对策建议》**

---

## 目录结构

```
twitter-ai-kol-fetcher/
├── config.json                  # API 配置文件（用户填 key）
├── SKILL.md                     # 本文件
├── references/
│   ├── kol_list.json            # KOL 账号列表（82个）
│   ├── llm_prompts.md          # LLM 提示词
│   └── internal_report_template.md  # 内参模板
└── scripts/
    ├── 01_fetch_kols.py        # 抓取 KOL 推文
    ├── 02_filter_and_score.py  # 过滤、评分、聚类
    ├── 03_generate_report.py   # 机会判定 + 报告生成
    └── main.py                 # 主流程脚本
```

---

## Twitter API

服务商：https://twitterapi.io

| 资源 | 价格 |
|------|------|
| Tweets | $0.15 / 1K 条 |
| Profiles | $0.18 / 1K 个 |
| Followers | $0.15 / 1K 个 |

计费：15 Credits/条推文，1 USD = 100,000 Credits

---

## 工作流（优化版）

```
[Step 1] 抓取数据
    ↓
[Step 2] 规则过滤 + 热度评分
    ↓
[Step 3] 话题聚类（新增！基于关键词相似度）
    ↓
[Step 4] LLM 机会判定（Lightning 模型，便宜）
    ↓
[Step 5] LLM 报告生成（M2.1 模型，强推理）
    ↓
[Step 6] 发送到飞书 → 删除临时文件
```

---

## 核心优化点

### 1. 模型分离（成本优化）

| 阶段 | 模型 | 理由 | 成本 |
|------|------|------|------|
| 数据抓取 | 82 KOL × 1条 | Tweets.io API | ~$0.012 |
| 机会判定 | **MiniMax-M2.5** | 逻辑判断 + 优先级排序 | ~$0.01 |
| 报告生成 | **Gemini 3.1 Pro** × 3 | 大上下文、强推理、文笔好 | ~$1.20 |
| **总计** | | | **~$1.22/天** |

### 2. 话题聚类（质量提升）

**问题**：原来的逻辑是"一条推文 = 一个话题"，但内参的价值在于**发现趋势和主题**。

**解决方案**：基于关键词相似度将相关推文聚类
- 3个KOL讨论"Claude 4发布" → 合并为一个主题
- 5个KOL聊"AI安全法案" → 这是重点话题

**效果**：
- 减少重复内容
- 话题更有代表性
- 报告更有深度

### 3. 扩大信源 + 减少单KOL抓取量

- **信源扩大**：从 34 个扩展到更多 KOL（AI公司、CEO、投资人、博主、研究员）
- **每KOL抓取量**：从 5 条减少到 1 条（最新）
- **效果**：覆盖更广，成本可控

### 4. 并行报告生成（速度优化）

- **原来**：串行生成 3 篇报告 → ~3分钟
- **现在**：并行生成 3 篇报告 → ~1分钟
- **效果**：速度翻倍，更快交付

### 5. 防漏抓机制（关键！）

| 问题 | 解决方案 |
|------|----------|
| 漏掉 VIP 用户 | **兜底机制**：sama/elonmusk 等发的强制纳入 |
| 漏掉突发事件 | **关键词兜底**：含 "launching" 等强制纳入 |
| 漏掉高互动 | **互动兜底**：点赞>5000 或 转发>500 强制纳入 |

### 4. 兜底规则

```
如果满足以下任一条件，强制纳入话题池：
1. VIP 用户（sama, elonmusk 等）发布的
2. 包含 "launching", "announcing", "new", "breaking" 等关键词
3. 点赞 > 5000 或 转发 > 500
```

### 4. KOL 列表（82个）

从 `references/kol_list.json` 加载，分类：

| 类型 | 数量 | 说明 |
|------|------|------|
| company | 28 | AI 公司官方（OpenAI, Anthropic, Google DeepMind 等） |
| influencer | 11 | 技术博主（swyx, fireship, heyBarsee 等） |
| ceo | 9 | CEO（Sam Altman, Elon Musk, Demis Hassabis 等） |
| researcher | 8 | 研究员（Yann LeCun, Ilya, Noam Brown 等） |
| vc | 5 | 投资机构（a16z, Sequoia, Greylock 等） |
| platform | 5 | 平台（GitHub, LangChain, Streamlit 等） |
| investor | 4 | 个人投资人 |
| 其他 | 12 | newsletter, analyst, framework 等 |

**总计：82 个 KOL**（覆盖 AI 公司、投资、产品、研究、媒体）

### 5. 过滤规则

- **AI 关键词过滤**：匹配 AI 相关内容
- **热度评分**：转发×2 + 点赞×1 + 浏览×0.001
- **内参触发词**：launch, release, funding, safety, policy...
- **话题聚类**：基于关键词相似度合并相关推文

### 6. LLM 参与点

1. **机会判定**（Lightning）：判断聚类后的话题是否值得写内参
2. **报告生成**（M2.1）：按模板生成 Markdown 报告

### 7. 报告结构优化

| 章节 | 内容 | 目的 |
|------|------|------|
| 核心要点 | 3条最核心发现 | 一句话摘要 |
| 事件还原 | 发生了什么、时间线 | 背景铺垫 |
| 战略意义分析 | 为什么重要、影响 | **核心部分** |
| 各方观点 | 支持/质疑/中立 | 呈现多视角 |
| 趋势判断 | 短/中/长期判断 | 明确战略预测 |
| 对策建议 | 跟踪关注、行动建议 | 可操作建议 |

---

## 使用方式

### 方式1：手动执行

```bash
# 设置 API Key
export OPENROUTER_API_KEY="your-key"

# 运行主流程
python3 scripts/main.py
```

### 方式2：定时任务

```
任务: 每日 AI 内参
- 时间: 工作日 9:00
- 输出: 发送到飞书 → 删除临时文件
```

---

## 关键文件说明

### references/kol_list.json
KOL 账号列表，JSON 格式，可动态扩展。

### references/llm_prompts.md
LLM 提示词模板，包含：
- 机会判定 Prompt
- 报告生成 Prompt
- 关键词配置

### references/internal_report_template.md
内参模板，对齐中关村两院风格。

### scripts/01_fetch_kols.py
抓取 KOL 推文，输出 JSON。

### scripts/02_filter_and_score.py
过滤和评分，输出热门话题。

### scripts/03_generate_report.py
调用 LLM 生成报告。

---

## 配置

### config.json

在项目根目录创建 `config.json`，填入 API Key：

```json
{
  "twitter_api_key": "your-twitter-api-key",
  "openrouter_api_key": "your-openrouter-api-key"
}
```

获取方式：
- **Twitter API**: https://twitterapi.io/dashboard
- **OpenRouter API**: https://openrouter.ai/settings

### 可配置参数

- KOL 列表：`references/kol_list.json`
- 关键词：`references/llm_prompts.md`
- 热度阈值：脚本中 `MIN_HOTNESS = 500`
- 报告数量：脚本中 `max_reports = 3`

---

## 输出流程（关键！）

```
生成内参 → Markdown 文本 → 发送到飞书 → 删除临时文件
```

**重要：不保存本地文件！**
