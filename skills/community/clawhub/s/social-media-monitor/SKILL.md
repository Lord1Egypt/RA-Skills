---
name: social-media-monitor
description: 社交媒体舆情分析工具 - 品牌方/电商卖家/运营人员的平价舆情监控助手，支持关键词监测、负面预警、声量趋势分析
homepage: https://clawhub.ai/skills/social-media-monitor
tags: [social-media, sentiment-analysis, brand-monitoring, xiaohongshu, marketing, pr, ecommerce, operations]
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "social-media-monitor",
              "path": ".",
              "label": "安装社交媒体舆情分析工具",
            },
          ],
      },
  }
---

# Social Media Monitor

**Version:** 1.0.0  
**Author:** 小爪 🦞  
**License:** MIT  
**Tags:** #social-media #sentiment-analysis #brand-monitoring #xiaohongshu #marketing #pr #ecommerce #operations

---

## 📊 社交媒体舆情分析工具

**专为品牌方、电商卖家、运营人员打造的平价舆情监控助手**。基于 MCP 协议，提供关键词监测、负面预警、声量趋势分析等核心功能，帮助您快速掌握社交媒体舆情动态。

## 🎯 这个工具能帮你做什么？

- **如果你是品牌方**：实时监控品牌声量，第一时间发现负面舆情，避免危机发酵。无需昂贵企业软件，免费使用。

- **如果你是电商卖家**：监测产品关键词，了解用户评价情感，优化产品和运营策略。支持小红书店铺数据导入。

- **如果你是运营人员**：追踪内容标签热度，分析声量趋势，生成专业周报。让数据驱动内容决策，提升工作效率。

- **如果你是中小商家**：这个工具提供核心功能，即装即用，无需培训，完全免费。

## ⚠️ 注意事项

- **当前版本仅处理本地 CSV 数据，不包含任何网络爬虫功能。** 未来若增加此类功能，会另行发布。
- **数据隐私：** 所有数据在本地处理，不会上传到外部服务器。
- **情感分析：** 基于词典的简单分析，准确率约 70%，适合快速筛查。如需更高精度，建议人工复核。
- **报告输出：** 报告保存在技能目录内的 `reports/` 文件夹，确保安全性。
- **完全免费：** 永久免费使用，即装即用。

## 功能特性

### 🔍 核心监控功能

- **关键词监测** - 自定义监测关键词，追踪提及情况
- **负面预警** - 情感分低于阈值时自动预警，避免危机发酵
- **声量趋势** - 文字图表展示声量变化，直观易懂
- **情感分析** - 分析文本情感倾向（支持中文）
- **关键词提取** - 从文本中提取核心关键词
- **周报生成** - 自动生成舆情分析周报（Markdown 格式）

### 📊 数据管理

- **CSV 导入** - 支持小红书数据 CSV 导入
- **分类管理** - 关键词支持分类管理（品牌/产品/负面等）
- **阈值配置** - 可自定义负面预警阈值
- **本地存储** - 所有数据本地存储，安全可控

## 快速开始

### 1. 安装 Skill

```bash
clawhub install social-media-monitor
```

或手动安装：

```bash
cd /path/to/skill
npm install
```

### 2. 启动服务器

```bash
npm start
```

### 3. 在 OpenClaw 中调用

通过 mcporter CLI：

```bash
# 列出所有工具
mcporter list

# ===== 关键词监测 =====
# 添加监测关键词
mcporter call social-media-monitor.add_keyword keyword:"品牌名" category:"品牌"
mcporter call social-media-monitor.add_keyword keyword:"产品名" category:"产品"
mcporter call social-media-monitor.add_keyword keyword:"避雷" category:"负面"

# 查看监测列表
mcporter call social-media-monitor.list_keywords

# 监测关键词匹配
mcporter call social-media-monitor.monitor_keywords source:"sample" limit:20

# ===== 负面预警 =====
# 设置预警阈值（建议 -2 到 -5）
mcporter call social-media-monitor.set_alert_threshold threshold:-2

# 检查负面舆情
mcporter call social-media-monitor.check_alerts source:"sample"

# ===== 声量趋势 =====
# 获取声量趋势（文字图表）
mcporter call social-media-monitor.get_volume_trend days:7

# ===== 基础功能 =====
# 情感分析
mcporter call social-media-monitor.analyze_sentiment text:"这个产品很好用" language:"zh"

# 关键词提取
mcporter call social-media-monitor.extract_keywords text:"小红书运营数据分析" limit:5

# 生成周报
mcporter call social-media-monitor.generate_weekly_report limit:20
```

