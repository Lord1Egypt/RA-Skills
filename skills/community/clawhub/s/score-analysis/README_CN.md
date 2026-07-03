# 📊 成绩分析 Skill

AI驱动的班级成绩分析工具，生成可视化图表和专业报告，支持学校品牌定制。

[![OpenClaw Skills](https://img.shields.io/badge/OpenClaw-Skills-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ 功能特性

- 📊 **自动识别表头** - 支持Excel/CSV，合并单元格、中英文混合表头
- 📈 **多维度分析** - 横向（同层次班级）& 纵向（时间趋势）对比
- 🎯 **临界生识别** - 距上线分数线差X分以内的学生，配雷达图
- 📉 **偏科诊断** - 识别严重偏科学生
- 📋 **分组雷达图** - 按学生类型分组（临界生、偏科生）
- 📄 **专业报告** - Word格式，三线表、嵌入图表
- 🎨 **品牌定制** - 支持学校logo、配色、页眉页脚

## 🚀 快速开始

### 安装

```bash
# 通过 OpenClaw
openclaw skills install score-analysis

# 或手动复制到skills目录
cp -r score-analysis ~/.openclaw/workspace/skills/
```

### 依赖

```bash
pip install python-docx matplotlib pandas numpy openpyxl
```

### 使用方法

1. 提供成绩数据（Excel/CSV）
2. Skill自动识别表头并验证数据
3. 用户确认数据准确性
4. 运行分析，生成图表和报告

## 📋 工作流程

```
数据输入 → 表头识别 → 数据验证 → 分析 → 图表 → 报告 → PPT（可选）
    ↓           ↓           ↓        ↓       ↓       ↓
  自动识别    自动检测    用户确认   多维度   雷达图   Word文档
  文件格式                准确性     分析     分组    品牌定制
```

## 📊 分析维度

### 横向对比（同层次班级）
- 总分均分对比
- 各科均分对比
- 分数段分布对比
- 特控线/本科线上线率对比
- 尖子生分布对比

### 纵向对比（时间维度）
- 班级均分变化趋势
- 上线人数变化
- 学生排名波动
- 学科成绩变化

### 个体分析
- 学生成绩波动（稳定性）
- 偏科诊断（学科均衡性）
- 进步/退步归因
- 临界生识别（差X分上线）

## 📈 图表类型

| 图表 | 说明 |
|------|------|
| 各科均分柱状图 | 对比各科平均分 |
| 班级对比图 | 与同层次班级对比 |
| 分数段分布图 | 分数段人数分布 |
| 临界生雷达图 | 距上线差10分以内的学生 |
| 偏科生雷达图 | 偏科指数最高的学生 |

## 📄 报告输出

专业Word报告包含：
- 学校logo和品牌元素
- 三线表（科研风格）
- 嵌入图表
- 高亮框（强调关键结论）
- 页眉页脚（含页码）

## ⚙️ 配置

### 学科成绩取值规则

| 学科 | 默认成绩类型 |
|------|-------------|
| 语文、数学、英语、物理 | 原始分 |
| 化学、生物、政治、地理 | 赋分 |
| 总分 | 赋分总分 |

### 自定义

编辑 `scripts/generate_report.py` 自定义：
- 学校配色（第12-19行）
- 报告布局
- 图表样式

## 📁 目录结构

```
score-analysis/
├── SKILL.md                 # 技能说明
├── README.md                # 英文文档
├── README_CN.md             # 中文文档
├── LICENSE                  # MIT协议
├── CONTRIBUTING.md          # 贡献指南
├── scripts/
│   ├── create_template.py           # 模板生成器
│   ├── generate_report_from_template.py  # 基于模板生成报告
│   ├── generate_radar_charts.py     # 雷达图生成器
│   └── generate_report.py           # 直接生成报告
├── references/
│   └── analysis_framework.md        # 分析框架
├── assets/
│   └── report_template.docx         # Word模板
└── examples/
    └── sample_data.json             # 示例数据
```

## 🤝 贡献

欢迎贡献！请先阅读 [贡献指南](CONTRIBUTING.md)。

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- 为 [OpenClaw](https://openclaw.ai) 生态构建
- 图表生成：[matplotlib](https://matplotlib.org/)
- 文档生成：[python-docx](https://python-docx.readthedocs.io/)
