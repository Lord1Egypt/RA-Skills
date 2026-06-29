# ============================================================
# LASSO / Elastic Net Regression (glmnet)
# Supports: classification (binomial), regression (gaussian),
#           survival (cox), multinomial
# Features: full alpha path, CV selection, coefficient paths
# ============================================================

source("scripts/utils.R")
library(glmnet)
library(caret)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
test_path <- opts$test
alpha <- as.numeric(opts$alpha %||% "1")  # 1=LASSO, 0.5=Elastic Net, 0=Ridge
cv_folds <- as.numeric(opts$cv %||% "10")
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "lasso"
type_measure <- opts$measure %||% "default"

set.seed(seed)
df <- read_data(data_path)
y <- df[[target]]

# Prepare matrix
predictors <- setdiff(names(df), target)
X_num <- df[, predictors] |>
  mutate(across(where(is.character), as.factor)) |>
  mutate(across(where(is.factor), as.numeric))
X_mat <- as.matrix(X_num)
# Handle missing values
X_mat[is.na(X_mat)] <- 0

message("===================================")
message("   LASSO / Elastic Net (alpha=", alpha, ")")
message("===================================")
message("Data: ", nrow(df), " x ", ncol(X_mat), " features")

# Determine family
if (is.numeric(y)) {
  family <- "gaussian"
  if (type_measure == "default") type_measure <- "mse"
} else if (is_binary(y) || (is.factor(y) && nlevels(y) == 2)) {
  family <- "binomial"
  y <- as.numeric(y) - 1
  if (type_measure == "default") type_measure <- "auc"
} else if (is.factor(y)) {
  family <- "multinomial"
  if (type_measure == "default") type_measure <- "class"
} else {
  family <- "gaussian"
  if (type_measure == "default") type_measure <- "mse"
}
message("Family: ", family, " | Measure: ", type_measure)

# Cross-validated LASSO
message("\n--- Cross-Validation ---")
cv_fit <- cv.glmnet(X_mat, y, alpha = alpha, family = family,
                     type.measure = type_measure, nfolds = cv_folds,
                     parallel = FALSE)

message("Lambda min: ", round(cv_fit$lambda.min, 5))
message("Lambda 1se: ", round(cv_fit$lambda.1se, 5))

# Best model
best_lam <- if (opts$lambda == "min") cv_fit$lambda.min else cv_fit$lambda.1se
model_min <- glmnet(X_mat, y, alpha = alpha, family = family, lambda = cv_fit$lambda.min)
model_1se <- glmnet(X_mat, y, alpha = alpha, family = family, lambda = cv_fit$lambda.1se)

# Coefficient extraction
coef_min <- as.matrix(coef(cv_fit, s = "lambda.min"))
coef_1se <- as.matrix(coef(cv_fit, s = "lambda.1se"))

n_nonzero_min <- sum(coef_min != 0) - ifelse("(Intercept)" %in% rownames(coef_min), 1, 0)
n_nonzero_1se <- sum(coef_1se != 0) - ifelse("(Intercept)" %in% rownames(coef_1se), 1, 0)

message("Non-zero (lambda.min): ", n_nonzero_min)
message("Non-zero (lambda.1se): ", n_nonzero_1se)

# CV plot
png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_cv.png")),
    width = 8, height = 6, units = "in", res = 300)
par(mar = c(5, 5, 4, 2))
plot(cv_fit, main = paste0("LASSO CV (alpha = ", alpha, ")"))
dev.off()
message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_cv.png")))

# Coefficient path plot
png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_path.png")),
    width = 9, height = 7, units = "in", res = 300)
par(mar = c(5, 5, 4, 2))
plot(model_min, xvar = "lambda", label = TRUE, main = "LASSO Coefficient Path")
abline(v = log(cv_fit$lambda.min), lty = 2, col = "red")
abline(v = log(cv_fit$lambda.1se), lty = 2, col = "blue")
dev.off()
message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_path.png")))

# Non-zero coefficients table (lambda.1se)
coef_df <- data.frame(
  Variable = rownames(coef_1se),
  Coefficient = round(coef_1se[, 1], 4)
) |> filter(Coefficient != 0, Variable != "(Intercept)") |>
  arrange(desc(abs(Coefficient)))

if (nrow(coef_df) > 0) {
  message("\nNon-zero coefficients (lambda.1se): ", nrow(coef_df))
  print(head(coef_df, 20), row.names = FALSE)
  save_csv(coef_df, paste0(tag, "_coefs"))
  
  # Top coefficients plot
  top_n <- min(30, nrow(coef_df))
  coef_df$Variable <- factor(coef_df$Variable, levels = coef_df$Variable[order(coef_df$Coefficient)])
  p_coef <- ggplot(head(coef_df, top_n), aes(x = Variable, y = Coefficient)) +
    geom_col(aes(fill = Coefficient > 0), alpha = 0.85, show.legend = FALSE) +
    coord_flip() +
    scale_fill_manual(values = c("TRUE" = "#D73027", "FALSE" = "#1A5599")) +
    labs(title = paste0("LASSO Coefficients (alpha = ", alpha, ")"),
         x = "", y = "Coefficient") +
    theme_pub()
  save_plot(p_coef, paste0(tag, "_coefs"))
}

# Predict on test set
if (!is.null(test_path)) {
  test_df <- read_data(test_path)
  test_X <- test_df[, predictors] |>
    mutate(across(where(is.character), as.factor)) |>
    mutate(across(where(is.factor), as.numeric)) |>
    as.matrix()
  test_X[is.na(test_X)] <- 0
  
  preds <- predict(cv_fit, newx = test_X, s = "lambda.1se", type = "response")
  save_csv(data.frame(Prediction = as.vector(preds)), paste0(tag, "_predictions"))
}

# Save models
save_model(cv_fit, paste0(tag, "_cv"))
save_model(model_1se, paste0(tag, "_model"))
save_csv(coef_df, paste0(tag, "_coefs"))

message("\n[OK] LASSO complete.")
