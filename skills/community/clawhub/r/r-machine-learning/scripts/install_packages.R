# ============================================================
# Install all R dependency packages
# ============================================================

args <- commandArgs(trailingOnly = TRUE)
reinstall <- "--force" %in% args || "--reinstall" %in% args

packages <- c(
  # Core data manipulation
  "dplyr", "tidyr", "purrr", "tibble", "stringr", "forcats",
  
  # ML framework
  "caret", "tidymodels", "recipes", "rsample", "workflows", "tune",
  "parsnip", "yardstick", "dials",
  
  # Algorithms
  "glmnet",           # LASSO/Elastic Net
  "xgboost",          # XGBoost
  "randomForest",     # Random Forest
  "ranger",           # Fast Random Forest
  "kernlab",          # SVM
  "e1071",            # SVM + misc
  "nnet",             # Neural Networks
  "gbm",              # GBM
  
  # Feature selection
  "Boruta",
  
  # Model interpretation
  "fastshap",
  "DALEX", "DALEXtra", "ingredients", "iBreakDown",
  
  # Evaluation
  "pROC",
  "PRROC",
  "rms",
  "ResourceSelection",
  
  # Survival
  "survival",
  "survminer",
  "randomForestSRC",
  "survivalmodels",   # DeepSurv, XGBoost survival
  "coxed",            # Expected survival
  "riskRegression",
  
  # Visualization
  "ggplot2", "ggpubr", "ggrepel",
  "corrplot",
  "pheatmap",
  "viridis",
  "RColorBrewer",
  "scales",
  
  # Reporting
  "rmarkdown",
  "knitr",
  "kableExtra",
  "DT",
  "formattable",
  
  # IO
  "openxlsx",
  "readxl",
  "data.table",
  
  # SHAP specific
  "shapr"
)

# CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org"))
options(Ncpus = parallel::detectCores() - 1)

install_if_missing <- function(pkg, force = FALSE) {
  if (force || !requireNamespace(pkg, quietly = TRUE)) {
    message("[INSTALL] Installing ", pkg, " ...")
    tryCatch({
      install.packages(pkg, quiet = TRUE)
      message("[OK] ", pkg, " installed.")
    }, error = function(e) {
      message("[WARN] Failed to install ", pkg, ": ", e$message)
    })
  } else {
    message("[SKIP] ", pkg, " already installed.")
  }
}

message("========================================")
message(" R ML Workbench - Package Installation")
message("========================================")
message("Total packages: ", length(packages))
message("")

for (pkg in packages) {
  install_if_missing(pkg, force = reinstall)
}

# XGBoost survival extension (GitHub if not available)
if (!requireNamespace("xgboost.surv", quietly = TRUE)) {
  message("[INSTALL] Installing xgboost.surv from GitHub ...")
  tryCatch({
    if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
    remotes::install_github("barnahl/mlsurvlrnrs", quiet = TRUE)
    message("[OK] xgboost.surv installed.")
  }, error = function(e) {
    message("[WARN] xgboost.surv not available: ", e$message)
  })
}

message("")
message("Installation complete!")
message("To verify, run: library(caret); library(tidymodels); library(xgboost)")
