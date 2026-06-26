---
name: skill-usage-analyzer
description: Analyze any OpenClaw skill and generate a comprehensive usage guide. Extracts examples, best practices, configuration options, and common pitfalls from SKILL.md files. Use when you want to quickly understand how to use a new skill without reading the full documentation.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["python3"] },
        "notes": "Reads SKILL.md files and generates human-friendly summaries with actionable insights.",
      },
  }
---

# Skill Usage Analyzer

Quickly understand any OpenClaw skill by analyzing its SKILL.md file and generating a comprehensive usage guide.

## Features

- 📖 **智能解析** - 自动提取 SKILL.md 的关键信息
- 📝 **生成摘要** - 用表格和列表展示核心功能
- 💡 **提取示例** - 找出所有使用示例和代码片段
- ⚙️ **配置分析** - 列出所有可配置参数
- ⚠️ **风险提示** - 识别常见问题和注意事项
- 🎯 **最佳实践** - 给出使用建议

## Quick Start

### 分析单个技能

```bash
# 分析指定技能
python3 scripts/analyze_skill.py /path/to/skill/SKILL.md

# 分析已安装的技能
python3 scripts/analyze_skill.py ~/.openclaw/workspace/skills/stock-watcher/SKILL.md
```

### 分析所有已安装技能

```bash
# 生成所有技能的快速参考
python3 scripts/analyze_all.py
```

## Usage Examples

### Example 1: 分析 Stock Watcher 技能

输入：
```bash
python3 scripts/analyze_skill.py ~/.openclaw/workspace/skills/stock-watcher/SKILL.md
```

输出示例：
```
🔍 技能分析报告: stock-watcher
═══════════════════════════════════════════════════════════

📋 基本信息
───────────────────────────────────────────────────────────
名称: stock-watcher
描述: Manage and monitor a personal stock watchlist...
适用场景: 股票监控、自选股管理、行情查看

🎯 核心功能 (4个)
───────────────────────────────────────────────────────────
1. 添加股票 - 使用6位股票代码添加到自选股
2. 删除股票 - 按代码删除自选股
3. 查看列表 - 显示当前所有自选股
4. 行情总结 - 获取股票行情摘要

💻 使用示例
───────────────────────────────────────────────────────────
添加股票:
  python3 scripts/add_stock.py 000938 "紫光股份"

查看行情:
  python3 scripts/summarize_performance.py

⚙️ 配置选项
───────────────────────────────────────────────────────────
存储路径: ~/.clawdbot/stock_watcher/watchlist.txt
数据格式: 代码|名称 (每行一个)

⚠️ 注意事项
───────────────────────────────────────────────────────────
• 股票代码格式: 使用6位数字代码
• 数据延迟: 行情可能有1-3分钟延迟
• 网络依赖: 需要网络连接获取实时数据

💡 最佳实践
───────────────────────────────────────────────────────────
1. 定期清理不再关注的股票
2. 结合技术分析指标使用
3. 设置价格预警（需配合其他工具）
```

### Example 2: 对比多个技能

```bash
python3 scripts/compare_skills.py skill1 skill2 skill3
```

## Output Format

分析报告包含以下部分：

| 部分 | 内容 |
|------|------|
| 📋 基本信息 | 技能名称、描述、适用场景 |
| 🎯 核心功能 | 功能列表，带序号和简要说明 |
| 💻 使用示例 | 具体的命令和代码示例 |
| ⚙️ 配置选项 | 可配置参数和默认值 |
| 📁 文件结构 | 技能包含的文件和目录 |
| ⚠️ 注意事项 | 常见问题、限制、风险提示 |
| 💡 最佳实践 | 使用建议和优化技巧 |
| 🔗 相关链接 | 相关技能、文档链接 |

## Advanced Usage

### 自定义输出格式

```bash
# 输出为 Markdown
python3 scripts/analyze_skill.py SKILL.md --format markdown

# 输出为 JSON
python3 scripts/analyze_skill.py SKILL.md --format json

# 只显示示例
python3 scripts/analyze_skill.py SKILL.md --examples-only
```

### 批量分析

```bash
# 分析所有技能并生成索引
python3 scripts/analyze_all.py --output ~/skill-index.md

# 查找包含特定功能的技能
python3 scripts/search_skills.py "股票" "监控"
```

## How It Works

1. **读取 SKILL.md** - 解析技能的元数据和文档内容
2. **提取结构** - 识别标题、列表、代码块等结构
3. **语义分析** - 理解功能描述和使用场景
4. **生成报告** - 按模板组织信息，生成易读的摘要

## Creative Usage Ideas 💡

### 1. 技能组合推荐
分析多个技能后，自动发现可以组合使用的技能对：
```bash
# 找出可以组合使用的技能
python3 scripts/find_combinations.py
```

输出示例:
```
🔍 技能组合推荐

1. 💡 内容创作流水线
   描述: 搜索资料→总结→创作→影视化
   已安装: tavily-search, summarize, novel-generator
   使用场景: 搜索热点话题→生成小说→改编剧本

2. 💡 GitHub自动化
   描述: 管理stars、自动修复issues
   已安装: github-star-manager
   未安装: gh-issues (建议安装)
   使用场景: 清理过时的 starred repos

🔮 基于描述分析的潜在组合:
  • 数据相关: stock-watcher, tavily-search
  • 内容相关: novel-generator, film-production-assistant
```

