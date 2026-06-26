# 安装、运行、部署、中文字体

## 单文件 app.R 结构

教学分发用**单文件 `app.R`** 最省事（一个文件 = 一个 app，复制即走）：

```r
library(shiny)
library(bslib)
# 1) 顶部：主题、数据、辅助函数（只跑一次）
thematic::thematic_shiny(font = "auto")
theme <- bs_theme(version = 5, primary = "#1f4e79", bg = "#fff", fg = "#1f2933")
dat <- data.frame(x = 1:20, y = cumsum(rnorm(20)))   # 或 read.csv("data.csv")

# 2) UI：长什么样
ui <- page_navbar(title = "课程标题", theme = theme,
  nav_panel("第一节", "...")
)

# 3) server：交互逻辑（输入怎么变成输出）
server <- function(input, output, session) {
  output$p <- renderPlot({ plot(dat$x, dat$y) })
}

# 4) 启动
shinyApp(ui, server)
```

## 装包

```r
install.packages(c(
  "shiny", "bslib", "bsicons",      # 框架 + 图标
  "ggplot2", "plotly", "DT",        # 图表 + 交互表
  "thematic", "showtext"            # 图表配色跟随主题 + 中文字体
))
# 按需：shinydashboard / bs4Dash（经典看板）、leaflet（地图）、DiagrammeR（流程图）
```
> 现代 bslib 函数（`page_navbar`、`value_box`、`layout_columns`、`accordion`）需 **bslib ≥ 0.5**。装最新版即可：`install.packages("bslib")`。R 建议 ≥ 4.1。

## 运行

- **RStudio**：打开 `app.R`，右上角点 **Run App**（旁边下拉可选"在窗口/浏览器/Viewer 打开"）。
- **控制台**：
  ```r
  shiny::runApp("app.R", launch.browser = TRUE)   # 指向文件或其所在文件夹
  ```
- 课堂用：**本地 `runApp()` 最稳**，不依赖外网。停止按 Esc 或 Stop。

## plot 里的中文（最容易踩的坑）

UI 里的中文（标题、按钮、文字）是浏览器渲染的，**没问题**。但 **ggplot2 / base R 画出来的图里中文默认是方框**。两种解法：

**① 用 plotly 画图——中文自动正常**（plotly 在浏览器里用 HTML/SVG 渲染，吃系统字体）。能用 `plotlyOutput` 就省掉字体烦恼，教学交互图也更友好。

**② 静态 ggplot/base 图——用 showtext**：

```r
library(showtext)
# 加一个系统中文字体（按平台挑一个存在的路径/名字）：
# Windows: font_add("hei", "C:/Windows/Fonts/msyh.ttc")        # 微软雅黑
# macOS:   font_add("hei", "/System/Library/Fonts/PingFang.ttc")
# Linux:   font_add("hei", "/usr/share/fonts/.../wqy-microhei.ttc")  # 文泉驿/Noto CJK
showtext_auto()    # 之后所有图自动用注册的字体渲染中文
# ggplot 里指定：
# + theme_minimal(base_family = "hei")
```
- 找系统中文字体：`sysfonts::font_files()` 列出可用字体文件。
- `font_add_google()` 能下中文字体但**需要联网、国内可能慢**——优先用本地系统字体。
- `thematic_shiny(font = "auto")` 会尽量自动处理字体，但中文仍建议显式 showtext 兜底。

## reactive 速记（templates 都靠它）

- `renderPlot({...})` / `renderPlotly` / `renderDT` / `renderUI` / `renderText`：**里面用到的 `input$x` 一变，就自动重算重画**——这就是"改输入→看结果"的闭环。
- `reactive({...})`：算一次给多处用的中间值，`val()` 取用。
- `eventReactive(input$go, {...})` / `observeEvent(input$go, {...})`：只在**点按钮**时才触发（分步揭示、运行模拟、提交测验用）。
- `req(input$x)`：输入还没准备好时安静跳过，避免红色报错糊在屏上（课堂上很尴尬）。

## 分发 / 部署

| 方式 | 适合 | 要点 |
|---|---|---|
| **本地 `runApp()`** | 自己上课用 | 最稳，无需联网/账号；把数据文件和 app.R 放同一文件夹 |
| **shinylive** | 把教学 app 发给学生**自己开**、无服务器 | 用 `shinylive::export()` 导成**纯静态网页**，R 在浏览器里靠 WebAssembly 跑，丢到任意静态托管/U盘即可。限制：部分包不支持，首次加载需下载运行时 |
| **shinyapps.io** | 放云端给一个链接 | `rsconnect::deployApp()`，免费额度够课堂；需注册账号 |
| **Shiny Server / Posit Connect** | 学校/机构自建 | 自托管，适合长期课程门户 |

> 给学生课后自己玩 → 首选 **shinylive**（一个链接/一个文件夹，不用装 R）。课堂老师现场演示 → 本地 `runApp()`。
