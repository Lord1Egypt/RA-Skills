---
name: research-orchestrator
description: 深度研究工作流，支持多源搜索、事实验证、专业报告生成。Use when user needs comprehensive research, market analysis, competitive analysis, or professional research reports. Supports web search, multi-language output, and Markdown reports. 深度研究、市场分析、竞品分析、研究报告、行业分析。
version: 2.0.1
license: MIT-0
metadata: {"openclaw": {"emoji": "🔬", "requires": {"bins": ["curl", "python3"], "env": []}, "always": false}}
---

# 深度研究 Deep Research

真正能工作的深度研究工作流。支持多源搜索、事实验证、专业报告生成。

**与旧版本的区别：**
- ✅ 真正能搜索（使用 curl 调用搜索 API）
- ✅ 真正能分析（多源交叉验证）
- ✅ 真正能生成报告（完整内容，无占位符）
- ✅ 真正能工作（端到端自动化）

## 触发条件 Trigger Conditions

**中文 Chinese:**
- "深度研究..." / "深度分析..."
- "帮我研究一下..."
- "市场分析" / "竞品分析"
- "行业研究报告"
- "全面分析..."

**English English:**
- "Deep research on..."
- "Research report about..."
- "Market analysis" / "Competitive analysis"
- "Industry research..."
- "Comprehensive analysis..."

---

## 核心能力 Capabilities

### 1. 多源搜索 Multi-Source Search
- **Web 搜索**: 使用 SearXNG API 或其他搜索 API
- **学术搜索**: arXiv、Google Scholar
- **新闻搜索**: 最新资讯
- **数据搜索**: 统计数据、行业报告

### 2. 事实验证 Fact Verification
- 多源交叉验证
- 可信度评估
- 冲突检测
- 来源追溯

### 3. 专业报告 Professional Reports
- 结构化内容
- 数据可视化建议
- 参考文献
- 中英文支持

---

## 执行流程 Execution Workflow

### Step 1: 理解需求 Understand Requirements

```
从用户输入中提取：
1. 研究主题（Topic）
2. 研究范围（Scope）
3. 输出语言（Language）
4. 研究深度（Depth）- 基础/中等/深度
```

### Step 2: 设计研究角度 Design Research Angles

**市场分析类 Market Analysis:**
```
1. 市场规模与增长 Market Size & Growth
2. 主要玩家分析 Key Players Analysis
3. 技术趋势 Technology Trends
4. 投资与并购 Investment & M&A
5. 政策环境 Policy Environment
```

**竞品分析类 Competitive Analysis:**
```
1. 竞品概览 Competitor Overview
2. 产品对比 Product Comparison
3. 市场份额 Market Share
4. 优劣势分析 SWOT Analysis
5. 战略动向 Strategic Moves
```

**行业研究类 Industry Research:**
```
1. 行业现状 Industry Status
2. 发展历程 Development History
3. 产业链分析 Supply Chain Analysis
4. 未来趋势 Future Trends
5. 投资机会 Investment Opportunities
```

### Step 3: 执行搜索 Execute Search

**搜索命令模板 Search Command Template:**

```bash
# Web 搜索
curl -s "https://searxng.example.com/search?q=QUERY&format=json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for result in data.get('results', [])[:5]:
    print(f\"- {result['title']}: {result['url']}\")
    print(f\"  {result.get('content', '')[:200]}\")
"

# 学术搜索 (arXiv)
curl -s "http://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5" | python3 -c "
import sys, xml.etree.ElementTree as ET
data = sys.stdin.read()
root = ET.fromstring(data)
ns = {'atom': 'http://www.w3.org/2005/Atom'}
for entry in root.findall('atom:entry', ns):
    title = entry.find('atom:title', ns).text.strip()
    print(f\"- {title}\")
"
```

**搜索查询生成 Search Query Generation:**

根据研究角度生成多个搜索查询：

```python
# 中文查询
queries_zh = [
    f"{topic} 市场规模 2026",
    f"{topic} 行业分析",
    f"{topic} 主要厂商",
    f"{topic} 发展趋势",
    f"{topic} 投资动态",
]

# 英文查询
queries_en = [
    f"{topic} market size 2026",
    f"{topic} industry analysis",
    f"{topic} key players",
    f"{topic} trends",
    f"{topic} investment",
]
```

### Step 4: 信息提取与验证 Extract & Verify

**信息提取模板 Extraction Template:**

