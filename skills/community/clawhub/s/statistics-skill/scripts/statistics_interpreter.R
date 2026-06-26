# statistics_interpreter.R
# 统计结果解读助手 - 支持SPSS原始输出解析

library(stringr)
library(httr)
library(jsonlite)

# ========== 请在这里填写你的API信息 ==========
KIMI_API_KEY <- "sk-kwe4WnYviimoCDIXOXgG82Xh91c9hWSNNobXj3OMUvfabOSF"
KIMI_BASE_URL <- "https://api.moonshot.cn/v1"
# ===========================================

# 调用Kimi API进行解读
interpret_with_kimi <- function(text) {
  url <- paste0(KIMI_BASE_URL, "/chat/completions")
  
  system_prompt <- "你是一位统计专家和学术论文写作顾问。请解读用户提供的统计结果，输出可以直接粘贴到论文结果部分的学术化段落。要求：1) 指出统计方法 2) 报告关键统计量 3) 解释p值的意义 4) 如果有效应量，解释其大小 5) 用中文输出，语言规范。"
  
  user_prompt <- sprintf("
请解读以下统计结果，输出可直接用于论文的学术化段落：

统计结果：
%s

请直接输出解读段落，不要加额外说明。
", text)
  
  body <- list(
    model = "moonshot-v1-8k",
    messages = list(
      list(role = "system", content = system_prompt),
      list(role = "user", content = user_prompt)
    ),
    temperature = 0.5
  )
  
  response <- POST(
    url,
    add_headers(
      "Authorization" = paste("Bearer", KIMI_API_KEY),
      "Content-Type" = "application/json"
    ),
    body = toJSON(body, auto_unbox = TRUE),
    encode = "json"
  )
  
  if (status_code(response) == 200) {
    result <- fromJSON(content(response, "text", encoding = "UTF-8"))
    return(result$choices$message$content)
  } else {
    return(paste("❌ API调用失败：", content(response, "text")))
  }
}

# 交互式运行
run_interactive <- function() {
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("📊 统计结果解读助手\n")
  cat(rep("=", 60), "\n\n", sep = "")
  
  cat("支持的统计方法：\n")
  cat("  • t检验、方差分析、卡方检验、相关分析、回归分析\n")
  cat("  • 中介效应分析、调节效应分析\n")
  cat("  • 信度分析(Cronbach's α)、因子分析\n")
  cat("  • 非参数检验(Mann-Whitney/Wilcoxon/Kruskal-Wallis)\n\n")
  
  cat("示例输入：\n")
  cat("  t(58)=2.34, p=0.023, Cohen's d=0.61\n")
  cat("  中介效应：indirect effect = 0.187, 95% CI [0.089, 0.292]\n\n")
  
  cat("请粘贴您的统计结果（输入完成后，新起一行输入 END 结束）:\n\n")
  
  lines <- c()
  while (TRUE) {
    line <- readline()
    if (toupper(trimws(line)) == "END") break
    lines <- c(lines, line)
  }
  
  if (length(lines) == 0) {
    cat("❌ 未输入内容\n")
    return()
  }
  
  text <- paste(lines, collapse = "\n")
  
  cat("\n🤖 正在生成解读...\n")
  interpretation <- interpret_with_kimi(text)
  
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("📝 解读结果：\n")
  cat(rep("-", 50), "\n", sep = "")
  cat(interpretation)
  cat("\n", rep("-", 50), "\n", sep = "")
  
  # 保存结果
  timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
  output_file <- paste0("interpretation_", timestamp, ".txt")
  writeLines(interpretation, output_file, useBytes = TRUE)
  cat(sprintf("\n💾 结果已保存到：%s\n", output_file))
  cat(rep("=", 60), "\n", sep = "")
}

# 测试函数
test <- function() {
  cat("🧪 测试模式\n\n")
  
  test_text <- "t(58)=2.34, p=0.023, Cohen's d=0.61"
  cat("测试输入：", test_text, "\n\n")
  
  result <- interpret_with_kimi(test_text)
  cat("输出：\n", result, "\n")
}

# 主函数
main <- function() {
  cat("\n请选择运行模式：\n")
  cat("1. 交互式使用\n")
  cat("2. 运行测试\n")
  cat("3. 退出\n")
  
  choice <- readline(prompt = "\n请输入 (1/2/3): ")
  
  if (choice == "1") {
    run_interactive()
  } else if (choice == "2") {
    test()
  } else {
    cat("👋 再见！\n")
  }
}

main()