# stepwise-reveal.R — 分步揭示讲解（替代幻灯片"逐点出现"）
# 需要：shiny, bslib
# 运行：shiny::runApp("stepwise-reveal.R")
# 用法：把推导/讲解拆进 steps 列表，按"下一步"逐条揭示。
#       适合需要悬念、按节奏推进的推导、解题、论证。

library(shiny); library(bslib)

# —— 讲解步骤：换成你的（h 标题，b 正文，可含 HTML）——
steps <- list(
  list(h = "第 1 步：提出问题", b = "我们想知道……（陈述要解决的问题）"),
  list(h = "第 2 步：建立模型", b = "假设……，于是可以写成……"),
  list(h = "第 3 步：求解",     b = "代入并化简，得到……"),
  list(h = "第 4 步：结论",     b = "因此……（点题，连回开头的问题）")
)

theme <- bs_theme(version = 5, primary = "#1f4e79",
                  base_font = c("system-ui", "PingFang SC", "Microsoft YaHei", "sans-serif"))

ui <- page_sidebar(
  title = "分步推导", theme = theme,
  sidebar = sidebar(
    actionButton("nxt", "下一步 ▶", class = "btn-primary"),
    actionButton("reset", "重来"),
    accordion(open = FALSE,
      accordion_panel("补充阅读（可选）",
        "把「想深入再看」的材料折叠在这里，不打断主线。"))),
  uiOutput("revealed")
)

server <- function(input, output, session) {
  shown <- reactiveVal(1)
  observeEvent(input$nxt,   { if (shown() < length(steps)) shown(shown() + 1) })
  observeEvent(input$reset, { shown(1) })
  output$revealed <- renderUI({
    cards <- lapply(seq_len(shown()), function(i)
      card(card_header(steps[[i]]$h), HTML(steps[[i]]$b)))
    do.call(tagList, cards)
  })
}

shinyApp(ui, server)
