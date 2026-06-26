---
name: shiny-teaching-dashboard
description: 用 R 语言 Shiny 制作课堂讲解 dashboard，替代幻灯片（PPT）。当用户想把课程内容/讲义/某一章做成可交互的网页讲解、用 Shiny 做教学演示、把 PPT 换成能让学生动手调参数看结果的看板，或提到 bslib/shinydashboard/sliderInput/plotly/value_box 等 Shiny 组件用于教学时使用。产出单文件 app.R（R + Shiny），内置 5 套配色方案（bslib bs_theme）、各 Shiny 组件用于展示什么教学内容的经验判断、以及 6 个可复制调用的组件组合 template（章节式讲座/参数探索/分步揭示/概念对比/数据叙事/课堂自测），每个 template 在本 SKILL.md 给出了用法建议。即使用户只说"用 Shiny 做个教学演示/把这章做成交互的/不想用 PPT 了"，只要意图是用 R Shiny 做课堂展示，也应使用本 skill。
---

# Shiny Teaching Dashboard：用 Shiny 做替代幻灯片的课堂讲解

把一节课做成**单文件 `app.R`**：学生不再被动看播放，而是动手改输入、即时看结果。核心思维转变——**幻灯片是单向播放，dashboard 是可操作的学习闭环**。

## 四条核心原则

1. **每屏一个核心观点**——一个章节（`nav_panel`）只承载一个能讲清的点，不要把整本书塞进一页。
2. **控件是给学生动手的**——留下来的每个 `sliderInput`/`radioButtons` 都要值得学生亲手试；只会被你拖到固定值的，应该是静态图。
3. **让结果会解释自己**——改了输入，除了图变，最好配一句随之变化的 `textOutput`，把"看到现象"接到"理解原因"。
4. **按真实教室设计**——投影 + 后排看不清：字号放大、元素少而大、本地 `runApp()` 跑最稳、按光线选明暗配色。

## 工作流（5 步）

1. **定结构、选架构**：这节课讲几个点？哪些点适合让学生动手？据此从 `references/layout-patterns.md` 选整体骨架（章节式 `page_navbar` 最常用 / 控制台+舞台 / 侧边栏菜单 / 经典 shinydashboard）。
2. **选一个 template 作起点**：按下面《Templates 用法建议》挑最贴近的，复制到 `app.R`。
3. **把内容落到组件**：用 `references/components.md` 的经验判断，决定每个点"用什么输入让学生动手、用什么输出呈现结果"。别堆控件，一屏 2–4 个足够。
4. **选配色**：按学科语境从 `references/color-schemes.md` 选一套 `bs_theme()`，注意课堂投影优先高对比/大字号那套。
5. **填好、跑通、交付**：装包 → 本地 `shiny::runApp("app.R")` 跑通 → 检查无报错。**plot 里有中文记得用 plotly 或 showtext**（见 `references/setup-and-run.md`），否则中文是方框。

## 组件 → 教学用途（速查，详见 references/components.md）

- 让学生动手：`sliderInput`（参数因果，最有价值）、`radioButtons`（切视角）、`actionButton`（推进/揭示/提交）、`selectInput`（切数据集）。
- 呈现结果：`plotlyOutput`（交互探索图）、`plotOutput`（ggplot 概念图）、`DTOutput`（可翻查的数据表）、`value_box`（核心数字/结论）、`verbatimTextOutput`（代码/统计输出）、`uiOutput`（动态/分步内容）。
- 组织骨架：`nav_panel`（=一节）、`card`（=一个知识块）、`layout_sidebar`（控制台+舞台）、`accordion`（折叠的深入内容）、`navset_card_tab`（并置对比）。

## Templates 用法建议

6 个完整可运行的 `app.R` 在 `templates/`（语法均已校验）。复制后把占位内容换成你的，保留结构。挑选指南：

- **`navbar-lecture.R` — 章节式讲座（★默认首选，替代整套幻灯片）**
  何时用：把一整章/一节课做成交互讲解，多个并列主题。顶部每个 tab 是一"节"（引入/原理/应用/小结），跟着点着走。
  装：shiny, bslib, bsicons, ggplot2。改造：增删 `nav_panel()` 调整章节；"原理"节里那个 slider→plot 换成你的可调演示；"小结"节的 `value_box` 放本章 take-home。大多数"把这章做成交互的"需求从它起步。

