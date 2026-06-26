# 📊 PyThesisPlot

> **Claude Code 科研作图 Skill** — 将原始数据转化为符合 Nature/Science 标准的顶刊级图表。

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/stephenlzc/pythesis-plot)](https://github.com/stephenlzc/pythesis-plot/releases)
[![English](https://img.shields.io/badge/English-README-red.svg)](README.md)

---

## 🎯 PyThesisPlot 是什么？

PyThesisPlot 是一个 **Claude Code Skill**，教会 AI 助手如何从原始数据创建顶刊级科研图表。它提供：

- 📊 **智能工作流**：数据 → 分析 → 推荐 → 确认 → 图表
- 🎨 **顶刊品质输出**：300 DPI，符合 Nature/Science 标准
- 🔬 **多领域支持**：生物、心理、经济、化学
- 📁 **规范输出**：带时间戳的目录 + 可复现代码

**触发条件**：当你上传数据文件（CSV/Excel/TXT）并请求作图时自动激活。

---

## 📦 安装

### 给人类用户

复制粘贴这段给你的 AI 助手（Claude Code、Cursor 等）：

```
帮我安装 PyThesisPlot skill：
https://github.com/stephenlzc/pythesis-plot
```

或者如果你喜欢被 YAML 折磨，阅读[安装指南](docs/installation.md)。但说真的，让 AI 去处理吧。人类总是会复制错路径。

### 给 AI 助手

```bash
git clone https://github.com/stephenlzc/pythesis-plot.git ~/.claude/skills/pythesis-plot
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

**完整说明**：[docs/installation.md](docs/installation.md)

---

## 🚀 跳过这篇 README

我们已经过了手动折腾图表的时代。直接粘贴这段给你的 AI：

```
我有一些数据，需要给论文生成顶刊级图表。
用 PyThesisPlot skill 帮我：
https://github.com/stephenlzc/pythesis-plot
```

---

## 🚀 快速开始

安装完成后，只需上传数据并询问：

> "**帮我为论文创建一些图表**"

> "**为我的科研论文绘制这些数据**"

> "**从这个 Excel 文件生成顶刊级图表**"

Skill 将自动：
1. **分析** 你的数据结构和类型
2. **推荐** 合适的图表类型
3. **等待你的确认** 选择图表方案
4. **生成** 300 DPI PNG 图表 + 可复现 Python 代码

---

## 📋 Skill 结构

```
pythesis-plot/
├── SKILL.md                          # Skill 定义（触发条件）
├── README.md                         # 英文文档
├── README.zh-CN.md                   # 本文档
├── scripts/
│   ├── workflow.py                   # 主编排器
│   ├── data_analyzer.py              # 数据分析引擎
│   └── plot_generator.py             # 图表生成引擎
├── references/
│   ├── workflow_guide.md             # 工作流文档
│   ├── chart_types.md                # 图表选择指南
│   ├── style_guide.md                # 视觉标准
│   └── examples.md                   # 代码示例
└── assets/themes/
    ├── academic.mplstyle             # 学术期刊风格
    ├── nature.mplstyle               # Nature 期刊风格
    └── presentation.mplstyle         # 演示汇报风格
```

---

## 🎨 支持的图表类型

| 图表类型 | 适用场景 | 示例 |
|:----------:|:---------|:-----------------|
| 📈 折线图 | 时间序列、趋势 | 基因表达随时间变化 |
| 📊 柱状图 | 分组对比 | 治疗组 vs 对照组 |
| 🎯 箱线图 | 分布、异常值 | qPCR Ct值分布 |
| ⚡ 散点+回归 | 相关性分析 | 剂量-效应关系 |
| 🔥 热力图 | 相关性矩阵 | 多基因表达相关性 |
| 📋 仪表盘 | 多子图组合 | 研究全貌展示 |

---

## 💡 应用示例

### 示例 1：生物医学研究（qPCR 数据）

```
用户："我有 PCOS 研究的 qPCR 数据，帮我创建图表"

AI: 分析 Mouse_PCOS_BRAC1_RawData_108.xlsx...
    检测到：108 样本，3 组，基因表达数据
    
    推荐图表：
    1. 体重对比（柱状图）
    2. BRAC1 表达量（对数刻度柱状图）
    3. qPCR Ct 分布（箱线图）
    4. 2×2 综合仪表盘

用户："全部生成"

AI: ✅ 已在 output/20250312-143052-PCOS/ 生成 4 张顶刊级图表
```

### 示例 2：心理学 RCT 研究

```
用户："绘制我的心理健康干预结果"

AI: 分析 Adolescent_Mental_Health_Intervention_1200.xlsx...
    检测到：1200 参与者，4 组 RCT，前后测数据
    
    推荐图表：
    1. CONSORT 风格研究流程
    2. SDQ 前后对比
    3. 响应者分析（堆叠柱状图）
    4. 效应量森林图

用户："生成方案 1、2、3"

AI: ✅ 已生成 3 张含统计显著性标注的图表
```

---

## ⚙️ 工作原理

### 1. Skill 触发

当你在 `SKILL.md` 中的 YAML `description` 匹配到请求时，skill 自动激活：

```yaml
---
name: pythesis-plot
description: | 
  Python 科研作图工具...
  当用户上传数据文件（txt/md/excel/csv）
  并提到"帮我作图"、"创建图表"、"数据可视化"、
  "论文图表"、"科研绘图"时触发...
---
```

### 2. 工作流阶段

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   数据上传   │────▶│    数据分析  │────▶│    图表推荐   │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                                                ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   生成交付   │◀────│    图表生成  │◀────│   用户确认   │
│ (PNG+代码)  │     │             │     │   (必需)    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 3. 输出组织

所有输出保存到带时间戳的目录：

```
output/
└── 20250312-143052-your-data/
    ├── 20250312-143052-your-data.csv    # 原始数据（重命名）
    ├── analysis_report.md               # 数据分析报告
    ├── plot_config.json                 # 图表配置
    ├── 20250312-143052_plot.py          # 可复现 Python 代码
    └── *.png                            # 300 DPI 图表
```

---

## 📖 文档

- **[工作流程指南](references/workflow_guide.md)** — 完整工作流说明
- **[图表类型](references/chart_types.md)** — 何时使用何种图表
- **[样式规范](references/style_guide.md)** — 配色方案和视觉标准
- **[示例](references/examples.md)** — 代码示例和教程

---

## 🔧 依赖要求

```bash
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

---

## 🤝 贡献指南

欢迎贡献！本 skill 遵循标准 SKILL.md 格式：

1. **Fork** 本仓库
2. **修改** SKILL.md 或添加新图表类型
3. **测试** 使用样本数据
4. **提交** Pull Request

### Skill 格式

```yaml
---
name: pythesis-plot
description: | 
  清晰的触发条件，说明 AI 何时应加载此 skill。
  列出具体短语和上下文。
---

# Skill 正文

## 快速开始
简要说明...

## 功能
- 功能 1
- 功能 2
```

---

## 🌐 多语言

- **English**: [README.md](README.md)
- **中文**: [README.zh-CN.md](README.zh-CN.md)（本文档）

---

## 📄 开源协议

MIT 协议 — 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- 🎨 配色方案参考 [Nature](https://www.nature.com/) 和 [Science](https://www.science.org/) 风格指南
- 📊 可视化最佳实践来自 [Seaborn](https://seaborn.pydata.org/)
- 🎓 学术标准参考 [Matplotlib](https://matplotlib.org/)

---

<div align="center">

**用 ❤️ 为科研工作者打造**

[⬆ 返回顶部](#-pythesisplot)

</div>
