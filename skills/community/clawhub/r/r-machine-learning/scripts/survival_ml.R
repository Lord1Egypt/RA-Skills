# ============================================================
# Survival ML: Random Survival Forest, XGBoost Cox, Coxnet
# ============================================================

source("scripts/utils.R")
library(survival)
library(survminer)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
time_col <- opts$time %||% stop("--time required (survival time column)")
event_col <- opts$event %||% stop("--event required (event indicator column)")
model_type <- opts$model %||% "rfsrc"  # rfsrc, coxnet, xgb_cox
test_path <- opts$test
cv <- as.numeric(opts$cv %||% "5")
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "survival"

set.seed(seed)
df <- read_data(data_path)

message("===================================")
message("   Survival Machine Learning")
message("===================================")
message("Method: ", model_type)
message("Rows: ", nrow(df), " | Features: ", ncol(df) - 2)
event_rate <- mean(df[[event_col]], na.rm = TRUE)
message("Event rate: ", round(event_rate * 100, 1), "%")

# Prepare data
predictors <- setdiff(names(df), c(time_col, event_col))

# Create survival object
surv_obj <- Surv(df[[time_col]], df[[event_col]])

# ---- Random Survival Forest ----
if (model_type == "rfsrc") {
  if (!requireNamespace("randomForestSRC", quietly = TRUE)) {
    install.packages("randomForestSRC")
  }
  library(randomForestSRC)
  
  message("\n--- Random Survival Forest ---")
  ntree <- as.numeric(opts$trees %||% "1000")
  mtry <- as.numeric(opts$mtry %||% max(1, floor(sqrt(length(predictors)))))
  nodesize <- as.numeric(opts$nodesize %||% "15")
  
  rf_formula <- as.formula(paste("Surv(", time_col, ",", event_col, ") ~ ."))
  
  # Tune mtry?
  if (opts$tune == "TRUE") {
    message("Tuning mtry...")
    oob_errors <- sapply(seq(2, min(ncol(df)-2, 20), by = 2), function(m) {
      rf <- rfsrc(rf_formula, data = df, ntree = ntree, mtry = m,
                   nodesize = nodesize, importance = TRUE, seed = seed)
      rf$err.rate[ntree]
    })
    best_mtry <- seq(2, min(ncol(df)-2, 20), by = 2)[which.min(oob_errors)]
    message("Best mtry: ", best_mtry)
    mtry <- best_mtry
  }
  
  model <- rfsrc(rf_formula, data = df, ntree = ntree, mtry = mtry,
                  nodesize = nodesize, importance = TRUE, seed = seed)
  
  # Error rate
  message("OOB error rate at ", ntree, " trees: ", round(model$err.rate[ntree], 4))
  
  # Variable importance (VIMP)
  vimp <- data.frame(
    Variable = names(model$importance),
    Importance = round(model$importance, 4)
  ) |> arrange(desc(Importance))
  message("\nTop 10 variables (VIMP):")
  print(head(vimp, 10), row.names = FALSE)
  save_csv(vimp, paste0(tag, "_vimp"))
  
  p_vimp <- ggplot(head(vimp, 20), aes(x = reorder(Variable, Importance), y = Importance)) +
    geom_col(fill = "#1A5599", alpha = 0.85) +
    coord_flip() +
    labs(title = "Random Survival Forest Variable Importance",
         x = "", y = "VIMP") +
    theme_pub()
  save_plot(p_vimp, paste0(tag, "_vimp"))
  
  # Survival curves for different risk groups
  risk_score <- predict(model)$predicted
  risk_grp <- cut(risk_score, breaks = quantile(risk_score, c(0, 0.33, 0.67, 1)),
                  labels = c("Low", "Medium", "High"), include.lowest = TRUE)
  
  km_fit <- survfit(Surv(df[[time_col]], df[[event_col]]) ~ risk_grp, data = df)
  p_km <- ggsurvplot(km_fit, data = df,
                      pval = TRUE, pval.coord = c(0, 0.2),
                      risk.table = TRUE, risk.table.col = "strata",
                      palette = c("#1A5599", "#F7A800", "#D73027"),
                      title = "Kaplan-Meier by RSF Risk Group",
                      xlab = "Time", ylab = "Survival Probability",
                      legend.title = "Risk Group",
                      ggtheme = theme_pub())
  
  pdf(file.path(OUTPUT_DIR, "plots", paste0(tag, "_km.pdf")),
      width = 10, height = 8)
  print(p_km)
  dev.off()
  png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_km.png")),
      width = 10, height = 8, units = "in", res = 300)
  print(p_km)
  dev.off()
  message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_km.png")))
  
  # C-index
  cindex <- 1 - model$err.rate[ntree]  # approximate
  message("Approximate C-index: ", round(cindex, 4))
}

