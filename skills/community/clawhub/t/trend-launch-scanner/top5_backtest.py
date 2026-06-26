#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOP5等权策略回测
- 每天收盘后读取当日TOP5
- 假设以收盘价等权买入
- 持有1周后计算收益
- 汇总所有历史周收益
"""
import pandas as pd
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_scan")
BACKTEST_FILE = DATA_DIR / "top5_backtest.json"
SCAN_DIR = DATA_DIR


def fetch_price(code, date):
    """获取指定日期的收盘价（前复权）"""
    code = str(code).zfill(6)
    sym = 'sh' + code if code.startswith('6') else 'sz' + code
    
    # 计算日期范围
    target_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = (target_date - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = (target_date + timedelta(days=30)).strftime("%Y-%m-%d")
    
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param={sym},day,{start_date},{end_date},100,qfq"
    
    try:
        r = requests.get(url, timeout=10)
        text = r.text
        
        if 'kline_dayhfq=' in text:
            json_str = text.split('kline_dayhfq=')[1]
            data = json.loads(json_str)
            
            if 'data' in data and sym in data['data']:
                day_data = data['data'][sym].get('qfqday') or data['data'][sym].get('day', [])
                
                # 找到目标日期的数据
                for candle in day_data:
                    if candle[0] == date:
                        return float(candle[2])
                
                # 如果当天没有数据，找最近的一个
                for candle in reversed(day_data):
                    if candle[0] <= date:
                        return float(candle[2])
    except Exception as e:
        pass
    
    # 备用：用qt接口获取实时价格
    try:
        qt_url = f"https://qt.gtimg.cn/q={sym}"
        r = requests.get(qt_url, timeout=5)
        if '~' in r.text:
            parts = r.text.split('~')
            return float(parts[3])  # 现价
    except:
        pass
    
    return None


def get_week_price(code, buy_date):
    """获取1周后的收盘价"""
    code = str(code).zfill(6)
    sym = 'sh' + code if code.startswith('6') else 'sz' + code
    
    # 找到5个交易日后的日期
    target_date = datetime.strptime(buy_date, "%Y-%m-%d")
    current_date = target_date
    trading_days = 0
    while trading_days < 5:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:
            trading_days += 1
    
    end_date = current_date.strftime("%Y-%m-%d")
    start_date = (target_date - timedelta(days=30)).strftime("%Y-%m-%d")
    
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param={sym},day,{start_date},{end_date},100,qfq"
    
    try:
        r = requests.get(url, timeout=10)
        text = r.text
        
        if 'kline_dayhfq=' in text:
            json_str = text.split('kline_dayhfq=')[1]
            data = json.loads(json_str)
            
            if 'data' in data and sym in data['data']:
                day_data = data['data'][sym].get('qfqday') or data['data'][sym].get('day', [])
                
                # 返回5天后的数据
                for candle in day_data:
                    if candle[0] > buy_date:
                        return float(candle[2]), candle[0]
    except Exception as e:
        pass
    
    return None, None


def load_backtest_data():
    """加载回测数据"""
    if BACKTEST_FILE.exists():
        with open(BACKTEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"weeks": [], "summary": {}}


def save_backtest_data(data):
    """保存回测数据"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(BACKTEST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def scan_historical_scans():
    """扫描历史扫描结果"""
    scan_files = sorted(SCAN_DIR.glob("trend_scan_2026-*.csv"))
    
    weeks = []
    for scan_file in scan_files:
        date_str = scan_file.stem.replace("trend_scan_", "")
        
        try:
            df = pd.read_csv(scan_file, encoding="utf-8")
            
            # 获取TOP5（评分>=60）
            df_top5 = df[df["score"] >= 60].head(5)
            
            if len(df_top5) < 5:
                continue
            
            week_data = {
                "date": date_str,
                "stocks": []
            }
            
            for _, row in df_top5.iterrows():
                stock = {
                    "code": row["code"],
                    "name": row["name"],
                    "score": int(row["score"]),
                    "buy_price": None,
                    "sell_price": None,
                    "gain_pct": None,
                    "sell_date": None,
                    "status": "pending"
                }
                week_data["stocks"].append(stock)
            
            weeks.append(week_data)
            
        except Exception as e:
            print(f"读取{scan_file}失败: {e}")
    
    return weeks


