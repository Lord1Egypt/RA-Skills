# ============================================================
# Report Generator (R Markdown)
# ============================================================

source("scripts/utils.R")

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
tag <- opts$tag %||% "report"

df <- read_data(data_path)
y <- df[[target]]

is_class <- is.factor(y) || is_binary(y)

message("===================================")
message("     Report Generation")
message("===================================")

# Create R Markdown file
rmd_path <- file.path(OUTPUT_DIR, "reports", paste0(tag, "_report.Rmd"))

rmd_content <- '---
title: "R Machine Learning Analysis Report"
output:
  html_document:
    toc: true
    toc_float: true
    theme: flatly
    highlight: tango
    code_folding: hide
params:
  tag: "report"
  target: "outcome"
  data_path: "data.csv"
  type: "classification"
  n_train: 0
  n_test: 0
  n_features: 0
  results: NULL
  output_dir: "output"
editor_options:
  chunk_output_type: console
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = FALSE, warning = FALSE, message = FALSE)
library(ggplot2)
library(dplyr)
library(knitr)
library(kableExtra)
library(pROC)
library(DT)
```

# Executive Summary

**Report Generated:** `r Sys.Date()`

| Metric | Value |
|--------|-------|
| Target Variable | `r params$target` |
| Analysis Type | `r params$type` |
| Training Samples | `r params$n_train` |
| Test Samples | `r params$n_test` |
| Features | `r params$n_features` |

# Data Overview

```{r data-overview}
df <- read.csv(params$data_path)
y <- df[[params$target]]

# Missing values
na_df <- data.frame(
  Variable = names(colSums(is.na(df))),
  Missing = colSums(is.na(df)),
  Pct = round(colSums(is.na(df)) / nrow(df) * 100, 1)
) |> filter(Missing > 0)

if (nrow(na_df) > 0) {
  cat("### Missing Values\n")
  kable(na_df, caption = "Missing Value Summary") |>
    kable_styling(bootstrap_options = c("striped", "hover"))
}
```

## Target Distribution

```{r target-dist}
if (is.factor(y) || is.character(y)) {
  tab <- as.data.frame(table(y))
  names(tab) <- c("Level", "Count")
  tab$Percent <- round(tab$Count / sum(tab$Count) * 100, 1)
  kable(tab, caption = "Target Distribution") |>
    kable_styling(bootstrap_options = c("striped", "hover"))
} else {
  cat(sprintf("Mean: %.3f, SD: %.3f, Range: [%.3f, %.3f]",
              mean(y, na.rm=TRUE), sd(y, na.rm=TRUE),
              min(y, na.rm=TRUE), max(y, na.rm=TRUE)))
}
```

# Method

The analysis employed a comprehensive machine learning pipeline including:

```{r methods}
methods_list <- c(
  "**Data Splitting:** 70/30 train-test stratified split",
  "**Preprocessing:** Centering, scaling, missing value imputation",
  "**Algorithms:** Random Forest (ranger), XGBoost, LASSO (glmnet), SVM (kernlab)",
  "**Validation:** k-fold cross-validation",
  paste("**Tuning:** Grid/random hyperparameter search"),
  "**Evaluation:** ROC-AUC, sensitivity, specificity, accuracy, calibration",
  "**Interpretation:** Variable importance, SHAP values"
)
cat(paste("-", methods_list, collapse = "\n"))
```

# Model Results

```{r results, results="asis"}
if (!is.null(params$results) && nrow(params$results) > 0) {
  cat("### Model Performance Comparison\n\n")
  kable(params$results, caption = "Test Set Performance", digits = 4) |>
    kable_styling(bootstrap_options = c("striped", "hover", "condensed")) |>
    row_spec(1, bold = TRUE, background = "#E8F5E9")
}
```

## Best Model Details

```{r best-model}
best_name <- params$results$Model[1]
cat("**Best Model:** ", best_name, "\n\n")

# Check for saved plots
plot_dir <- file.path(params$output_dir, "plots")
plot_files <- list.files(plot_dir, pattern = paste0(params$tag, ".*\\.png$"), full.names = TRUE)

for (pf in head(plot_files, 10)) {
  cat("\n\n")
  include_graphics(pf)
}
```

# Model Interpretation

```{r shap-section}
shap_file <- file.path(params$output_dir, "tables", "shap_importance.csv")
if (file.exists(shap_file)) {
  cat("### SHAP Feature Importance\n\n")
  shap_df <- read.csv(shap_file)
  if (nrow(shap_df) > 0) {
    kable(head(shap_df, 15), caption = "Top 15 Features by Mean |SHAP|") |>
      kable_styling(bootstrap_options = c("striped", "hover"))
  }
}
```

# Variable Importance

```{r importance-table}
# Find variable importance files
tbl_dir <- file.path(params$output_dir, "tables")
imp_files <- list.files(tbl_dir, pattern = "(importance|vimp).*\\.csv$", full.names = TRUE)

for (f in head(imp_files, 3)) {
  imp_df <- tryCatch(read.csv(f), error = function(e) NULL)
  if (!is.null(imp_df) && nrow(imp_df) > 0) {
    cat("\n### ", basename(f), "\n\n")
    kable(head(imp_df, 15), digits = 4) |>
      kable_styling(bootstrap_options = c("striped", "hover", "condensed"))
  }
}
```

# Conclusion

This report summarizes the machine learning analysis conducted on the provided dataset.
The best performing model was **`r best_name`**, selected based on test set performance.

---

*Generated by R Machine Learning Workbench'
"

writeLines(rmd_content, rmd_path)
message("[SAVED] ", rmd_path)

# Render
rmd_output <- file.path(OUTPUT_DIR, "reports", paste0(tag, "_report.html"))
tryCatch({
  rmarkdown::render(rmd_path, output_file = rmd_output, quiet = TRUE,
                    params = list(
                      tag = tag,
                      target = target,
                      data_path = normalizePath(data_path),
                      type = if (is_class) "classification" else "regression",
                      n_train = nrow(df),
                      n_test = 0,
                      n_features = ncol(df) - 1,
                      results = data.frame(),
                      output_dir = normalizePath(OUTPUT_DIR)
                    ))
  message("[OK] Report: ", rmd_output)
}, error = function(e) {
  message("[WARN] Render failed: ", e$message)
  message("R Markdown template saved at: ", rmd_path)
})

message("\n[OK] Report generation complete.")
