# ============================================================
# R Machine Learning Workbench - Utilities
# ============================================================

library(dplyr)
library(tidyr)
library(ggplot2)

#' Parse command-line arguments
parse_args <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  opts <- list()
  i <- 1
  while (i <= length(args)) {
    if (startsWith(args[i], "--")) {
      key <- gsub("^--", "", args[i])
      if (i < length(args) && !startsWith(args[i+1], "--")) {
        opts[[key]] <- args[i+1]
        i <- i + 1
      } else {
        opts[[key]] <- TRUE
      }
    }
    i <- i + 1
  }
  opts
}

#' Source base dir
BASE_DIR <- tryCatch({
  cmd <- commandArgs()
  file.path(dirname(dirname(sub("--file=", "", cmd[grep("--file=", cmd)]))))
}, error = function(e) getwd())
OUTPUT_DIR <- file.path(BASE_DIR, "output")

#' Ensure output directories exist
ensure_dirs <- function() {
  dirs <- c("plots", "models", "predictions", "reports", "tables")
  for (d in dirs) {
    dir.create(file.path(OUTPUT_DIR, d), showWarnings = FALSE, recursive = TRUE)
  }
}

#' Save plot
save_plot <- function(p, name, width = 8, height = 6) {
  ensure_dirs()
  path_pdf <- file.path(OUTPUT_DIR, "plots", paste0(name, ".pdf"))
  path_png <- file.path(OUTPUT_DIR, "plots", paste0(name, ".png"))
  ggsave(path_pdf, plot = p, width = width, height = height, device = "pdf")
  ggsave(path_png, plot = p, width = width, height = height, device = "png", dpi = 300)
  message("[SAVED] ", path_pdf)
  message("[SAVED] ", path_png)
  invisible(path_pdf)
}

#' Save data frame
save_csv <- function(df, name) {
  ensure_dirs()
  path <- file.path(OUTPUT_DIR, "tables", paste0(name, ".csv"))
  write.csv(df, path, row.names = FALSE)
  message("[SAVED] ", path)
  invisible(path)
}

#' Save model object
save_model <- function(model, name) {
  ensure_dirs()
  path <- file.path(OUTPUT_DIR, "models", paste0(name, ".rds"))
  saveRDS(model, path)
  message("[SAVED] ", path)
  invisible(path)
}

#' Read data with auto-detection
read_data <- function(path) {
  if (grepl("\\.csv$", path, ignore.case = TRUE)) {
    read.csv(path, stringsAsFactors = TRUE)
  } else if (grepl("\\.tsv$|\\.txt$", path, ignore.case = TRUE)) {
    read.delim(path, stringsAsFactors = TRUE)
  } else if (grepl("\\.rds$", path, ignore.case = TRUE)) {
    readRDS(path)
  } else if (grepl("\\.xlsx$|\\.xls$", path, ignore.case = TRUE)) {
    if (!require(openxlsx, quietly = TRUE)) {
      stop("Install openxlsx to read Excel files.")
    }
    read.xlsx(path)
  } else {
    read.csv(path, stringsAsFactors = TRUE)
  }
}

#' Compute evaluation metrics
calc_metrics <- function(obs, pred, type = "classification") {
  if (type == "classification") {
    if (is.factor(obs)) {
      cm <- caret::confusionMatrix(pred, obs)
      metrics <- list(
        accuracy = cm$overall["Accuracy"],
        kappa = cm$overall["Kappa"],
        sensitivity = cm$byClass["Sensitivity"],
        specificity = cm$byClass["Specificity"],
        ppv = cm$byClass["Pos Pred Value"],
        npv = cm$byClass["Neg Pred Value"],
        f1 = cm$byClass["F1"]
      )
      return(metrics)
    }
  } else if (type == "regression") {
    rmse <- sqrt(mean((obs - pred)^2))
    mae <- mean(abs(obs - pred))
    r2 <- 1 - sum((obs - pred)^2) / sum((obs - mean(obs))^2)
    return(list(RMSE = rmse, MAE = mae, R2 = r2))
  }
}

#' Theme for publication-ready plots
theme_pub <- function(base_size = 14) {
  theme_bw(base_size = base_size) +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", size = base_size + 2),
      axis.title = element_text(face = "bold"),
      legend.position = "bottom",
      legend.title = element_text(face = "bold"),
      strip.background = element_rect(fill = "grey90"),
      strip.text = element_text(face = "bold"),
      panel.grid.minor = element_blank()
    )
}

#' Check if target is binary classification
is_binary <- function(x) {
  if (is.factor(x)) {
    nlevels(x) == 2
  } else {
    length(unique(na.omit(x))) == 2
  }
}

#' Check if target is survival
is_survival <- function(data, time_col, event_col) {
  all(c(time_col, event_col) %in% names(data))
}

message("[INFO] R ML Workbench utilities loaded.")
