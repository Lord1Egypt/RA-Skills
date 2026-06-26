# Shiny 组件 → 教学用途的经验判断

替代幻灯片的核心思路转变：幻灯片是**单向播放**，dashboard 是**让学生动手改输入、即时看结果**。每个组件的价值不在"显示信息"，而在它能把哪种教学内容变成**可操作的学习闭环**。下面是逐组件的经验判断。

## 输入组件（给学生"动手"的把手）

| 组件 | 最适合教什么 | 经验判断 |
|---|---|---|
| `sliderInput` | **参数因果、敏感性**："如果 X 变大会怎样" | 教学价值最高的输入。把抽象关系变成可拖动的实验。加 `animate = TRUE` 可自动播放，像放动画演示时间演化 |
| `radioButtons` | 切换**视角/模型/案例**（选项少、要全部可见） | 选项 ≤5 且想让学生看到所有选项时用；强调"互斥的几种情况" |
| `selectInput` | 切换**数据集/对象**（选项多） | 选项多（国家、变量、章节）时用，省空间；`multiple = TRUE` 可多选叠加 |
| `checkboxGroupInput` | **叠加图层/条件对比** | 让学生勾选"显示哪几组"，做加减法对比 |
| `checkboxInput` | 单个**开关**（显示参考线/答案/注释） | 配合"显示/隐藏"渐进揭示 |
| `numericInput` | **精确设定**（样本量 n、显著性水平 α） | 需要确切数值而非范围拖动时 |
| `actionButton` | **推进步骤、揭示答案、运行模拟、提交测验** | 替代幻灯片"点一下出下一点"。务必配 `eventReactive`/`observeEvent`，不要让结果在点之前就显示 |
| `textInput`/`textAreaInput` | 学生**自由输入探索**（输入函数式、句子、关键词） | 开放式探究；注意校验非法输入避免报错 |
| `dateRangeInput` | **时间窗口**选择 | 时间序列、历史数据教学 |

> 别堆控件。一屏 2–4 个输入就够；每多一个控件，学生的认知负担就多一分。问自己：这个控件去掉，核心概念还讲得清吗？讲得清就去掉。

## 输出组件（呈现"结果"的舞台）

| 组件（包） | 最适合展示什么 | 经验判断 |
|---|---|---|
| `plotOutput`（ggplot2/base） | **静态概念图、统计图** | 最通用。配 `thematic` 自动跟主题配色。讲分布/趋势/关系的主力 |
| `plotlyOutput`（plotly） | **交互探索**：hover 看精确值、缩放、图例点选隐藏 | 想让学生"自己发现"数据细节时用；比静态图多一层探究感。注意比 ggplot 重 |
| `DTOutput`（DT） | **原始数据、对照表**（可排序/搜索/分页） | 展示数据集让学生翻看、找规律；大表必用（自动分页） |
| `value_box`（bslib）/`valueBox`（shinydashboard） | **核心数字、take-home 结论** | 替代幻灯片的"大字结论"。把一节最该记住的一个数/一句话做成醒目方块 |
| `verbatimTextOutput` | **代码输出、模型 `summary()`、统计结果** | 代码教学、回归/检验结果原样呈现，保留 R 的等宽对齐 |
| `uiOutput` + `renderUI` | **动态/分步揭示、条件内容** | 按输入或步骤动态生成 UI；分步讲解的引擎 |
| `textOutput`/`htmlOutput` | **随输入变化的一句话解释** | 让结论"会说话"：参数一变，下面的文字解释跟着变 |
| `uiOutput` + `withMathJax` | **数学公式（可随参数变化）** | 推导、可调公式；`withMathJax()` 包住含 `$$...$$` 的内容 |
| `leafletOutput`（leaflet） | **地图** | 地理、区域数据、流行病传播、历史地图 |
| `grVizOutput`（DiagrammeR）/ visNetwork | **流程图、概念图、关系网络、决策树** | 讲"结构与关系"；DiagrammeR 用 Graphviz/Mermaid 语法 |
| `imageOutput`/`renderImage` | 现成**照片/图片/实验图** | 不是所有内容都要画；史料图、显微照片直接放 |

## 布局 / 容器（组织一节课的骨架，bslib）

| 组件 | 教学角色 |
|---|---|
| `nav_panel`（在 `page_navbar` 里） | **一个"章节"**——替代幻灯片"节"的主结构，顶部 tab 切换 |
| `card` + `card_header` | **一个知识块**——把相关的控件+输出+说明装进一张卡 |
| `layout_sidebar` / `sidebar()` | **"控制台 + 舞台"**：边栏放控件，主区放结果。参数探索类的标准布局 |
| `accordion` / `accordion_panel` | **渐进式披露**：次要/深入内容折叠，点开才看；FAQ、可选拓展 |
| `navset_card_tab` / `tabsetPanel` | **并置对比**：同一主题的几个面（如"假设/推导/应用/练习"） |
| `layout_columns` / `layout_column_wrap` | 并排多张卡/图，做**对照** |
| `value_box` 一行 | 一节开头/结尾的**关键指标条** |
| `conditionalPanel` | **分支讲解**：按选择显示对应内容 |

## 教学内容 → 组件组合 → 对应 template

把要讲的东西落到一种组合，再去 `templates/` 取现成骨架（用法建议见 SKILL.md）：

| 你要讲…… | 组件组合 | template |
|---|---|---|
| 一整节课/多主题（替代整套幻灯片） | `page_navbar` + 多个 `nav_panel`，每节 card + 图 | `navbar-lecture.R` |
| 一个可调参数的模型/关系 | `layout_sidebar`（slider）+ `plotlyOutput` + `textOutput` 解释 | `param-explorer.R` |
| 需要"一点一点出现"的讲解/推导 | `actionButton` + `uiOutput` 分步 +（可选）`accordion` | `stepwise-reveal.R` |
| 几个概念/学派/案例的对比 | `navset_card_tab` 或并置 `layout_columns` | `concept-compare.R` |
| 一份数据的分析叙事 | `value_box` 行 + `selectInput` + `plotlyOutput` + `DTOutput` | `data-story.R` |
| 课堂自测/即时投票 | `radioButtons` + `actionButton` + 即时反馈 `uiOutput` | `quiz-checkpoint.R` |

## 三条总原则

1. **每屏一个核心观点**。dashboard 替代幻灯片，不是把整本书塞进一页。一个 `nav_panel` 只承载一个能说清的点。
2. **控件是给学生动手的，不是给你点的**。如果一个滑块你只会拖到某个固定值讲完就走，那它该是静态图。留下来的控件都要值得学生亲手试。
3. **让结果"会解释自己"**。改了输入，除了图变，最好有一句 `textOutput` 文字跟着变（"当 n 增大，置信区间变窄"）——把"看到现象"接到"理解原因"。
