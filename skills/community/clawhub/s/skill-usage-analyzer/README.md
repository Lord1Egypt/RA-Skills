# 🔍 Skill Usage Analyzer

智能分析 OpenClaw 技能，生成使用指南、创意用法和组合推荐。

## ✨ 功能特点

- 📖 **智能解析** - 自动提取 SKILL.md 的关键信息
- 📝 **生成摘要** - 用表格和列表展示核心功能
- 💡 **创意用法** - 提供超出文档描述的创意使用场景
- 🔗 **组合推荐** - 发现可以协同使用的技能组合
- 🎯 **智能推荐** - 根据任务描述推荐最适合的技能
- 📊 **对比矩阵** - 对比多个相似技能，帮助选择

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装
npx clawhub install skill-usage-analyzer

# 或手动安装
git clone <repository-url>
cd skill-usage-analyzer
```

### 使用方法

```bash
# 1. 分析单个技能
python3 scripts/analyze_skill.py /path/to/skill/SKILL.md

# 2. 获取创意用法
python3 scripts/creative_usage.py stock-watcher

# 3. 发现技能组合
python3 scripts/find_combinations.py

# 4. 智能推荐技能
python3 scripts/recommend_skill.py "我想监控股票价格"

# 5. 对比多个技能
python3 scripts/compare_matrix.py skill1 skill2

# 6. 分析所有技能
python3 scripts/analyze_all.py -o skill-index.md
```

## 📦 包含脚本

| 脚本 | 功能 |
|------|------|
| `analyze_skill.py` | 分析单个技能，生成完整报告 |
| `creative_usage.py` | 生成技能的创意用法建议 |
| `find_combinations.py` | 发现可组合使用的技能 |
| `recommend_skill.py` | 根据任务描述推荐技能 |
| `compare_matrix.py` | 对比多个相似技能 |
| `analyze_all.py` | 批量分析所有已安装技能 |

## 💡 创意用法示例

### 分析 stock-watcher 技能

```bash
python3 scripts/creative_usage.py stock-watcher
```

输出：
```
💡 stock-watcher 创意用法指南

1. 📊 智能选股助手
   💭 结合AI分析，自动筛选潜力股票
   步骤:
      1. 批量添加关注的板块股票
      2. 筛选涨幅/跌幅异常的股票
      3. 用AI分析基本面和技术面
      4. 生成每日选股报告
   ✅ 价值: 从手动监控升级为智能选股

2. 🤖 自动化交易提醒
   💭 设置条件单，自动触发买卖提醒
   ...
```

### 发现技能组合

```bash
python3 scripts/find_combinations.py
```

输出：
```
🔍 技能组合推荐

1. 💡 内容创作流水线
   描述: 搜索资料→总结→创作→影视化
   已安装: tavily-search, summarize, novel-generator
   使用场景: 搜索热点话题→生成小说→改编剧本

2. 💡 GitHub自动化
   描述: 管理stars、自动修复issues
   ...
```

## 📝 输出格式

支持多种输出格式：

```bash
# 文本格式（默认）
python3 scripts/analyze_skill.py SKILL.md

# Markdown格式
python3 scripts/analyze_skill.py SKILL.md -f markdown

# JSON格式
python3 scripts/analyze_skill.py SKILL.md -f json
```

## 🔧 系统要求

- Python 3.6+
- OpenClaw 环境
- 无需额外依赖（使用标准库）

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📞 联系方式

- GitHub: [your-repo-url]
- ClawHub: skill-usage-analyzer
