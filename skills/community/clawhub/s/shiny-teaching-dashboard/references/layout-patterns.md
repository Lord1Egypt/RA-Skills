# 布局架构：用 dashboard 替代幻灯片

先选**整体骨架**（一节课怎么组织），再往里填组件（components.md）。下面四种架构覆盖绝大多数课堂场景，全部基于 bslib（现代、配色统一）；最后给经典 shinydashboard 备选。完整可运行代码在 `templates/`，这里讲怎么选、骨架长什么样。

## 选哪种架构？

| 你的课是…… | 选 | 为什么 |
|---|---|---|
| 一整套讲座、多个并列主题（最常见的"替代幻灯片"） | **章节式 `page_navbar`** | 顶部 tab = 幻灯片的"节"，点着走，结构清楚 |
| 章节很多、像参考手册/百科式翻阅 | **侧边栏菜单式** | 左侧菜单容纳多层级，适合 10+ 小节 |
| 就讲透一个可交互的概念/模型 | **控制台+舞台 `page_sidebar`** | 边栏控件 + 主区结果，注意力集中 |
| 想要管理后台那种指标墙 | **经典 shinydashboard** | valueBox/box 风格，数据看板感强 |

## 1. 章节式 page_navbar（替代幻灯片的主力）

顶部导航每个 tab 是一"节"，学生跟着你一节节点过去。每个 `nav_panel` 内部就是这一节的内容（标题 + 要点 + 一个交互图/表）。

```r
ui <- page_navbar(
  title = "热力学第一定律", theme = theme,    # theme 见 color-schemes.md
  nav_panel("引入",   layout_columns(card(card_header("现象"), "..."), card(card_header("问题"), "..."))),
  nav_panel("原理",   layout_sidebar(sidebar = sidebar(sliderInput("Q","加热量 Q",0,100,50)),
                                     plotOutput("p1"), textOutput("explain"))),
  nav_panel("应用",   navset_card_tab(nav_panel("案例A","..."), nav_panel("案例B","..."))),
  nav_panel("小结",   value_box("一句话结论", "ΔU = Q − W", showcase = bsicons::bs_icon("lightbulb"))),
  nav_spacer(),
  nav_item(input_dark_mode())                  # 可选：明暗切换
)
```
→ 完整版见 `templates/navbar-lecture.R`。**这是默认推荐**：大多数"把一章做成交互讲解"都用它。

## 2. 侧边栏菜单式（章节多时）

bslib 用带 `sidebar` 的 `page_navbar`，或经典 `page_sidebar` 配 `accordion` 当目录；shinydashboard 用 `menuItem`。适合小节多、需要层级目录的长内容。

```r
ui <- page_sidebar(
  title = "统计推断", theme = theme,
  sidebar = sidebar(width = 260,
    accordion(open = FALSE,
      accordion_panel("第一章 抽样", actionLink("g1", "去这节")),
      accordion_panel("第二章 估计", actionLink("g2", "去这节")),
      accordion_panel("第三章 检验", actionLink("g3", "去这节")))),
  uiOutput("section")     # server 端按点击渲染对应小节
)
```

## 3. 控制台 + 舞台 page_sidebar（单一概念讲透）

最聚焦的布局：边栏放 2–4 个控件，主区放图/表 + 文字解释。讲"一个可调模型"的标准型。

```r
ui <- page_sidebar(
  title = "正态分布的参数", theme = theme,
  sidebar = sidebar(
    sliderInput("mu", "均值 μ", -5, 5, 0, step = .1),
    sliderInput("sd", "标准差 σ", 0.5, 5, 1, step = .1)),
  layout_columns(
    card(card_header("密度曲线"), plotlyOutput("dens")),
    value_box("此刻", textOutput("info"), theme = "primary"))
)
```
→ 完整版见 `templates/param-explorer.R`。

## 4. 经典 shinydashboard（指标墙风格）

需要传统 dashboard 观感时用。结构固定：Header + Sidebar(menu) + Body(tabItems)。

```r
library(shinydashboard)
ui <- dashboardPage(
  dashboardHeader(title = "课程看板"),
  dashboardSidebar(sidebarMenu(
    menuItem("概览", tabName = "ov", icon = icon("dashboard")),
    menuItem("分析", tabName = "an", icon = icon("chart-line")))),
  dashboardBody(tabItems(
    tabItem("ov", fluidRow(valueBox(42, "关键指标", icon = icon("star")))),
    tabItem("an", box(plotOutput("p"), width = 12))))
)
```
> shinydashboard 配色自成体系（`skin =`），和 bslib 的 `bs_theme()` 不通用。要 bslib 的精细配色就用前三种；要这种经典观感就接受它自带的皮肤，或改用 `bs4Dash`（Bootstrap 4、更现代、支持更多主题）。

## 课堂"演示模式"注意事项（替代幻灯片的关键细节）

替代幻灯片不只是搬到网页，还要适配**真实教室**：

- **字号放大**：投影 + 后排 → 在 theme 里调 `"font-size-base" = "1.15rem"`（见高对比配色），或对关键输出套大字号。
- **元素少而大**：一屏 ≤1 个核心图 + ≤4 个控件。信息密度按"最后一排能看清"来定，不是按你的显示器。
- **全屏**：浏览器 F11 全屏；`page_navbar(fillable = TRUE)` 让内容铺满高度。
- **键盘/遥控翻页**：tab 之间可点；要顺序翻可加"上一节/下一节"`actionButton` 配 `nav_select()`（server 端 `bslib::nav_select("navbar_id", "目标节")`），配合 USB 翻页笔（多数翻页笔发的是 PageUp/PageDown 或方向键，可绑快捷键）。
- **预加载与稳定**：课堂网络可能差——本地 `runApp()` 跑最稳；用到的数据尽量打包进 app 或随附 csv，别现场连外网 API。
- **明暗应景**：白天大教室用亮色高对比；晚间/机房用"暗夜讲堂"。
