---
name: walter-info
description: 获取全球五大洲主要城市天气预报与跨境电商热点资讯，并生成格式化Markdown文档和JSON数据文件。当用户需要查询天气、跨境电商资讯，或要求生成报告时触发。
---

# walter-info Skill

跨境电商 + 天气的双模块 skill，支持一键运行和单独运行。

---

## 目录结构

```
walter-info/
├── SKILL.md
├── config.json          # 本地配置（key 等敏感信息，不上传 clawhub）
├── config.example.json  # clawhub 上传的示例配置（无真实 key）
├── scripts/
│   ├── run.py              # 统一入口（完整流程）
│   ├── fetch_news.py        # 资讯核心脚本
│   └── fetch_weather.py    # 天气脚本
└── output/
    ├── news_report_YYYYMMDD.md   # 最终报告（含 LLM 摘要）
    ├── news_report_YYYYMMDD.json # JSON 数据
    ├── ennews_YYYYMMDD.md       # ennews 原始数据
    ├── cifnews_YYYYMMDD.md      # cifnews 原始数据
    ├── weather_report_YYYYMMDD.md
    └── weather_report_YYYYMMDD.json
```

---

## 快速开始

### 方式一：一键完整运行（推荐）

```bash
python scripts/run.py
```

自动完成：
1. **Step 1**：抓取 ennews + cifnews → 权重排序 → Top 10 → 初始 JSON
2. **Step 2**：AI Agent 生成 cifnews 摘要（读取 `llm_input_*.json` → 生成摘要 → 更新 JSON）
3. **Step 3**：输出 ennews / cifnews 分源文件

### 方式二：仅 Python 抓取（跳过 LLM）

```bash
python scripts/run.py --python-only
```

### 方式三：单独运行各模块

```bash
python scripts/fetch_news.py           # 仅抓取资讯
python scripts/fetch_weather.py       # 仅抓取天气
```

---

## 资讯模块详解

### 数据来源

| 来源 | 说明 |
|------|------|
| **ennews.com** | 工作日更新，抓取当天内容 |
| **cifnews.com** | JS 动态渲染首页，但 HTML 中含 data-fetch-id/data-fetch-title 属性，字节级解析可提取标题和 URL |

### 完整流程

```
fetch_news.py
  ↓
1. 抓取 ennews + cifnews（原始数据）
2. 计算 Impact Score（业务相关性 + 影响程度 + 品类加成 + 时间衰减）
3. Greedy 去重（≥2 核心关键词重叠 = 同一事件）
4. 取 Top 10 → 初始 JSON（cifnews 摘要为正文前两段）
  ↓
run.py 写入 llm_input_*.json（cifnews Top 10 全文）
  ↓
AI Agent 读取 → 为每篇 cifnews 生成 LLM 摘要（50 字以内）
  ↓
update_summaries.py 更新 JSON + Markdown
  ↓
最终文件：news_report_*.md（含 LLM 摘要）
```

### 权重体系（Impact Score 0-100）

| 维度 | 最高分 | 说明 |
|------|--------|------|
| 业务相关性 | 30 | Amazon FBA（直接词：FBA/亚马逊FBA/亚马逊物流；间接词：亚马逊）= 30；TikTok Shop（直接词：TikTok Shop；间接词：TikTok）= 18；其他平台 = 12；泛跨境 = 5 |
| 影响程度 | 30 | 高影响词（tariff/ban/fee/penalty等）= 30；中等影响词（expansion/investment/GMV等）= 15 |
| 品类加成 | 15 | 服饰/美妆/时尚品类 +15 |
| 时间衰减 | 15 | 24h 内 = 15；48h = 10；72h = 5 |
| 来源权威性 | 10 | Official = 25；Tier1 = 20；Tier2 = 12；Tier3 = 5；Tier4 = 3；unrated = 0 |

> ennews / cifnews 暂无权威评级，默认 +0

### 关键词分层体系

**Amazon FBA 确认（+30）**：
- 直接词（命中即确认）：`FBA`、`amazon fba`、`亚马逊FBA`、`亚马逊物流`、`fba头程`、`fba仓储`、`fba费用`、`fba标签`、`亚马逊卖家`、`亚马逊店铺`
- 间接词（命中即确认）：`亚马逊`

**TikTok Shop 确认（+18）**：
- 直接词：`TikTok Shop`、`tiktok shop`
- 间接词：`tiktok`、`抖音电商`

**其他平台（+12）**：`temu`、`shein`、`速卖通`、`美客多` 等

### 摘要生成策略

| 来源 | 进入 Top 10 | 未进入 Top 10 |
|------|------------|---------------|
| ennews | 正文前两段（已含摘要） | 不输出（不在 Top 10） |
| cifnews | **LLM 全文摘要**（AI Agent 生成） | 正文前两段 |

---

## 配置说明

clawhub 下载后，参考 `config.example.json` 创建本地 `config.json`：

```json
{
  "cities": {
    "亚洲": [["上海", "Shanghai"], ["东京", "Tokyo"], ...]
  }
}
```

`news_api_key`（GNews）目前脚本中未使用，可留空或填入真实 key。

---

## 天气模块

见 `fetch_weather.py`，使用 wttr.in API，无需 key。

---

## 输出文件说明

| 文件 | 说明 |
|------|------|
| `news_report_*.md` | 最终报告，含 LLM 摘要的 Top 10 |
| `news_report_*.json` | 结构化 JSON，含所有元数据 |
| `ennews_*.md` | ennews 原始数据（10 条，便于核对） |
| `cifnews_*.md` | cifnews 原始数据（4 条，含正文前两段） |
