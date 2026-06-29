# ============================================================
# Multi-Model Comparison (caret resamples)
# ============================================================

source("scripts/utils.R")
library(caret)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
models_str <- opts$models %||% "rf,xgboost,svm,lasso"
cv <- as.numeric(opts$cv %||% "5")
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "compare"

set.seed(seed)
df <- read_data(data_path)
y <- df[[target]]

is_class <- is.factor(y) || is_binary(y)
if (is_class && !is.factor(y)) df[[target]] <- as.factor(y)

model_list <- strsplit(models_str, ",")[[1]]
message("===================================")
message("      Multi-Model Comparison")
message("===================================")
message("Models: ", paste(model_list, collapse = ", "))
message("CV: ", cv, "-fold")
message("")

# Shared train control
ctrl <- trainControl(
  method = "cv", number = cv,
  savePredictions = "final",
  classProbs = is_class,
  summaryFunction = if (is_class) twoClassSummary else defaultSummary,
  returnResamp = "all",
  verboseIter = FALSE
)

# Define model configs
model_configs <- list(
  rf = list(method = "ranger",
    tuneGrid = expand.grid(mtry = floor(sqrt(ncol(df) - 1)),
                           splitrule = if (is_class) "gini" else "variance",
                           min.node.size = if (is_class) 1 else 5),
    num.trees = 500),
  xgboost = list(method = "xgbTree",
    tuneGrid = expand.grid(nrounds = 200, max_depth = 5, eta = 0.05, gamma = 0,
                           colsample_bytree = 0.8, min_child_weight = 1, subsample = 0.8)),
  svm = list(method = "svmRadial",
    tuneGrid = expand.grid(sigma = 0.05, C = 1)),
  lasso = list(method = "glmnet",
    tuneGrid = expand.grid(alpha = 1, lambda = 0.01)),
  gbm = list(method = "gbm",
    tuneGrid = expand.grid(n.trees = 200, interaction.depth = 3, shrinkage = 0.05,
                           n.minobsinnode = 10)),
  nnet = list(method = "nnet",
    tuneGrid = expand.grid(size = c(5, 10), decay = c(0.01, 0.1)),
    MaxNWts = 10000, trace = FALSE)
)

# Train each model
trained_models <- list()
for (m in model_list) {
  if (!m %in% names(model_configs)) {
    message("[SKIP] Unknown model: ", m)
    next
  }
  cfg <- model_configs[[m]]
  message("Training ", m, " ...")
  
  train_args <- list(
    form = as.formula(paste(target, "~ .")),
    data = df,
    method = cfg$method,
    trControl = ctrl,
    tuneGrid = cfg$tuneGrid,
    metric = if (is_class) "ROC" else "RMSE",
    verbose = FALSE
  )
  # Add extra args
  for (n in setdiff(names(cfg), c("method", "tuneGrid"))) {
    train_args[[n]] <- cfg[[n]]
  }
  
  trained_models[[m]] <- tryCatch(
    do.call(train, train_args),
    error = function(e) {
      message("[WARN] ", m, " failed: ", e$message)
      NULL
    }
  )
}

# Remove failed models
trained_models <- trained_models[!sapply(trained_models, is.null)]

if (length(trained_models) < 2) {
  stop("Need at least 2 successful models for comparison.")
}

message("\n--- Model Comparison ---")

# Resamples
resamps <- resamples(trained_models)
summary_resamps <- summary(resamps)

# Print
metric_names <- if (is_class) c("ROC", "Sens", "Spec") else c("RMSE", "Rsquared")
for (met in metric_names) {
  if (met %in% colnames(resamps$values)) {
    message("\n", met, ":")
    print(summary_resamps$statistics[[met]][, c("Mean", "SD", "Min", "Max")])
  }
}

# Statistical tests (paired t-test / Wilcoxon)
if (length(trained_models) >= 2) {
  message("\n--- Pairwise Model Comparisons ---")
  diffs <- diff(resamps)
  for (met in metric_names) {
    if (met %in% colnames(diffs$values)) {
      message("\n", met, " differences:")
      print(summary(diffs)[[met]])
    }
  }
}

# Dotplot
pdf(file.path(OUTPUT_DIR, "plots", paste0(tag, "_dotplot.pdf")),
    width = 10, height = max(5, 2 * length(trained_models)))
dotplot(resamps, metric = metric_names[1], main = "Model Comparison")
dev.off()
png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_dotplot.png")),
    width = 10, height = max(5, 2 * length(trained_models)), units = "in", res = 300)
dotplot(resamps, metric = metric_names[1], main = "Model Comparison")
dev.off()
message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_dotplot.png")))

# Boxplot
pdf(file.path(OUTPUT_DIR, "plots", paste0(tag, "_boxplot.pdf")),
    width = 10, height = 6)
bwplot(resamps, main = "Model Performance Distribution")
dev.off()
png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_boxplot.png")),
    width = 10, height = 6, units = "in", res = 300)
bwplot(resamps, main = "Model Performance Distribution")
dev.off()
message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_boxplot.png")))

# Save summary table
summary_df <- data.frame()
for (met in metric_names) {
  if (met %in% names(summary_resamps$statistics)) {
    tmp <- as.data.frame(summary_resamps$statistics[[met]])
    tmp$Metric <- met
    tmp$Model <- rownames(tmp)
    summary_df <- rbind(summary_df, tmp)
  }
}
save_csv(summary_df, paste0(tag, "_summary"))

# Rank models
message("\n--- Model Rankings ---")
if (is_class) {
  rankings <- summary_df |>
    filter(Metric == metric_names[1]) |>
    arrange(desc(Mean))
} else {
  rankings <- summary_df |>
    filter(Metric == metric_names[1]) |>
    arrange(Mean)
}
print(rankings[, c("Model", "Mean", "SD")], row.names = FALSE)

message("\n[OK] Model comparison complete.")
message("Best model: ", rankings$Model[1])
