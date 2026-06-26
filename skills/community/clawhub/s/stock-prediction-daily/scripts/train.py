"""
Training pipeline: fetch CSI-300 stock data, engineer features,
train XGBoost binary classifier with feature-importance selection,
and report 10-fold cross-validation results.

Uses Tencent daily API for training and daily-signal inference.
"""
import json
import os
import time
import warnings
from datetime import datetime

import akshare as ak
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
from xgboost import XGBClassifier

import config
from features import add_technical_features, create_label, get_all_feature_columns, get_feature_metadata

warnings.filterwarnings("ignore")


# ────────────────────────────── Data fetching ──────────────────────────────

def code_to_tx_symbol(code):
    """Convert 6-digit stock code to Tencent symbol format (sh/sz prefix)."""
    code = str(code).zfill(6)
    if code.startswith("6"):
        return f"sh{code}"
    return f"sz{code}"


def get_hs300_constituents():
    """Get CSI 300 constituent stock codes."""
    print("[1/5] Fetching CSI 300 constituent list ...")
    try:
        df = ak.index_stock_cons(symbol="000300")
        codes = df["品种代码"].astype(str).str.zfill(6).tolist()
        print(f"  Got {len(codes)} constituents via index_stock_cons")
        return codes
    except Exception as e:
        print(f"  index_stock_cons failed: {e}")
    try:
        df = ak.index_stock_cons_csindex(symbol="000300")
        col = [c for c in df.columns if "代码" in c][0]
        codes = df[col].astype(str).str.zfill(6).tolist()
        print(f"  Got {len(codes)} constituents via index_stock_cons_csindex")
        return codes
    except Exception as e:
        print(f"  index_stock_cons_csindex failed: {e}")
    raise RuntimeError("Failed to fetch CSI 300 constituents from akshare")


