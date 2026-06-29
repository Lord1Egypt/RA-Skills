# ============================================================
# Random Forest Model (caret + ranger)
# Supports: classification, regression
# Features: tuning, variable importance, partial dependence
# ============================================================

source("scripts/utils.R")
library(caret)
library(ranger)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
test_path <- opts$test
cv <- as.numeric(opts$cv %||% "5")
tune_flag <- opts$tune %||% "FALSE"
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "rf"
ntrees <- as.numeric(opts$trees %||% "500")

set.seed(seed)
df <- read_data(data_path)
y <- df[[target]]

# Determine mode
is_class <- is.factor(y) || is_binary(y)
if (is_class) {
  if (!is.factor(y)) df[[target]] <- as.factor(y)
  mode_str <- "classification"
} else {
  mode_str <- "regression"
}

message("===================================")
message("    Random Forest (", mode_str, ")")
message("===================================")
message("Data: ", nrow(df), " x ", ncol(df) - 1, " features")
message("CV: ", cv, "-fold | Trees: ", ntrees)

# Train control
trctrl <- trainControl(
  method = "cv",
  number = cv,
  savePredictions = "final",
  classProbs = is_class,
  summaryFunction = if (is_class) twoClassSummary else defaultSummary,
  verboseIter = FALSE
)

if (tune_flag == "TRUE") {
  message("\n--- Hyperparameter Tuning ---")
  tune_grid <- expand.grid(
    mtry = floor(seq(2, max(2, sqrt(ncol(df)-1) * 2), length.out = 4)),
    splitrule = if (is_class) "gini" else "variance",
    min.node.size = c(1, 3, 5, 10)
  )
  message("Grid size: ", nrow(tune_grid))
} else {
  tune_grid <- expand.grid(
    mtry = floor(sqrt(ncol(df) - 1)),
    splitrule = if (is_class) "gini" else "variance",
    min.node.size = if (is_class) 1 else 5
  )
}

# Train model
message("\n--- Training ---")
model <- train(
  as.formula(paste(target, "~ .")),
  data = df,
  method = "ranger",
  trControl = trctrl,
  tuneGrid = tune_grid,
  num.trees = ntrees,
  importance = "impurity",
  verbose = FALSE
)

message("Best mtry: ", model$bestTune$mtry)
message("Best min.node.size: ", model$bestTune$min.node.size)

# Results
message("\n--- Results ---")
print(model$results[model$results$mtry == model$bestTune$mtry &
                      model$results$min.node.size == model$bestTune$min.node.size, ])

# Variable importance
imp <- varImp(model)$importance
imp$Variable <- rownames(imp)
imp <- imp[order(-imp$Overall), ]
message("\nTop 10 important features:")
print(head(imp, 10), row.names = FALSE)

p_imp <- ggplot(head(imp, 20), aes(x = reorder(Variable, Overall), y = Overall)) +
  geom_col(fill = "forestgreen", alpha = 0.8) +
  coord_flip() +
  labs(title = "Random Forest Variable Importance", x = "", y = "Importance") +
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

# Save model
save_model(model, paste0(tag, "_model"))
save_csv(imp, paste0(tag, "_importance"))

message("\n[OK] Random Forest complete.")
