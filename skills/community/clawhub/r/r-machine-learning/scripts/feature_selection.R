# ============================================================
# Feature Selection: Boruta / RFE / LASSO
# ============================================================

source("scripts/utils.R")
library(caret)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
method <- opts$method %||% "boruta"  # boruta, rfe, lasso, all
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "feat_select"

df <- read_data(data_path)
y <- df[[target]]
set.seed(seed)

message("===================================")
message("     Feature Selection: ", toupper(method))
message("===================================")
message("Total features: ", ncol(df) - 1)

# Remove target from predictors
predictors <- setdiff(names(df), target)
X <- df[, predictors, drop = FALSE]

# Ensure no missing
if (any(is.na(X))) {
  message("[WARN] Missing values detected, performing median/mode imputation...")
  for (col in names(X)) {
    if (is.numeric(X[[col]])) {
      X[[col]][is.na(X[[col]])] <- median(X[[col]], na.rm = TRUE)
    } else {
      X[[col]][is.na(X[[col]])] <- names(sort(table(X[[col]]), decreasing = TRUE))[1]
    }
  }
}

# ---- BORUTA ----
boruta_select <- function() {
  library(Boruta)
  message("\n--- Running Boruta ---")
  
  # Boruta needs all numeric
  X_num <- X |> mutate(across(where(is.character), as.factor)) |>
    mutate(across(where(is.factor), as.numeric))
  
  boruta_result <- Boruta(x = X_num, y = y, maxRuns = as.numeric(opts$runs %||% "100"),
                          pValue = as.numeric(opts$pval %||% "0.01"))
  
  # Results
  att_stats <- attStats(boruta_result)
  confirmed <- rownames(att_stats)[att_stats$decision == "Confirmed"]
  tentative <- rownames(att_stats)[att_stats$decision == "Tentative"]
  rejected <- rownames(att_stats)[att_stats$decision == "Rejected"]
  
  message("  Confirmed: ", length(confirmed))
  message("  Tentative: ", length(tentative))
  message("  Rejected:  ", length(rejected))
  
  # Plot
  if (length(confirmed) > 0) {
    png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_boruta.png")),
        width = 10, height = 7, units = "in", res = 300)
    plot(boruta_result, las = 2, cex.axis = 0.7, main = "Boruta Feature Selection")
    dev.off()
    message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_boruta.png")))
  }
  
  selected <- if (opts$strict == "TRUE") confirmed else c(confirmed, tentative)
  save_model(boruta_result, paste0(tag, "_boruta"))
  save_csv(att_stats, paste0(tag, "_boruta_stats"))
  
  list(features = selected, stats = att_stats, result = boruta_result)
}

# ---- RFE ----
rfe_select <- function() {
  message("\n--- Running RFE ---")
  sizes <- as.numeric(strsplit(opts$sizes %||% "5,10,15,20,25,30", ",")[[1]])
  sizes <- sizes[sizes < ncol(X)]
  if (length(sizes) == 0) sizes <- round(seq(2, min(ncol(X), 30), length.out = 5))
  
  ctrl <- rfeControl(functions = if (is.numeric(y)) caretFuncs else rfFuncs,
                     method = "cv", number = as.numeric(opts$cv %||% "5"),
                     verbose = FALSE)
  
  rfe_result <- rfe(x = X, y = y, sizes = sizes, rfeControl = ctrl)
  
  message("  Selected features: ", length(predictors(rfe_result)))
  message("  Top features: ", paste(head(predictors(rfe_result), 10), collapse = ", "))
  
  save_model(rfe_result, paste0(tag, "_rfe"))
  save_csv(data.frame(Variable = predictors(rfe_result), Rank = seq_along(predictors(rfe_result))),
           paste0(tag, "_rfe_vars"))
  
  list(features = predictors(rfe_result), result = rfe_result)
}

# ---- LASSO ----
lasso_select <- function() {
  library(glmnet)
  message("\n--- Running LASSO ---")
  
  X_num <- X |> mutate(across(where(is.character), as.factor)) |>
    mutate(across(where(is.factor), as.numeric))
  X_mat <- as.matrix(X_num)
  
  if (is.numeric(y)) {
    cv_fit <- cv.glmnet(X_mat, y, alpha = 1, nfolds = as.numeric(opts$cv %||% "10"))
  } else {
    y_num <- as.numeric(y) - 1
    cv_fit <- cv.glmnet(X_mat, y_num, alpha = 1, family = "binomial",
                        nfolds = as.numeric(opts$cv %||% "10"))
  }
  
  # Extract non-zero coefficients at lambda.1se
  coef_mat <- as.matrix(coef(cv_fit, s = "lambda.1se"))
  selected_vars <- rownames(coef_mat)[coef_mat[, 1] != 0]
  selected_vars <- setdiff(selected_vars, "(Intercept)")
  
  message("  Lambda min: ", round(cv_fit$lambda.min, 4))
  message("  Lambda 1se: ", round(cv_fit$lambda.1se, 4))
  message("  Selected features: ", length(selected_vars))
  
  # Plot
  png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_lasso_cv.png")),
      width = 8, height = 6, units = "in", res = 300)
  plot(cv_fit, main = "LASSO Cross-Validation")
  dev.off()
  message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_lasso_cv.png")))
  
  # Coefficient plot
  nonzero <- coef_mat[coef_mat[,1] != 0, , drop = FALSE]
  if (nrow(nonzero) > 1) {
    coef_df <- data.frame(
      Variable = rownames(nonzero),
      Coefficient = nonzero[, 1]
    ) |> filter(Variable != "(Intercept)") |>
      arrange(desc(abs(Coefficient)))
    
    coef_df$Variable <- factor(coef_df$Variable, levels = coef_df$Variable[order(coef_df$Coefficient)])
    p <- ggplot(coef_df, aes(x = Variable, y = Coefficient)) +
      geom_col(aes(fill = Coefficient > 0), alpha = 0.8, show.legend = FALSE) +
      coord_flip() +
      scale_fill_manual(values = c("TRUE" = "darkred", "FALSE" = "navy")) +
      labs(title = paste("LASSO Coefficients (lambda.1se)"), x = "", y = "Coefficient") +
      theme_pub()
    save_plot(p, paste0(tag, "_lasso_coefs"))
  }
  
  save_model(cv_fit, paste0(tag, "_lasso_cv"))
  save_csv(data.frame(Variable = selected_vars), paste0(tag, "_lasso_vars"))
  
  list(features = selected_vars, fit = cv_fit)
}

# ---- EXECUTE ----
result <- NULL

if (method == "boruta" || method == "all") {
  result <- boruta_select()
}
if (method == "rfe" || method == "all") {
  result <- rfe_select()
}
if (method == "lasso" || method == "all") {
  result <- lasso_select()
}

# Save final selected features
if (!is.null(result) && !is.null(result$features)) {
  save_csv(data.frame(Selected = result$features), paste0(tag, "_final"))
  message("\nFinal selected features (", length(result$features), "):")
  cat(paste(result$features, collapse = ", "), "\n")
}

message("\n[OK] Feature selection complete.")