### 2. 技能依赖图谱
生成技能之间的依赖关系图：
```bash
# 生成依赖关系图（Mermaid 格式）
python3 scripts/dependency_graph.py --format mermaid

# 输出:
# ```mermaid
# graph TD
#     stock-watcher --> cron
#     github-star-manager --> gh
#     novel-generator --> openai
# ```
```

### 3. 技能使用频率分析
分析工作区中使用记录，找出最常用的技能：
```bash
# 分析使用频率
python3 scripts/usage_stats.py --days 30

# 输出:
# 📊 近30天技能使用统计:
# 1. stock-watcher: 45次 (35%)
# 2. github-star-manager: 23次 (18%)
# 3. novel-generator: 12次 (9%)
```

### 4. 技能能力标签云
为所有技能生成能力标签，快速找到需要的功能：
```bash
# 生成能力标签云
python3 scripts/generate_tags.py

# 输出:
# 🏷️ 技能能力标签:
# 数据获取: stock-watcher, github-star-manager, tavily-search
# 内容创作: novel-generator, film-production-assistant
# 代码开发: gh-issues, agent-browser
```

### 5. 智能技能推荐
根据当前任务描述，推荐最适合的技能：
```bash
# 智能推荐
python3 scripts/recommend_skill.py "我想监控股票并自动发送通知"

# 输出:
# 💡 推荐技能组合:
# 1. stock-watcher (股票监控)
# 2. qqbot-cron (定时任务)
# 3. qqbot-media (发送通知)
#
# 使用流程:
# 1. 用 stock-watcher 添加股票
# 2. 用 qqbot-cron 设置定时检查
# 3. 用 qqbot-media 发送价格提醒
```

### 6. 技能学习路径
为新手生成技能学习路径：
```bash
# 生成学习路径
python3 scripts/learning_path.py --goal "自动化内容创作"

# 输出:
# 🎓 学习路径: 自动化内容创作
# 
# 阶段1: 基础 (1-2天)
#   └─ summarize (内容总结)
#   └─ tavily-search (资料搜集)
#
# 阶段2: 进阶 (3-5天)
#   └─ novel-generator (小说生成)
#   └─ prompt-engineer-ultra (提示词优化)
#
# 阶段3: 高级 (1周+)
#   └─ film-production-assistant (影视制作)
```

### 7. 技能对比矩阵
对比多个相似技能，帮助选择：
```bash
# 对比搜索类技能
python3 scripts/compare_matrix.py tavily-search web-search exa-search

# 输出:
# ┌──────────────┬─────────────┬─────────────┬─────────────┐
# │   功能       │ tavily-search│ web-search  │  exa-search  │
# ├──────────────┼─────────────┼─────────────┼─────────────┤
# │ 实时搜索     │     ✅      │     ✅      │     ✅      │
# │ 内容提取     │     ✅      │     ❌      │     ✅      │
# │ 免费额度     │   1000次/月 │   无限制    │   100次/月  │
# │ 需要API Key  │     ✅      │     ✅      │     ✅      │
# └──────────────┴─────────────┴─────────────┴─────────────┘
```

### 8. 自动化技能审计
定期检查技能库，发现潜在问题：
```bash
# 技能审计
python3 scripts/audit_skills.py

# 输出:
# 🔍 技能审计报告:
# ⚠️  发现 3 个技能缺少 SKILL.md
# ⚠️  发现 2 个技能依赖未安装
# 💡 建议更新: stock-watcher (新版本可用)
```

### 9. 创意用法生成器 ⭐新
为任意技能生成超出常规用法的创意场景：
```bash
# 获取技能的创意用法
python3 scripts/creative_usage.py stock-watcher
```

输出示例:
```
💡 stock-watcher 创意用法指南

🎯 精选创意用法:

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
   步骤:
      1. 设置价格预警
      2. 结合cron定时检查
      3. 通过QQ/Telegram推送通知
   ✅ 价值: 不再错过交易时机

3. 📈 投资组合分析
   💭 管理多只股票，分析整体收益
   ✅ 价值: 从单股监控到组合管理
```

**创意用法特点：**
- 🎯 **超越基础功能** - 不仅限于文档描述的用法
- 🔗 **技能组合** - 推荐与其他技能协同使用
- 💡 **场景化** - 针对具体使用场景给出建议
- 📊 **价值量化** - 说明创意用法带来的价值提升

**支持预设创意用法的技能：**
- stock-watcher - 股票监控的3种创意用法
- novel-generator - 小说生成的3种创意用法
- film-production-assistant - 影视制作的2种创意用法
- tavily-search - 搜索技能的2种创意用法
- summarize - 总结技能的2种创意用法
- character-creator-cn - 角色设计的2种创意用法
- github-star-manager - GitHub管理的2种创意用法

**其他技能：** 自动生成基于描述的智能建议

## Tips

- 对于复杂的技能，分析报告可以节省大量阅读时间
- 对比多个技能的报告，可以快速选择最适合的工具
- 定期运行 analyze_all.py 可以生成技能库的完整索引
- 使用 `--format json` 可以将分析结果导入其他工具进一步处理