- **`param-explorer.R` — 参数探索器（讲透一个可调模型）**
  何时用：聚焦讲清**一个**含参数的模型/关系（分布、函数、供需、物理定律……），让学生拖参数看曲线怎么变。
  装：shiny, bslib, plotly。改造：把"正态分布"换成你的模型，sidebar 放它的关键参数，主区 `plotlyOutput` 画随参数变化的图，`value_box` 显示当前关键读数。plotly 中文免处理。

- **`stepwise-reveal.R` — 分步揭示（替代幻灯片"逐点出现"）**
  何时用：推导、解题、论证——需要按节奏一步步揭示、留悬念的内容。点"下一步"逐条出现。
  装：shiny, bslib。改造：把推导拆进 `steps` 列表（每步 `h` 标题 + `b` 正文，正文可含公式/HTML）；可选的深入材料放进 `accordion`。

- **`concept-compare.R` — 概念/案例/学派对比**
  何时用：讲"两种理论""三种方法""正反观点"等需要对比的内容。前几个 tab 各讲一个视角，最后一页并置三栏按维度对照。
  装：shiny, bslib。改造：每个 `nav_panel` 填一个视角的主张+证据；并置页按你的对比维度（假设/适用/局限……）逐行对齐。纯展示，server 为空。

- **`data-story.R` — 数据叙事**
  何时用：带学生分析一份数据集，讲"从数据里看出了什么"。关键指标 + 自选 X/Y 的交互散点 + 可翻查原始表。
  装：shiny, bslib, plotly, DT。改造：把 `dat` 换成你的数据（`read.csv` 或随堂数据），`value_box` 放最该强调的几个数，`selectInput` 的 choices 跟着你的变量名走。

- **`quiz-checkpoint.R` — 课堂自测/投票**
  何时用：一节讲完做巩固检查点，或课堂即时提问。选答后点"提交"给即时对错+讲解。
  装：shiny, bslib。改造：把题目填进 `quiz` 列表（`q` 题干 / `opts` 选项 / `ans` 正确项序号 / `why` 讲解）。注意选项文字里别用英文双引号（会断字符串），用中文「」。

## 输出约定

- 产出一个**单文件 `app.R`**（教学分发最省事），文件名或所在文件夹用 kebab-case 反映主题。默认写到当前工作目录，用户指定路径就用用户的。
- **不要把整份 R 源码贴进对话**——用 Write 写文件，对话里只给：路径、`install.packages(...)` 一行、`shiny::runApp("…")` 一行、以及一句说明（这个 app 分几节、关键交互是什么、用了哪个 template 和哪套配色）。
- 本环境通常无法替用户启动 Shiny GUI/浏览器，**交付即文件 + 运行命令**；如能用 `Rscript -e "parse('app.R')"` 验证语法就先验一下再交付。

## 渐进式披露：何时读哪个文件

| 你正要…… | 读 |
|---|---|
| 选整体骨架（章节式/控制台+舞台/侧边栏/经典看板）、处理课堂投影演示 | `references/layout-patterns.md` |
| 判断某教学内容该用哪个输入/输出/容器组件 | `references/components.md` |
| 选配色、让图表配色跟随主题、字体设置 | `references/color-schemes.md` |
| 装包/运行/部署/**plot 中文字体**/reactive 速记 | `references/setup-and-run.md` |
| 要现成的组件组合骨架 | `templates/` 下对应文件 + 上面的用法建议 |

## 常见反模式（别犯）

- ❌ 把 PPT 逐页搬成静态卡片——那只是网页版 PPT，没用上 Shiny 的交互价值。每节问"学生能动手试什么"。
- ❌ 一屏堆十个控件和五张图——认知过载。一屏 ≤1 核心图 + ≤4 控件。
- ❌ ggplot 图里中文不管——会显示成方框。用 plotly 或 showtext（setup-and-run.md）。
- ❌ R 字符串里嵌英文双引号——会断字符串导致解析失败，中文文案用「」或单引号。
- ❌ 现场依赖外网 API/数据——课堂网络不可靠。数据随 app 打包，本地 `runApp()`。
- ❌ 把几百行 R 糊进对话——Write 写文件，对话只给路径 + 运行命令。
