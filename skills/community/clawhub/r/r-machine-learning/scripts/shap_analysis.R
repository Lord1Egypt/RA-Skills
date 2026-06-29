# ============================================================
# SHAP Analysis (fastshap / DALEX / shapr)
# ============================================================

source("scripts/utils.R")
library(ggplot2)

opts <- parse_args()
model_path <- opts$model %||% stop("--model required (rds path)")
data_path <- opts$data %||% stop("--data required (feature data CSV)")
target <- opts$target %||% stop("--target required")
n_shap <- as.numeric(opts$n %||% "1000")
tag <- opts$tag %||% "shap"

message("===================================")
message("     SHAP Explainability Analysis")
message("===================================")

model <- readRDS(model_path)
df <- read_data(data_path)
y <- df[[target]]
X <- df[, setdiff(names(df), target), drop = FALSE]

# Try fastshap first (needs prediction function)
shap_available <- FALSE
shap_values <- NULL

message("Extracting model structure...")
# For caret train objects
if (inherits(model, "train")) {
  message("Model type: caret train object")
  
  # Try fastshap
  if (requireNamespace("fastshap", quietly = TRUE)) {
    message("Using fastshap for SHAP values...")
    library(fastshap)
    
    pred_fun <- function(object, newdata) {
      predict(object, newdata = newdata, type = "prob")[, 2]
    }
    
    # Sample for speed
    if (nrow(X) > n_shap) {
      set.seed(42)
      idx <- sample(nrow(X), n_shap)
      X_sample <- X[idx, , drop = FALSE]
    } else {
      X_sample <- X
    }
    
    shap_values <- tryCatch({
      explain(model, X = X_sample, pred_wrapper = pred_fun, nsim = 30)
    }, error = function(e) {
      message("[WARN] fastshap failed: ", e$message)
      NULL
    })
    
    if (!is.null(shap_values)) {
      shap_available <- TRUE
    }
  }
  
  # Try DALEX as alternative
  if (!shap_available && requireNamespace("DALEX", quietly = TRUE) &&
      requireNamespace("DALEXtra", quietly = TRUE)) {
    message("Using DALEX for variable importance...")
    library(DALEX)
    library(DALEXtra)
    
    explainer <- tryCatch({
      explain_tidymodels(model, data = X, y = y,
                         label = "model", verbose = FALSE)
    }, error = function(e) {
      tryCatch({
        DALEX::explain(model, data = X, y = y, label = "model", verbose = FALSE)
      }, error = function(e2) NULL)
    })
    
    if (!is.null(explainer)) {
      # Variable importance
      vip <- model_parts(explainer, type = "difference", N = n_shap)
      shap_available <- TRUE
      
      # Save VIP
      vip_df <- vip[vip$variable != "_full_model_" & vip$variable != "_baseline_", ]
      save_csv(vip_df, paste0(tag, "_dalex_vip"))
      
      # Plot VIP
      p_vip <- plot(vip) + labs(title = "Feature Importance (DALEX)")
      ggsave(file.path(OUTPUT_DIR, "plots", paste0(tag, "_dalex_vip.pdf")),
             plot = p_vip, width = 10, height = 7)
      ggsave(file.path(OUTPUT_DIR, "plots", paste0(tag, "_dalex_vip.png")),
             plot = p_vip, width = 10, height = 7, dpi = 300)
      message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_dalex_vip.png")))
      
      # Partial dependence
      for (i in seq_len(min(5, ncol(X)))) {
        var_name <- names(X)[i]
        if (is.numeric(X[[var_name]])) {
          pdp <- model_profile(explainer, variables = var_name, N = n_shap)
          p_pdp <- plot(pdp) + labs(title = paste("Partial Dependence:", var_name))
          ggsave(file.path(OUTPUT_DIR, "plots", paste0(tag, "_pdp_", var_name, ".png")),
                 plot = p_pdp, width = 8, height = 6, dpi = 300)
        }
      }
    }
  }
}

