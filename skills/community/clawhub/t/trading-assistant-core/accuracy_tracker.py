#!/usr/bin/env python3
"""
Prediction Accuracy Tracker
预测准确度追踪系统
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

# Paths
ACCURACY_FILE = Path(__file__).parent / "accuracy_log.json"
REPORTS_DIR = Path(__file__).parent / "reports"

def load_accuracy_log():
    """Load accuracy log."""
    if not ACCURACY_FILE.exists():
        return {"predictions": [], "statistics": {}}
    
    with open(ACCURACY_FILE) as f:
        return json.load(f)

def save_accuracy_log(data):
    """Save accuracy log."""
    with open(ACCURACY_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def log_prediction(date, symbol, predicted_change, actual_close=None):
    """Log a prediction."""
    data = load_accuracy_log()
    
    # Check if already logged for this date+symbol
    for pred in data["predictions"]:
        if pred["date"] == date and pred["symbol"] == symbol:
            # Update existing
            if actual_close:
                pred["actual_close"] = actual_close
                pred["actual_change"] = calculate_change(pred["base_price"], actual_close)
                pred["accurate"] = is_accurate(pred["predicted_change"], pred["actual_change"])
            save_accuracy_log(data)
            return
    
    # Add new
    data["predictions"].append({
        "date": date,
        "symbol": symbol,
        "predicted_change": predicted_change,
        "base_price": 0,
        "actual_close": actual_close,
        "actual_change": 0,
        "accurate": None,  # Will be calculated when actual is available
        "timestamp": datetime.now().isoformat()
    })
    
    save_accuracy_log(data)
    print(f"✅ 记录预测：{symbol} {date} {predicted_change}")

def calculate_change(base, current):
    """Calculate percentage change."""
    if base == 0:
        return 0
    return ((current - base) / base) * 100

def is_accurate(predicted, actual):
    """Check if prediction was accurate (within range)."""
    # Simple logic: same direction or within 2%
    if predicted > 0 and actual > 0:
        return True
    elif predicted < 0 and actual < 0:
        return True
    elif abs(actual) < 2:  # Small movement, hard to predict
        return True
    return False

def update_accuracy(actual_data):
    """
    Update accuracy with actual closing prices.
    actual_data: {symbol: {date: close_price}}
    """
    data = load_accuracy_log()
    updated = 0
    
    for pred in data["predictions"]:
        date = pred["date"]
        symbol = pred["symbol"]
        
        if symbol in actual_data and date in actual_data[symbol]:
            close_price = actual_data[symbol][date]
            
            if pred["actual_close"] is None:
                pred["actual_close"] = close_price
                pred["actual_change"] = calculate_change(pred["base_price"], close_price)
                pred["accurate"] = is_accurate(pred["predicted_change"], pred["actual_change"])
                updated += 1
                print(f"✅ 更新准确：{symbol} {date} 预测{pred['predicted_change']:+.1f}% 实际{pred['actual_change']:+.1f}% {'✅' if pred['accurate'] else '❌'}")
    
    if updated > 0:
        save_accuracy_log(data)
        print(f"\n✅ 更新 {updated} 条预测准确度")
    
    return updated

def calculate_statistics(days=30):
    """Calculate accuracy statistics."""
    data = load_accuracy_log()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    total = 0
    accurate = 0
    by_symbol = {}
    by_date = {}
    
    for pred in data["predictions"]:
        if pred["date"] < cutoff_date:
            continue
        if pred["accurate"] is None:
            continue
        
        total += 1
        if pred["accurate"]:
            accurate += 1
        
        # By symbol
        symbol = pred["symbol"]
        if symbol not in by_symbol:
            by_symbol[symbol] = {"total": 0, "accurate": 0}
        by_symbol[symbol]["total"] += 1
        if pred["accurate"]:
            by_symbol[symbol]["accurate"] += 1
        
        # By date
        date = pred["date"]
        if date not in by_date:
            by_date[date] = {"total": 0, "accurate": 0}
        by_date[date]["total"] += 1
        if pred["accurate"]:
            by_date[date]["accurate"] += 1
    
    # Calculate rates
    accuracy_rate = (accurate / total * 100) if total > 0 else 0
    
    stats = {
        "period_days": days,
        "total_predictions": total,
        "accurate_predictions": accurate,
        "accuracy_rate": accuracy_rate,
        "by_symbol": {k: {"total": v["total"], "accurate": v["accurate"], "rate": v["accurate"]/v["total"]*100 if v["total"]>0 else 0} for k, v in by_symbol.items()},
        "by_date": by_date
    }
    
    data["statistics"][f"{days}d"] = stats
    save_accuracy_log(data)
    
    return stats

def generate_report(stats):
    """Generate accuracy report text."""
    report = f"\n## 🎯 预测准确度统计 ({stats['period_days']}天)\n\n"
    report += f"**总预测**: {stats['total_predictions']} 次\n"
    report += f"**准确次数**: {stats['accurate_predictions']} 次\n"
    report += f"**准确度**: {stats['accuracy_rate']:.1f}%\n\n"
    
    if stats['by_symbol']:
        report += "### 按股票统计\n\n"
        report += "| 股票 | 预测次数 | 准确次数 | 准确度 |\n"
        report += "|------|---------|---------|-------|\n"
        
        for symbol, data in sorted(stats['by_symbol'].items(), key=lambda x: x[1]['rate'], reverse=True):
            report += f"| {symbol} | {data['total']} | {data['accurate']} | {data['rate']:.1f}% |\n"
    
    return report

def get_today_predictions():
    """Get today's predictions for verification."""
    data = load_accuracy_log()
    today = datetime.now().strftime("%Y-%m-%d")
    
    predictions = []
    for pred in data["predictions"]:
        if pred["date"] == today:
            predictions.append(pred)
    
    return predictions

def main():
    """Main function."""
    print("=" * 60)
    print("🎯 预测准确度追踪系统")
    print("=" * 60)
    
    # Calculate statistics
    print("\n计算统计...\n")
    
    for days in [7, 30, 90]:
        stats = calculate_statistics(days)
        print(f"{days}天准确度：{stats['accuracy_rate']:.1f}% ({stats['accurate_predictions']}/{stats['total_predictions']})")
    
    # Generate report
    stats_30d = calculate_statistics(30)
    report = generate_report(stats_30d)
    print(report)
    
    print("=" * 60)

if __name__ == "__main__":
    main()
