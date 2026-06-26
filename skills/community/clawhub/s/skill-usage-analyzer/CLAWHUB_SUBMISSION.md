# ClawHub 技能提交材料

## 📋 基本信息

| 字段 | 内容 |
|------|------|
| **技能ID** | skill-usage-analyzer |
| **名称** | Skill Usage Analyzer |
| **版本** | 1.0.0 |
| **作者** | OpenClaw Community |
| **许可证** | MIT |
| **分类** | Development, Productivity, Documentation |

## 📝 技能描述

**一句话描述**: 智能分析 OpenClaw 技能，生成使用指南、创意用法和组合推荐

**详细描述**: 
Skill Usage Analyzer 是一个智能技能分析工具，帮助用户快速理解和使用任何 OpenClaw 技能。它不仅能提取 SKILL.md 的关键信息，还能发现技能之间的组合可能性，提供超出文档描述的创意使用场景。

## 🎯 核心功能

1. **📖 智能解析** - 自动提取 SKILL.md 的关键信息
2. **💡 创意用法** - 为技能提供6种创意使用场景
3. **🔗 组合推荐** - 发现可以协同使用的技能组合
4. **🎯 智能推荐** - 根据任务描述推荐最适合的技能
5. **📊 对比矩阵** - 对比多个相似技能，帮助选择
6. **📦 批量分析** - 一键分析所有已安装技能

## 💻 使用方法

```bash
# 分析单个技能
python3 scripts/analyze_skill.py /path/to/skill/SKILL.md

# 获取创意用法
python3 scripts/creative_usage.py stock-watcher

# 发现技能组合
python3 scripts/find_combinations.py

# 智能推荐
python3 scripts/recommend_skill.py "我想监控股票价格"

# 对比技能
python3 scripts/compare_matrix.py skill1 skill2

# 批量分析
python3 scripts/analyze_all.py -o skill-index.md
```

## 📦 文件清单

```
skill-usage-analyzer/
├── SKILL.md                    # 技能文档
├── README.md                   # 使用指南
├── LICENSE                     # MIT许可证
├── CHANGELOG.md                # 更新日志
├── package.json                # NPM配置
├── install.sh                  # 安装脚本
├── .clawhub/meta.json          # ClawHub元数据
├── scripts/
│   ├── analyze_skill.py        # 基础分析
│   ├── analyze_all.py          # 批量分析
│   ├── creative_usage.py       # 创意用法
│   ├── find_combinations.py    # 技能组合
│   ├── recommend_skill.py      # 智能推荐
│   └── compare_matrix.py       # 对比矩阵
└── tests/
    └── test_analyze_skill.py   # 单元测试
```

## 🔧 系统要求

- **Python**: >= 3.6
- **OpenClaw**: 任意版本
- **依赖**: 无（仅使用Python标准库）

## 🎨 图标

**Emoji**: 🔍

**自定义图标**（可选）: 可以提供一个 128x128 的 PNG 图标

## 📸 截图

### 1. 基础分析
```
🔍 技能分析报告: stock-watcher
════════════════════════════════════════════════════════════

📋 基本信息
────────────────────────────────────────────────────────────
名称: stock-watcher
描述: Manage and monitor a personal stock watchlist...

🎯 核心功能
────────────────────────────────────────────────────────────
1. 添加股票
2. 删除股票
3. 查看列表
4. 行情总结
```

### 2. 创意用法
```
💡 stock-watcher 创意用法指南

1. 📊 智能选股助手
   💭 结合AI分析，自动筛选潜力股票
   步骤:
      1. 批量添加关注的板块股票
      2. 筛选涨幅/跌幅异常的股票
      3. 用AI分析基本面和技术面
   ✅ 价值: 从手动监控升级为智能选股
```

### 3. 技能组合
```
🔍 技能组合推荐

1. 💡 内容创作流水线
   描述: 搜索资料→总结→创作→影视化
   已安装: tavily-search, summarize, novel-generator
   使用场景: 搜索热点话题→生成小说→改编剧本
```

## 🏷️ 标签

`skill`, `analyzer`, `usage`, `documentation`, `cli`, `productivity`, `development`

## 🔗 相关链接

- **仓库**: https://github.com/openclaw-community/skill-usage-analyzer
- **问题反馈**: https://github.com/openclaw-community/skill-usage-analyzer/issues
- **文档**: https://github.com/openclaw-community/skill-usage-analyzer#readme

## 📊 使用统计

- **下载量**: 0（新发布）
- **安装量**: 0（新发布）
- **评分**: 待用户评分

## ✅ 自检清单

- [x] 包含完整的 SKILL.md
- [x] 包含 README.md 使用指南
- [x] 包含 LICENSE 许可证文件
- [x] 包含 CHANGELOG.md 更新日志
- [x] 包含 .clawhub/meta.json 元数据
- [x] 所有脚本都有可执行权限
- [x] 无外部依赖（仅使用标准库）
- [x] 包含测试文件
- [x] 包含安装脚本
- [x] 代码注释完整

## 📝 更新日志

### v1.0.0 (2026-03-21)

**新增功能:**
- 基础技能分析功能
- 创意用法生成器
- 技能组合发现
- 智能技能推荐
- 技能对比矩阵
- 批量分析所有技能

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

## 📞 联系方式

- GitHub Issues: https://github.com/openclaw-community/skill-usage-analyzer/issues
- Email: your-email@example.com

---

**提交日期**: 2026-03-21
**提交者**: OpenClaw Community
