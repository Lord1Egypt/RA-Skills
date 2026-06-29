# ============================================================
# XGBoost Model (caret + xgboost)
# Supports: classification, regression
# Features: early stopping, hyperparameter tuning
# ============================================================

source("scripts/utils.R")
library(caret)
library(xgboost)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
test_path <- opts$test
cv <- as.numeric(opts$cv %||% "5")
tune_flag <- opts$tune %||% "TRUE"
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "xgboost"
nrounds <- as.numeric(opts$nrounds %||% "1000")
early_stop <- as.numeric(opts$early_stop %||% "50")

set.seed(seed)
df <- read_data(data_path)
y <- df[[target]]

# Determine mode
is_class <- is.factor(y) || is_binary(y)
if (is_class) {
  if (!is.factor(y)) df[[target]] <- as.factor(y)
  if (nlevels(df[[target]]) == 2) {
    mode_str <- "binary"
    # Ensure levels are valid for caret
    levels(df[[target]]) <- make.names(levels(df[[target]]))
  } else {
    mode_str <- "multiclass"
  }
} else {
  mode_str <- "regression"
}

message("===================================")
message("    XGBoost (", mode_str, ")")
message("===================================")
message("Data: ", nrow(df), " x ", ncol(df) - 1, " features")
message("CV: ", cv, "-fold | Nrounds: ", nrounds)

# Train control
if (is_class && mode_str == "binary") {
  trctrl <- trainControl(
    method = "cv", number = cv,
    savePredictions = "final",
    classProbs = TRUE,
    summaryFunction = twoClassSummary,
    verboseIter = FALSE
  )
} else if (is_class) {
  trctrl <- trainControl(
    method = "cv", number = cv,
    savePredictions = "final",
    classProbs = TRUE,
    summaryFunction = multiClassSummary,
    verboseIter = FALSE
  )
} else {
  trctrl <- trainControl(
    method = "cv", number = cv,
    savePredictions = "final",
    summaryFunction = defaultSummary,
    verboseIter = FALSE
  )
}

# Tuning grid
if (tune_flag == "TRUE") {
  message("\n--- Hyperparameter Tuning ---")
  tune_grid <- expand.grid(
    nrounds = c(100, 200, 500),
    max_depth = c(3, 5, 7),
    eta = c(0.01, 0.05, 0.1),
    gamma = c(0, 0.1, 0.5),
    colsample_bytree = c(0.6, 0.8, 1.0),
    min_child_weight = c(1, 3, 5),
    subsample = c(0.7, 0.8, 1.0)
  )
  message("Grid size: ", nrow(tune_grid))
  
  # Use random search for large grids
  if (nrow(tune_grid) > 50) {
    tune_length <- as.numeric(opts$tune_length %||% "30")
    message("Random search: sampling ", tune_length, " combinations")
    trctrl$search <- "random"
  }
} else {
  tune_grid <- expand.grid(
    nrounds = nrounds,
    max_depth = 6,
    eta = 0.05,
    gamma = 0,
    colsample_bytree = 0.8,
    min_child_weight = 1,
    subsample = 0.8
  )
}

# Train
message("\n--- Training ---")
model <- tryCatch({
  train(
    as.formula(paste(target, "~ .")),
    data = df,
    method = "xgbTree",
    trControl = trctrl,
    tuneGrid = if (trctrl$search != "random") tune_grid else NULL,
    tuneLength = if (trctrl$search == "random") as.numeric(opts$tune_length %||% "30") else NULL,
    verbose = FALSE
  )
}, error = function(e) {
  message("[WARN] xgbTree failed, trying xgbLinear: ", e$message)
  train(
    as.formula(paste(target, "~ .")),
    data = df,
    method = "xgbLinear",
    trControl = trctrl,
    tuneLength = if (trctrl$search == "random") as.numeric(opts$tune_length %||% "30") else 10,
    verbose = FALSE
  )
})

message("\nBest parameters:")
print(model$bestTune)

# Variable importance
message("\n--- Variable Importance ---")
imp <- varImp(model)$importance
imp$Variable <- rownames(imp)
imp <- imp[order(-imp$Overall), ]
print(head(imp, 15), row.names = FALSE)

p_imp <- ggplot(head(imp, 20), aes(x = reorder(Variable, Overall), y = Overall)) +
  geom_col(fill = "darkorange", alpha = 0.85) +
  coord_flip() +
  labs(title = "XGBoost Variable Importance", x = "", y = "Importance") +
  theme_pub()
save_plot(p_imp, paste0(tag, "_importance"))

# Test prediction
if (!is.null(test_path)) {
  test_df <- read_data(test_path)
  preds <- predict(model, newdata = test_df)
  if (is_class) {
    probs <- predict(model, newdata = test_df, type = "prob")
    pred_df <- data.frame(Predicted = as.character(preds), probs)
  } else {
    pred_df <- data.frame(Predicted = preds)
  }
  save_csv(pred_df, paste0(tag, "_predictions"))
}

save_model(model, paste0(tag, "_model"))
save_csv(imp, paste0(tag, "_importance"))

message("\n[OK] XGBoost complete.")