## 工具详解

### 关键词监测工具组

#### add_keyword
添加自定义监测关键词。

**参数：**
- `keyword` (string, 必填) - 要监测的关键词
- `category` (string, 可选) - 关键词分类（品牌/产品/负面等），默认"default"

**示例：**
```bash
mcporter call social-media-monitor.add_keyword keyword:"小红书" category:"平台"
# 输出：{"status": "success", "keyword": "小红书", "category": "平台", "total": 1}
```

#### list_keywords
查看当前监测的关键词列表。

**示例：**
```bash
mcporter call social-media-monitor.list_keywords
# 输出：{"keywords": [{"keyword": "小红书", "category": "平台"}], "total": 1}
```

#### monitor_keywords
监测关键词在笔记中的匹配情况。

**参数：**
- `source` (string, 可选) - 数据源：csv 或 sample，默认"sample"
- `limit` (number, 可选) - 分析笔记数量，默认 20

**示例：**
```bash
mcporter call social-media-monitor.monitor_keywords source:"sample" limit:20
# 输出：{"monitoredKeywords": ["小红书"], "matches": [...], "totalMatches": 5}
```

---

### 负面预警工具组

#### set_alert_threshold
设置负面情感预警阈值。

**参数：**
- `threshold` (number, 必填) - 情感分阈值，范围 -10 到 10，建议 -2 到 -5

**说明：**
- 情感分计算：正面词 +1 分，负面词 -1 分
- 当笔记情感分低于阈值时，触发预警
- 建议值：-2（敏感）到 -5（宽松）

**示例：**
```bash
mcporter call social-media-monitor.set_alert_threshold threshold:-3
# 输出：{"status": "success", "threshold": -3, "message": "负面预警阈值已设置为 -3"}
```

#### check_alerts
检查是否有负面舆情（情感分低于阈值）。

**参数：**
- `source` (string, 可选) - 数据源：csv 或 sample，默认"sample"

**示例：**
```bash
mcporter call social-media-monitor.check_alerts source:"sample"
# 输出：
# {
#   "threshold": -3,
#   "alerts": [],
#   "totalAlerts": 0,
#   "message": "✅ 未发现负面舆情"
# }
```

---

### 声量趋势工具

#### get_volume_trend
获取声量趋势（按日期统计笔记数量，文字图表展示）。

**参数：**
- `source` (string, 可选) - 数据源：csv 或 sample，默认"sample"
- `days` (number, 可选) - 统计天数，默认 7

**输出示例：**
```
2026-03-11: ██████████ 1
2026-03-12: ██████████ 1
2026-03-13: ██████████ 1
2026-03-14: ████████░░ 8
2026-03-15: █████████░ 9
2026-03-16: ██████████ 10
2026-03-17: ████████░░ 8
```

**示例：**
```bash
mcporter call social-media-monitor.get_volume_trend days:7
```

---

### 基础分析工具

#### analyze_sentiment
情感分析工具。

**参数：**
- `text` (string) - 要分析的文本
- `language` (string) - 语言：zh 或 en，默认"zh"

**示例：**
```bash
mcporter call social-media-monitor.analyze_sentiment text:"这个产品很好用，推荐购买"
# 输出：{"score": 2, "sentiment": "positive", "confidence": 0.33}
```

#### extract_keywords
关键词提取工具。

**参数：**
- `text` (string) - 要提取关键词的文本
- `limit` (number) - 返回数量，默认 10
- `language` (string) - 语言，默认"zh"

**示例：**
```bash
mcporter call social-media-monitor.extract_keywords text:"小红书运营数据分析" limit:5
```

#### list_notes
笔记列表工具。

**参数：**
- `source` (string) - 数据源
- `limit` (number) - 数量限制
- `sortBy` (string) - 排序字段
- `order` (string) - 排序顺序

