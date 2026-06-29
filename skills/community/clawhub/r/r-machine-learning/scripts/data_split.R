# ============================================================
# Data Splitting - Train/Validation/Test
# Supports: simple split, stratified, grouped, timeslice
# ============================================================

source("scripts/utils.R")
library(rsample)
library(caret)

opts <- parse_args()
data_path <- opts$data %||% stop("--data required (CSV path)")
target <- opts$target %||% stop("--target required (column name)")
ratio <- as.numeric(opts$ratio %||% "0.7")
valid_ratio <- as.numeric(opts$valid %||% "0")
method <- opts$method %||% "simple"  # simple, stratified, grouped
seed <- as.numeric(opts$seed %||% "42")
tag <- opts$tag %||% "split1"

message("===================================")
message("         Data Split")
message("===================================")

df <- read_data(data_path)
message("Rows: ", nrow(df), " | Columns: ", ncol(df))

if (!target %in% names(df)) stop("Target column '", target, "' not found.")
y <- df[[target]]
set.seed(seed)

# --- METHODS ---

if (method == "stratified") {
  # Stratified split - preserves class proportions
  if (is_binary(y) || is.factor(y)) {
    train_idx <- createDataPartition(y, p = ratio, list = FALSE)[,1]
  } else {
    # Stratified by quantiles for continuous
    y_grp <- cut(y, breaks = 5, labels = FALSE)
    train_idx <- createDataPartition(y_grp, p = ratio, list = FALSE)[,1]
  }
} else if (method == "grouped") {
  group_col <- opts$group %||% stop("--group required for grouped split")
  groups <- unique(df[[group_col]])
  n_groups <- length(groups)
  n_train <- max(1, round(n_groups * ratio))
  train_groups <- sample(groups, n_train)
  train_idx <- which(df[[group_col]] %in% train_groups)
} else {
  # Simple random
  train_idx <- sample(nrow(df), round(nrow(df) * ratio))
}

train <- df[train_idx, , drop = FALSE]
remaining <- df[-train_idx, , drop = FALSE]

# Validation split
if (valid_ratio > 0) {
  valid_n <- round(nrow(remaining) * valid_ratio / (1 - ratio))
  valid_idx <- sample(nrow(remaining), min(valid_n, nrow(remaining)))
  valid <- remaining[valid_idx, , drop = FALSE]
  test <- remaining[-valid_idx, , drop = FALSE]
} else {
  valid <- NULL
  test <- remaining
}

# --- SAVE ---
out_dir <- file.path(OUTPUT_DIR, "tables")
dir.create(out_dir, showWarnings = FALSE)

write.csv(train, file.path(out_dir, paste0(tag, "_train.csv")), row.names = FALSE)
write.csv(test, file.path(out_dir, paste0(tag, "_test.csv")), row.names = FALSE)
if (!is.null(valid)) {
  write.csv(valid, file.path(out_dir, paste0(tag, "_valid.csv")), row.names = FALSE)
}

# Summary
message("")
message("Split results:")
message("  Train: ", nrow(train), " (", round(nrow(train)/nrow(df)*100, 1), "%)")
message("  Test:  ", nrow(test), " (", round(nrow(test)/nrow(df)*100, 1), "%)")
if (!is.null(valid)) {
  message("  Valid: ", nrow(valid), " (", round(nrow(valid)/nrow(df)*100, 1), "%)")
}

# Target distribution
if (is_binary(y) || is.factor(y)) {
  message("")
  message("Target distribution (train):")
  print(prop.table(table(train[[target]])))
}

message("")
message("[OK] Saved to output/tables/")
