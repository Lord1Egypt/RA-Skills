# data-story.R — 数据叙事（关键指标 + 交互图 + 数据表）
# 需要：shiny, bslib, plotly, DT
# 运行：shiny::runApp("data-story.R")
# 用法：把 dat 换成你的数据（read.csv 或随堂数据）；value_box 放最该强调的几个数；
#       让学生自己选 X/Y 探索关系，下面摆原始表供翻查。

library(shiny); library(bslib); library(plotly); library(DT)

# —— 数据：换成你的 ——
dat <- mtcars
dat$car <- rownames(mtcars)

theme <- bs_theme(version = 5, primary = "#1f4e79",
                  base_font = c("system-ui", "PingFang SC", "Microsoft YaHei", "sans-serif"))

ui <- page_fillable(
  theme = theme, title = "数据叙事",
  layout_columns(fill = FALSE,
    value_box("样本量", nrow(dat), theme = "primary"),
    value_box("变量数", ncol(mtcars), theme = "secondary"),
    value_box("平均油耗 mpg", round(mean(dat$mpg), 1), theme = "info")),
  layout_sidebar(
    sidebar = sidebar(
      selectInput("x", "X 轴变量", choices = names(mtcars), selected = "wt"),
      selectInput("y", "Y 轴变量", choices = names(mtcars), selected = "mpg")),
    card(card_header("散点关系（悬停看是哪辆车）"), plotlyOutput("sc", height = "320px"))),
  card(card_header("原始数据（可排序、搜索、翻页）"), DTOutput("tbl"))
)

server <- function(input, output, session) {
  output$sc <- renderPlotly({
    plot_ly(dat, x = ~get(input$x), y = ~get(input$y), text = ~car,
            type = "scatter", mode = "markers",
            marker = list(color = "#1f4e79", size = 10, opacity = .75)) |>
      layout(xaxis = list(title = input$x), yaxis = list(title = input$y))
  })
  output$tbl <- renderDT(datatable(dat, options = list(pageLength = 6)))
}

shinyApp(ui, server)
