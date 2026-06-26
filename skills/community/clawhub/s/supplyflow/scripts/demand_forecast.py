#!/usr/bin/env python3
"""需求预测 — 付费版：基于历史销量数据，使用移动平均和指数平滑预测未来需求。

Usage:
    python3 demand_forecast.py --history '[{"month":"2025-01","demand":1200},{"month":"2025-02","demand":1350}]' --months 3
    python3 demand_forecast.py --history '...' --months 6 --method exp_smooth --alpha 0.3
"""

import argparse
import json
import math
import sys


def moving_average(history: list[float], window: int = 3) -> list[float]:
    if len(history) < window:
        window = len(history)
    return [sum(history[-window:]) / window]


def exp_smooth(history: list[float], alpha: float = 0.3) -> list[float]:
    if not history:
        return [0]
    s = history[0]
    for val in history[1:]:
        s = alpha * val + (1 - alpha) * s
    return [s]


def linear_regression(history: list[float]) -> float:
    n = len(history)
    if n < 2:
        return history[0] if history else 0
    x_mean = (n - 1) / 2
    y_mean = sum(history) / n
    num = sum((i - x_mean) * (history[i] - y_mean) for i in range(n))
    den = sum((i - x_mean) ** 2 for i in range(n))
    if den == 0:
        return y_mean
    slope = num / den
    intercept = y_mean - slope * x_mean
    return slope * n + intercept


def mape(actual: list[float], predicted: list[float]) -> float:
    if len(actual) != len(predicted):
        return float("inf")
    errors = []
    for a, p in zip(actual, predicted):
        if a != 0:
            errors.append(abs((a - p) / a) * 100)
    return sum(errors) / len(errors) if errors else 0


def forecast_demand(history_data: list[dict], months: int = 3,
                    method: str = "ensemble", alpha: float = 0.3) -> dict:
    demands = [d["demand"] for d in history_data]
    labels = [d.get("month", "") for d in history_data]

    if len(demands) < 2:
        return {
            "error": "至少需要2个月历史数据",
            "history": demands,
        }

    avg = moving_average(demands)
    smooth = exp_smooth(demands, alpha)
    trend = linear_regression(demands)

    backtest = []
    for i in range(2, len(demands)):
        ma_pred = sum(demands[max(0, i - 3):i]) / min(3, i)
        backtest.append((demands[i], ma_pred))

    overall_mape = mape([x[0] for x in backtest], [x[1] for x in backtest]) if backtest else None

    if method == "ma":
        base = avg[0]
    elif method == "exp_smooth":
        base = smooth[0]
    elif method == "trend":
        base = trend
    else:  # ensemble
        base = (avg[0] + smooth[0] + trend) / 3

    # Add slight trend adjustment for multi-month
    if len(demands) >= 3:
        trend_rate = (demands[-1] - demands[0]) / (len(demands) - 1)
        monthly_rate = trend_rate * 0.3  # dampen the trend
    else:
        monthly_rate = 0

    predictions = []
    for i in range(1, months + 1):
        pred = max(0, round(base + monthly_rate * i))
        predictions.append(pred)

    # Stats
    avg_demand = sum(demands) / len(demands)
    std_demand = math.sqrt(sum((d - avg_demand) ** 2 for d in demands) / len(demands)) if len(demands) > 1 else 0
    cv = (std_demand / avg_demand * 100) if avg_demand > 0 else 0
    total_forecast = sum(predictions)
    peak = max(predictions)
    trough = min(predictions)

    return {
        "history_labels": labels,
        "history_values": demands,
        "avg_demand": round(avg_demand, 1),
        "std_demand": round(std_demand, 1),
        "cv": round(cv, 1),
        "ma_prediction": round(avg[0], 1),
        "smooth_prediction": round(smooth[0], 1),
        "trend_prediction": round(trend, 1),
        "method": method,
        "predictions": predictions,
        "total_forecast": total_forecast,
        "peak": peak,
        "trough": trough,
        "backtest_mape": round(overall_mape, 1) if overall_mape is not None else None,
        "volatility": "高" if cv > 30 else "中" if cv > 15 else "低",
    }


def render_md(data: dict) -> str:
    if "error" in data:
        return f"## ❌ 需求预测失败\n\n{data['error']}\n"

    lines = ["## 📊 需求预测报告\n"]

    lines.append(f"**历史数据点:** {len(data['history_values'])} 个月  |  "
                 f"平均需求: {data['avg_demand']:,.1f}/月  |  "
                 f"波动系数(CV): {data['cv']:.1f}% ({data['volatility']}波动)\n")

    lines.append("### 📈 历史需求趋势")
    lines.append("")
    lines.append("| 月份 | 需求量 | 趋势 |")
    lines.append("|------|--------|------|")
    vals = data["history_values"]
    for i, v in enumerate(vals):
        if i > 0:
            delta = v - vals[i - 1]
            arrow = "📈" if delta > 0 else "📉" if delta < 0 else "➡️"
            change = f"{arrow} {delta:+.0f}"
        else:
            change = "—"
        label = data["history_labels"][i] if i < len(data["history_labels"]) else f"月{i + 1}"
        lines.append(f"| {label} | {v:,.0f} | {change} |")

    lines.append("")
    lines.append("### 🔮 需求预测")
    lines.append("")
    lines.append(f"| 方法 | 预测值 |")
    lines.append("|------|--------|")
    lines.append(f"| 移动平均(3月) | {data['ma_prediction']:,.1f} |")
    lines.append(f"| 指数平滑(α=0.3) | {data['smooth_prediction']:,.1f} |")
    lines.append(f"| 线性趋势 | {data['trend_prediction']:,.1f} |")
    lines.append(f"| **{data['method']} 综合** | **{(sum(data['predictions']) / len(data['predictions'])):,.1f}/月** |")

    lines.append("")
    lines.append("### 📅 逐月预测")
    lines.append("")
    lines.append("| 预测月份 | 预测需求量 | 累计 |")
    lines.append("|----------|------------|------|")
    cum = 0
    for i, p in enumerate(data["predictions"]):
        cum += p
        lines.append(f"| 第{i + 1}月 | {p:,.0f} | {cum:,.0f} |")

    lines.append("")
    if data.get("backtest_mape") is not None:
        lines.append(f"**回测MAPE:** {data['backtest_mape']:.1f}%  |  "
                      f"预测峰值: {data['peak']:,.0f}  |  "
                      f"预测谷值: {data['trough']:,.0f}\n")

    # Recommendations
    lines.append("### 💡 建议")
    cv = data["cv"]
    if cv > 30:
        lines.append("- ⚠️ 需求波动较高，建议保持1.5-2个月的安全库存")
    elif cv > 15:
        lines.append("- 需求波动中等，建议保持1个月的安全库存")
    else:
        lines.append("- 需求稳定，可按预测量精益备货，保持2周安全库存")
    lines.append(f"- 预测总量: {data['total_forecast']:,.0f} 单位，请提前备料")

    lines.append("")
    lines.append("---\n*SupplyFlow 需求预测 · 付费版*\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="需求预测工具")
    parser.add_argument("--history", type=str, required=True, help='JSON: [{"month":"2025-01","demand":1200},...]')
    parser.add_argument("--months", type=int, default=3, help="预测月数")
    parser.add_argument("--method", choices=["ma", "exp_smooth", "trend", "ensemble"], default="ensemble")
    parser.add_argument("--alpha", type=float, default=0.3, help="指数平滑系数")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    history = json.loads(args.history)
    data = forecast_demand(history, args.months, args.method, args.alpha)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_md(data))


if __name__ == "__main__":
    main()
