---
name: trump-daily-report
description: 每日特朗普动态追踪报告。采集Truth Social/Twitter及美国媒体(Bloomberg/CNBC/Reuters/WSJ/FT)信息，生成中英双语市场分析报告，支持早报(8:00)和晚报(16:00)双时段及收盘对照分析。
author: Trump Daily Report Skill
version: 1.2.1
summary:
  zh: |
    每日特朗普动态追踪报告（v1.1.6）。采集Truth Social/Twitter及美国媒体(Bloomberg/CNBC/Reuters/WSJ/FT)信息，生成中英双语市场分析报告。
    
    **核心功能**：Truth Social追踪、媒体监控、外汇/股市/商品分析、A股/港股预测、早报(8:00)+晚报(16:00)双时段
    
    **数据源**: Bloomberg, CNBC, Reuters, WSJ, FT, BBC News, Agent Reach (r.jina.ai)
    
    **v1.2.1 更新**：Agent Reach 零配置搜索已加入——当 Tavily 限额满时，使用 r.jina.ai 抓取 BBC/彭博等新闻，无需 API key。
  en: |
    Trump Daily Report (v1.1.6). Track Trump posts and US media, bilingual market analysis. Morning(8:00) + Evening(16:00) reports.
    
    **v1.2.0 Updates**
    - 中英文双语完整版：早报/晚报均生成CN+EN双版本
    - 英文报告先发，中文报告后发，便于一览+深度阅读
    - 报告差异化：早报侧重预测，晚报侧重复盘+深度持仓分析

**v1.1.2 Updates**
    - Added commodity data sources (gold/oil/natural gas)
    - Fixed 04/13 report file save path issue
    - Added prediction verification tracking
    
    **Core Features**
    - 🐦 Truth Social + Twitter post tracking
    - 📰 US major media real-time monitoring
    - 📊 FX/Stock/Commodity/Bond market analysis
    - 🌏 A-Share and HK-Share impact prediction
    - 🔮 Forward-looking market forecasting
    
    **数据源**: Bloomberg, CNBC, Reuters, WSJ, FT, Kitco, OilPrice, EIA
---

# 特朗普动态日报

## 概述

自动追踪特朗普前一日社交媒体发言及美国主流媒体相关报道，**与历史报告对比分析**市场趋势变化，生成具有预测性的**中英双语综合报告**。

## 核心功能

1. **双语报告生成** - 同步输出中文+英文版本
2. **报告历史记忆** - 自动存档，支持历史追溯
3. **趋势对比分析** - 与前期报告对比，识别变化
4. **情境变化追踪** - 标注市场情绪、政策走向变化
5. **前瞻性预测** - 基于趋势给出未来展望

## 信息源

### 特朗普社交媒体
- Truth Social（主要来源）
- Twitter/X：`realDonaldTrump`
- 检测时间范围：前一天0:00-24:00（北京时间）

### 美国主流媒体（按优先级）
1. **Bloomberg** - 金融市场分析
2. **CNBC** - 财经电视与市场反应
3. **Reuters** - 突发消息与政策跟踪
4. **Wall Street Journal** - 深度分析与评论
5. **Financial Times** - 国际金融市场视角
6. **New York Times** - 政治经济交叉分析
7. **CNN / Fox News** - 政治立场不同的视角

### 关键词监控
- `Trump`, `tariff`, `trade war`, `sanction`, `Fed`, `dollar`, `China`, `EU`, `Mexico`
- `executive order`, `policy`, `White House`, `congress`
- 市场相关词：`market`, `stock`, `rally`, `selloff`, `bond`, `yield`, `oil`, `gold`

### 大宗商品数据源（黄金/原油/天然气）
当报告涉及能源市场或避险情绪时，**必须**使用以下专用数据源获取黄金和原油价格：

| 品种 | 首选数据源 | 搜索关键词 |
|------|-----------|-----------|
| 黄金 | Kitco (kitco.com) | `gold price today` / `XAU USD` |
| 黄金 | Gold-Eagle (gold-eagle.com) | `gold rate` |
| 原油 | OilPrice.com | `brent crude price today` |
| 原油 | EIA (eia.gov) | `crude oil price` |
| 原油 | CNBC Commodities | `oil price` |
| 天然气 | Natural Gas Intelligence | `natural gas price` |
| 综合 | Bloomberg Commodities | `commodities markets` |

