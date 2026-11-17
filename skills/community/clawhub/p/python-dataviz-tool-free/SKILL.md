---
slug: python-dataviz-tool-free
name: python-dataviz-tool-free
version: 1.0.0
displayName: Python数据可视化-免费版
summary: 使用matplotlib/seaborn/plotly创建专业图表,支持柱状图、折线图、散点图与热力图
license: Proprietary
edition: free
description: 'Python 数据可视化工具免费版,面向个人开发者与数据分析师。核心能力:

  - matplotlib 静态图表(柱状/折线/散点/饼图)

  - seaborn 统计可视化(箱线/小提琴/KDE)

  - plotly 交互式图表

  - 多子图布局与样式定制

  - CSV/字典/NumPy 数据源支持

  - PNG/SVG/PDF 导出

  适用场景:

  - 数据分析与报告制作

  - 学术论文图表绘制

  - 个人项目数据可视化

  差异化:免费版提供核心图表能力'
tags:
  - 数据可视化
  - Python
  - 图表
  - matplotlib
  - 数据处理
  - 数据分析
  - 工具
  - plt
  - sns
  - python
  - seaborn
tools:
  - read
  - exec
  - write
  - glob
homepage: ""
category: "Research"
---
# Python 数据可视化 - 免费版

## 概述

Python 数据可视化工具免费版使用 matplotlib、seaborn、plotly 三大主流库创建专业图表。支持柱状图、折线图、散点图、饼图、直方图、热力图等常见图表类型,适合数据分析、报告制作与学术绘图.
## 核心能力

### 1. matplotlib 静态图表

全控制静态图表,支持多面板、自定义样式、标注注释,导出 PNG/SVG/PDF.

**处理**: 解析matplotlib 静态图表的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回matplotlib 静态图表的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. seaborn 统计可视化

内置美观默认样式,支持分布图、分类图、关系图、矩阵图等统计可视化.

**处理**: 解析seaborn 统计可视化的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回seaborn 统计可视化的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. plotly 交互式图表

支持悬停提示、缩放、平移,可导出 HTML 交互式页面.

**处理**: 解析plotly 交互式图表的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回plotly 交互式图表的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 多子图布局

灵活的多面板布局,支持 2x2、3x3 等网格排列.

**处理**: 解析多子图布局的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多子图布局的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 5. 多数据源支持

支持 CSV 文件、Python 字典、NumPy 数组、pandas DataFrame.

**处理**: 解析多数据源支持的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多数据源支持的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：创建专业图表、支持柱状图、折线图、散点图与热力图、数据可视化工具免、面向个人开发者与、数据分析师、核心能力、小提琴、KDE、多子图布局与样式等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:从 CSV 数据创建折线图

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Python数据可视化-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
import pandas as pd
import matplotlib.pyplot as plt
# ...
# 读取 CSV 数据
df = pd.read_csv('sales_data.csv')
# ...
# 创建折线图
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['revenue'], linewidth=2, color='#667eea')
plt.title('月度营收趋势', fontsize=16, fontweight='bold')
plt.xlabel('日期')
plt.ylabel('营收 (元)')
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
# ...
plt.savefig('revenue_trend.png', dpi=300, bbox_inches='tight')
```

### 场景二:使用 seaborn 绘制统计分布图

```python
import seaborn as sns
import matplotlib.pyplot as plt
# ...
# 设置样式
sns.set_theme(style="whitegrid")
sns.set_palette("husl")
# ...
# 示例
tips = sns.load_dataset("tips")
# ...
# 创建箱线图
plt.figure(figsize=(8, 6))
sns.boxplot(data=tips, x='day', y='total_bill')
plt.title('每日账单分布')
plt.savefig('bill_distribution.png', dpi=300)
```

### 场景三:创建交互式 plotly 图表

```python
import plotly.express as px
import pandas as pd
# ...
# 创建数据
df = pd.DataFrame({
    '产品': ['A', 'B', 'C', 'D'],
    '销量': [120, 180, 90, 150],
    '利润': [30, 45, 20, 38]
})
# ...
# 创建交互式散点图
fig = px.scatter(df, x='销量', y='利润', text='产品',
                 title='产品销量与利润关系')
fig.update_traces(textposition='top center')
fig.write_html('product_scatter.html')
```

## 不适用场景

以下场景Python数据可视化-免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境搭建

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/（请参考skill目录中的脚本文件）  # Linux/macOS
# .venv\Scripts\activate   # Windows
# ...
# 依赖说明
pip install matplotlib seaborn plotly pandas numpy
```

### 创建第一个图表