# If SHAP values computed, create plots
if (shap_available && !is.null(shap_values)) {
  message("\n--- SHAP Summary Analysis ---")
  
  # SHAP summary (beeswarm)
  shap_df <- as.data.frame(shap_values)
  
  # Mean absolute SHAP for importance
  mean_shap <- colMeans(abs(shap_df))
  top_features <- names(sort(mean_shap, decreasing = TRUE))
  
  message("Top 10 features by mean |SHAP|:")
  for (i in seq_len(min(10, length(top_features)))) {
    message(sprintf("  %d. %s: %.4f", i, top_features[i], mean_shap[top_features[i]]))
  }
  
  # Remove non-numeric columns from X_sample for SHAP plots
  X_sample_numeric <- X_sample[, sapply(X_sample, is.numeric), drop = FALSE]
  X_sample_numeric <- X_sample_numeric[, intersect(names(X_sample_numeric), names(shap_df)), drop = FALSE]
  shap_df <- shap_df[, names(X_sample_numeric), drop = FALSE]
  
  if (ncol(shap_df) > 0) {
    # Beeswarm summary plot
    shap_melt <- shap_df |>
      mutate(obs_id = row_number()) |>
      pivot_longer(-obs_id, names_to = "Feature", values_to = "SHAP") |>
      left_join(
        X_sample_numeric |>
          mutate(obs_id = row_number()) |>
          pivot_longer(-obs_id, names_to = "Feature", values_to = "Value"),
        by = c("obs_id", "Feature")
      ) |>
      mutate(
        Feature = factor(Feature, levels = rev(top_features[top_features %in% Feature])),
        Value_bin = cut(Value, breaks = 10, labels = FALSE)
      ) |>
      filter(!is.na(Feature))
    
    p_beeswarm <- ggplot(shap_melt, aes(x = SHAP, y = Feature, color = Value)) +
      geom_jitter(width = 0, height = 0.2, size = 1.5, alpha = 0.7) +
      scale_color_gradient2(low = "#1A5599", mid = "#F7F7F7", high = "#D73027",
                            midpoint = median(shap_melt$Value, na.rm = TRUE)) +
      geom_vline(xintercept = 0, linetype = "dashed", color = "grey50") +
      labs(title = "SHAP Summary (Beeswarm)",
           x = "SHAP Value (impact on model output)", y = "",
           color = "Feature Value") +
      theme_pub()
    save_plot(p_beeswarm, paste0(tag, "_beeswarm"), width = 12, height = max(6, ncol(shap_df) * 0.4))
    
    # Bar plot of mean |SHAP|
    mean_shap_df <- data.frame(
      Feature = factor(names(mean_shap), levels = rev(names(mean_shap))),
      MeanSHAP = mean_shap
    ) |> filter(Feature %in% names(shap_df))
    
    p_bar <- ggplot(mean_shap_df, aes(x = MeanSHAP, y = Feature)) +
      geom_col(fill = "steelblue", alpha = 0.85) +
      labs(title = "SHAP Feature Importance", x = "Mean |SHAP|", y = "") +
      theme_pub()
    save_plot(p_bar, paste0(tag, "_importance"), width = 10, height = max(5, ncol(shap_df) * 0.3))
    
    # Top feature dependence plots
    for (top_feat in head(top_features, 5)) {
      if (!top_feat %in% names(shap_df)) next
      dep_data <- data.frame(
        SHAP = shap_df[[top_feat]],
        Feature = X_sample_numeric[[top_feat]]
      ) |> filter(!is.na(Feature))
      
      p_dep <- ggplot(dep_data, aes(x = Feature, y = SHAP)) +
        geom_point(alpha = 0.5, color = "steelblue", size = 2) +
        geom_smooth(method = "loess", color = "#D73027", se = TRUE, fill = "#D73027", alpha = 0.15) +
        geom_hline(yintercept = 0, linetype = "dashed", color = "grey50") +
        labs(title = paste("SHAP Dependence:", top_feat),
             x = top_feat, y = "SHAP Value") +
        theme_pub()
      save_plot(p_dep, paste0(tag, "_dependence_", top_feat), width = 8, height = 6)
    }
    
    # Save SHAP values
    save_csv(shap_df, paste0(tag, "_values"))
    save_csv(mean_shap_df, paste0(tag, "_importance"))
  }
} else if (!shap_available) {
  message("\n[WARN] SHAP analysis not available for this model type.")
  message("Try: install.packages(c('fastshap', 'DALEX', 'DALEXtra'))")
  
  # Fallback: use varImp from caret
  if (inherits(model, "train")) {
    message("\nFallback: Using caret variable importance...")
    imp <- varImp(model)$importance
    if (!is.null(imp) && nrow(imp) > 0) {
      imp$Variable <- rownames(imp)
      imp <- imp[order(-imp$Overall), ]
      save_csv(imp, paste0(tag, "_caret_importance"))
      
      p_imp <- ggplot(head(imp, 20), aes(x = reorder(Variable, Overall), y = Overall)) +
        geom_col(fill = "steelblue", alpha = 0.8) +
        coord_flip() +
        labs(title = "Caret Variable Importance (SHAP unavailable)", x = "", y = "Importance") +
        theme_pub()
      save_plot(p_imp, paste0(tag, "_caret_importance"))
    }
  }
}

message("\n[OK] SHAP analysis complete.")
