# 可视化规范

支持三套专业风格模板，按用户选择应用对应规范。

---

## 通用约束（所有风格适用）

- **中文字体**: 使用 `/System/Library/Fonts/STHeiti Light.ttc`，通过 `FontProperties` 对象显式设置所有文本元素
- **图表尺寸**: 根据内容调整，一般为 `(10, 6)` 或 `(12, 7)`
- **DPI**: 保存时使用 300 DPI
- **占比数据**: 超过 5 项时用堆叠柱状图替代饼图
- **数据标签**: 百分比格式 `{:.1f}%`

## ⚠️ 布局关键规范（必须遵守，防止内容遮挡）

**核心原则：标题、副标题、来源注脚均不得与数据区域重叠。**

1. **禁止混用 `tight_layout` 和 `fig.add_axes`**  
   `fig.add_axes`（如 Economist 的顶部红色标签栏）与 `tight_layout` 不兼容，会导致布局错乱。  
   凡使用 `fig.add_axes` 的图表，**必须改用 `fig.subplots_adjust`** 显式控制子图边距。

2. **标题文字与数据区域必须分离**  
   使用 `fig.subplots_adjust(top=...)` 在子图上方预留足够空间，再用 `fig.text(x, y, ...)` 将标题放入该空间。  
   **不要**用 `ax.set_title` + 大 `pad` 值来腾挪空间——这在有 `fig.add_axes` 时会失效。

3. **推荐的安全边距设置**

   ```python
   # 有顶部标签栏（Economist 风格）
   fig.subplots_adjust(left=0.10, right=0.90, top=0.72, bottom=0.12)
   # 标题区：fig.text(x, 0.88~0.96, ...)
   # 红色栏：fig.add_axes([0, 0.975, 1, 0.025])

   # 无顶部标签栏（McKinsey / BCG 风格）
   fig.subplots_adjust(left=0.08, right=0.95, top=0.72, bottom=0.14)
   # 标题区：fig.text(x, 0.88~0.96, ...)
   ```

4. **y 轴上限留白**  
   垂直柱状图的 `ax.set_ylim` 上限应比最大数据值高 **15~20%**，确保柱顶标签不被截断。  
   例：最大值为 8.48，则 `ax.set_ylim(0, 10.5)`。

5. **底部来源注脚**  
   使用 `fig.text(x, 0.02~0.03, ...)` 放置，`subplots_adjust(bottom=0.12)` 确保不被裁切。

---

## Style 1：BCG 风格（默认）

### 设计原则
简洁、克制，数据说话。绿色为唯一主色，无渐变，无装饰。

### 规范
| 属性 | 值 |
|------|-----|
| 主色 | `#2ca02c`（BCG 绿） |
| 背景 | 白色 |
| 上/右边框 | 去除 |
| 下/左边框 | 保留（黑色，1px） |
| 网格线 | 关闭 |
| 标题字号 | 20，加粗 |
| 标题内容 | 描述性，含样本量 `(N=X)` |
| 轴标签字号 | 16 |

### 代码模板

```python
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# ── 字体 ──────────────────────────────────────────────
font_path = '/System/Library/Fonts/STHeiti Light.ttc'
fp = FontProperties(fname=font_path)

# ── 配色 ──────────────────────────────────────────────
COLOR_MAIN = '#2ca02c'   # BCG 绿

# ── 数据（示例） ───────────────────────────────────────
labels = ['类别A', '类别B', '类别C', '类别D']
values = [42.5, 31.2, 16.8, 9.5]
N = 200

# ── 画布 ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

# ── 绘图（水平柱状图示例） ─────────────────────────────
bars = ax.barh(range(len(labels)), values, color=COLOR_MAIN, height=0.6)
ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels, fontproperties=fp, fontsize=13)
ax.set_xlabel('占比 (%)', fontproperties=fp, fontsize=16)
ax.set_title(f'维度名称 (N={N})', fontproperties=fp, fontsize=20, fontweight='bold')

# ── 边框处理 ───────────────────────────────────────────
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['left'].set_linewidth(1)

# ── 网格 ───────────────────────────────────────────────
ax.grid(False)

# ── 数据标签 ───────────────────────────────────────────
for i, (bar, val) in enumerate(zip(bars, values)):
    ax.text(val + 0.8, i, f'{val:.1f}%', va='center', fontproperties=fp, fontsize=12)

plt.tight_layout()
plt.savefig('output_bcg.png', dpi=300, bbox_inches='tight')
plt.close()
```

