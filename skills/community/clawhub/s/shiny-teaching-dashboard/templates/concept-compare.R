# concept-compare.R — 多概念 / 案例 / 学派对比
# 需要：shiny, bslib
# 运行：shiny::runApp("concept-compare.R")
# 用法：每个 nav_panel 装一个视角；最后一页用并置三栏做维度对照。
#       适合讲"两种理论""三种方法""正反观点"这类需要对比的内容。

library(shiny); library(bslib)

theme <- bs_theme(version = 5, primary = "#9a3412", bg = "#fdf8f0", fg = "#382c22",
                  base_font = c("system-ui", "PingFang SC", "Microsoft YaHei", "sans-serif"))

ui <- page_fillable(
  theme = theme, title = "概念对比",
  h3("对比主题：换成你的"),
  navset_card_tab(
    nav_panel("视角 A",
      layout_columns(
        card(card_header("核心主张"), "A 主张……"),
        card(card_header("支持证据"), "支持 A 的证据 / 例子……"))),
    nav_panel("视角 B",
      layout_columns(
        card(card_header("核心主张"), "B 主张……"),
        card(card_header("支持证据"), "支持 B 的证据 / 例子……"))),
    nav_panel("并置对照",
      layout_columns(col_widths = c(4, 4, 4),
        card(card_header("对比维度"),
             tags$ul(tags$li("基本假设"), tags$li("适用范围"), tags$li("主要局限"))),
        card(card_header("视角 A"), tags$ul(tags$li("假设：…"), tags$li("适用：…"), tags$li("局限：…"))),
        card(card_header("视角 B"), tags$ul(tags$li("假设：…"), tags$li("适用：…"), tags$li("局限：…")))))
  )
)

server <- function(input, output, session) {}

shinyApp(ui, server)