# ---- Coxnet (LASSO Cox) ----
if (model_type == "coxnet") {
  library(glmnet)
  
  message("\n--- Coxnet (LASSO Cox Regression) ---")
  
  # Prepare matrix
  X_num <- df[, predictors] |>
    mutate(across(where(is.character), as.factor)) |>
    mutate(across(where(is.factor), as.numeric))
  X_mat <- as.matrix(X_num)
  X_mat[is.na(X_mat)] <- 0
  
  y_surv <- Surv(df[[time_col]], df[[event_col]])
  
  cv_fit <- cv.glmnet(X_mat, y_surv, family = "cox", alpha = 1,
                       nfolds = cv, type.measure = "C")
  
  message("Lambda min: ", round(cv_fit$lambda.min, 5))
  message("Lambda 1se: ", round(cv_fit$lambda.1se, 5))
  
  # Non-zero coefficients (lambda.1se)
  coef_mat <- as.matrix(coef(cv_fit, s = "lambda.1se"))
  nonzero <- rownames(coef_mat)[coef_mat[, 1] != 0]
  message("Selected features: ", length(nonzero))
  
  coef_df <- data.frame(
    Variable = rownames(coef_mat)[coef_mat[,1] != 0],
    Coefficient = round(coef_mat[coef_mat[,1] != 0, 1], 4),
    HR = round(exp(coef_mat[coef_mat[,1] != 0, 1]), 4)
  ) |> arrange(desc(abs(Coefficient)))
  
  if (nrow(coef_df) > 0) {
    print(head(coef_df, 15), row.names = FALSE)
    save_csv(coef_df, paste0(tag, "_coxnet_coefs"))
    
    p_coef <- ggplot(head(coef_df, 30), aes(x = reorder(Variable, Coefficient), y = Coefficient)) +
      geom_col(aes(fill = Coefficient > 0), alpha = 0.85, show.legend = FALSE) +
      scale_fill_manual(values = c("TRUE" = "#D73027", "FALSE" = "#1A5599")) +
      coord_flip() +
      labs(title = "Coxnet Coefficients (lambda.1se)", x = "", y = "Coefficient (log HR)") +
      theme_pub()
    save_plot(p_coef, paste0(tag, "_coxnet_coefs"))
  }
  
  # CV plot
  png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_coxnet_cv.png")),
      width = 8, height = 6, units = "in", res = 300)
  plot(cv_fit, main = "Coxnet Cross-Validation")
  dev.off()
  message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_coxnet_cv.png")))
  
  # Risk scores and KM
  lp <- predict(cv_fit, newx = X_mat, s = "lambda.1se", type = "link")
  risk_grp <- cut(as.vector(lp), breaks = quantile(lp, c(0, 0.33, 0.67, 1), na.rm = TRUE),
                  labels = c("Low", "Medium", "High"), include.lowest = TRUE)
  
  km_fit <- survfit(Surv(df[[time_col]], df[[event_col]]) ~ risk_grp)
  p_km <- ggsurvplot(km_fit, data = df, pval = TRUE,
                      palette = c("#1A5599", "#F7A800", "#D73027"),
                      title = "Kaplan-Meier by Coxnet Risk Group",
                      risk.table = TRUE,
                      ggtheme = theme_pub())
  
  pdf(file.path(OUTPUT_DIR, "plots", paste0(tag, "_coxnet_km.pdf")),
      width = 10, height = 8)
  print(p_km)
  dev.off()
  png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_coxnet_km.png")),
      width = 10, height = 8, units = "in", res = 300)
  print(p_km)
  dev.off()
  message("[SAVED] KM plot.")
  
  model <- cv_fit
}

# ---- XGBoost Cox ----
if (model_type == "xgb_cox") {
  if (!requireNamespace("xgboost", quietly = TRUE)) {
    install.packages("xgboost")
  }
  library(xgboost)
  
  message("\n--- XGBoost Cox PH ---")
  
  X_num <- df[, predictors] |>
    mutate(across(where(is.character), as.factor)) |>
    mutate(across(where(is.factor), as.numeric))
  X_mat <- as.matrix(X_num)
  X_mat[is.na(X_mat)] <- 0
  
  # xgboost survival requires cox ph objective
  dtrain <- xgb.DMatrix(X_mat, label = df[[time_col]])
  setinfo(dtrain, "censored", 1 - df[[event_col]])  # 0=event, 1=censored
  
  params <- list(
    objective = "survival:cox",
    eval_metric = "cox-nloglik",
    eta = as.numeric(opts$eta %||% "0.05"),
    max_depth = as.numeric(opts$max_depth %||% "4"),
    subsample = as.numeric(opts$subsample %||% "0.8"),
    colsample_bytree = as.numeric(opts$colsample %||% "0.8"),
    min_child_weight = as.numeric(opts$min_child %||% "3")
  )
  nrounds <- as.numeric(opts$nrounds %||% "200")
  
  model <- xgb.train(params = params, data = dtrain, nrounds = nrounds,
                     verbose = 0, early_stopping_rounds = 20)
  
  # Feature importance
  imp_matrix <- xgb.importance(feature_names = colnames(X_mat), model = model)
  message("\nTop 10 features:")
  print(head(imp_matrix, 10))
  save_csv(imp_matrix, paste0(tag, "_xgb_importance"))
  
  p_imp <- xgb.ggplot.importance(imp_matrix[1:20, ]) +
    labs(title = "XGBoost Survival Feature Importance") +
    theme_pub()
  save_plot(p_imp, paste0(tag, "_xgb_importance"))
  
  # Risk scores
  risk_score <- predict(model, dtrain)
  risk_grp <- cut(risk_score, breaks = quantile(risk_score, c(0, 0.33, 0.67, 1), na.rm = TRUE),
                  labels = c("Low", "Medium", "High"), include.lowest = TRUE)
  
  km_fit <- survfit(Surv(df[[time_col]], df[[event_col]]) ~ risk_grp)
  p_km <- ggsurvplot(km_fit, data = df, pval = TRUE,
                      palette = c("#1A5599", "#F7A800", "#D73027"),
                      title = "Kaplan-Meier by XGBoost Risk Group",
                      ggtheme = theme_pub())
  
  pdf(file.path(OUTPUT_DIR, "plots", paste0(tag, "_xgb_km.pdf")),
      width = 10, height = 8)
  print(p_km)
  dev.off()
  png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_xgb_km.png")),
      width = 10, height = 8, units = "in", res = 300)
  print(p_km)
  dev.off()
  message("[SAVED] KM plot.")
}

# Save
save_model(model, paste0(tag, "_model"))

message("\n[OK] Survival ML complete.")
