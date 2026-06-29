# ============================================================
# Hyperparameter Tuning (Grid / Random / Bayesian)
# ============================================================

source("scripts/utils.R")
library(caret)
library(tidymodels)
library(dials)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
model_type <- opts$model %||% "rf"  # rf, xgboost, svm
method <- opts$method %||% "grid"   # grid, random, bayesian
cv <- as.numeric(opts$cv %||% "5")
iter <- as.numeric(opts$iter %||% "30")
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "tune"

set.seed(seed)
df <- read_data(data_path)
y <- df[[target]]

is_class <- is.factor(y) || is_binary(y)
if (is_class && !is.factor(y)) df[[target]] <- as.factor(y)

message("===================================")
message("  Hyperparameter Tuning")
message("===================================")
message("Model: ", model_type, " | Method: ", method)

# Define search grid based on model type
if (method == "grid") {
  if (model_type == "rf") {
    tune_grid <- expand.grid(
      mtry = floor(seq(2, max(2, ncol(df)-1), length.out = 5)),
      splitrule = if (is_class) "gini" else "variance",
      min.node.size = c(1, 3, 5, 10)
    )
  } else if (model_type == "xgboost") {
    tune_grid <- expand.grid(
      nrounds = c(100, 200, 500),
      max_depth = c(3, 5, 7),
      eta = c(0.01, 0.05, 0.1),
      gamma = c(0, 0.1),
      colsample_bytree = c(0.6, 0.8, 1),
      min_child_weight = c(1, 3, 5),
      subsample = c(0.7, 0.8, 1)
    )
  } else if (model_type == "svm") {
    tune_grid <- expand.grid(
      sigma = c(0.01, 0.05, 0.1, 0.5),
      C = c(0.1, 0.5, 1, 2, 5, 10)
    )
  }
  message("Grid size: ", nrow(tune_grid))
}

# Train control
tune_ctrl <- trainControl(
  method = "cv",
  number = cv,
  search = if (method == "random") "random" else "grid",
  savePredictions = "final",
  classProbs = is_class,
  summaryFunction = if (is_class) twoClassSummary else defaultSummary,
  verboseIter = FALSE
)

# Train with tuning
if (method == "grid") {
  model <- train(
    as.formula(paste(target, "~ .")),
    data = df,
    method = switch(model_type,
      rf = "ranger",
      xgboost = "xgbTree",
      svm = "svmRadial"
    ),
    trControl = tune_ctrl,
    tuneGrid = tune_grid,
    num.trees = if (model_type == "rf") 500 else NULL,
    metric = if (is_class) "ROC" else "RMSE"
  )
} else {
  # Random / Bayesian search
  model <- train(
    as.formula(paste(target, "~ .")),
    data = df,
    method = switch(model_type,
      rf = "ranger",
      xgboost = "xgbTree",
      svm = "svmRadial"
    ),
    trControl = tune_ctrl,
    tuneLength = iter,
    num.trees = if (model_type == "rf") 500 else NULL,
    metric = if (is_class) "ROC" else "RMSE"
  )
}

# Results
message("\n--- Best Parameters ---")
print(model$bestTune)

best_result <- model$results
for (col in names(model$bestTune)) {
  best_result <- best_result[best_result[[col]] == model$bestTune[[col]], ]
}
message("\nBest performance:")
print(best_result[, !names(best_result) %in% c("sigma", "C", "mtry", "splitrule", "min.node.size",
                                                 "nrounds", "max_depth", "eta", "gamma",
                                                 "colsample_bytree", "min_child_weight", "subsample")])

# Tuning visualization
if (method == "grid" && nrow(tune_grid) > 3) {
  p_tune <- ggplot(model) + theme_pub()
  save_plot(p_tune, paste0(tag, "_", model_type))
}

save_model(model, paste0(tag, "_", model_type))
save_csv(model$results, paste0(tag, "_", model_type, "_results"))

message("\n[OK] Hyperparameter tuning complete.")
