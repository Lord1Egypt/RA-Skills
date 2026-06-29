# ============================================================
# Exploratory Data Analysis
# ============================================================

source("scripts/utils.R")

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target
tag <- opts$tag %||% "explore"

df <- read_data(data_path)

message("===================================")
message("   Exploratory Data Analysis")
message("===================================")
message("Dataset: ", basename(data_path))
message("Rows: ", nrow(df), " | Columns: ", ncol(df))
message("")

# --- Structure ---
message("--- Column Types ---")
for (col in names(df)) {
  cls <- class(df[[col]])[1]
  nas <- sum(is.na(df[[col]]))
  uniq <- if (is.numeric(df[[col]])) {
    sprintf("range [%.3f, %.3f]", min(df[[col]], na.rm = TRUE), max(df[[col]], na.rm = TRUE))
  } else {
    sprintf("%d unique values", length(unique(na.omit(df[[col]]))))
  }
  message(sprintf("  %-30s %-12s NAs=%-4d %s", col, cls, nas, uniq))
}

# --- Missing Data ---
na_counts <- colSums(is.na(df))
any_miss <- sum(na_counts > 0)
if (any_miss > 0) {
  message("\n--- Missing Values ---")
  na_df <- data.frame(
    Variable = names(na_counts[na_counts > 0]),
    N_missing = na_counts[na_counts > 0],
    Pct = round(na_counts[na_counts > 0] / nrow(df) * 100, 1)
  )
  na_df <- na_df[order(-na_df$N_missing), ]
  print(na_df, row.names = FALSE)
  
  # Plot
  if (nrow(na_df) > 0) {
    na_df$Variable <- factor(na_df$Variable, levels = na_df$Variable[order(na_df$N_missing)])
    p <- ggplot(na_df, aes(x = Variable, y = N_missing)) +
      geom_col(fill = "coral3", alpha = 0.8) +
      geom_text(aes(label = paste0(Pct, "%")), hjust = -0.1, size = 3) +
      coord_flip() +
      labs(title = "Missing Values", x = "", y = "Count") +
      theme_pub()
    save_plot(p, paste0(tag, "_missing"))
  }
}

# --- Numeric Summary ---
numeric_cols <- names(df)[sapply(df, is.numeric)]
if (length(numeric_cols) > 0) {
  message("\n--- Numeric Variables Summary ---")
  num_sum <- df[, numeric_cols, drop = FALSE] |>
    summarise(across(everything(), list(
      Mean = ~mean(., na.rm = TRUE),
      SD = ~sd(., na.rm = TRUE),
      Min = ~min(., na.rm = TRUE),
      Q25 = ~quantile(., 0.25, na.rm = TRUE),
      Median = ~median(., na.rm = TRUE),
      Q75 = ~quantile(., 0.75, na.rm = TRUE),
      Max = ~max(., na.rm = TRUE),
      Skew = ~moments::skewness(., na.rm = TRUE),
      Kurtosis = ~moments::kurtosis(., na.rm = TRUE)
    ))) |>
    pivot_longer(everything(), names_to = c("Variable", ".value"), names_sep = "_")
  print(num_sum, row.names = FALSE)
  
  # Correlation heatmap
  if (length(numeric_cols) >= 3) {
    cor_mat <- cor(df[, numeric_cols], use = "pairwise.complete.obs")
    png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_correlation.png")),
        width = 8, height = 7, units = "in", res = 300)
    corrplot::corrplot(cor_mat, method = "color", type = "upper",
                       addCoef.col = "black", number.cex = 0.6,
                       tl.col = "black", tl.cex = 0.7,
                       order = "hclust", col = colorRampPalette(c("navy", "white", "darkred"))(200))
    dev.off()
    message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_correlation.png")))
    
    # Distribution plots for top variables
    if (length(numeric_cols) <= 20) {
      df_long <- df[, numeric_cols, drop = FALSE] |>
        pivot_longer(everything(), names_to = "Variable", values_to = "Value")
      p_hist <- ggplot(df_long, aes(x = Value)) +
        geom_histogram(bins = 30, fill = "steelblue", color = "white", alpha = 0.8) +
        facet_wrap(~Variable, scales = "free", ncol = 4) +
        labs(title = "Variable Distributions") +
        theme_pub() +
        theme(strip.text = element_text(size = 8))
      save_plot(p_hist, paste0(tag, "_distributions"), width = 14, height = max(6, ceiling(length(numeric_cols)/4)*3))
    }
  }
}

# --- Categorical Summary ---
factor_cols <- names(df)[sapply(df, function(x) is.factor(x) || is.character(x))]
if (length(factor_cols) > 0) {
  message("\n--- Categorical Variables Summary ---")
  for (col in factor_cols) {
    if (col == target) next
    tab <- table(df[[col]], useNA = "ifany")
    if (length(tab) <= 20) {
      message("  ", col, " (", length(tab), " levels):")
      ptab <- prop.table(tab) * 100
      for (i in seq_len(min(10, length(tab)))) {
        message(sprintf("    %-20s %5.1f%%", names(tab)[i], ptab[i]))
      }
      if (length(tab) > 10) message("    ... (", length(tab) - 10, " more)")
    }
  }
}

# --- Target Analysis ---
if (!is.null(target) && target %in% names(df)) {
  message("\n--- Target Variable: ", target, " ---")
  y <- df[[target]]
  if (is.numeric(y)) {
    message(sprintf("  Mean=%.3f  SD=%.3f  Range=[%.3f, %.3f]",
                    mean(y, na.rm = TRUE), sd(y, na.rm = TRUE),
                    min(y, na.rm = TRUE), max(y, na.rm = TRUE)))
    
    p_target <- ggplot(df, aes(x = .data[[target]])) +
      geom_histogram(bins = 40, fill = "steelblue", color = "white", alpha = 0.85) +
      geom_density(aes(y = after_stat(count) * diff(range(.data[[target]], na.rm = TRUE))/40),
                   color = "darkred", linewidth = 1) +
      labs(title = paste("Target Distribution:", target), x = target, y = "Count") +
      theme_pub()
    save_plot(p_target, paste0(tag, "_target_dist"))
  } else {
    tab <- table(y, useNA = "ifany")
    prop <- prop.table(tab) * 100
    target_summary <- data.frame(
      Level = names(tab), Count = as.vector(tab), Percent = round(as.vector(prop), 1)
    )
    print(target_summary, row.names = FALSE)
  }
}

save_csv(data.frame(
  Metric = c("Rows", "Columns", "Numeric Cols", "Factor Cols", "Missing Cells"),
  Value = c(nrow(df), ncol(df), length(numeric_cols), length(factor_cols), sum(is.na(df)))
), paste0(tag, "_summary"))

message("\n[OK] Exploratory analysis complete.")
