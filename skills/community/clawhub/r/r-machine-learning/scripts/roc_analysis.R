# ============================================================
# ROC Analysis + PR Curve (pROC + PRROC)
# ============================================================

source("scripts/utils.R")
library(pROC)
library(PRROC)

opts <- parse_args()
pred_path <- opts$preds %||% stop("--preds required (CSV with prediction columns)")
truth_path <- opts$truth %||% stop("--truth required (CSV with ground truth)")
outcome_col <- opts$outcome %||% stop("--outcome required (true label column)")
pred_col <- opts$pred %||% "Predicted"  # column name for positive class probability
pos_class <- opts$positive %||% NULL   # which class is positive
ci_flag <- opts$ci %||% "TRUE"
tag <- opts$tag %||% "roc"

preds <- read_data(pred_path)
truth <- read_data(truth_path)

# Merge if necessary
if (nrow(preds) != nrow(truth)) {
  message("[INFO] Files have different row counts. Attempting merge by row order...")
}
if (nrow(preds) > nrow(truth)) preds <- preds[1:nrow(truth), ]
if (nrow(truth) > nrow(preds)) truth <- truth[1:nrow(preds), ]

y_true <- truth[[outcome_col]]

message("===================================")
message("        ROC & PR Analysis")
message("===================================")

# Detect probability columns (exclude non-prob columns)
prob_cols <- setdiff(names(preds), pred_col)
if (length(prob_cols) == 0) prob_cols <- names(preds)