```markdown
## {角度名称}

### 关键发现 Key Findings
- 发现1 [来源: URL] (置信度: 高)
- 发现2 [来源: URL] (置信度: 中)

### 数据点 Data Points
| 指标 | 数值 | 来源 | 置信度 |
|------|------|------|--------|
| 市场规模 | $XX亿 | Gartner | 高 |
| 增长率 | XX% | IDC | 高 |

### 来源列表 Sources
1. [来源名称](URL) - 可信度: 高
2. [来源名称](URL) - 可信度: 中
```

**可信度评估规则 Credibility Rules:**

```
高可信度: 官方数据、知名研究机构、上市公司财报
中可信度: 行业媒体、专业分析、权威新闻
低可信度: 个人博客、社交媒体、匿名来源
```

### Step 5: 生成报告 Generate Report

**报告结构 Report Structure:**

```markdown
---
title: "{研究主题}"
subtitle: "深度研究报告"
date: "{当前日期}"
author: "Deep Research Agent"
version: "1.0"
---

# 执行摘要 Executive Summary

> 本报告对"{研究主题}"进行了全面深入的研究与分析。

**关键发现 Key Findings:**
- 发现1
- 发现2
- 发现3

---

# 目录 Table of Contents

1. 研究方法论 Methodology
2. 研究发现 Research Findings
3. 深度分析 Deep Analysis
4. 风险与机遇 Risks & Opportunities
5. 结论与建议 Conclusions & Recommendations
6. 参考文献 References

---

# 1. 研究方法论 Methodology

## 1.1 研究概述 Research Overview

本研究采用多源信息收集与交叉验证方法...

## 1.2 数据来源 Data Sources

| 来源类型 | 数量 | 说明 |
|----------|------|------|
| 行业报告 | X | Gartner、IDC等 |
| 新闻报道 | X | 主流媒体 |
| 学术论文 | X | arXiv、Google Scholar |
| 官方数据 | X | 政府、企业 |

---

# 2. 研究发现 Research Findings

## 2.1 {角度1}

[根据搜索结果填充]

## 2.2 {角度2}

[根据搜索结果填充]

---

# 3. 深度分析 Deep Analysis

## 3.1 关键洞察 Key Insights

[分析发现之间的关联]

## 3.2 趋势分析 Trend Analysis

[分析未来发展方向]

---

# 4. 风险与机遇 Risks & Opportunities

## 4.1 主要风险 Key Risks

[列出潜在风险]

## 4.2 发展机遇 Development Opportunities

[列出潜在机遇]

---

# 5. 结论与建议 Conclusions & Recommendations

## 5.1 主要结论 Main Conclusions

[总结核心发现]

## 5.2 建议 Recommendations

[给出行动建议]

---

# 6. 参考文献 References

[列出所有来源]
```

---

## 完整示例 Full Example

### 用户输入 User Input

```
帮我深度研究一下2026年AI芯片市场
```

### AI 执行流程 AI Execution Flow

```
🔬 深度研究开始
━━━━━━━━━━━━━━━━━━━━
主题: 2026年AI芯片市场
范围: 市场规模、竞争格局、技术趋势
语言: 中文
━━━━━━━━━━━━━━━━━━━━

📊 研究进度
━━━━━━━━━━━━━━━━━━━━
Phase 1: 需求分析 ✅
Phase 2: 多源搜索 🔄
├─ 市场规模: ✅ (6 sources)
├─ 竞争格局: ✅ (5 sources)
├─ 技术趋势: ✅ (4 sources)
└─ 投资动态: 🔄 (搜索中...)
Phase 3: 事实验证 ⏳
Phase 4: 报告生成 ⏳
━━━━━━━━━━━━━━━━━━━━
```

### 搜索执行 Search Execution

```bash
# 搜索市场规模
curl -s "https://search.example.com/search?q=AI芯片市场规模2026&format=json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('results', [])[:5]:
    print(f\"- {r['title']}: {r['url']}\")
    print(f\"  {r.get('content', '')[:200]}\n\")
"

# 搜索竞争格局
curl -s "https://search.example.com/search?q=NVIDIA+AMD+Intel+AI芯片市场份额&format=json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('results', [])[:5]:
    print(f\"- {r['title']}: {r['url']}\")
    print(f\"  {r.get('content', '')[:200]}\n\")
"
```

### 报告生成 Report Generation