**商品数据搜索策略：**
1. 使用 `tavily_search(topic=finance)` 搜索黄金/原油价格
2. 使用 `web_fetch` 直接抓取 Kitco 或 OilPrice 当日价格
3. 在报告中标注格式：`黄金：$XXXX [Kitco, HH:MM]` 或 `布伦特原油：$XX.XX [OilPrice, HH:MM]`
4. **禁止**仅凭历史均值或推断填补价格数据

### 🆕 Agent Reach 零配置搜索（v1.3.0）
**当 Tavily 返回 432 错误（使用限额满）时，切换 Agent Reach：**

**BBC News 搜索（最可靠）：**
```bash
python -c "
import urllib.request
url = 'https://r.jina.ai/https://www.bbc.com/news/world/us_and_canada'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode('utf-8', errors='replace')
with open('memory/trump_draft.txt', 'w', encoding='utf-8') as f: f.write(data)
print('OK')
"
```

**抓取具体文章：**
```bash
python -c "
import urllib.request
url = 'https://r.jina.ai/https://www.bbc.com/news/articles/ARTICLE_ID'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode('utf-8', errors='replace')
fname = 'memory/' + url.split('/')[-1] + '.txt'
with open(fname, 'w', encoding='utf-8') as f: f.write(data)
print('OK')
"
```

**适用场景：**
- 新闻检索（BBC News、The Straits Times、新加坡联合早报等）
- 突发新闻追踪（Iran War、Trump Policy、Trade War 等）
- 市场评论文章抓取

**限制：**
- r.jina.ai 对部分媒体（WSJ、NYT、Reuters、AP）返回 451/403，需换其他源
- BBC News 和 Straits Times 可用，优先使用 BBC 获取美国政治新闻
- 编码问题：Windows PowerShell 打印可能报错，重要输出应写入文件

## 工作流程

### 步骤1：读取历史报告（记忆检索）

**先检查 `memory_path` 目录下是否有历史报告**

路径：由 `memory_path` 参数指定（默认 `./memory/trump-daily`）

如果存在历史报告，读取最近3-5份，识别：
- 核心议题的变化（从关税→伊朗→其他）
- 市场情绪变化（避险→冒险）
- 关键价格水平变化（黄金、原油、美元指数等）

### 步骤2：收集特朗普前一日社交内容

使用 `tavily_search`（topic=news）搜索：

```
Trump Truth Social [昨天日期]
Trump [昨天日期] social media
```

使用 `tavily_search`（topic=finance）搜索市场相关：

```
Trump tariff [昨天日期]
Trump Iran [昨天日期]
Trump market [昨天日期]
```

**【重要】同步获取大宗商品数据：**
在步骤2和步骤3之间，**必须**执行以下商品数据查询：

1. **黄金价格查询：**
   ```
   tavily_search(topic=finance, query="gold price XAU USD today")
   web_fetch(url="https://kitco.com") 提取当日黄金现货价格
   ```

2. **原油价格查询：**
   ```
   tavily_search(topic=finance, query="brent crude oil price today")
   web_fetch(url="https://oilprice.com") 提取当日原油价格
   ```

3. **天然气价格查询（如能源危机情境）：**
   ```
   tavily_search(topic=finance, query="natural gas price Europe today")
   ```

4. **美元指数查询：**
   ```
   tavily_search(topic=finance, query="US dollar index DXY today")
   ```

**数据标注要求：**
- 所有价格必须标注来源和时间，格式：`[来源, HH:MM]`
- 未能获取的数据标注`[未能获取]`，不得推断
- 商品数据在市场影响分析章节中与上期进行对比

### 步骤3：搜索主流媒体对特朗普的报道

使用 `tavily_search`（topic=news）：

```
Trump [昨天日期] market impact
Trump [昨天日期] Bloomberg
Trump [昨天日期] Reuters
```

使用 `tavily_extract` 深入抓取关键文章（最多3篇）。

### 步骤4：生成双语报告（对比分析）

**必须同时生成中文版和英文版两个版本**

---

## 中文报告模板