for (prob_col in prob_cols) {
  if (!is.numeric(preds[[prob_col]])) next
  
  message("\n--- ", prob_col, " ---")
  
  if (is.factor(y_true)) {
    levels_y <- levels(y_true)
    if (length(levels_y) != 2) {
      message("[SKIP] Multi-class ROC not supported in this script. Use pROC::multiclass.roc")
      next
    }
    if (is.null(pos_class)) {
      # Use the level with higher mean probability
      pos_class_use <- levels_y[which.max(tapply(preds[[prob_col]], y_true, mean, na.rm = TRUE))]
    } else {
      pos_class_use <- pos_class
    }
    y_binary <- ifelse(y_true == pos_class_use, 1, 0)
    message("Positive class: ", pos_class_use)
  } else if (all(y_true %in% c(0, 1))) {
    y_binary <- y_true
    pos_class_use <- 1
  } else {
    y_binary <- as.numeric(y_true == max(y_true))
    pos_class_use <- max(y_true)
  }
  
  # ROC
  roc_obj <- roc(y_binary, preds[[prob_col]], ci = (ci_flag == "TRUE"), quiet = TRUE)
  
  auc_val <- auc(roc_obj)
  ci_auc <- if (ci_flag == "TRUE") ci.auc(roc_obj) else NULL
  
  message("AUC: ", round(auc_val, 4))
  if (!is.null(ci_auc)) {
    message("95% CI: [", round(ci_auc[1], 4), ", ", round(ci_auc[3], 4), "]")
  }
  
  # Optimal threshold (Youden index)
  youden <- coords(roc_obj, "best", best.method = "youden",
                   ret = c("threshold", "specificity", "sensitivity", "accuracy",
                           "ppv", "npv"))
  message("Optimal threshold: ", round(youden$threshold, 4))
  message("  Sensitivity: ", round(youden$sensitivity, 4))
  message("  Specificity: ", round(youden$specificity, 4))
  message("  Accuracy: ", round(youden$accuracy, 4))
  message("  PPV: ", round(youden$ppv, 4))
  message("  NPV: ", round(youden$npv, 4))
  
  # ROC plot
  png(file.path(OUTPUT_DIR, "plots", paste0(tag, "_", prob_col, "_roc.png")),
      width = 8, height = 7, units = "in", res = 300)
  plot(roc_obj, main = paste("ROC Curve -", prob_col),
       col = "#D73027", lwd = 2, cex.main = 1.3)
  legend("bottomright",
         legend = paste0("AUC = ", round(auc_val, 3),
                         if (!is.null(ci_auc)) paste0("\n95% CI [", round(ci_auc[1], 3), "-", round(ci_auc[3], 3), "]")),
         bty = "n", cex = 1.1)
  dev.off()
  message("[SAVED] ", file.path(OUTPUT_DIR, "plots", paste0(tag, "_", prob_col, "_roc.png")))
  
  # ggplot version
  roc_df <- data.frame(
    specificity = rev(roc_obj$specificities),
    sensitivity = rev(roc_obj$sensitivities)
  )
  p_roc <- ggplot(roc_df, aes(x = 1 - specificity, y = sensitivity)) +
    geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "grey50") +
    geom_line(color = "#D73027", linewidth = 1.2) +
    annotate("text", x = 0.75, y = 0.25,
             label = paste0("AUC = ", round(auc_val, 3),
                            if (!is.null(ci_auc)) paste0("\n95% CI: ", round(ci_auc[1], 3), "-", round(ci_auc[3], 3))),
             size = 4.5, fontface = "bold") +
    labs(title = paste("ROC Curve -", prob_col),
         x = "1 - Specificity", y = "Sensitivity") +
    theme_pub()
  save_plot(p_roc, paste0(tag, "_", prob_col, "_roc_gg"))
  
  # PR Curve
  pr_obj <- pr.curve(scores.class0 = preds[[prob_col]][y_binary == 1],
                     scores.class1 = preds[[prob_col]][y_binary == 0],
                     curve = TRUE)
  message("PR AUC: ", round(pr_obj$auc.integral, 4))
  
  # Sensitivity/Specificity over thresholds
  thresh_seq <- seq(0, 1, by = 0.01)
  sens_spec <- data.frame(
    Threshold = numeric(),
    Sensitivity = numeric(),
    Specificity = numeric(),
    Accuracy = numeric()
  )
  for (th in thresh_seq) {
    pred_class <- ifelse(preds[[prob_col]] >= th, 1, 0)
    tp <- sum(pred_class == 1 & y_binary == 1)
    tn <- sum(pred_class == 0 & y_binary == 0)
    fp <- sum(pred_class == 1 & y_binary == 0)
    fn <- sum(pred_class == 0 & y_binary == 1)
    sens_spec <- rbind(sens_spec, data.frame(
      Threshold = th,
      Sensitivity = ifelse((tp+fn) > 0, tp/(tp+fn), NA),
      Specificity = ifelse((tn+fp) > 0, tn/(tn+fp), NA),
      Accuracy = ifelse(nrow(preds) > 0, (tp+tn)/nrow(preds), NA)
    ))
  }
  
  p_thresh <- sens_spec |>
    pivot_longer(-Threshold, names_to = "Metric", values_to = "Value") |>
    ggplot(aes(x = Threshold, y = Value, color = Metric)) +
    geom_line(linewidth = 1) +
    geom_vline(xintercept = youden$threshold, linetype = "dashed", color = "grey40") +
    annotate("text", x = youden$threshold + 0.05, y = 0.5,
             label = paste("Optimal:", round(youden$threshold, 3)), size = 3.5, angle = 90) +
    scale_color_manual(values = c("Sensitivity" = "#D73027", "Specificity" = "#1A5599",
                                  "Accuracy" = "#1B9E77")) +
    labs(title = "Performance vs. Threshold", x = "Threshold", y = "Value") +
    theme_pub()
  save_plot(p_thresh, paste0(tag, "_", prob_col, "_threshold"))
  
  # PR plot
  pr_df <- data.frame(Recall = pr_obj$curve[, 1], Precision = pr_obj$curve[, 2])
  p_pr <- ggplot(pr_df, aes(x = Recall, y = Precision)) +
    geom_line(color = "#1A5599", linewidth = 1.2) +
    annotate("text", x = 0.75, y = 0.25,
             label = paste("PR AUC =", round(pr_obj$auc.integral, 3)),
             size = 4.5, fontface = "bold") +
    labs(title = paste("PR Curve -", prob_col), x = "Recall", y = "Precision") +
    theme_pub()
  save_plot(p_pr, paste0(tag, "_", prob_col, "_pr"))
  
  # Save metrics table
  metrics_df <- data.frame(
    Metric = c("AUC", "AUC_CI_Lower", "AUC_CI_Upper", "PR_AUC",
               "Optimal_Threshold", "Sensitivity", "Specificity",
               "Accuracy", "PPV", "NPV"),
    Value = c(
      round(auc_val, 4),
      if (!is.null(ci_auc)) round(ci_auc[1], 4) else NA,
      if (!is.null(ci_auc)) round(ci_auc[3], 4) else NA,
      round(pr_obj$auc.integral, 4),
      round(youden$threshold, 4), round(youden$sensitivity, 4),
      round(youden$specificity, 4), round(youden$accuracy, 4),
      round(youden$ppv, 4), round(youden$npv, 4)
    )
  )
  save_csv(metrics_df, paste0(tag, "_", prob_col, "_metrics"))
}

message("\n[OK] ROC analysis complete.")
