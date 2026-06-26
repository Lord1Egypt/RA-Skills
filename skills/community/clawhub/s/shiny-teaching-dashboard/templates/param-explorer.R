# param-explorer.R — 参数探索器（讲透一个可调模型）
# 需要：shiny, bslib, plotly
# 运行：shiny::runApp("param-explorer.R")
# 用法：把"正态分布"换成你要讲的模型，sidebar 放它的关键参数，
#       主区放随参数变化的图 + 一个会说话的 value_box。

library(shiny); library(bslib); library(plotly)

theme <- bs_theme(version = 5, primary = "#0d9488", bg = "#f7fcfa", fg = "#15302b",
                  base_font = c("system-ui", "PingFang SC", "Microsoft YaHei", "sans-serif"))

ui <- page_sidebar(
  title = "正态分布的参数", theme = theme,
  sidebar = sidebar(
    sliderInput("mu", "均值 μ", -5, 5, 0, step = .1),
    sliderInput("sd", "标准差 σ", 0.5, 5, 1, step = .1),
    checkboxInput("ref", "叠加标准正态 N(0,1) 作参照", TRUE)),
  layout_columns(col_widths = c(8, 4),
    card(card_header("密度曲线（可缩放/悬停看值）"), plotlyOutput("dens", height = "360px")),
    value_box("此刻", uiOutput("info"), theme = "primary"))
)

server <- function(input, output, session) {
  output$dens <- renderPlotly({
    x <- seq(-12, 12, 0.05)
    p <- plot_ly(x = x, y = dnorm(x, input$mu, input$sd),
                 type = "scatter", mode = "lines", name = "当前",
                 line = list(color = "#0d9488", width = 3))
    if (input$ref)
      p <- add_trace(p, y = dnorm(x, 0, 1), name = "N(0,1)",
                     line = list(color = "#999999", dash = "dash", width = 2))
    layout(p, xaxis = list(title = "x"), yaxis = list(title = "密度"))
  })
  output$info <- renderUI({
    HTML(sprintf("μ = %.1f<br>σ = %.1f<br>峰高 ≈ %.3f<br>68%% 区间：[%.1f, %.1f]",
                 input$mu, input$sd, dnorm(input$mu, input$mu, input$sd),
                 input$mu - input$sd, input$mu + input$sd))
  })
}

shinyApp(ui, server)