```
📊 特朗普动态日报
📅 [YYYY-MM-DD] | 报告序号：[N]
*数据来源：[来源列表] | 查询时间：[时间]*

━━━ 🔄 前期回顾（昨日报告摘要）━━━
• 核心议题：[上期主要话题]
• 市场情绪：[上期情绪判断]
• 关键价格水平：
  - 标普500：±X% [来源]
  - 布伦特原油：$XX [来源]
  - 黄金：$XXXX [来源]
  - 美元指数：XXX [来源]

━━━ 🐦 特朗普社交媒体动态 ━━━
📍 [时间] [平台]
[引用的发言内容]

📍 伊朗/关税/其他重要议题：
[简述]

━━━ 📰 主流媒体反应 ━━━
🔵 [媒体名称]：[标题]
   核心观点：1-2句摘要

━━━ 📉 市场影响分析 ━━━
| 品种 | 本期 | 上期 | 变化 |
|------|------|------|------|
| 标普500 | ±X.X% [来源] | ±X.X% [来源] | ↑/↓/→ |
| 纳斯达克 | ±X.X% [来源] | ±X.X% [来源] | ↑/↓/→ |
| 布伦特原油 | $XX [来源] | $XX [来源] | ↑/↓/→ |
| 黄金 | $X,XXX [来源] | $X,XXX [来源] | ↑/↓/→ |
| 美元指数 | XXX [来源] | XXX [来源] | ↑/↓/→ |

━━━ 🔀 情境变化分析 ━━━
【新变化】本期vs上期的主要变化：
1. [变化点1]
2. [变化点2]

【市场情绪切换】
  前期：[避险/中性/冒险]
  本期：[避险/中性/冒险]
  变化原因：[简述]

【议题演变】
  [如：从关税战转向中东局势] → [新方向]

━━━ 📈 前瞻预测（1-3日内展望）━━━
• 短期市场可能方向：[看涨/看跌/震荡]
• 主要风险点：
  - ⚠️ [风险1]
  - ⚠️ [风险2]
• 操作建议：[谨慎/积极/观望]
• 需重点关注的事件：[日期/事件]

━━━ 🇨🇳🇭🇰 A股与港股影响预测 ━━━
【A股影响】
• 开盘方向：[高开/低开/平开]
• 关键板块：
  - [受益板块]：[逻辑简述]
  - [受损板块]：[逻辑简述]
• 成交量判断：[放量/缩量] [来源]
• 重点关注：
  - [个股/板块异动]
  - [北向资金流向，如可获取]

【港股影响】
• 开盘方向：[高开/低开/平开]
• 恒生指数压力位/支撑位：[XXXXX / XXXXX]
• 港股特有板块：
  - [科技股]：[逻辑简述]
  - [中概股]：[逻辑简述]
• 南向资金：[净买入/净卖出] [来源]
• 汇率风险：[人民币升值/贬值对港股影响]

━━━ ⚠️ 风险提示 ━━━
[标注需要关注的风险点]
```

### 步骤5：保存报告到记忆文件

**⚠️ 重要：使用配置参数 `memory_path`**

- `memory_path` 由配置文件或 cron 任务参数传递（默认 `./memory/trump-daily`）
- 如果 `memory_path` 目录不存在，agent 应先创建该目录
- 禁止硬编码任何绝对路径

**必须执行三个保存操作：**

1. **中文完整报告存档**：
   - 路径：`{memory_path}/{YYYY-MM-DD}_CN.md`
   - 内容：中文版完整报告

3. **英文完整报告存档**：
   - 路径：`{memory_path}/{YYYY-MM-DD}_EN.md`
   - 内容：英文版完整报告

4. **更新摘要索引**（中英双语摘要）：
   - 路径：`{memory_path}/index.md`
   - 格式：中英双语摘要+核心数据

1. **中文完整报告存档**
   - 路径：`{memory_path}/{YYYY-MM-DD}_CN.md`
   - 内容：中文版完整报告

2. **英文完整报告存档**
   - 路径：`{memory_path}/{YYYY-MM-DD}_EN.md`
   - 内容：英文版完整报告

3. **更新摘要索引**（中英双语摘要）
   - 路径：`{memory_path}/index.md`
   - 格式：中英双语摘要+核心数据

