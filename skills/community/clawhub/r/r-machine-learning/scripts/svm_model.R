# ============================================================
# Support Vector Machine (kernlab + caret)
# Supports: classification (C-SVC), regression (eps-regression)
# Kernels: linear, radial, polynomial, sigmoid
# Features: hyperparameter tuning, probability estimates
# ============================================================

source("scripts/utils.R")
library(caret)
library(kernlab)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
test_path <- opts$test
kernel <- opts$kernel %||% "radial"  # linear, radial, polynomial, sigmoid
cv <- as.numeric(opts$cv %||% "5")
tune_flag <- opts$tune %||% "TRUE"
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "svm"

set.seed(seed)
df <- read_data(data_path)
y <- df[[target]]

# Determine mode
is_class <- is.factor(y) || is_binary(y)
if (is_class) {
  if (!is.factor(y)) df[[target]] <- as.factor(y)
  if (nlevels(df[[target]]) == 2) {
    levels(df[[target]]) <- make.names(levels(df[[target]]))
    mode_str <- "binary"
  } else {
    mode_str <- "multiclass"
  }
} else {
  mode_str <- "regression"
}

message("===================================")
message("    SVM (", mode_str, ", ", kernel, " kernel)")
message("===================================")
message("Data: ", nrow(df), " x ", ncol(df) - 1, " features")
message("CV: ", cv, "-fold")

# Standardize predictors
preproc <- preProcess(df[, setdiff(names(df), target)], method = c("center", "scale"))
df_proc <- predict(preproc, df)

# Train control
if (is_class && mode_str == "binary") {
  trctrl <- trainControl(
    method = "cv", number = cv,
    classProbs = TRUE,
    summaryFunction = twoClassSummary,
    savePredictions = "final",
    verboseIter = FALSE
  )
  metric_opt <- "ROC"
} else if (is_class) {
  trctrl <- trainControl(
    method = "cv", number = cv,
    classProbs = TRUE,
    summaryFunction = multiClassSummary,
    savePredictions = "final",
    verboseIter = FALSE
  )
  metric_opt <- "Accuracy"
} else {
  trctrl <- trainControl(
    method = "cv", number = cv,
    savePredictions = "final",
    verboseIter = FALSE
  )
  metric_opt <- "RMSE"
}

# Select method based on kernel
if (kernel == "linear") {
  svm_method <- "svmLinear"
  if (tune_flag == "TRUE") {
    tune_grid <- expand.grid(C = c(0.01, 0.1, 0.5, 1, 2, 5, 10))
  } else {
    tune_grid <- expand.grid(C = 1)
  }
} else if (kernel == "radial") {
  svm_method <- "svmRadial"
  if (tune_flag == "TRUE") {
    tune_grid <- expand.grid(
      sigma = 10^seq(-3, 0, length.out = 4),
      C = c(0.1, 0.5, 1, 2, 5, 10)
    )
  } else {
    tune_grid <- expand.grid(sigma = 0.05, C = 1)
  }
} else if (kernel == "polynomial") {
  svm_method <- "svmPoly"
  if (tune_flag == "TRUE") {
    tune_grid <- expand.grid(
      degree = c(2, 3, 4),
      scale = c(0.001, 0.01, 0.1),
      C = c(0.1, 1, 5)
    )
  } else {
    tune_grid <- expand.grid(degree = 3, scale = 0.01, C = 1)
  }
} else {
  stop("Unsupported kernel: ", kernel, ". Choose: linear, radial, polynomial")
}

message("\n--- Training ---")
model <- train(
  as.formula(paste(target, "~ .")),
  data = df_proc,
  method = svm_method,
  trControl = trctrl,
  tuneGrid = tune_grid,
  metric = metric_opt,
  prob.model = is_class
)

message("\nBest parameters:")
print(model$bestTune)
message("\nBest ", metric_opt, ": ", round(max(model$results[[metric_opt]], na.rm = TRUE), 4))

# Tuning plot
if (nrow(tune_grid) > 3) {
  p_tune <- ggplot(model) + theme_pub() +
    labs(title = paste("SVM Tuning (", kernel, " kernel)", sep = ""))
  save_plot(p_tune, paste0(tag, "_tuning"))
}

# Variable importance (only for linear kernel)
if (kernel == "linear") {
  imp <- varImp(model)$importance
  imp$Variable <- rownames(imp)
  imp <- imp[order(-imp$Overall), ]
  save_csv(imp, paste0(tag, "_importance"))
  
  p_imp <- ggplot(head(imp, 20), aes(x = reorder(Variable, Overall), y = Overall)) +
    geom_col(fill = "purple4", alpha = 0.8) +
    coord_flip() +
    labs(title = "SVM (Linear) Variable Importance", x = "", y = "|Weight|") +
    theme_pub()
  save_plot(p_imp, paste0(tag, "_importance"))
}

# Test prediction
if (!is.null(test_path)) {
  test_df <- read_data(test_path)
  test_proc <- predict(preproc, test_df)
  preds <- predict(model, newdata = test_proc)
  if (is_class) {
    probs <- predict(model, newdata = test_proc, type = "prob")
    pred_df <- data.frame(Predicted = as.character(preds), probs)
  } else {
    pred_df <- data.frame(Predicted = preds)
  }
  save_csv(pred_df, paste0(tag, "_predictions"))
}

save_model(model, paste0(tag, "_model"))
save_model(preproc, paste0(tag, "_preproc"))

message("\n[OK] SVM complete.")
