"""Daily evaluation pipeline using Tencent daily data only.

It reads historical predictions, fetches Tencent daily prices around the
prediction date, and evaluates the prediction against the next available
trading day's close.
"""
import time
from datetime import timedelta

import akshare as ak
import pandas as pd

import config


EVALUATION_COLUMNS = [
    "股票代码",
    "股票名称",
    "预测时间",
    "预测生成时间",
    "当时价格",
    "预测结果",
    "上涨概率",
    "预测数据频率",
    "一天后价格",
    "评估数据频率",
    "实际涨跌",
    "预测是否准确",
]


def code_to_tx_symbol(code):
    code = str(code).zfill(6)
    return f"sh{code}" if code.startswith("6") else f"sz{code}"


def _normalize_daily_df(df):
    """Normalize Tencent daily dataframe."""
    df = df.copy()
    df.rename(columns={"date": "datetime"}, inplace=True)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    return df.sort_values("datetime").reset_index(drop=True)


def fetch_daily_data_around(code, target_dt):
    """Fetch Tencent daily data around the prediction date."""
    dt = pd.to_datetime(target_dt)
    start_d = (dt - timedelta(days=30)).strftime("%Y%m%d")
    end_d = (dt + timedelta(days=10)).strftime("%Y%m%d")
    try:
        tx_sym = code_to_tx_symbol(code)
        df = ak.stock_zh_a_hist_tx(
            symbol=tx_sym,
            start_date=start_d,
            end_date=end_d,
            adjust="qfq",
        )
        if df is not None and not df.empty:
            return _normalize_daily_df(df), "daily.tencent"
    except Exception:
        pass
    return None, None


def get_price_next_trading_day(code, pred_time):
    """Return the close price of the next available trading day."""
    df, freq = fetch_daily_data_around(code, pred_time)
    if df is None or df.empty:
        return None, None

    pred_dt = pd.to_datetime(pred_time).normalize()
    after = df[df["datetime"] > pred_dt]
    if not after.empty:
        return float(after.iloc[0]["close"]), freq
    return None, None


def _merge_evaluation_history(eval_rows):
    """Persist full evaluation history keyed by stock code and prediction date."""
    eval_df = pd.DataFrame(eval_rows)
    eval_df["股票代码"] = eval_df["股票代码"].astype(str).str.zfill(6)
    eval_df["预测时间"] = pd.to_datetime(eval_df["预测时间"]).dt.strftime("%Y-%m-%d")
    if "预测生成时间" not in eval_df.columns:
        eval_df["预测生成时间"] = eval_df["预测时间"] + " 00:00:00"
    eval_df["预测生成时间"] = pd.to_datetime(eval_df["预测生成时间"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    eval_df = eval_df.sort_values(["预测生成时间", "预测时间", "股票代码"], ascending=[False, False, True])
    eval_df = eval_df.drop_duplicates(subset=["股票代码", "预测时间"], keep="first")
    eval_df = eval_df.sort_values(["预测生成时间", "预测时间", "股票代码"], ascending=[False, False, True]).reset_index(drop=True)
    eval_df = eval_df.reindex(columns=EVALUATION_COLUMNS)
    eval_df.to_csv(config.EVALUATION_PATH, index=False, encoding="utf-8-sig")
    return eval_df


def _dedupe_predictions_for_evaluation(pred_df):
    """Keep one prediction per stock per trade date, preferring the latest batch."""
    deduped_df = pred_df.copy()
    deduped_df["股票代码"] = deduped_df["股票代码"].astype(str).str.zfill(6)
    deduped_df["当前时间"] = pd.to_datetime(deduped_df["当前时间"]).dt.strftime("%Y-%m-%d")
    if "预测生成时间" not in deduped_df.columns:
        deduped_df["预测生成时间"] = deduped_df["当前时间"] + " 00:00:00"
    deduped_df["预测生成时间"] = pd.to_datetime(deduped_df["预测生成时间"])
    deduped_df = deduped_df.sort_values(["预测生成时间", "当前时间", "股票代码"], ascending=[False, False, True])
    deduped_df = deduped_df.drop_duplicates(subset=["股票代码", "当前时间"], keep="first")
    deduped_df["预测生成时间"] = deduped_df["预测生成时间"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return deduped_df.reset_index(drop=True)


def run_evaluation():
    print("=" * 60)
    print("  Stock Price Direction Prediction — Daily Evaluation Pipeline")
    print("=" * 60)

    try:
        pred_df = pd.read_csv(config.PREDICTION_PATH)
    except FileNotFoundError:
        print("  ⚠ No prediction file found. Run predict.py first.")
        return []

    pred_df = _dedupe_predictions_for_evaluation(pred_df)

    print(f"  Evaluating {len(pred_df)} deduplicated historical predictions ...\n")
    eval_rows = []
    for _, row in pred_df.iterrows():
        code = str(row["股票代码"]).zfill(6)
        name = row["股票名称"]
        pred_time = row["当前时间"]
        generated_at = row["预测生成时间"]
        pred_price = float(row["当前价格"])
        pred_result = row["预测结果"]
        up_prob = float(row["上涨概率"])
        pred_freq = row.get("数据频率", None)

        print(f"  {name}({code}) @ {pred_time} / {generated_at} [{pred_freq or '?'}] ...", end=" ")
        later_price, eval_freq = get_price_next_trading_day(code, pred_time)
        time.sleep(config.FETCH_DELAY)

        if later_price is None:
            actual_dir = "数据不足"
            correct = "N/A"
            print("数据不足")
        else:
            actual_dir = "上涨" if later_price > pred_price else "下跌"
            correct = "✓" if actual_dir == pred_result else "✗"
            print(f"→ {later_price:.2f} ({actual_dir}) [{eval_freq}] {correct}")

        eval_rows.append({
            "股票代码": code,
            "股票名称": name,
            "预测时间": pred_time,
            "预测生成时间": generated_at,
            "当时价格": pred_price,
            "预测结果": pred_result,
            "上涨概率": up_prob,
            "预测数据频率": pred_freq if pred_freq else "N/A",
            "一天后价格": later_price if later_price else "N/A",
            "评估数据频率": eval_freq if eval_freq else "N/A",
            "实际涨跌": actual_dir,
            "预测是否准确": correct,
        })

    eval_df = _merge_evaluation_history(eval_rows)
    print(f"\n  Evaluation saved → {config.EVALUATION_PATH}")

    # Overall accuracy (exclude N/A)
    valid = [r for r in eval_rows if r["预测是否准确"] in ("✓", "✗")]
    if valid:
        acc = sum(1 for r in valid if r["预测是否准确"] == "✓") / len(valid)
        print(f"\n  ★ 整体准确率: {acc:.2%} ({sum(1 for r in valid if r['预测是否准确'] == '✓')}/{len(valid)})")
    else:
        print("\n  ⚠ 无法计算准确率 (没有可对比的数据)")

    print("\n✅ Evaluation complete!\n")
    return eval_df.to_dict(orient="records")


if __name__ == "__main__":
    run_evaluation()