```markdown
---
title: "2026年AI芯片市场深度研究报告"
subtitle: "市场规模、竞争格局与技术趋势"
date: "2026年04月16日"
author: "Deep Research Agent"
---

# 执行摘要

本报告对2026年AI芯片市场进行了全面深入的研究与分析。

**关键发现:**
- 2026年全球AI芯片市场规模预计达到1200亿美元
- NVIDIA继续主导市场，份额约80%
- 边缘AI芯片成为新增长点

---

# 1. 市场规模与增长

## 1.1 全球市场规模

根据Gartner和IDC的数据：

| 年份 | 市场规模 | 增长率 |
|------|----------|--------|
| 2024 | $800亿 | - |
| 2025 | $1000亿 | +25% |
| 2026 | $1200亿 | +20% |
| 2030 | $4000亿 | - |

## 1.2 增长驱动因素

1. **数据中心需求**: 云服务商大规模采购AI芯片
2. **边缘计算**: 手机、汽车、IoT设备AI化
3. **大模型训练**: GPT、Claude等模型需要更多算力

---

[... 完整报告内容 ...]
```

---

## 快速开始 Quick Start

### 基础研究 Basic Research

```
用户: "帮我研究一下新能源汽车市场"
AI: 执行完整研究流程，生成专业报告
```

### 指定深度 Specify Depth

```
用户: "深度分析OpenAI的竞争优势，要详细一点"
AI: 执行深度研究，包含更多数据点和分析
```

### 指定语言 Specify Language

```
用户: "Research about AI chips market, output in English"
AI: 执行英文研究，生成英文报告
```

---

## 搜索配置 Search Configuration

### 默认搜索源 Default Sources

```bash
# Web 搜索
SEARCH_API="https://searxng.example.com/search"

# 学术搜索
ACADEMIC_API="http://export.arxiv.org/api/query"

# 新闻搜索
NEWS_API="https://newsapi.org/v2/everything"
```

### 自定义搜索源 Custom Sources

如果默认搜索源不可用，可以使用其他 API：

```bash
# DuckDuckGo (无需 API key)
curl -s "https://api.duckduckgo.com/?q=QUERY&format=json"

# Wikipedia
curl -s "https://en.wikipedia.org/api/rest_v1/page/summary/QUERY"
```

---

## 与其他 Skills 集成 Integration

### 与 word-studio 集成

生成 Word 格式的研究报告：

```bash
# 使用 word-studio 生成 Word 文档
npx clawhub@latest install word-studio
# 然后将研究报告传递给 word-studio
```

### 与 chart-maker 集成

生成数据可视化图表：

```bash
# 使用 chart-maker 生成图表
npx clawhub@latest install chart-maker
# 为研究数据生成可视化图表
```

### 与 universal-translator 集成

支持多语言研究：

```bash
# 使用 universal-translator 翻译
npx clawhub@latest install universal-translator
# 将研究报告翻译成其他语言
```

---

## 输出格式 Output Formats

### Markdown 格式 (默认)

```
output/report.md
```

### 建议的后续处理

1. **生成 Word**: 使用 word-studio 转换为 Word 格式
2. **生成 PDF**: 使用 pdf-studio 转换为 PDF 格式
3. **生成图表**: 使用 chart-maker 生成可视化图表

---

## 注意事项 Important Notes

### ⚠️ 限制 Limitations

1. **搜索依赖**: 需要可用的搜索 API
2. **网络依赖**: 需要网络连接
3. **数据时效**: 搜索结果的时效性取决于数据源
4. **准确性**: 交叉验证可提高准确性，但不能保证100%正确

### ✅ 最佳实践 Best Practices

1. **交叉验证**: 至少从2-3个来源验证关键数据
2. **标注来源**: 所有数据都要标注来源
3. **评估可信度**: 标注每个来源的可信度
4. **保持更新**: 定期更新研究数据

### 💡 使用建议 Usage Tips

1. **明确范围**: 研究范围越明确，结果越精准
2. **指定深度**: 根据需求选择研究深度
3. **检查来源**: 阅读报告时注意检查来源可信度
4. **迭代改进**: 根据初步结果调整研究方向

---

## 快速触发短语 Quick Trigger Phrases

**中文 Chinese:**
- 深度研究
- 深度分析
- 帮我研究一下
- 市场分析
- 竞品分析
- 行业研究
- 研究报告
- 全面分析

**English English:**
- Deep research
- Research report
- Market analysis
- Competitive analysis
- Industry research
- Comprehensive analysis

---

## 版本历史 Version History

- v2.0.0 (2026-04-16): 重大重写
  - 真正能搜索（使用 curl 调用搜索 API）
  - 真正能分析（多源交叉验证）
  - 真正能生成报告（完整内容，无占位符）
  - 真正能工作（端到端自动化）
  - 支持中英文双语
  - 集成 word-studio/pdf-studio/chart-maker

- v1.2.0: 旧版本（存在问题）
  - 搜索不工作
  - 报告有占位符
  - 脚本互不相连
