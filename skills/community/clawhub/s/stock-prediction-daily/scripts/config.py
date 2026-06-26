import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
RESULT_DIR = os.path.join(BASE_DIR, "results")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SECTOR_REPORTS_DIR = os.path.join(REPORTS_DIR, "sector_analysis")
STOCK_REPORTS_DIR = os.path.join(REPORTS_DIR, "stock_analysis")
PREDICTION_HISTORY_DIR = os.path.join(RESULT_DIR, "prediction_history")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

for d in [
    DATA_DIR,
    MODEL_DIR,
    RESULT_DIR,
    REPORTS_DIR,
    SECTOR_REPORTS_DIR,
    STOCK_REPORTS_DIR,
    PREDICTION_HISTORY_DIR,
    TEMPLATE_DIR,
    STATIC_DIR,
]:
    os.makedirs(d, exist_ok=True)

# Training data date range
TRAIN_START_DATE = "2024-01-01 09:30:00"
TRAIN_END_DATE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Target stocks for prediction
TARGET_STOCKS = {
    "600436": "片仔癀",
    "300750": "宁德时代",
    "002475": "立讯精密",
    "000568": "泸州老窖",
    "000538": "云南白药",
    "000338": "潍柴动力",
    "600031": "三一重工",
    "600111": "北方稀土",
    "002415": "海康威视",
    "000858": "五粮液",
}

# Model paths
MODEL_PATH = os.path.join(MODEL_DIR, "xgb_stock_model.pkl")
FEATURE_PATH = os.path.join(MODEL_DIR, "feature_names.json")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
REPORT_PATH = os.path.join(RESULT_DIR, "model_report.json")
PREDICTION_PATH = os.path.join(RESULT_DIR, "predictions.csv")
EVALUATION_PATH = os.path.join(RESULT_DIR, "evaluation.csv")

# XGBoost parameters
XGB_PARAMS = {
    "objective": "binary:logistic",
    "eval_metric": "logloss",
    "max_depth": 6,
    "learning_rate": 0.05,
    "n_estimators": 300,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 5,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0,
    "random_state": 42,
    "n_jobs": -1,
}

# Feature importance threshold (top N features)
TOP_N_FEATURES = 40

# Cross-validation folds
CV_FOLDS = 10

# Data fetch delay (seconds between requests)
FETCH_DELAY = 1.5