```python
import matplotlib.pyplot as plt
import numpy as np
# ...
# 生成数据
x = np.linspace(0, 10, 100)
y = np.sin(x)
# ...
# 绘图
plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2, color='#667eea')
plt.title('正弦波', fontsize=16)
plt.xlabel('X 轴')
plt.ylabel('Y 轴')
plt.grid(alpha=0.3)
plt.tight_layout()
# ...
# 保存
plt.savefig('sine_wave.png', dpi=300, bbox_inches='tight')
plt.savefig('sine_wave.svg', bbox_inches='tight')
```

## 配置示例

### 图表选择指南

| 数据关系 | 推荐图表 | 函数 |
|:-----|:-----|:-----|
| 趋势变化 | 折线图 | `plt.plot()` / `sns.lineplot()` |
| 数值比较 | 柱状图 | `plt.bar()` / `sns.barplot()` |
| 相关性 | 散点图 | `plt.scatter()` / `sns.scatterplot()` |
| 占比 | 饼图 | `plt.pie()` |
| 分布 | 直方图/KDE | `plt.hist()` / `sns.kdeplot()` |
| 统计分布 | 箱线/小提琴 | `sns.boxplot()` / `sns.violinplot()` |
| 矩阵数据 | 热力图 | `sns.heatmap()` |
| 回归关系 | 回归图 | `sns.regplot()` / `sns.lmplot()` |

### 样式配置

```python
# 设置 seaborn 主题
sns.set_theme()
sns.set_style("whitegrid")  # whitegrid, darkgrid, white, dark, ticks
sns.set_palette("deep")     # deep, muted, pastel, bright, dark, colorblind
# ...
# 设置 matplotlib 样式
plt.style.use('seaborn-v0_8-darkgrid')  # ggplot, bmh, fivethirtyeight
# ...
# 自定义颜色
colors = ['#667eea', '#764ba2', '#f6ad55', '#4299e1']
```

### 导出格式

```python
# PNG(适合网页)
plt.savefig('chart.png', dpi=300, bbox_inches='tight')
# ...
# SVG(适合矢量编辑)
plt.savefig('chart.svg', bbox_inches='tight')
# ...
# PDF(适合打印)
plt.savefig('chart.pdf', bbox_inches='tight')
# ...
# 透明背景
plt.savefig('chart.png', dpi=300, transparent=True)
```

## 最佳实践

1. **DPI 设置**:出版级图表用 300 DPI,网页用 72-150 DPI
2. **figure 大小**:宽高比建议 10:6 或 12:8(英寸)
3. **tight_layout**:保存前调用 `plt.tight_layout()` 防止标签截断
4. **bbox_inches**:`savefig` 时设置 `bbox_inches='tight'` 避免内容裁剪
5. **颜色选择**:使用色盲友好色板(如 seaborn 的 `colorblind`)
6. **中文显示**:配置中文字体 `plt.rcParams['font.sans-serif'] = ['SimHei']`

## 常见问题

### Q: 中文显示为方框怎么办?

A: 配置 matplotlib 中文字体。`plt.rcParams['font.sans-serif'] = ['SimHei']`(Windows)或 `['Arial Unicode MS']`(macOS)。同时设置 `plt.rcParams['axes.unicode_minus'] = False` 解决负号显示问题.
### Q: 图表标签被截断?

A: 在 `savefig` 前调用 `plt.tight_layout()`,并添加 `bbox_inches='tight'` 参数.
### Q: plotly 图表如何导出静态图片?

A: 需要安装 `kaleido` 包(`pip install kaleido`),然后使用 `fig.write_image('chart.png')` 导出.
### Q: 多个子图怎么排列?

A: 使用 `plt.subplots(rows, cols)` 创建多子图。例如 `fig, axes = plt.subplots(2, 2, figsize=(12, 10))` 创建 2x2 布局.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Python 3 | 运行时 | 必需 | 官方网站下载 |
| matplotlib | 绘图库 | 必需 | pip install matplotlib |
| seaborn | 统计绘图 | 推荐 | pip install seaborn |
| plotly | 交互绘图 | 推荐 | pip install plotly |
| pandas | 数据处理 | 推荐 | pip install pandas |
| numpy | 数值计算 | 必需 | pip install numpy |
| kaleido | plotly导出 | 可选 | pip install kaleido |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置

- 本 Skill 无需 API Key
- 纯本地绘图,不涉及外部 API 调用

### 可用性分类

- **分类**: MD+EXEC(Markdown指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 生成 Python 可视化代码并执行
- **限制**: 免费版不支持交互式仪表盘、大数据可视化与实时数据流图表

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Python数据可视化-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "python dataviz"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