**index.md 格式示例：**
```markdown
## 历史报告索引 | Report Index

### 2026-04-08
- **核心议题/Core Topic**：美伊达成两周停火协议 / US-Iran 2-week Ceasefire Agreement
- **市场情绪/Market Sentiment**：🔄 从避险切换至冒险 / 🔄 Risk-off → Risk-on
- **标普500/S&P 500**：+2.5% [来源] | **布伦特原油/Brent**：-15%+ [来源] | **黄金/Gold**：$XXXX [来源] | **美元指数/DXY**：-1%+ [来源]
- **风险等级/Risk Level**：⚠️ 中 / ⚠️ Medium

### 2026-04-09
- **核心议题/Core Topic**：停火协议出现裂痕 / Ceasefire Shows Cracks
- **市场情绪/Market Sentiment**：🟡 谨慎乐观 / 🟡 Cautious Optimism
- **标普500/S&P 500**：+0.30% [来源] | **VIX**：XX.XX (+X.XX%) [来源] | **美元指数/DXY**：-0.16% [来源]
- **风险等级/Risk Level**：🔴 高 / 🔴 High
```

### 步骤6：推送双语报告

**使用 `message` 工具发送两消息到飞书群：**

1. **先发英文版**（供快速浏览）
2. **再发中文版**（便于详细阅读）

- 群ID：`{feishu_group_id}`（由参数配置）
- Channel: feishu
- 中英文报告之间用分隔线 `━━━━━━━━━━` 隔开

## 报告质量标准

### 数据准确性原则（最高优先级）

⚠️ **数据准确性是报告的生命线，绝不允许编造或推断未经核实的数据。**

1. **来源标注必须**：
   - 报告中所有价格/百分比数据必须标注**数据来源**
   - 格式：`[数据来源] | [查询时间]`
   - 示例：`标普500：+2.5% [Bloomberg, 04/09 08:30]`

2. **未能获取的数据处理**：
   - 未能获取的数据明确标注`[未能获取]`或`[数据暂缺]`
   - **禁止**使用历史均值、预期值、合理估算等方式填充
   - 缺失数据的位置用`[未能获取]`标注，不留空白也不推断

3. **历史对比数据要求**：
   - 对比数据必须基于**实际查询的历史报告或数据库**
   - **严禁**凭记忆或"大概"自行编造历史价格
   - 如果历史数据未能查询到，明确标注`[上期数据未能获取]`

4. **推断的禁止**：
   - 市场评论中"可能"、"或许"属于预判，可以包含
   - **具体价格/百分比数据**必须来自实际查询，禁止推断
   - 如果某项数据缺失，直接标注缺失，不推算不填补

5. **大宗商品数据要求（黄金/原油/天然气）**：
   - **必须**在步骤2-3之间使用专用数据源查询价格
   - 优先使用 Kitco（黄金）、OilPrice/EIA（原油）
   - 黄金价格格式：`$X,XXX [Kitco, HH:MM]`
   - 原油价格格式：`$XX.XX [OilPrice, HH:MM]`
   - 如果专用源失败，使用 `tavily_search(topic=finance, query="gold price today")` 作为后备

### 内容质量标准

5. **双语同步**：中英文版本必须同步生成，内容一致
6. **对比分析必须**：必须包含"上期vs本期"对比，不得孤立报数据
7. **变化标注必须**：价格/情绪/议题的任何变化必须明确标注方向
8. **预测必须有依据**：每项预测需基于具体数据变化
9. **风险提示必须**：识别出的风险必须列出，不得遗漏

### 数据来源优先级

当多个数据源价格不一致时：
- 优先使用 **Bloomberg** 的价格数据
- 次选 **Reuters**、**Yahoo Finance**
- 标注格式：`[数据源, 查询时间]`

## 关键术语对照表

| 中文 | English |
|------|---------|
| 特朗普动态日报 | Trump Daily Report |
| 避险 | Risk-off |
| 冒险/风险偏好 | Risk-on |
| 谨慎乐观 | Cautious Optimism |
| 涨幅收窄 | Rally Fades |
| 停火协议 | Ceasefire Agreement |
| 脆弱 | Fragile |
| 市场情绪 | Market Sentiment |
| 前瞻预测 | Forward Outlook |
| 风险提示 | Risk Alerts |

## 备注

- 如果特朗普当天没有重要发言，报告应说明"昨日无重大公开发言" / "No significant public statements yesterday"
- 报告语言：中文+英文双语（中文为主，英文为辅）
- 市场数据优先使用最新交易日数据
- 如遇重大突发事件（如政策声明、紧急公告），单独标注⚡️
- 历史报告保存至少30天，超过30天的报告可归档到 `archive/` 子目录
- 所有路径和目标群ID均通过参数配置，不包含硬编码值