---

## Style 2：The Economist 风格

> 参考：[Making Economist-Style Plots in Matplotlib](https://medium.com/data-science/making-economist-style-plots-in-matplotlib-e7de6d679739)

### 设计原则
严肃媒体风格，数据优先，排版精准。无论图表类型（柱状/折线/Dumbbell），都共享同一套视觉骨架：

**五个必备元素（缺一不可）：**
1. 顶部全宽红色横线（`#E3120B`）
2. 左上角红色方块 tag（`#E3120B`）
3. 左对齐基准线（红线起点 / tag / 标题 / 分类标签都从同一 x 坐标开始）
4. 仅数据轴方向的网格线（其他方向关闭）
5. 底部左侧数据来源注脚

### 共享配色与常量

```python
# ── 字体 ──────────────────────────────────────────────
font_path = '/System/Library/Fonts/STHeiti Light.ttc'
fp      = fm.FontProperties(fname=font_path)
fp_bold = fm.FontProperties(fname=font_path, weight='bold')

# ── Economist 配色（源自 ggthemes + 官网） ───────────
ECON_RED    = '#E3120B'   # 红线 + tag 方块
ECON_BLUE   = '#006BA2'   # 主系列
ECON_CYAN   = '#3EBCD2'   # 次系列 1
ECON_GREEN  = '#379A8B'   # 次系列 2
ECON_YELLOW = '#EBB434'   # 次系列 3（强调）
ECON_GREY   = '#758D99'   # 灰化系列 / 来源注脚
ECON_GRID   = '#A8BAC4'   # 网格线
TEXT_DARK   = '#121212'
TEXT_SUB    = '#555555'

# ── 布局常量（三种图表类型共用） ──────────────────────
LEFT_X       = 0.14   # 左对齐基准：红线起点/tag/标题/分类标签
RED_LINE_Y   = 0.970  # 红线 y 位置（figure 最顶部）
TAG_W, TAG_H = 0.055, 0.030
TITLE_Y      = 0.920  # 标题位置（红线下方）
SUBTITLE_Y   = 0.860  # 副标题位置
SOURCE_Y     = 0.025  # 来源注脚位置
```

### 通用框架函数（复用）

```python
def apply_economist_frame(fig, ax, title, subtitle, source):
    """为任意 Axes 套上经济学人的红线、tag、标题、来源外框。"""
    # ① 红色横线
    ax.plot([LEFT_X, 1.0], [RED_LINE_Y, RED_LINE_Y],
            transform=fig.transFigure, clip_on=False,
            color=ECON_RED, linewidth=2.5, solid_capstyle='butt', zorder=20)
    # ② 左上角红色方块 tag
    ax.add_patch(mpatches.Rectangle(
        xy=(LEFT_X, RED_LINE_Y - TAG_H),
        width=TAG_W, height=TAG_H,
        facecolor=ECON_RED, edgecolor='none',
        transform=fig.transFigure, clip_on=False, zorder=20))
    # ③ 标题、副标题、来源（全部用 fig.text 对齐到 LEFT_X）
    fig.text(LEFT_X, TITLE_Y,    title,
             fontproperties=fp_bold, fontsize=13,
             color=TEXT_DARK, va='top', ha='left')
    fig.text(LEFT_X, SUBTITLE_Y, subtitle,
             fontproperties=fp, fontsize=10.5,
             color=TEXT_SUB, va='top', ha='left')
    fig.text(LEFT_X, SOURCE_Y,   source,
             fontproperties=fp, fontsize=9,
             color=ECON_GREY, va='bottom', ha='left')

def style_economist_axes(ax, grid_axis='y'):
    """通用轴处理：只保留底部轴线，仅一个方向有网格，无刻度线。"""
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['bottom'].set_color('#444444')
    ax.spines['bottom'].set_linewidth(1.2)
    if grid_axis == 'y':
        ax.yaxis.grid(True, color=ECON_GRID, linewidth=1.0, zorder=0)
        ax.xaxis.grid(False)
    else:
        ax.xaxis.grid(True, color=ECON_GRID, linewidth=1.0, zorder=0)
        ax.yaxis.grid(False)
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', length=0, labelsize=10, labelcolor=ECON_GREY)
```

### ⚠️ 四条铁律

1. **红线和 tag 只能用 `ax.plot` / `mpatches.Rectangle` 加 `fig.transFigure + clip_on=False`**，禁用 `fig.add_axes`（会与布局系统冲突）。
2. **背景必须白色**，不是蓝灰（蓝灰是 ggplot 主题的误导，真实经济学人图表是白底）。
3. **轴刻度 formatter 禁止含中文汉字**（会变方块）。
4. **禁用 `ax.set_ylabel` 放单位**：y 轴 label 默认在轴线左外侧（即使用 `loc='top'` 配 `rotation=0`），必然伸出 `LEFT_X` 之外破坏对齐。**y 方向的单位一律写进副标题**（如"城镇居民人均可支配收入，万元"）。`set_xlabel` 在 x 轴下方居中，不会破坏左对齐，可以使用。

---

### 模板 A：水平柱状图（Horizontal Bar Chart）

**适用场景**：分类比较、排行榜。分类名放在**条形外部左侧**，左对齐到 `LEFT_X`。

```python
cities = ['上海', '北京', '杭州', '广州', '深圳', '武汉']
values = [8.48, 8.18, 8.06, 8.05, 7.69, 6.17]

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
# left=0.24 给外部标签留空间；标签本身 x=LEFT_X=0.14
fig.subplots_adjust(left=0.24, right=0.94, top=0.76, bottom=0.10)

y_pos = list(range(len(cities)))
ax.barh(y_pos, values, color=ECON_BLUE, height=0.55, zorder=3)
ax.set_yticks(y_pos)
ax.set_yticklabels([])      # 必须清空默认标签！
ax.set_xlim(0, max(values) * 1.2)
ax.set_xlabel('（单位）', fontproperties=fp, fontsize=11, color=ECON_GREY)

# ── 分类标签：x 用 figure 坐标（对齐 LEFT_X），y 用数据坐标（跟随条形）─
trans = blended_transform_factory(fig.transFigure, ax.transData)
for i, label in enumerate(cities):
    ax.text(LEFT_X, i, label, transform=trans, ha='left', va='center',
            fontproperties=fp, fontsize=13, color=TEXT_DARK, clip_on=False)

# ── 数据标签：条形右端，数据坐标 ───────────────────────
for i, val in enumerate(values):
    ax.text(val + max(values) * 0.015, i, f'{val:.2f}',
            va='center', fontproperties=fp, fontsize=11, color=TEXT_DARK)

style_economist_axes(ax, grid_axis='x')   # 水平条形 → 垂直网格
apply_economist_frame(fig, ax,
    title='标题：对比结论的一句话描述',
    subtitle='副标题：单位与时间范围',
    source='来源：数据来源说明')

plt.savefig('output_economist_hbar.png', dpi=300, bbox_inches='tight', facecolor='white')
```

---

### 模板 B：垂直柱状图（Column Chart）

**适用场景**：分类比较且类别数 ≤ 10。分类名放在**x 轴下方**，与柱子中心对齐。

```python
categories = ['2019', '2020', '2021', '2022', '2023']
values     = [5.2, 6.1, 7.4, 8.0, 8.48]

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
# 垂直柱状图不需要左侧标签空间，left 回到 LEFT_X
fig.subplots_adjust(left=LEFT_X, right=0.94, top=0.76, bottom=0.14)

x_pos = list(range(len(categories)))
ax.bar(x_pos, values, color=ECON_BLUE, width=0.55, zorder=3)
ax.set_xticks(x_pos)
ax.set_xticklabels(categories, fontproperties=fp, fontsize=12, color=TEXT_DARK)
ax.set_ylim(0, max(values) * 1.2)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0f}'))

# ── 数据标签：柱顶上方 ────────────────────────────────
for i, val in enumerate(values):
    ax.text(i, val + max(values) * 0.02, f'{val:.2f}',
            ha='center', va='bottom',
            fontproperties=fp, fontsize=11, color=TEXT_DARK)

style_economist_axes(ax, grid_axis='y')   # 垂直柱 → 水平网格
ax.tick_params(axis='x', labelsize=12, labelcolor=TEXT_DARK)  # x 轴分类保持深色

apply_economist_frame(fig, ax,
    title='标题：趋势结论',
    subtitle='副标题：单位与时间范围',
    source='来源：数据来源说明')

plt.savefig('output_economist_vbar.png', dpi=300, bbox_inches='tight', facecolor='white')
```

---

### 模板 C：折线图（Line Chart / 时间序列）

**适用场景**：时间趋势，多系列对比。核心做法：**用颜色突出 1~2 条重点线，其余系列灰化 `#758D99`，每条线末端标注系列名**（替代传统图例）。

```python
years = list(range(2019, 2024))
shanghai = [7.0, 7.2, 7.7, 7.96, 8.48]
beijing  = [6.8, 7.1, 7.5, 7.77, 8.18]
national = [4.24, 4.38, 4.74, 4.93, 5.18]
series = [
    ('上海', shanghai, ECON_RED),     # 重点
    ('北京', beijing,  ECON_BLUE),    # 重点
    ('全国', national, ECON_GREY),    # 灰化对照
]

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
# 折线图右侧留空间给末端系列名
fig.subplots_adjust(left=LEFT_X, right=0.88, top=0.76, bottom=0.12)

for name, vals, color in series:
    ax.plot(years, vals, color=color, linewidth=2.5,
            marker='o', markersize=6, markerfacecolor=color,
            markeredgecolor='white', markeredgewidth=1.5, zorder=3)
    # ── 末端系列名（替代图例）──
    ax.text(years[-1] + 0.12, vals[-1], name,
            fontproperties=fp_bold, fontsize=11, color=color,
            va='center', ha='left')

ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], fontsize=11, color=TEXT_DARK)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0f}'))
ax.set_xlim(years[0] - 0.3, years[-1] + 1.0)   # 右侧预留末端标签空间

style_economist_axes(ax, grid_axis='y')   # 折线图 → 水平网格
ax.tick_params(axis='x', labelsize=11, labelcolor=TEXT_DARK)

apply_economist_frame(fig, ax,
    title='标题：趋势差异的结论',
    subtitle='副标题：单位与时间范围',
    source='来源：数据来源说明')

plt.savefig('output_economist_line.png', dpi=300, bbox_inches='tight', facecolor='white')
```

---

### 三种图表的关键差异

| 元素 | 水平柱状图 | 垂直柱状图 | 折线图 |
|------|-----------|-----------|--------|
| `subplots_adjust(left)` | **0.24**（给外部标签留空间） | 0.14 | 0.14 |
| `subplots_adjust(right)` | 0.94 | 0.94 | **0.88**（给末端标签留空间） |
| 网格方向 | `grid_axis='x'`（垂直网格） | `grid_axis='y'`（水平网格） | `grid_axis='y'`（水平网格） |
| 分类标签位置 | **条形外部左侧**（blended_transform） | x 轴下方（默认 tick） | 无（线末端标注系列名） |
| 多系列突出方式 | 很少用多系列 | 很少用多系列 | **重点上色，其他灰化** |

---

## Style 3：McKinsey 风格

> 参考：《McKinsey Global Survey on competitive advantage》《中国汽车行业 CEO 季刊》等官方报告

### 设计原则
**极简、高反差对比，Top performer 式的对照叙事。** 大部分麦肯锡图表只做一件事：**把重点组（通常是"Top performers"）用亮青蓝突出，对照组（"Others"）用浅灰**，两色贯穿全报告。

### 七个标志特征
1. **左上小灰字"Exhibit X"**（或中文"图X"），10pt，灰色 `#8C8C8C`
2. **下方细分隔线**：紧贴 Exhibit 标签下方，全宽，浅灰 `#D4D4D4`，0.5pt
3. **超大粗体结论句**标题，15~17pt（比常规标题大得多），黑色 `#051C2C`
4. **副标题/说明**：黑色粗体，12~13pt，附带单位（如"% of respondents"）
5. **图例位于右上角**，色块 + 文字，两系列纵向排列
6. **柱子很窄**（`width=0.32~0.38`），给数据留呼吸空间
7. **数据标签直接写在柱内或柱外**，粗体深色，无需 y 轴刻度

### 配色（严格按真实报告）
| 名称 | 变量 | hex | 用途 |
|------|------|-----|------|
| 亮青蓝（主） | `MCK_CYAN` | `#2CBDEF` | Top performers / 重点系列 |
| 浅灰（辅） | `MCK_GRAY` | `#D4D4D4` | Others / 对照组 |
| 深色文字 | `MCK_DARK` | `#051C2C` | 标题、数据标签 |
| 中灰（Exhibit 标签/来源） | `MCK_META` | `#8C8C8C` | Exhibit 标签、来源注脚 |
| 分隔线 | `MCK_LINE` | `#D4D4D4` | 顶部和底部的细分隔线 |

### 共享配色与工具函数

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

font_path = '/System/Library/Fonts/STHeiti Light.ttc'
fp      = fm.FontProperties(fname=font_path)
fp_bold = fm.FontProperties(fname=font_path, weight='bold')

# ── McKinsey 配色（2025 真实报告提取）──────────────
MCK_CYAN = '#2CBDEF'   # Top performers / 重点
MCK_GRAY = '#D4D4D4'   # Others / 对照
MCK_DARK = '#051C2C'   # 文字主色
MCK_META = '#8C8C8C'   # Exhibit 标签 / 来源
MCK_LINE = '#D4D4D4'   # 分隔线

# ── 布局常量 ──────────────────────────────────────────
LEFT_X       = 0.08
EXHIBIT_Y    = 0.96   # "Exhibit X" 标签
SEP_LINE_Y   = 0.935  # 分隔线 y 位置
TITLE_Y      = 0.90   # 超大结论句标题
SUBTITLE_Y   = 0.78   # 副标题（描述 + 单位）
LEGEND_RIGHT = 0.92   # 图例右上角 x 起点
SOURCE_Y     = 0.04

def apply_mckinsey_frame(fig, ax, exhibit_label, title, subtitle,
                         legend_items, source, notes=None):
    """
    参数：
      exhibit_label: 如 "Exhibit 4" 或 "图4"
      title: 超大结论句
      subtitle: 描述 + 单位，如 "Share of annual budget... % of respondents"
      legend_items: [(name, color), ...]，右上角图例
      source: 资料来源（不含前缀，会自动加 "Source:" 或 "资料来源："）
      notes: 可选，脚注列表 ["¹ ...", "² ..."]
    """
    # ① Exhibit 标签
    fig.text(LEFT_X, EXHIBIT_Y, exhibit_label,
             fontproperties=fp, fontsize=10,
             color=MCK_META, va='top', ha='left')

    # ② 细分隔线（紧贴 Exhibit 下方，全宽）
    ax.plot([LEFT_X, 1 - LEFT_X/2], [SEP_LINE_Y, SEP_LINE_Y],
            transform=fig.transFigure, clip_on=False,
            color=MCK_LINE, linewidth=0.8, zorder=20)

    # ③ 超大结论句标题（分隔线下方）
    fig.text(LEFT_X, TITLE_Y, title,
             fontproperties=fp_bold, fontsize=16,
             color=MCK_DARK, va='top', ha='left')

    # ④ 副标题（加粗，含单位）
    fig.text(LEFT_X, SUBTITLE_Y, subtitle,
             fontproperties=fp_bold, fontsize=11.5,
             color=MCK_DARK, va='top', ha='left')

    # ⑤ 右上角图例（纵向排列，色块 + 文字）
    legend_y = SUBTITLE_Y + 0.02
    for name, color in legend_items:
        ax.add_patch(mpatches.Rectangle(
            xy=(LEGEND_RIGHT, legend_y - 0.018), width=0.02, height=0.016,
            facecolor=color, edgecolor='none',
            transform=fig.transFigure, clip_on=False, zorder=20))
        fig.text(LEGEND_RIGHT + 0.026, legend_y - 0.010, name,
                 fontproperties=fp, fontsize=10,
                 color=MCK_DARK, va='center', ha='left')
        legend_y -= 0.028

    # ⑥ 底部脚注（可选）+ 资料来源
    footer_y = SOURCE_Y + 0.03 * (len(notes) if notes else 0)
    if notes:
        for note in notes:
            fig.text(LEFT_X, footer_y, note,
                     fontproperties=fp, fontsize=8.5,
                     color=MCK_DARK, va='bottom', ha='left')
            footer_y -= 0.022
    fig.text(LEFT_X, SOURCE_Y, f'Source: {source}',
             fontproperties=fp, fontsize=9,
             color=MCK_DARK, va='bottom', ha='left')

def style_mckinsey_axes(ax, show_bottom=True):
    """关闭所有边框和网格；可选保留 x 轴底线。"""
    for spine in ax.spines.values():
        spine.set_visible(False)
    if show_bottom:
        ax.spines['bottom'].set_visible(True)
        ax.spines['bottom'].set_color(MCK_LINE)
        ax.spines['bottom'].set_linewidth(0.8)
    ax.grid(False)
    ax.tick_params(axis='both', length=0, labelsize=10, labelcolor=MCK_DARK)
    ax.set_yticks([])   # 默认隐藏 y 轴刻度（数字写在柱上）
```

### ⚠️ 五条铁律

1. **主色是亮青 `#2CBDEF`、辅色是浅灰 `#D4D4D4`**——不是深蓝，不是中蓝。
2. **柱子必须窄**：`width=0.32~0.38`（默认 0.8 太粗，不像麦肯锡）。
3. **图例位置在右上角**（不是顶部或左上），色块 + 文字，纵向排列。
4. **Exhibit 标签下方必须有细分隔线**，这是标志性视觉锚点。
5. **标题字号要足够大**（15~17pt），远大于 Economist 风格的 13pt——麦肯锡标题是图表主角。

---

### 模板 A：分组垂直柱状图（Top performers vs Others）

**参考：Exhibit 6、Exhibit 7。最常用的麦肯锡图表类型。**

```python
categories = ['Less than\n5% changed', '5% to less\nthan 10%', '10% to less\nthan 20%',
              '20% to less\nthan 30%', '30% to less\nthan 50%', '50% to less\nthan 75%',
              '75% or\nmore']
top_perf = [8, 16, 23, 17, 9, 7, 12]
others   = [20, 30, 26, 11, 5, 2, 0]

fig, ax = plt.subplots(figsize=(11, 7.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X, right=0.96, top=0.70, bottom=0.18)

x = range(len(categories))
width = 0.35   # 窄柱，两组之间有呼吸空间
ax.bar([i - width/2 for i in x], top_perf, width=width,
       color=MCK_CYAN, zorder=3)
ax.bar([i + width/2 for i in x], others, width=width,
       color=MCK_GRAY, zorder=3)

# 柱顶数字（深色粗体）
for i, (t, o) in enumerate(zip(top_perf, others)):
    ax.text(i - width/2, t + 1, f'{t}', ha='center', va='bottom',
            fontproperties=fp_bold, fontsize=11, color=MCK_DARK)
    ax.text(i + width/2, o + 1, f'{o}', ha='center', va='bottom',
            fontproperties=fp_bold, fontsize=11, color=MCK_DARK)

ax.set_xticks(x)
ax.set_xticklabels(categories, fontproperties=fp, fontsize=10, color=MCK_DARK)
ax.set_ylim(0, max(max(top_perf), max(others)) * 1.3)

style_mckinsey_axes(ax)
apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 7',
    title='Top economic performers are much more likely than their peers\nto significantly reallocate resources from year to year.',
    subtitle='Share of annual budget that was reallocated to different\nbusiness areas this year, % of respondents¹',
    legend_items=[('Top performers²', MCK_CYAN), ('Others', MCK_GRAY)],
    source='McKinsey Global Survey on competitive advantage, 1,257 participants')
```

---

### 模板 B：分组水平条形图

**参考：Exhibit 4。类别名在左侧，数值横向延伸。**

```python
categories = ['Review findings from industry associations',
              'Track new product launches of competitors',
              'Monitor acquisitions by competitors',
              'Conduct customer interviews or focus groups',
              'Scan emerging external trends via start-ups',
              'Use AI to identify relevant trends',
              'Use AI to explore new uses',
              'Track competitors outside traditional set',
              'Monitor noncompetitors acquisitions',
              'None of the above']
top_perf = [63, 57, 44, 42, 37, 35, 33, 34, 27, 4]
others   = [53, 50, 37, 31, 24, 24, 22, 21, 19, 4]

fig, ax = plt.subplots(figsize=(11, 8.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
# 横向布局需要更大左边距给类别标签
fig.subplots_adjust(left=0.30, right=0.96, top=0.76, bottom=0.12)

y = range(len(categories))
height = 0.35
ax.barh([i - height/2 for i in y], top_perf, height=height,
        color=MCK_CYAN, zorder=3)
ax.barh([i + height/2 for i in y], others,   height=height,
        color=MCK_GRAY, zorder=3)

ax.set_yticks(y)
ax.set_yticklabels(categories, fontproperties=fp, fontsize=10, color=MCK_DARK)
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.tick_params(axis='x', labelsize=10, labelcolor=MCK_DARK)
# 水平条形需要顶部 x 轴，不要底部
ax.xaxis.tick_top()

style_mckinsey_axes(ax, show_bottom=False)
ax.set_yticks(y)
ax.set_yticklabels(categories, fontproperties=fp, fontsize=10, color=MCK_DARK)

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 4',
    title='Top economic performers track the signs of shifting advantage\nmore than others.',
    subtitle='Actions that respondents\' companies take at least quarterly\nto explore new growth opportunities, % of respondents¹',
    legend_items=[('Top performers²', MCK_CYAN), ('Others', MCK_GRAY)],
    source='McKinsey Global Survey on competitive advantage, 1,257 participants')
```

---

### 模板 C：100% 单条堆叠（Likert-scale / 分布）

**参考：Exhibit 1。展示占比分布，颜色用亮青的渐变层级（越右越深）。**

```python
segments = ['No clear\nperspective', 'Minimally', 'Somewhat', 'Significantly', 'Completely']
values   = [11, 17, 39, 30, 3]
# 从左到右的渐变（可选，越右越深青）
palette  = ['#FFFFFF', '#C3ECFA', '#7BD4ED', '#2CBDEF', '#0088CE']
edges    = [MCK_LINE] + [None]*4   # 第一段白色需要描边

fig, ax = plt.subplots(figsize=(12, 5.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X, right=0.96, top=0.56, bottom=0.35)

left_cursor = 0
for seg, val, color, edge in zip(segments, values, palette, edges):
    ax.barh(0, val, left=left_cursor, height=0.5,
            color=color, edgecolor=edge if edge else color,
            linewidth=0.8 if edge else 0, zorder=3)
    # 段内数字
    text_color = MCK_DARK if color in ['#FFFFFF', '#C3ECFA', '#7BD4ED'] else 'white'
    ax.text(left_cursor + val/2, 0, f'{val}',
            ha='center', va='center',
            fontproperties=fp_bold, fontsize=13, color=MCK_DARK)
    # 段上方标签
    ax.text(left_cursor + val/2, 0.55, seg,
            ha='center', va='bottom',
            fontproperties=fp, fontsize=10, color=MCK_DARK)
    left_cursor += val

ax.set_xlim(0, 100)
ax.set_ylim(-0.6, 1.0)
ax.axis('off')

# 底部 100% 标签
fig.text(0.5, 0.30, '100%', fontproperties=fp, fontsize=10,
         color=MCK_META, va='top', ha='center', style='italic')

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 1',
    title='One-third of executives believe there will be significant changes\nto the nature of their competitive advantage over the next five years.',
    subtitle='Extent of expected change in the competitive advantages of respondents\' companies,\nnext 5 years, % of respondents',
    legend_items=[],   # 100% 堆叠通常不需要图例
    source='McKinsey Global Survey on competitive advantage, 1,257 participants')
```

---

### 三种图表的关键差异

| 元素 | 分组垂直柱（A） | 分组水平条（B） | 100% 堆叠（C） |
|------|----------------|----------------|----------------|
| 柱宽/条高 | `width=0.35` | `height=0.35` | 单条 `height=0.5` |
| 类别标签位置 | x 轴下方 | y 轴左侧 | 各段上方 |
| 数据标签位置 | 柱顶上方 | 条末端外 | 段中央 |
| 图例 | 右上角两项 | 右上角两项 | 无（用颜色渐变） |
| x 轴刻度 | 无 | **0~100** 顶部 | 无 |
