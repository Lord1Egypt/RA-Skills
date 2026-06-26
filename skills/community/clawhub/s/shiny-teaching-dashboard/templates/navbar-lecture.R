# navbar-lecture.R — 章节式讲座（替代整套幻灯片）★主力模板
# 需要：shiny, bslib, bsicons, ggplot2
# 运行：shiny::runApp("navbar-lecture.R")
# 用法：每个 nav_panel() = 幻灯片里的一"节"。把占位内容换成你的，保留结构；
#       要加节就再加一个 nav_panel()。配色换法见 color-schemes.md。

library(shiny); library(bslib); library(ggplot2)

# —— 配色（此处「学院蓝」，换方案整段替换）——
theme <- bs_theme(version = 5, bg = "#ffffff", fg = "#1f2933",
                  primary = "#1f4e79", secondary = "#5b7a99",
                  base_font = c("system-ui", "PingFang SC", "Microsoft YaHei", "sans-serif"))
palette <- c("#1f4e79", "#0e7490", "#b45309", "#6b8e6b")

ui <- page_navbar(
  title = "课程标题：换成你的", theme = theme, fillable = TRUE,

  nav_panel("引入",
    layout_columns(
      card(card_header("现象 / 提问"),
           "用一个真实现象或问题开场，勾起好奇。换成你的内容。"),
      card(card_header("本节目标"),
           tags$ul(tags$li("学完能理解……"),
                   tags$li("能动手做到……"))))),

  nav_panel("原理",
    layout_sidebar(
      sidebar = sidebar(
        sliderInput("rate", "增长率 r", min = 0, max = 1, value = 0.3, step = .05),
        radioButtons("mode", "对比哪种增长", c("线性", "指数"), inline = TRUE)),
      card(card_header("可调演示——让学生拖动看变化"),
           plotOutput("plot1", height = "320px")),
      card(textOutput("explain")))),

  nav_panel("应用",
    navset_card_tab(
      nav_panel("案例 A", "案例 A 的讲解……"),
      nav_panel("案例 B", "案例 B 的讲解……"))),

  nav_panel("小结",
    layout_columns(
      value_box("一句话结论", "把这一章最该记住的一句放这里",
                showcase = bsicons::bs_icon("lightbulb"), theme = "primary"),
      value_box("关键公式 / 数字", "y = a · e^(r t)",
                showcase = bsicons::bs_icon("calculator"), theme = "info"))),

  nav_spacer(),
  nav_item(tags$a("课程主页", href = "#", class = "nav-link"))
)

server <- function(input, output, session) {
  output$plot1 <- renderPlot({
    x <- seq(0, 10, 0.1)
    y <- if (input$mode == "指数") exp(input$rate * x) else 1 + input$rate * x
    ggplot(data.frame(x, y), aes(x, y)) +
      geom_line(linewidth = 1.3, color = palette[1]) +
      labs(x = "时间", y = "数量") + theme_minimal(base_size = 15)
  })
  output$explain <- renderText({
    if (input$mode == "指数")
      sprintf("指数增长：每一步按比例 r=%.2f 叠加，曲线越来越陡——这就是复利/疫情/裂变的形状。", input$rate)
    else
      sprintf("线性增长：每步加固定量 r=%.2f，斜率始终不变。", input$rate)
  })
}

shinyApp(ui, server)
