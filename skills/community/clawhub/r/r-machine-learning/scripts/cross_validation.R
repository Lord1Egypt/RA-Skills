# ============================================================
# Cross-Validation (k-fold, repeated, leave-one-out)
# ============================================================

source("scripts/utils.R")
library(caret)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
model_type <- opts$model %||% "rf"
k <- as.numeric(opts$k %||% "5")
repeats <- as.numeric(opts$repeats %||% "1")
method_cv <- opts$method_cv %||% "cv"  # cv, repeatedcv, loocv, bootstrap
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "cv"

set.seed(seed)
df <- read_data(data_path)
y <- df[[target]]

is_class <- is.factor(y) || is_binary(y)
if (is_class && !is.factor(y)) df[[target]] <- as.factor(y)

message("===================================")
message("     Cross-Validation (", toupper(method_cv), ")")
message("===================================")
message("Model: ", model_type, " | K: ", k, " | Repeats: ", repeats)

# Train control
ctrl <- trainControl(
  method = method_cv,
  number = k,
  repeats = if (method_cv == "repeatedcv") repeats else NULL,
  savePredictions = "all",
  classProbs = is_class,
  summaryFunction = if (is_class) twoClassSummary else defaultSummary,
  returnResamp = "all",
  verboseIter = TRUE
)

# Select method and grid
if (model_type == "rf") {
  model_method <- "ranger"
  tg <- expand.grid(mtry = floor(sqrt(ncol(df) - 1)),
                    splitrule = if (is_class) "gini" else "variance",
                    min.node.size = if (is_class) 1 else 5)
  extra <- list(num.trees = 500)
} else if (model_type == "xgboost") {
  model_method <- "xgbTree"
  tg <- expand.grid(nrounds = 200, max_depth = 6, eta = 0.05, gamma = 0,
                    colsample_bytree = 0.8, min_child_weight = 1, subsample = 0.8)
  extra <- list()
} else if (model_type == "svm") {
  model_method <- "svmRadial"
  tg <- expand.grid(sigma = 0.05, C = 1)
  extra <- list()
} else if (model_type == "lasso") {
  model_method <- "glmnet"
  tg <- expand.grid(alpha = 1, lambda = 0.01)
  extra <- list()
} else {
  model_method <- "ranger"
  tg <- expand.grid(mtry = floor(sqrt(ncol(df) - 1)),
                    splitrule = if (is_class) "gini" else "variance",
                    min.node.size = if (is_class) 1 else 5)
  extra <- list(num.trees = 500)
}

# Train
model <- train(
  as.formula(paste(target, "~ .")),
  data = df,
  method = model_method,
  trControl = ctrl,
  tuneGrid = tg,
  metric = if (is_class) "ROC" else "RMSE",
  verbose = FALSE
)

# Aggregate results
resamples <- model$resample
message("\nCV Results:")
cv_summary <- resamples |>
  select(-Resample) |>
  summarise(across(everything(), list(
    Mean = ~mean(., na.rm = TRUE),
    SD = ~sd(., na.rm = TRUE),
    Min = ~min(., na.rm = TRUE),
    Max = ~max(., na.rm = TRUE)
  )))
print(t(cv_summary))

# Per-fold metrics
save_csv(resamples, paste0(tag, "_", model_type, "_folds"))
save_csv(data.frame(Metric = names(model$results), model$results), 
         paste0(tag, "_", model_type, "_summary"))

# CV variability plot
p_cv <- resamples |>
  select(-Resample) |>
  pivot_longer(everything(), names_to = "Metric", values_to = "Value") |>
  ggplot(aes(x = Metric, y = Value)) +
  geom_boxplot(fill = "steelblue", alpha = 0.7, outlier.colour = "red") +
  geom_jitter(width = 0.1, alpha = 0.5, color = "navy", size = 2) +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 3, color = "darkred") +
  labs(title = paste(k, "-Fold CV Performance (", model_type, ")", sep = ""),
       x = "", y = "Value") +
  theme_pub()
save_plot(p_cv, paste0(tag, "_", model_type, "_cvbox"))

save_model(model, paste0(tag, "_", model_type, "_model"))
message("\n[OK] Cross-validation complete.")