**示例：**
```bash
mcporter call social-media-monitor.list_notes source:"sample" limit:10 sortBy:"likes" order:"desc"
```

#### generate_weekly_report
生成周报工具。

**参数：**
- `limit` (number) - 分析笔记数量，默认 10

**示例：**
```bash
mcporter call social-media-monitor.generate_weekly_report limit:20
# 输出：{"status": "success", "reportPath": "/path/to/report.md"}
```

---

## 应用场景

### 品牌方日常监控

**每天 5 分钟，掌握品牌舆情：**

```bash
# 1. 检查负面预警（1 分钟）
check_alerts source:"sample"

# 2. 查看关键词匹配（2 分钟）
monitor_keywords source:"sample" limit:20

# 3. 查看声量趋势（1 分钟）
get_volume_trend days:7

# 4. 如有负面，及时处理（1 分钟）
```

### 电商卖家产品分析

**了解用户评价，优化产品：**

```bash
# 1. 添加产品关键词
add_keyword keyword:"产品名" category:"产品"
add_keyword keyword:"质量" category:"评价"
add_keyword keyword:"性价比" category:"评价"

# 2. 监测用户评价
monitor_keywords source:"sample" limit:50

# 3. 分析情感倾向
analyze_sentiment text:"用户评价内容"
```

### 运营人员周报生成

**一键生成专业周报：**

```bash
# 周五下午 5 点，生成周报
generate_weekly_report limit:50

# 输出：reports/周报_2026-03-17.md
# 包含：数据概览、热门笔记、关键词分析、声量趋势
```

---

## 技术栈

- Node.js 22+
- @modelcontextprotocol/sdk (官方 MCP SDK)
- sentiment (情感分析库)
- keyword-extractor (关键词提取)
- zod (参数验证)

---

## 常见问题

### Q: 数据从哪里来？

A: 当前版本支持用户上传 CSV 文件。小红书数据可通过官方后台导出，或使用第三方数据工具导出。

### Q: 情感分析准确率如何？

A: 当前版本使用基于词典的简单分析，准确率约 70%。适合快速筛查，重要决策建议人工复核。后续可接入专业 NLP API 提升准确率。

### Q: 负面预警多久检查一次？

A: 当前版本需要手动调用 `check_alerts` 工具。后续版本可配置定时检查（如每小时自动检查）。

### Q: 支持哪些社交媒体平台？

A: 当前版本以小红书为主（CSV 格式）。理论上支持任何可导出为 CSV 的社交媒体数据（抖音、微博等）。

### Q: 这个工具收费吗？

A: **完全免费。** 永久免费使用，即装即用。

### Q: 数据会上传到外部吗？

A: **不会。** 所有数据在本地处理，存储在技能目录内，不会上传到任何外部服务器。

### Q: 如何备份数据？

A: 数据存储在 `data/` 目录下，定期备份该目录即可。建议每周备份一次。

---

## 更新日志

### v1.0.0 (2026-03-17)
- ✅ 初始版本发布
- ✅ 关键词监测（add_keyword, list_keywords, monitor_keywords）
- ✅ 负面预警（set_alert_threshold, check_alerts）
- ✅ 声量趋势（get_volume_trend）
- ✅ 基础分析（analyze_sentiment, extract_keywords, list_notes, generate_weekly_report）
- ✅ 完整测试套件
- ✅ 完全免费，即装即用

---

## 许可证

MIT License

---

**作者：** 小爪 🦞  
**GitHub:** （仓库筹备中，敬请期待）  
**ClawHub:** social-media-monitor

---

## 💡 使用建议

### 新手入门（第 1 周）

1. **第 1 天：** 安装工具，添加 3-5 个关键词
2. **第 2-3 天：** 每天检查负面预警（1 分钟）
3. **第 4-5 天：** 查看关键词匹配和声量趋势
4. **周末：** 生成第一份周报

### 进阶使用（第 2 周起）

1. **优化关键词列表** - 根据实际需求调整
2. **调整预警阈值** - 找到适合的敏感度
3. **建立监控流程** - 每天固定时间检查
4. **定期复盘** - 每周分析趋势，优化策略

---

**让数据驱动决策，让舆情尽在掌握！** 📊✨
