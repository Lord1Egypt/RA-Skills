# Social Media Monitor - 社交媒体舆情分析工具

📊 **完全免费的舆情监控助手** - 专为品牌方、电商卖家、运营人员打造

---

## 🚀 快速开始

### 安装

```bash
clawhub install social-media-monitor
cd social-media-monitor
npm install
npm start
```

### 使用

```bash
# 添加监测关键词
mcporter call social-media-monitor.add_keyword keyword:"品牌名" category:"品牌"

# 检查负面预警
mcporter call social-media-monitor.check_alerts source:"sample"

# 查看声量趋势
mcporter call social-media-monitor.get_volume_trend days:7

# 生成周报
mcporter call social-media-monitor.generate_weekly_report limit:20
```

---

## 📋 功能特性

- 🔍 **关键词监测** - 自定义监测关键词，追踪提及情况
- ⚠️ **负面预警** - 情感分低于阈值时自动预警
- 📈 **声量趋势** - 文字图表展示声量变化
- 📊 **情感分析** - 分析文本情感倾向
- 📝 **周报生成** - 自动生成舆情分析周报

---

## 📁 目录结构

```
social-media-monitor/
├── src/
│   └── server.js          # MCP 服务器（10 个工具）
├── data/
│   ├── sample.csv         # 示例数据
│   ├── keywords/
│   │   └── monitor_list.json  # 关键词列表
│   └── config.json        # 配置文件
├── SKILL.md               # 详细文档
├── README.md              # 本文件
└── package.json           # 项目配置
```

---

## 🎯 使用场景

### 品牌方日常监控（每天 5 分钟）

```bash
check_alerts          # 1 分钟 - 检查负面
monitor_keywords      # 2 分钟 - 查看匹配
get_volume_trend      # 1 分钟 - 查看趋势
```

### 电商卖家产品分析

```bash
add_keyword keyword:"产品名" category:"产品"
monitor_keywords source:"sample" limit:50
analyze_sentiment text:"用户评价内容"
```

### 运营人员周报生成

```bash
generate_weekly_report limit:50
# 输出：reports/周报_2026-03-17.md
```

---

## 📖 详细文档

完整使用说明请查看 [SKILL.md](./SKILL.md)

---

## 💡 提示

- **数据源：** 当前版本支持 CSV 文件导入
- **情感分析：** 基于词典的简单分析，准确率约 70%
- **数据隐私：** 所有数据本地处理，不上传外部
- **完全免费：** 永久免费使用

---

**让数据驱动决策，让舆情尽在掌握！** 📊✨
