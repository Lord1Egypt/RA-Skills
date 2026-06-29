#!/bin/bash
# R Machine Learning Workbench - Launcher
# Usage: bash scripts/launcher.sh <command> [options]

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
R_SCRIPT_DIR="$BASE_DIR/scripts"

# Create output directories
mkdir -p "$BASE_DIR/output/plots"
mkdir -p "$BASE_DIR/output/models"
mkdir -p "$BASE_DIR/output/predictions"
mkdir -p "$BASE_DIR/output/reports"
mkdir -p "$BASE_DIR/output/tables"

CMD=$1
shift

case $CMD in
  install)
    Rscript "$R_SCRIPT_DIR/install_packages.R" "$@"
    ;;
  split)
    Rscript "$R_SCRIPT_DIR/data_split.R" "$@"
    ;;
  explore)
    Rscript "$R_SCRIPT_DIR/data_explore.R" "$@"
    ;;
  feature_engineer)
    Rscript "$R_SCRIPT_DIR/feature_engineering.R" "$@"
    ;;
  feature_select)
    Rscript "$R_SCRIPT_DIR/feature_selection.R" "$@"
    ;;
  rf)
    Rscript "$R_SCRIPT_DIR/rf_model.R" "$@"
    ;;
  xgboost)
    Rscript "$R_SCRIPT_DIR/xgboost_model.R" "$@"
    ;;
  lasso)
    Rscript "$R_SCRIPT_DIR/lasso_model.R" "$@"
    ;;
  svm)
    Rscript "$R_SCRIPT_DIR/svm_model.R" "$@"
    ;;
  tune)
    Rscript "$R_SCRIPT_DIR/hyperparameter_tune.R" "$@"
    ;;
  cv)
    Rscript "$R_SCRIPT_DIR/cross_validation.R" "$@"
    ;;
  compare)
    Rscript "$R_SCRIPT_DIR/model_compare.R" "$@"
    ;;
  roc)
    Rscript "$R_SCRIPT_DIR/roc_analysis.R" "$@"
    ;;
  calibration)
    Rscript "$R_SCRIPT_DIR/calibration.R" "$@"
    ;;
  shap)
    Rscript "$R_SCRIPT_DIR/shap_analysis.R" "$@"
    ;;
  survival)
    Rscript "$R_SCRIPT_DIR/survival_ml.R" "$@"
    ;;
  pipeline)
    Rscript "$R_SCRIPT_DIR/pipeline.R" "$@"
    ;;
  report)
    Rscript "$R_SCRIPT_DIR/report_generator.R" "$@"
    ;;
  *)
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Available commands:"
    echo "  install            Install all dependency packages"
    echo "  split              Split data into train/test/validation"
    echo "  explore            Exploratory data analysis"
    echo "  feature_engineer   Automated feature engineering"
    echo "  feature_select     Feature selection (Boruta/RFE/LASSO)"
    echo "  rf                 Random Forest"
    echo "  xgboost            XGBoost"
    echo "  lasso              LASSO regression"
    echo "  svm                SVM"
    echo "  tune               Hyperparameter tuning"
    echo "  cv                 Cross-validation"
    echo "  compare            Multi-model comparison"
    echo "  roc                ROC analysis"
    echo "  calibration        Calibration curves"
    echo "  shap               SHAP explainability"
    echo "  survival           Survival ML"
    echo "  pipeline           One-click full pipeline"
    echo "  report             Generate analysis report"
    exit 1
    ;;
esac

exit $?
