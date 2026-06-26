---
name: scholarsearch
description: Academic literature search and briefing generation with Tavily API, PubMed, and Google Scholar. Use when you need to search for latest academic papers on specific topics, generate Top 10 literature briefing with relevance rankings, save reports to Obsidian vault in daily format, or send summaries via Feishu. Accepts multiple keywords separated by comma or space.
---

# Scholar Search 🔬📚

Automated academic literature discovery and briefing generation. This skill searches PubMed, Google Scholar, and other academic databases using Tavily API, generates relevance-ranked Top 10 reports, and delivers them to your Obsidian vault and Feishu.

## Quick Start

```bash
# Search papers on specific topic
scholarsearch 关键词：房颤，导管消融，脉冲电场消融
```

Or multiple keywords separated by comma or space:
```bash
scholarsearch 房颤，afib, 心房颤动，catheter ablation，消融，pulsed field ablation
```

## What It Does

1. **Multi-source search**: Queries PubMed, Google Scholar, and academic web sources via Tavily API
2. **Relevance ranking**: Evaluates papers based on scoring criteria below
3. **Top 10 curation**: Selects most relevant papers with scores 0.0-1.0
4. **Report generation**: Creates formatted briefing with links, abstracts, and key findings
5. **Dual delivery**: Saves to Obsidian + sends complete content via Feishu

## 评分标准 (Relevance Scoring)

**评分范围**: 0.0 - 1.0，越高表示越相关

### 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| **时效性** | 25% | 2025-2026 年优先，年度排名前 3 月内加分 |
| **临床/研究价值** | 30% | 人体试验、RCT 随机对照研究、临床试验结果 |
| **权威性** | 20% | 同行评审期刊、知名机构/研究者、高引用率 |
| **直接相关性** | 25% | 标题/摘要/内容直接匹配关键词 |

### 评分等级

- **0.90-1.0**: 高度相关，必看论文，核心研究成果
- **0.80-0.89**: 高度相关，重要文献，强烈推荐阅读
- **0.70-0.79**: 中等偏上，有价值的研究
- **0.60-0.69**: 一般相关，可作为背景阅读
- **0.00-0.59**: 低相关，辅助材料

### 优先规则

1. **人体试验数据** 优先于 动物/离体实验
2. **2026 年最新研究** 优先于 早期研究
3. **多中心/大样本 RCT** 优先于 单中心/小样本
4. **同行评审期刊** 优先于 会议摘要/预印本
5. **系统综述/Meta 分析** 优先级最高

### 排除规则

- 非学术来源 (商业网站、博客、新闻稿无实质内容)
- 动物实验仅作为参考，评分降低 0.1-0.2
- 远 2025 年的研究，除非是经典文献

## 评分说明

** Tavily API 评分解释**：

Tavily 返回的相关性评分基于其内部算法，综合考虑：
- 网页内容质量
- 搜索结果与查询匹配度
- 来源权威性
- 页面结构完整性

**本技能的评分转换**：

将 Tavily 的原始评分 (0-100) 转换为 0.0-1.0 的学术相关性评分：

```
学术评分 = min(原始评分 / 100, 1.0) × 评分系数
```

**评分系数**：
- 人体临床试验：1.0 (基准)
- 动物/细胞研究：0.8-0.9
- 会议摘要：0.7-0.8
- 系统综述/Meta 分析：1.0-1.1 (可超 1.0)
- 新闻/商业内容：0.5-0.6 (即使 Tavily 评分高)

## When to Use

- ✅ Morning academic briefings (configurable timing, defaults to 5:00 AM)
- ✅ Literature review on specific medical/technical topics
- ✅ Tracking emerging research in a field
- ✅ Getting curated "Top 10" lists with context

## Parameters

Accept **comma-separated or space-separated** keywords:

```
scholarsearch 房颤，心房颤动，pulsed field ablation，catheter ablation
scholarsearch AFib, atrial fibrillation, ablation, electrogram
scholarsearch 机器学习，深度学习，神经网络，大模型
```

## Output Format

```markdown
# 每日学术更新 - [Topic] 研究简报

**日期**: YYYY-MM-DD  
**更新时间**: HH:MM Asia/Shanghai  
**关键词**: [your keywords]

---

## 📊 Top 10 精选文献

按相关性评分排序 (0.0-1.0):

### 1️⃣ [Paper Title]
**评分**: 0.XX  
**链接**: https://...  
**摘要**: [Brief summary with key findings]

... (10 papers)

---

## 📝 本期要点总结

### 🔥 核心发现

[Bullet points of major breakthroughs/trends]

### 🎯 临床/研究关注重点

[What to watch for]

---

## 🔄 配置说明

**检索频率**: [Set to user preference]  
**来源**: Tavily API (PubMed, Google Scholar, etc.)  
**保存路径**: Obsidian 每日学术更新/YYYY-MM-DD.md  
**排序方式**: 相关性评分 + 发表时间

---

*自动生成 | ☕🐕 CoffeeDog | [Topic] | YYYY-MM-DD*
```

## Error Handling

- **No results**: Adjust keywords, widen search terms
- **Low-quality links**: Skip non-academic sources, prioritize peer-reviewed
- **API limits**: Retry with backoff, rate limit protection

## Integration Points

- **Tavily API**: Academic web search with PubMed/Scholar support
- **Feishu**: Daily delivery of complete briefing content
- **Obsidian**: Auto-save to `Obsidian 每日学术更新/YYYY-MM-DD.md`

## Notes

- For automatic scheduling: Use cron or heartbeat to run at 5:00 AM daily
- Use English keywords for better PubMed results
- Mix Chinese + English terms for comprehensive coverage
- Consider topic-specific parameters: "房颤 2026，PFA 临床试验"

---

*Academic discovery automated. CoffeeDog knows the papers. ☕🐕*
