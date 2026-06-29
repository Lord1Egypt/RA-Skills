# ============================================================
# One-Click Full ML Pipeline
# ============================================================

source("scripts/utils.R")
library(caret)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
type <- opts$type %||% "auto"  # classification, regression, survival, auto
cv <- as.numeric(opts$cv %||% "5")
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "pipeline"
models_str <- opts$models %||% "rf,xgboost,lasso,svm"

set.seed(seed)
message("===================================")
message("   One-Click ML Pipeline")
message("===================================")
message("Data: ", data_path, " | Target: ", target)

df <- read_data(data_path)
y <- df[[target]]

# Auto-detect type
if (type == "auto") {
  type <- if (is.numeric(y)) "regression" else "classification"
  message("Auto-detected type: ", type)
}

out_dir <- file.path(OUTPUT_DIR, tag)
dir.create(out_dir, showWarnings = FALSE)
dir.create(file.path(out_dir, "plots"), showWarnings = FALSE)
dir.create(file.path(out_dir, "models"), showWarnings = FALSE)
dir.create(file.path(out_dir, "tables"), showWarnings = FALSE)

message("\n[STEP 1/6] Data Splitting...")
set.seed(seed)
if (type == "classification") {
  train_idx <- createDataPartition(y, p = 0.7, list = FALSE)[,1]
} else {
  train_idx <- sample(nrow(df), round(0.7 * nrow(df)))
}
train <- df[train_idx, , drop = FALSE]
test <- df[-train_idx, , drop = FALSE]
message("  Train: ", nrow(train), " | Test: ", nrow(test))

write.csv(train, file.path(out_dir, "tables", "train.csv"), row.names = FALSE)
write.csv(test, file.path(out_dir, "tables", "test.csv"), row.names = FALSE)

# Prepare data for modeling
is_class <- type == "classification"
if (is_class && !is.factor(y)) {
  train[[target]] <- as.factor(train[[target]])
  test[[target]] <- as.factor(test[[target]])
}

# Train control
ctrl <- trainControl(
  method = "cv", number = cv,
  savePredictions = "final",
  classProbs = is_class,
  summaryFunction = if (is_class) twoClassSummary else defaultSummary,
  returnResamp = "all",
  verboseIter = FALSE
)

# Step 2-5: Train multiple models
model_list <- strsplit(models_str, ",")[[1]]
results <- data.frame()

for (m in model_list) {
  message(sprintf("\n[STEP 2/6] Training: %s ...", m))
  
  cfg <- switch(m,
    rf = list(method = "ranger",
      grid = expand.grid(mtry = floor(sqrt(ncol(train) - 1)),
                         splitrule = if (is_class) "gini" else "variance",
                         min.node.size = if (is_class) 1 else 5),
      extra = list(num.trees = 500)),
    xgboost = list(method = "xgbTree",
      grid = expand.grid(nrounds = 200, max_depth = 5, eta = 0.05, gamma = 0,
                         colsample_bytree = 0.8, min_child_weight = 1, subsample = 0.8),
      extra = list()),
    lasso = list(method = "glmnet",
      grid = expand.grid(alpha = 1, lambda = 0.01),
      extra = list()),
    svm = list(method = "svmRadial",
      grid = expand.grid(sigma = 0.05, C = 1),
      extra = list()),
    gbm = list(method = "gbm",
      grid = expand.grid(n.trees = 200, interaction.depth = 3,
                         shrinkage = 0.05, n.minobsinnode = 10),
      extra = list()),
    nnet = list(method = "nnet",
      grid = expand.grid(size = 5, decay = 0.1),
      extra = list(MaxNWts = 10000, trace = FALSE))
  )
  
  train_args <- list(
    form = as.formula(paste(target, "~ .")),
    data = train,
    method = cfg$method,
    trControl = ctrl,
    tuneGrid = cfg$grid,
    metric = if (is_class) "ROC" else "RMSE",
    verbose = FALSE
  )
  for (n in setdiff(names(cfg$extra), names(train_args))) {
    train_args[[n]] <- cfg$extra[[n]]
  }
  
  model <- tryCatch(do.call(train, train_args), error = function(e) NULL)
  
  if (!is.null(model)) {
    saveRDS(model, file.path(out_dir, "models", paste0(m, ".rds")))
    
    # Test set evaluation
    message(sprintf("[STEP 3/6] Evaluating: %s ...", m))
    preds <- predict(model, newdata = test)
    
    if (is_class) {
      probs <- predict(model, newdata = test, type = "prob")
      cm <- confusionMatrix(preds, test[[target]])
      metric_val <- cm$overall["Accuracy"]
      metric_name <- "Accuracy"
      auc_val <- tryCatch({
        roc_obj <- pROC::roc(test[[target]], probs[, 2], quiet = TRUE)
        pROC::auc(roc_obj)
      }, error = function(e) NA)
      
      save_csv(cbind(Observed = as.character(test[[target]]), 
                     Predicted = as.character(preds), probs),
               file.path(out_dir, "tables", paste0(m, "_preds")))
      
      results <- rbind(results, data.frame(
        Model = m, Accuracy = round(metric_val, 4),
        Kappa = round(cm$overall["Kappa"], 4),
        AUC = round(auc_val, 4),
        Sensitivity = round(cm$byClass["Sensitivity"], 4),
        Specificity = round(cm$byClass["Specificity"], 4),
        stringsAsFactors = FALSE
      ))
    } else {
      rmse <- sqrt(mean((as.numeric(preds) - as.numeric(test[[target]]))^2))
      r2 <- 1 - sum((as.numeric(test[[target]]) - as.numeric(preds))^2) /
        sum((as.numeric(test[[target]]) - mean(as.numeric(test[[target]])))^2)
      
      save_csv(data.frame(Observed = test[[target]], Predicted = preds),
               file.path(out_dir, "tables", paste0(m, "_preds")))
      
      results <- rbind(results, data.frame(
        Model = m, RMSE = round(rmse, 4),
        R2 = round(r2, 4),
        stringsAsFactors = FALSE
      ))
    }
    message(sprintf("  Done: %s", m))
  } else {
    message(sprintf("  Failed: %s", m))
  }
}

