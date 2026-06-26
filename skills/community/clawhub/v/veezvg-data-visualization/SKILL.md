---
name: veezvg-data-visualization
version: 1.0.0
description: |
  根据数据类型智能选择图表，并按统一规范生成专业 Python matplotlib 可视化代码。
  支持三套专业风格模板：BCG（默认绿色简洁风）、The Economist（红线+青蓝媒体风）、McKinsey（亮青+浅灰咨询风）。
  触发场景：用户需要可视化数据、生成图表、画图、制作柱状图/折线图/饼图/散点图/热力图等。
  关键词：可视化、图表、chart、plot、visualization、画图、matplotlib、数据图、经济学人风格、麦肯锡风格、BCG风格
---

# Data Visualization

根据数据类型智能选择图表，按统一规范生成 Python matplotlib 代码。**三套风格均按真实报告视觉提取并可复刻。**

## 工作流程

1. **询问风格** - 若用户未指定风格，展示三套选项供选择
2. **分析数据** - 识别数据类型（时序、分类、占比等）
3. **选择图表** - 参考 `references/chart_selection.md` 匹配最佳图表类型
4. **找对应示例** - **优先从 `examples/` 中找最接近的模板脚本，直接照着改**
5. **查细节规范** - 遇到 examples 没覆盖的场景，查 `references/visualization_spec.md`
6. **输出代码** - 生成完整可运行的 Python 代码

## 风格选项

| # | 风格 | 适用场景 | 主色 |
|---|------|---------|------|
| 1 | **BCG**（默认） | 通用数据分析、研究报告 | 绿色 `#2ca02c` |
| 2 | **The Economist** | 媒体发布、公开报告 | 红线 `#E3120B` + 蓝 `#006BA2` |
| 3 | **McKinsey** | 咨询汇报、高管演示 | 亮青 `#2CBDEF` + 浅灰 `#D4D4D4` |

## 示例脚本（examples/）

**所有示例都是完整可运行的脚本，改数据即用。**

| 脚本 | 风格 | 图表类型 | 参考 |
|------|------|---------|------|
| `bcg_hbar.py` | BCG | 水平柱状图 | 通用调研报告 |
| `economist_hbar.py` | Economist | 水平条形图 | 类别排行对比 |
| `economist_line.py` | Economist | 折线图（时间序列） | 多系列趋势，重点上色 |
| `mckinsey_grouped_vbar.py` | McKinsey | 分组垂直柱 | Exhibit 7 样式 |
| `mckinsey_grouped_hbar.py` | McKinsey | 分组水平条 | Exhibit 4 样式 |
| `mckinsey_stack100.py` | McKinsey | 100% 堆叠单条 | Exhibit 1 样式（Likert-scale） |

## 图表选择速查

| 数据类型 | 推荐图表 |
|---------|---------|
| 趋势变化 | Line Chart |
| 类别比较 | Bar Chart |
| 占比分布 (≤5项) | Pie/Donut |
| 占比分布 (>5项) | Stacked Bar |
| Top vs Others 对比 | 分组柱状图（McKinsey 标配） |
| Likert-scale 分布 | 100% 堆叠单条（渐变色） |
| 相关性 | Scatter Plot |
| 层级结构 | Treemap |

完整 25 种数据类型映射见 `references/chart_selection.md`。

## 各风格核心规范速查

### BCG 风格
- 主色 `#2ca02c`（绿），无渐变
- 标题含样本量 `(N=X)`
- 去除上/右/下边框，无网格线

### The Economist 风格
- **白色背景**（非蓝灰）
- 顶部标志元素：全宽红线 `#E3120B` + 左上角红色方块 tag，都用 `fig.transFigure + clip_on=False`（**禁用 `fig.add_axes`**）
- 所有左对齐元素（红线起点/tag/标题/分类标签）共用基准 `LEFT_X=0.14`
- 主数据系列 `#006BA2`，灰化对照 `#758D99`
- 分类标签必须用 `blended_transform_factory(fig.transFigure, ax.transData)` 对齐，否则会超出 LEFT_X 左端

### McKinsey 风格
- **亮青 `#2CBDEF` + 浅灰 `#D4D4D4`** 二元对照（非单色高亮其他灰化）
- 左上"Exhibit X"小灰字 + 下方全宽细分隔线
- 超大粗体标题（15~17pt），结论句
- 图例在**右上角**，色块 + 文字纵向排列
- 柱子必须**窄**（`width=0.32~0.38`）
- y 轴隐藏刻度，数字直接写在柱上
- 来源注脚写 `Source:` 或"资料来源："

## 三条常见坑（必看）

1. **禁用 `fig.add_axes`**（会与布局系统冲突）。Economist 的红线/tag 用 `ax.plot + mpatches.Rectangle` 配 `fig.transFigure + clip_on=False`。
2. **禁用 `ax.set_ylabel` 放中文单位**（会伸出 `LEFT_X` 左侧破坏对齐）。y 方向单位写进副标题；`set_xlabel` 可用（在 x 轴下方居中）。
3. **轴刻度 formatter 禁止含中文汉字**（字体缺失变方块）。中文单位用副标题或 `set_xlabel`。

完整规范（三套共享工具函数 + 所有代码模板）见 `references/visualization_spec.md`。

## 关键约束

1. 占比数据超过 5 项时，用堆叠柱状图替代饼图
2. 中文必须通过 `FontProperties` 显式设置（`/System/Library/Fonts/STHeiti Light.ttc`）
3. BCG 标题含样本量 `(N=X)`；McKinsey 标题是结论句 + "Exhibit X"编号；Economist 标题是描述性短句
4. 数据标签格式 `{:.1f}%` 或 `{:.2f}`（看量级）
