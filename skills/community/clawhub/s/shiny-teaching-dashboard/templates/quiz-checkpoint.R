# quiz-checkpoint.R — 课堂自测 / 即时投票
# 需要：shiny, bslib
# 运行：shiny::runApp("quiz-checkpoint.R")
# 用法：把题目填进 quiz 列表（q 题干，opts 选项，ans 正确项序号，why 讲解）。
#       选答后点"提交"出即时反馈。适合一节讲完做巩固检查点。

library(shiny); library(bslib)

# —— 题库：换成你的 ——
quiz <- list(
  list(q = "渐进式披露的核心是什么？",
       opts = c("一次把所有内容展示出来", "按需逐层展开细节", "只用图片不用文字"),
       ans = 2, why = "渐进式披露 = 先给主干，细节按需展开，降低一次性的认知负荷。"),
  list(q = "下列哪种组件最适合讲「参数如何影响结果」？",
       opts = c("静态表格", "sliderInput 联动图表", "一段纯文字"),
       ans = 2, why = "滑块让学生亲手改参数、即时看结果，把现象接到理解，形成学习闭环。")
)

theme <- bs_theme(version = 5, primary = "#0d9488",
                  base_font = c("system-ui", "PingFang SC", "Microsoft YaHei", "sans-serif"))

ui <- page_sidebar(
  title = "课堂自测", theme = theme,
  sidebar = sidebar(
    numericInput("qid", "第几题", 1, min = 1, max = length(quiz)),
    actionButton("submit", "提交答案", class = "btn-primary")),
  card(uiOutput("question")),
  uiOutput("feedback")
)

server <- function(input, output, session) {
  cur <- reactive({ req(input$qid); quiz[[input$qid]] })
  output$question <- renderUI({
    q <- cur()
    tagList(
      h4(q$q),
      radioButtons("choice", NULL, choiceNames = q$opts,
                   choiceValues = as.character(seq_along(q$opts)),
                   selected = character(0)))
  })
  output$feedback <- renderUI({
    input$submit
    isolate({
      if (is.null(input$choice)) return(NULL)
      q <- cur()
      ok <- as.integer(input$choice) == q$ans
      div(class = paste("alert", if (ok) "alert-success" else "alert-danger"),
          strong(if (ok) "✓ 正确！" else "✗ 再想想。"),
          tags$br(), q$why)
    })
  })
}

shinyApp(ui, server)