message("\n[STEP 4/6] Comparing models...")
save_csv(results, file.path(out_dir, "tables", "model_comparison"))

# Comparison plot
if (is_class && "AUC" %in% names(results)) {
  p_comp <- ggplot(results, aes(x = reorder(Model, AUC), y = AUC, fill = Model)) +
    geom_col(alpha = 0.85, show.legend = FALSE) +
    geom_text(aes(label = round(AUC, 3)), hjust = -0.1, size = 3.5) +
    coord_flip() + ylim(0, 1) +
    scale_fill_brewer(palette = "Set2") +
    labs(title = "Model Comparison (Test AUC)", x = "", y = "AUC") +
    theme_pub()
} else if ("R2" %in% names(results)) {
  p_comp <- ggplot(results, aes(x = reorder(Model, R2), y = R2, fill = Model)) +
    geom_col(alpha = 0.85, show.legend = FALSE) +
    geom_text(aes(label = round(R2, 3)), hjust = -0.1, size = 3.5) +
    coord_flip() +
    scale_fill_brewer(palette = "Set2") +
    labs(title = "Model Comparison (Test R²)", x = "", y = "R²") +
    theme_pub()
}
save_plot(p_comp, paste0(tag, "_comparison"))

# Step 5: Best model SHAP
best_model_name <- results$Model[1]
message(sprintf("\n[STEP 5/6] SHAP analysis for best model: %s ...", best_model_name))
best_model <- readRDS(file.path(out_dir, "models", paste0(best_model_name, ".rds")))

tryCatch({
  if (requireNamespace("fastshap", quietly = TRUE)) {
    library(fastshap)
    test_X <- test[, setdiff(names(test), target), drop = FALSE]
    pred_fun <- function(object, newdata) {
      predict(object, newdata = newdata, type = "prob")[, 2]
    }
    shap_values <- explain(best_model, X = test_X, pred_wrapper = pred_fun, nsim = 20)
    
    shap_df <- as.data.frame(shap_values)
    mean_shap <- colMeans(abs(shap_df))
    top_feats <- names(sort(mean_shap, decreasing = TRUE)[1:15])
    
    shap_df <- shap_df[, intersect(top_feats, names(shap_df)), drop = FALSE]
    
    if (ncol(shap_df) > 0) {
      save_csv(as.data.frame(shap_values), file.path(out_dir, "tables", "shap_values"))
      
      mean_df <- data.frame(Feature = names(mean_shap), MeanSHAP = mean_shap) |>
        filter(Feature %in% names(shap_df)) |>
        arrange(desc(MeanSHAP))
      save_csv(mean_df, file.path(out_dir, "tables", "shap_importance"))
      
      p_shap <- ggplot(head(mean_df, 15), aes(x = MeanSHAP, y = reorder(Feature, MeanSHAP))) +
        geom_col(fill = "steelblue", alpha = 0.85) +
        labs(title = paste("SHAP Importance:", best_model_name), x = "Mean |SHAP|", y = "") +
        theme_pub()
      save_plot(p_shap, paste0(tag, "_shap"))
    }
  }
}, error = function(e) message("[WARN] SHAP skipped: ", e$message))

message("\n[STEP 6/6] Generating report...")
source(file.path(getwd(), "scripts", "report_generator.R"))

# Generate HTML report
report_script <- file.path(getwd(), "scripts", "report_generator.R")
tryCatch({
  rmarkdown::render(input = report_script,
                    output_file = file.path(out_dir, paste0(tag, "_report.html")),
                    params = list(
                      tag = tag,
                      target = target,
                      type = type,
                      n_train = nrow(train),
                      n_test = nrow(test),
                      n_features = ncol(train) - 1,
                      results = results,
                      output_dir = out_dir
                    ),
                    quiet = TRUE)
  message("Report: ", file.path(out_dir, paste0(tag, "_report.html")))
}, error = function(e) message("[WARN] Report generation failed: ", e$message))

message("\n===================================")
message(" Pipeline Complete!")
message("===================================")
message("Output: ", out_dir)
cat("Best model: ", best_model_name, "\n")
print(results, row.names = FALSE)
