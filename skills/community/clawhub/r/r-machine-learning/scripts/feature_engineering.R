# ============================================================
# Automated Feature Engineering
# ============================================================

source("scripts/utils.R")
library(recipes)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required")
target <- opts$target %||% stop("--target required")
tag <- opts$tag %||% "feat_eng"

df <- read_data(data_path)
y <- df[[target]]

message("===================================")
message("   Automated Feature Engineering")
message("===================================")

# Determine problem type
if (is.numeric(y)) {
  mode_type <- "regression"
} else if (is_binary(y)) {
  mode_type <- "classification"
} else {
  mode_type <- "multiclass"
}
message("Mode: ", mode_type)
message("Features before: ", ncol(df) - 1)

# Build recipe
rec <- recipe(as.formula(paste(target, "~ .")), data = df) |>
  # Remove zero-variance predictors
  step_zv(all_predictors()) |>
  # Remove near-zero variance predictors
  step_nzv(all_predictors()) |>
  # Impute numeric with median
  step_impute_median(all_numeric_predictors()) |>
  # Impute nominal with mode
  step_impute_mode(all_nominal_predictors()) |>
  # Create dummy variables for nominal
  step_dummy(all_nominal_predictors(), one_hot = FALSE) |>
  # Center and scale numeric
  step_center(all_numeric_predictors()) |>
  step_scale(all_numeric_predictors()) |>
  # Remove highly correlated (>0.9)
  step_corr(all_numeric_predictors(), threshold = 0.9) |>
  # PCA for dimensionality reduction (optional)
  step_pca(all_numeric_predictors(), threshold = 0.95)

# Additional engineered features (interaction terms)
if (opts$interactions == "TRUE" || opts$interact == "TRUE") {
  rec <- rec |> step_interact(terms = ~ all_numeric_predictors():all_numeric_predictors())
  message("Interaction terms: ON")
}

# Log-transform for skewed features
if (opts$log == "TRUE") {
  rec <- rec |> step_log(all_numeric_predictors(), offset = 1)
  message("Log transform: ON")
}

# Prepare and bake
prep <- prep(rec, training = df, verbose = FALSE)
df_processed <- bake(prep, new_data = NULL)

message("Features after: ", ncol(df_processed) - 1)

# Save processed data
save_csv(df_processed, paste0(tag, "_processed"))
save_model(prep, paste0(tag, "_recipe"))

message("\n[OK] Feature engineering complete.")
