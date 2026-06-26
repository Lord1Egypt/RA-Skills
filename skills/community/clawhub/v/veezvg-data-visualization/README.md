# data-visualization

一个专门生成**专业咨询 / 媒体报告风格图表代码**的 Skill。

它会根据数据类型自动选择合适图表，并输出可直接运行的 **Python matplotlib** 代码，重点支持三种常见的高质感配图风格：

- **McKinsey**，麦肯锡咨询汇报风
- **BCG**，波士顿咨询简洁分析风
- **The Economist**，经济学人媒体图表风

适合用在研究报告、咨询汇报、行业分析、内容配图、文章插图等场景。

## 效果展示

### BCG 风格

![BCG 风格水平条形图](assets/showcase/bcg-income-hbar.png)

六城居民可支配收入对比，绿色极简、适合研究报告和内部分析。

### The Economist 风格

![The Economist 风格水平条形图](assets/showcase/economist-income-hbar.png)

同一组收入数据改写为经济学人媒体图表语言，顶部红线和蓝色主系列更适合公开内容配图。

### McKinsey 风格

![McKinsey 风格分组横条图](assets/showcase/mckinsey-grouped-hbar.png)

典型咨询图表表达，适合做 Top performers vs Others 之类的对照分析。

![McKinsey 风格柱线组合图](assets/showcase/mckinsey-bar-line-combo.png)

柱线组合图示例，适合同时表达销量与人群规模等双指标趋势。

## 这个 Skill 能做什么

### 1. 按数据类型选图
它不是只会“画柱状图”的模板集合，而是会先判断数据结构，再选更合适的图表形式。

例如：
- 趋势变化 -> 折线图
- 类别比较 -> 柱状图 / 条形图
- Likert 量表分布 -> 100% 堆叠条
- Top vs Others -> 分组柱状图
- 占比项过多 -> 用堆叠条替代饼图

### 2. 输出可运行代码
生成的是完整 **matplotlib Python 脚本**，不是抽象建议。拿去改数据就能用。

### 3. 统一风格规范
内置三套风格规范，不只是换个配色，而是连标题、标注、图例、留白、分隔线、标签对齐方式都做了约束。

## 支持的三套风格

### McKinsey
适合：咨询汇报、高管材料、Exhibit 风格页面

特点：
- 亮青 + 浅灰的二元对照色
- 左上角 Exhibit 编号
- 强结论式标题
- 右上角纵向图例
- 柱子更窄，整体更克制

### BCG
适合：通用分析、研究报告、内部汇报

特点：
- 绿色主色
- 简洁、直给、信息密度高
- 标题中可包含样本量 N
- 去掉多余边框和装饰

### The Economist
适合：公开发布、媒体内容、文章配图

特点：
- 顶部标志性红线 + 红色 tag
- 蓝色主数据系列 + 灰蓝对照色
- 白底、强识别度、偏媒体表达
- 对标题、左侧标签对齐有明确规范

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── examples/
│   ├── bcg_hbar.py
│   ├── economist_hbar.py
│   ├── economist_line.py
│   ├── mckinsey_grouped_hbar.py
│   ├── mckinsey_grouped_vbar.py
│   └── mckinsey_stack100.py
└── references/
    ├── chart_selection.md
    └── visualization_spec.md
```

## examples 里有什么

仓库里的示例都是真正可运行的 matplotlib 脚本。

- `bcg_hbar.py`，BCG 风格水平条形图
- `economist_hbar.py`，经济学人风格水平条形图
- `economist_line.py`，经济学人风格折线图
- `mckinsey_grouped_vbar.py`，麦肯锡风格分组竖柱图
- `mckinsey_grouped_hbar.py`，麦肯锡风格分组横条图
- `mckinsey_stack100.py`，麦肯锡风格 100% 堆叠条图

## references 里有什么

### `references/chart_selection.md`
给出“数据类型 -> 推荐图表类型”的映射，方便在生成代码前先判断用什么图更合适。

### `references/visualization_spec.md`
沉淀三套风格的视觉规范，包括：
- 配色
- 标题层级
- 分隔线
- 标签位置
- 图例样式
- 数据标签格式
- 中文字体处理
- matplotlib 里的实现细节

## 使用方式

### 在 OpenClaw / Agent 场景中
把这个目录作为一个 Skill 使用。用户提出“帮我把这组数据画成麦肯锡风格图表”之类请求时，优先：

1. 判断数据类型
2. 选择图表形式
3. 从 `examples/` 找最接近模板
4. 参考 `references/visualization_spec.md` 补细节
5. 输出完整 Python 代码

### 你可以这样描述需求

- 用经济学人风格画一个折线图
- 把这组问卷结果做成麦肯锡风格 Exhibit
- 用 BCG 风格画 Top 10 排行条形图
- 帮我根据这张表自动选择合适图表并输出 matplotlib 代码

## 适合谁用

- 用户研究员
- 商业分析师
- 咨询顾问
- 内容创作者
- 需要快速做“像报告里那样的图”的人

## 为什么这个 Skill 有价值

很多“图表生成”工具只解决“能画出来”，但不解决“画得像专业报告”。

这个 Skill 的重点是把三类高频视觉风格沉淀成**可复用规范 + 可运行模板**：

- 不是只有灵感，而是能复刻
- 不是只有截图，而是能生成代码
- 不是只有单图，而是能变成持续产出的工作流

## 注意事项

- 中文图表建议显式设置字体
- 占比项太多时不要硬上饼图
- 经济学人风格对对齐要求高，尤其是左侧标签和顶部标志元素
- 麦肯锡风格重点不只是配色，更在于标题语气、图例位置和版式秩序

## 未来可扩展方向

- 增加更多图表模板（散点图、热力图、瀑布图、桑基图）
- 增加 seaborn / plotly 版本
- 增加自动读 CSV / Excel 后直接出图的工作流
- 增加适配中文商业报告的主题模板

## License

如需开源发布，建议补充许可证后再进一步传播。
