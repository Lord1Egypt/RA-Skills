# ============================================================
# Calibration Curves + Hosmer-Lemeshow Test
# ============================================================

source("scripts/utils.R")
library(rms)
library(ResourceSelection)
library(ggplot2)

opts <- parse_args()
pred_path <- opts$preds %||% stop("--preds required (predicted probabilities CSV)")
truth_path <- opts$truth %||% stop("--truth required (ground truth CSV)")
outcome_col <- opts$outcome %||% stop("--outcome required")
prob_col <- opts$prob %||% "Predicted"
groups <- as.numeric(opts$groups %||% "10")
tag <- opts$tag %||% "calibration"

preds <- read_data(pred_path)
truth <- read_data(truth_path)

if (nrow(preds) != nrow(truth)) {
  n <- min(nrow(preds), nrow(truth))
  preds <- preds[1:n, , drop = FALSE]
  truth <- truth[1:n, , drop = FALSE]
}

y_true <- truth[[outcome_col]]  
y_prob <- preds[[prob_col]]

# Convert to binary if factor
if (is.factor(y_true)) {
  y_binary <- as.numeric(y_true) - 1
} else if (all(y_true %in% c(0, 1))) {
  y_binary <- y_true
} else {
  # Assume first unique value is negative
  uniq <- unique(y_true)
  y_binary <- ifelse(y_true == max(uniq), 1, 0)
}

message("===================================")
message("     Calibration Analysis")
message("===================================")
message("Groups: ", groups)

# Hosmer-Lemeshow test
hl_test <- hoslem.test(y_binary, y_prob, g = groups)
message("\nHosmer-Lemeshow Test:")
message("  X-squared: ", round(hl_test$statistic, 4))
message("  df: ", hl_test$parameter)
message("  p-value: ", round(hl_test$p.value, 4))
if (hl_test$p.value > 0.05) {
  message("  > Model is well-calibrated (p > 0.05)")
} else {
  message("  > Calibration is poor (p < 0.05)")
}

# Calibration curve data
cal_data <- data.frame(
  y = y_binary,
  prob = y_prob,
  bin = cut(y_prob, breaks = seq(0, 1, length.out = groups + 1),
            include.lowest = TRUE)
)

cal_curve <- cal_data |>
  group_by(bin) |>
  summarise(
    n = n(),
    mean_pred = mean(prob, na.rm = TRUE),
    mean_obs = mean(y, na.rm = TRUE),
    se = sqrt(mean_pred * (1 - mean_pred) / n()),
    .groups = "drop"
  ) |>
  filter(n > 0)

# Brier score
brier <- mean((y_binary - y_prob)^2)
message("\nBrier Score: ", round(brier, 5))
message("  > 0 = perfect, 0.25 = random, >0.25 = worse than random")

# Intercept calibration (calibration-in-the-large)
log_reg <- glm(y_binary ~ offset(qlogis(pmax(pmin(y_prob, 0.999), 0.001))),
               family = binomial)
cal_intercept <- coef(log_reg)
message("Calibration intercept: ", round(cal_intercept, 4))
message("  > 0 = systematic underestimation, < 0 = overestimation")

# Calibration slope
log_reg2 <- glm(y_binary ~ qlogis(pmax(pmin(y_prob, 0.999), 0.001)),
                family = binomial)
cal_slope <- coef(log_reg2)[2]
message("Calibration slope: ", round(cal_slope, 4))
message("  > 1 = well-calibrated, < 1 = overfitting (too extreme)")

# Calibration plot
p_cal <- ggplot(cal_curve, aes(x = mean_pred, y = mean_obs)) +
  geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "grey50", linewidth = 1) +
  geom_point(size = 3, color = "#D73027") +
  geom_errorbar(aes(ymin = mean_obs - 1.96 * se, ymax = mean_obs + 1.96 * se),
                width = 0.02, color = "#D73027", alpha = 0.6) +
  geom_smooth(method = "loess", se = TRUE, color = "#1A5599", fill = "#1A5599", alpha = 0.15) +
  coord_cartesian(xlim = c(0, 1), ylim = c(0, 1)) +
  scale_x_continuous(breaks = seq(0, 1, 0.2), labels = seq(0, 1, 0.2)) +
  scale_y_continuous(breaks = seq(0, 1, 0.2), labels = seq(0, 1, 0.2)) +
  annotate("text", x = 0.05, y = 0.95, hjust = 0, vjust = 1, size = 4,
           label = paste0(
             "Brier: ", round(brier, 4),
             "\nIntercept: ", round(cal_intercept, 3),
             "\nSlope: ", round(cal_slope, 3),
             "\nHL p: ", round(hl_test$p.value, 4)
           )) +
  labs(title = "Calibration Curve", x = "Predicted Probability", y = "Observed Frequency") +
  theme_pub()
save_plot(p_cal, paste0(tag, "_curve"))

# Calibration by decile bar plot
p_bar <- ggplot(cal_curve, aes(x = bin, y = mean_obs - mean_pred)) +
  geom_col(aes(fill = mean_obs - mean_pred > 0), alpha = 0.8, show.legend = FALSE) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey40") +
  geom_text(aes(label = round(n, 0)), y = 0.01, hjust = 0, size = 3, angle = 90) +
  scale_fill_manual(values = c("TRUE" = "#D73027", "FALSE" = "#1A5599")) +
  labs(title = "Calibration Error by Decile",
       x = "Risk Decile", y = "Observed - Predicted") +
  theme_pub() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7))
save_plot(p_bar, paste0(tag, "_error_decile"), width = 10, height = 6)

# Save calibration table
save_csv(cal_curve, paste0(tag, "_deciles"))

# Save overall metrics
metrics <- data.frame(
  Metric = c("Hosmer-Lemeshow_X2", "HL_df", "HL_p", "Brier_Score",
             "Cal_Intercept", "Cal_Slope"),
  Value = c(round(hl_test$statistic, 4), hl_test$parameter,
            round(hl_test$p.value, 5), round(brier, 5),
            round(cal_intercept, 4), round(cal_slope, 4))
)
save_csv(metrics, paste0(tag, "_metrics"))

message("\n[OK] Calibration analysis complete.")