def fetch_daily_data_tx(code, start_date="20240101", end_date=None, max_retries=3):
    """Fetch daily OHLCV data for a single stock via Tencent API."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    cache_path = os.path.join(config.DATA_DIR, f"{code}_daily.csv")
    if os.path.exists(cache_path):
        df = pd.read_csv(cache_path)
        if len(df) > 50:
            return df

    tx_symbol = code_to_tx_symbol(code)
    df = None
    for attempt in range(max_retries):
        try:
            df = ak.stock_zh_a_hist_tx(
                symbol=tx_symbol,
                start_date=start_date,
                end_date=end_date,
                adjust="qfq",
            )
            if df is not None and not df.empty:
                break
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
            continue

    if df is None or df.empty:
        return None

    # Normalise columns
    rename_map = {"date": "datetime"}
    df.rename(columns=rename_map, inplace=True)
    # Tencent returns 'amount' (turnover in lots); use as volume proxy
    if "volume" not in df.columns and "amount" in df.columns:
        df["volume"] = df["amount"]
    for c in ["open", "close", "high", "low", "volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df.to_csv(cache_path, index=False)
    return df


def fetch_all_training_data(codes):
    """Fetch daily data for a list of stock codes and concatenate."""
    print(f"[2/5] Fetching daily data for {len(codes)} stocks (cached results reused) ...")
    all_dfs = []
    failed = 0
    for i, code in enumerate(tqdm(codes, desc="Fetching")):
        df = fetch_daily_data_tx(code)
        if df is not None and len(df) > 50:
            df["stock_code"] = code
            all_dfs.append(df)
        else:
            failed += 1
        time.sleep(0.5)
        # Progress update every 50 stocks
        if (i + 1) % 50 == 0:
            print(f"  ... {i + 1}/{len(codes)}, success so far: {len(all_dfs)}")

    print(f"  Success: {len(all_dfs)}, Failed/skipped: {failed}")
    if not all_dfs:
        raise RuntimeError("No training data fetched")
    return pd.concat(all_dfs, ignore_index=True)


# ────────────────────────────── Feature engineering ──────────────────────────

def prepare_features(raw_df):
    """Engineer features and create labels for every stock in the dataframe."""
    print("[3/5] Engineering features ...")
    groups = []
    for code, grp in raw_df.groupby("stock_code"):
        grp = grp.copy()
        grp["datetime"] = pd.to_datetime(grp["datetime"])
        grp = grp.sort_values("datetime").reset_index(drop=True)
        grp = add_technical_features(grp)
        grp = create_label(grp)
        groups.append(grp)
    df = pd.concat(groups, ignore_index=True)

    feature_cols = get_all_feature_columns()
    feature_cols = [c for c in feature_cols if c in df.columns]
    df = df.dropna(subset=feature_cols + ["label"]).reset_index(drop=True)
    print(f"  Total samples: {len(df)}, features: {len(feature_cols)}")
    return df, feature_cols


# ────────────────────────────── Training ──────────────────────────────

def select_features_by_importance(X, y, feature_cols, top_n):
    """Train a preliminary model and pick top-N features by gain importance."""
    print("  Training preliminary model for feature selection ...")
    prelim = XGBClassifier(**config.XGB_PARAMS)
    prelim.fit(X, y)
    imp = pd.Series(prelim.feature_importances_, index=feature_cols)
    imp = imp.sort_values(ascending=False)
    selected = imp.head(top_n).index.tolist()
    print(f"  Selected {len(selected)} features from {len(feature_cols)}")
    return selected, imp


def cross_validate(X, y, params, n_folds=10):
    """Stratified K-Fold cross-validation, return per-fold and mean metrics."""
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
    metrics_list = []
    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
        X_tr, X_val = X[train_idx], X[val_idx]
        y_tr, y_val = y[train_idx], y[val_idx]
        model = XGBClassifier(**params)
        model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
        y_pred = model.predict(X_val)
        y_prob = model.predict_proba(X_val)[:, 1]
        m = {
            "fold": fold,
            "accuracy": round(accuracy_score(y_val, y_pred), 4),
            "precision": round(precision_score(y_val, y_pred, zero_division=0), 4),
            "recall": round(recall_score(y_val, y_pred, zero_division=0), 4),
            "f1": round(f1_score(y_val, y_pred, zero_division=0), 4),
            "auc": round(roc_auc_score(y_val, y_prob), 4),
        }
        metrics_list.append(m)
        print(f"    Fold {fold:2d} — Acc: {m['accuracy']:.4f}  AUC: {m['auc']:.4f}")
    mean_m = {
        "fold": "mean",
        "accuracy": round(np.mean([m["accuracy"] for m in metrics_list]), 4),
        "precision": round(np.mean([m["precision"] for m in metrics_list]), 4),
        "recall": round(np.mean([m["recall"] for m in metrics_list]), 4),
        "f1": round(np.mean([m["f1"] for m in metrics_list]), 4),
        "auc": round(np.mean([m["auc"] for m in metrics_list]), 4),
    }
    metrics_list.append(mean_m)
    return metrics_list


def train_final_model(X, y, params):
    """Train the final model on all data."""
    model = XGBClassifier(**params)
    model.fit(X, y, verbose=False)
    return model


# ────────────────────────────── EDA summary ──────────────────────────────

def generate_eda(raw_df, feature_df, feature_cols, label_col="label"):
    """Generate exploratory data analysis summary dict."""
    datetime_series = pd.to_datetime(raw_df["datetime"], errors="coerce")
    eda = {
        "num_stocks": int(raw_df["stock_code"].nunique()),
        "date_range": f'{datetime_series.min()} ~ {datetime_series.max()}',
        "total_raw_rows": int(len(raw_df)),
        "total_samples_after_fe": int(len(feature_df)),
        "label_distribution": {
            "up (1)": int((feature_df[label_col] == 1).sum()),
            "down (0)": int((feature_df[label_col] == 0).sum()),
            "up_ratio": round(float((feature_df[label_col] == 1).mean()), 4),
        },
        "feature_stats": {},
    }
    for c in feature_cols:
        if c in feature_df.columns:
            eda["feature_stats"][c] = {
                "mean": round(float(feature_df[c].mean()), 6),
                "std": round(float(feature_df[c].std()), 6),
                "min": round(float(feature_df[c].min()), 6),
                "max": round(float(feature_df[c].max()), 6),
            }
    return eda


# ────────────────────────────── Report ──────────────────────────────

def build_report(eda, selected_features, importance_dict, cv_metrics, params):
    """Build a comprehensive model report dict."""
    feature_metadata = get_feature_metadata()
    selected_set = set(selected_features)
    feature_catalog = []
    for feature_name, importance in sorted(importance_dict.items(), key=lambda item: -item[1]):
        stats = eda.get("feature_stats", {}).get(feature_name, {})
        meta = feature_metadata.get(feature_name, {})
        feature_catalog.append({
            "english_name": feature_name,
            "chinese_name": meta.get("chinese_name", feature_name),
            "logic": meta.get("logic", "-"),
            "category": meta.get("category", "未分类"),
            "importance": round(importance, 6),
            "selected": feature_name in selected_set,
            "stats": stats,
        })

    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "project_background": (
            "本项目基于沪深300成份股的行情数据，构建XGBoost二分类模型，"
            "预测个股下一交易日的价格涨跌方向。训练数据时间范围为2024年至今，"
            "使用akshare获取前复权的OHLCV数据，通过技术指标特征工程生成模型输入，"
            "并依据特征重要性筛选入模特征，最终以十折交叉验证评估模型泛化能力。"
            "模型在预测与评估阶段统一使用腾讯财经日线数据，评估口径为T+1。"
        ),
        "eda": eda,
        "feature_dimensions": {
            "total_candidate_features": len(importance_dict),
            "selected_features": len(selected_features),
            "selected_feature_names": selected_features,
            "feature_catalog": feature_catalog,
            "feature_importance": {
                k: round(v, 6) for k, v in
                sorted(importance_dict.items(), key=lambda x: -x[1])
            },
        },
        "model_performance": {
            "algorithm": "XGBoost (xgboost.XGBClassifier)",
            "hyperparameters": {k: v for k, v in params.items()},
            "cv_folds": len(cv_metrics) - 1,
            "cv_results": cv_metrics,
        },
        "usage_guide": (
            "1. 安装依赖: pip install -r requirements.txt\n"
            "2. 训练模型: python3 train.py\n"
            "3. 日线预测: python3 predict.py 2026-03-12\n"
            "4. T+1评估: python3 evaluate.py\n"
            "5. 启动网页: python3 app.py  → 浏览器访问 http://127.0.0.1:5000\n"
            "6. 一键执行: python3 main.py"
        ),
    }
    return report


# ────────────────────────────── Main ──────────────────────────────

def run_training():
    print("=" * 60)
    print("  Stock Price Direction Prediction — Training Pipeline")
    print("=" * 60)

    # 1. Get constituents
    codes = get_hs300_constituents()

    # 2. Fetch data
    raw_df = fetch_all_training_data(codes)

    # 3. Feature engineering
    feature_df, all_feature_cols = prepare_features(raw_df)

    X_all = feature_df[all_feature_cols].values
    y_all = feature_df["label"].values

    # 4. Feature selection
    print("[4/5] Feature importance selection + 10-fold CV ...")
    selected_features, importance_series = select_features_by_importance(
        X_all, y_all, all_feature_cols, config.TOP_N_FEATURES
    )
    importance_dict = importance_series.to_dict()

    X_sel = feature_df[selected_features].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_sel)

    # 10-fold CV
    print(f"  Running {config.CV_FOLDS}-fold cross-validation ...")
    cv_metrics = cross_validate(X_scaled, y_all, config.XGB_PARAMS, config.CV_FOLDS)
    mean_m = cv_metrics[-1]
    print(f"\n  ★ Mean CV — Acc: {mean_m['accuracy']:.4f}  "
          f"AUC: {mean_m['auc']:.4f}  F1: {mean_m['f1']:.4f}")

    # 5. Train final model & save
    print("\n[5/5] Training final model & saving artifacts ...")
    final_model = train_final_model(X_scaled, y_all, config.XGB_PARAMS)
    joblib.dump(final_model, config.MODEL_PATH)
    joblib.dump(scaler, config.SCALER_PATH)
    with open(config.FEATURE_PATH, "w") as f:
        json.dump(selected_features, f, ensure_ascii=False, indent=2)
    print(f"  Model saved → {config.MODEL_PATH}")
    print(f"  Scaler saved → {config.SCALER_PATH}")
    print(f"  Features saved → {config.FEATURE_PATH}")

    # EDA & report
    eda = generate_eda(raw_df, feature_df, selected_features)
    report = build_report(eda, selected_features, importance_dict, cv_metrics, config.XGB_PARAMS)
    with open(config.REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Report saved → {config.REPORT_PATH}")

    print("\n✅ Training complete!\n")
    return report


if __name__ == "__main__":
    run_training()