def run_backtest():
    """执行回测"""
    data = load_backtest_data()
    
    # 扫描历史数据
    weeks = scan_historical_scans()
    print(f"找到 {len(weeks)} 周的历史数据")
    
    all_gains = []
    completed_weeks = 0
    
    for week in weeks:
        date = week["date"]
        print(f"\n处理 {date} 的TOP5...")
        
        all_completed = True
        
        for stock in week["stocks"]:
            code = stock["code"]
            
            # 获取买入价格（当天收盘价）
            if stock["buy_price"] is None:
                buy_price = fetch_price(code, date)
                stock["buy_price"] = buy_price
            
            # 获取卖出价格（5天后）
            if stock["sell_price"] is None and stock["buy_price"]:
                sell_price, sell_date = get_week_price(code, date)
                stock["sell_price"] = sell_price
                stock["sell_date"] = sell_date
                
                if sell_price and stock["buy_price"]:
                    gain = (sell_price / stock["buy_price"] - 1) * 100
                    stock["gain_pct"] = round(gain, 2)
                    stock["status"] = "completed"
                else:
                    stock["status"] = "failed"
            
            if stock["status"] != "completed":
                all_completed = False
        
        # 计算本周收益
        completed_stocks = [s for s in week["stocks"] if s["status"] == "completed"]
        if completed_stocks:
            week_avg_gain = sum(s["gain_pct"] for s in completed_stocks) / len(completed_stocks)
            week["avg_gain"] = round(week_avg_gain, 2)
            all_gains.append(week_avg_gain)
            completed_weeks += 1
            print(f"  {date} 平均收益: {week_avg_gain:+.2f}%")
        
        week["status"] = "completed" if all_completed else "partial"
    
    # 汇总统计
    if all_gains:
        data["weeks"] = weeks
        data["summary"] = {
            "total_weeks": len(all_gains),
            "avg_gain": round(sum(all_gains) / len(all_gains), 2),
            "max_gain": round(max(all_gains), 2),
            "min_gain": round(min(all_gains), 2),
            "win_rate": round(len([g for g in all_gains if g > 0]) / len(all_gains) * 100, 1),
            "total_return": round(sum(all_gains), 2),
            "max_gain_week": weeks[all_gains.index(max(all_gains))]["date"],
            "min_gain_week": weeks[all_gains.index(min(all_gains))]["date"]
        }
    
    save_backtest_data(data)
    return data


def print_report(data):
    """打印回测报告"""
    print("\n" + "=" * 60)
    print("📊 TOP5等权策略回测报告")
    print("=" * 60)
    print()
    
    if not data["weeks"]:
        print("暂无回测数据")
        return
    
    summary = data["summary"]
    
    print("【策略说明】")
    print("  每周一以收盘价等权买入当日TOP5")
    print("  持有5个交易日后卖出")
    print("  计算平均收益")
    print()
    
    print("【汇总统计】")
    print(f"  回测周数: {summary['total_weeks']} 周")
    print(f"  平均收益: {summary['avg_gain']:+.2f}%")
    print(f"  总收益: {summary['total_return']:+.2f}%")
    print(f"  胜率: {summary['win_rate']:.1f}%")
    print(f"  最大周收益: {summary['max_gain']:+.2f}% ({summary['max_gain_week']})")
    print(f"  最小周收益: {summary['min_gain']:+.2f}% ({summary['min_gain_week']})")
    print()
    
    print("【逐周明细】")
    print("-" * 60)
    print(f"{'日期':<12} {'平均收益':>10} {'状态':<10}")
    print("-" * 60)
    
    for week in sorted(data["weeks"], key=lambda x: x["date"], reverse=True):
        avg_gain = week.get("avg_gain", 0)
        status = "✅" if avg_gain > 0 else "❌"
        print(f"{week['date']:<12} {avg_gain:>+10.2f}% {status}")
        
        # 显示个股
        for s in week["stocks"]:
            gain = s.get("gain_pct")
            if gain is not None:
                print(f"  {s['code']} {s['name']:<8} {gain:>+8.2f}%")
            else:
                print(f"  {s['code']} {s['name']:<8} {'pending':>8}")
    
    print()
    print("【结论】")
    if summary["avg_gain"] > 0:
        print(f"  🟢 策略有效，平均每周盈利 {summary['avg_gain']:.2f}%")
    else:
        print(f"  🔴 策略无效，平均每周亏损 {abs(summary['avg_gain']):.2f}%")
    print()
    print("⚠️ 回测结果仅供参考，不代表未来表现")


if __name__ == "__main__":
    data = run_backtest()
    print_report(data)
