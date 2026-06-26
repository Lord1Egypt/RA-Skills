#!/usr/bin/env python3
"""
Stock Analysis Framework — 六维分析工具
分析一只股票的基本面、技术面、消息面、资金面、心理面、宏观面

用法: python3 stock_analyze.py <股票名称或代码>
示例: python3 stock_analyze.py 600519
      python3 stock_analyze.py 铜陵有色
"""

import urllib.request
import json
import sys
import time
from datetime import datetime

def get_stock_code(name_or_code):
    """通过股票名或代码获取股票信息"""
    # 常见股票名称到代码的映射
    known = {
        "铜陵有色": "000630", "云铝股份": "000807", "神火股份": "000933",
        "四川黄金": "001337", "双鹭药业": "002038", "长城电工": "600192",
        "四川长虹": "600839", "华友钴业": "603799", "贵州茅台": "600519",
        "宁德时代": "300750", "比亚迪": "002594", "招商银行": "600036",
        "中国平安": "601318", "五粮液": "000858", "紫金矿业": "601899",
    }
    if name_or_code in known:
        return known[name_or_code], name_or_code

    # Try as code directly
    if name_or_code.isdigit() and len(name_or_code) == 6:
        return name_or_code, name_or_code

    # If name_or_code contains only digits, it's already a code
    if name_or_code.isdigit():
        return name_or_code, name_or_code

    return name_or_code, name_or_code

def get_quote(code):
    """获取实时行情"""
    market = "sh" if code.startswith("6") else "sz"
    url = f"https://hq.sinajs.cn/list={market}{code}"
    req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"})
    resp = urllib.request.urlopen(req, timeout=10)
    text = resp.read().decode("gbk")
    fields = text.split("=")[1].strip('";\n').split(",")

    return {
        "name": fields[0],
        "open": float(fields[1]),
        "prev_close": float(fields[2]),
        "current": float(fields[3]),
        "high": float(fields[4]),
        "low": float(fields[5]),
        "volume": int(fields[8]),
        "amount": float(fields[9]),
        "change_pct": round((float(fields[3]) - float(fields[2])) / float(fields[2]) * 100, 2)
    }

def get_fund_flow(code):
    """获取资金流向（昨日数据）"""
    try:
        import akshare as ak
        market = "sz" if not code.startswith("6") else "sh"
        df = ak.stock_individual_fund_flow(stock=code, market=market)
        latest = df.iloc[-1]
        return {
            "main_force": float(latest["主力净流入-净额"]),
            "super_large": float(latest["超大单净流入-净额"]),
            "large": float(latest["大单净流入-净额"]),
            "main_pct": float(latest["主力净流入-净占比"]),
            "date": latest["日期"],
        }
    except Exception:
        return None

def get_kline(code):
    """获取日K线数据"""
    try:
        import akshare as ak
        today = datetime.now().strftime("%Y%m%d")
        df = ak.stock_zh_a_hist(symbol=code, period="daily",
                                 start_date="20260401", end_date=today, adjust="qfq")
        if len(df) >= 20:
            closes = df["收盘"].tolist()
            ma5 = sum(closes[-5:]) / 5
            ma10 = sum(closes[-10:]) / 10
            ma20 = sum(closes[-20:]) / 20
            last = closes[-1]
            highs = df["最高"].tolist()
            lows = df["最低"].tolist()
            return {
                "ma5": round(ma5, 2),
                "ma10": round(ma10, 2),
                "ma20": round(ma20, 2),
                "trend": "多头" if ma5 > ma10 > ma20 else "空头" if ma5 < ma10 < ma20 else "震荡",
                "high_20": max(highs[-20:]) if len(highs) >= 20 else max(highs),
                "low_20": min(lows[-20:]) if len(lows) >= 20 else min(lows),
                "position": round((last - min(lows[-20:])) / (max(highs[-20:]) - min(lows[-20:])) * 100, 1) if max(highs[-20:]) > min(lows[-20:]) else 50,
            }
        return None
    except Exception:
        return None

def fmt_money(v):
    """格式化金额"""
    if abs(v) >= 100000000:
        return f"{v/100000000:.1f}亿"
    elif abs(v) >= 10000:
        return f"{v/10000:.0f}万"
    else:
        return f"{v:.0f}"

def fmt_change(v):
    """格式化涨跌幅"""
    return f"{v:+.2f}%"

def print_section(title, emoji="📊"):
    print(f"\n{'='*55}")
    print(f" {emoji} {title}")
    print(f"{'='*55}")

def analyze_stock(name_or_code):
    print(f"""
╔══════════════════════════════════════╗
║    📈 股票六维分析报告               ║
║    {datetime.now().strftime('%Y-%m-%d %H:%M')}             ║
╚══════════════════════════════════════╝""")

    code, name = get_stock_code(name_or_code)

    # 维度1: 实时行情（第②维技术面 + 第④维资金面初步）
    print_section("① 实时行情（技术面·资金面基础）", "📊")
    quote = get_quote(code)
    if not quote:
        print(f"  ❌ 未找到股票: {name_or_code}")
        return

    chg = quote["change_pct"]
    direction = "🟢" if chg > 0 else "🔴" if chg < 0 else "⚪"
    vol_shou = quote["volume"] // 100
    amount_yi = quote["amount"] / 100000000

    print(f"  {quote['name']}({code})")
    print(f"  现价: {quote['current']:.2f} {direction}  |  涨跌幅: {fmt_change(chg)}")
    print(f"  开盘: {quote['open']:.2f}  |  最高: {quote['high']:.2f}  |  最低: {quote['low']:.2f}")
    print(f"  昨收: {quote['prev_close']:.2f}")
    print(f"  成交量: {vol_shou:,}手  |  成交额: ¥{amount_yi:.2f}亿")

    # 维度2: 技术面分析
    print_section("② 技术面分析", "📈")
    kline_data = get_kline(code)
    if kline_data:
        print(f"  均线系统:")
        print(f"    MA5: {kline_data['ma5']:.2f}  |  MA10: {kline_data['ma10']:.2f}  |  MA20: {kline_data['ma20']:.2f}")
        print(f"  趋势判断: {kline_data['trend']}")
        print(f"  20日内最高: {kline_data['high_20']:.2f}  |  最低: {kline_data['low_20']:.2f}")
        print(f"  当前在20日区间: {kline_data['position']:.0f}%位置")
        if kline_data['position'] > 80:
            print(f"  ⚠️  高位区域（>80%），注意回调风险")
        elif kline_data['position'] < 20:
            print(f"  🟢  低位区域（<20%），可能是底部")
        else:
            print(f"  📊  中部区域，方向待定")
    else:
        print(f"  ⚠️  无法获取K线数据")

    # 维度3: 消息面
    print_section("③ 消息面", "📰")
    print(f"  最新消息需查询（建议关键词）:")
    print(f"    - {quote['name']} 最新公告")
    print(f"    - {quote['name']} 行业政策")
    print(f"    - {quote['name']} 一季报/半年报")

    # 维度4: 资金面
    print_section("④ 资金面", "💰")
    fund = get_fund_flow(code)
    if fund:
        main_label = "🟢🟢" if fund["main_force"] > 10000000 else "🟢" if fund["main_force"] > 0 else "🔴" if fund["main_force"] > -10000000 else "🔴🔴"
        print(f"  最新交易日: {fund['date']}")
        print(f"  主力净流入: {fmt_money(fund['main_force'])} {main_label}")
        print(f"  主力净占比: {fund['main_pct']:+.1f}%")
        print(f"    超大单: {fmt_money(fund['super_large'])}")
        print(f"    大单:   {fmt_money(fund['large'])}")
        if fund["main_force"] > 0:
            print(f"  → 大资金在买入，偏积极")
        else:
            print(f"  → 大资金在流出，需谨慎")
    else:
        print(f"  ⚠️  资金流向数据不可用")

    # 维度5: 市场心理面
    print_section("⑤ 市场心理面", "🧠")
    chg = quote["change_pct"]
    vol_ratio = "放量" if quote["volume"] > 10000000 else "正常" if quote["volume"] > 1000000 else "缩量"
    print(f"  今日涨跌幅: {fmt_change(chg)}")
    print(f"  成交量: {vol_ratio}")
    if chg > 3:
        print(f"  → 市场情绪偏热，注意追高风险")
    elif chg < -3:
        print(f"  → 市场情绪偏恐慌，可能是短期底部")
    elif abs(chg) < 1:
        print(f"  → 成交平淡，市场观望情绪浓厚")
    else:
        print(f"  → 正常波动")

    # 维度6: 宏观面
    print_section("⑥ 宏观/政策面", "🌐")
    # 根据股票行业给出方向性判断（A股常见板块）
    sector_hints = {
        "铜陵": "有色金属·铜 | 铜价受全球供需和美元影响，关注LME铜价走势",
        "云铝": "有色金属·铝 | 铝价受产能政策和下游需求影响",
        "神火": "有色+煤炭 | 双重属性，受煤价和有色金属双重影响",
        "四川黄金": "贵金属·黄金 | 受国际金价和央行购金影响，避险资产",
        "长城电工": "电力设备 | 受益于电网投资和新能源并网需求",
        "四川长虹": "黑色家电 | 消费属性，受地产政策和消费刺激政策影响",
        "华友钴业": "有色·新能源材料 | 受益于新能源车和储能需求增长",
        "贵州茅台": "白酒 | 消费龙头，受消费复苏和政策影响",
    }
    found = False
    for key, hint in sector_hints.items():
        if key in quote['name']:
            print(f"  行业: {hint}")
            found = True
            break
    if not found:
        print(f"  需确认行业归属。建议关注:")
        print(f"    - 行业政策动态")
        print(f"    - 宏观经济数据")

    # 综合建议
    print_section("💡 综合判断", "🎯")
    signals = []
    if quote["change_pct"] > 2:
        signals.append("🟢 今日强势")
    elif quote["change_pct"] < -2:
        signals.append("🔴 今日弱势")

    if fund and fund["main_force"] > 0:
        signals.append("🟢 资金面支持")
    elif fund and fund["main_force"] < 0:
        signals.append("🔴 资金面承压")

    if kline_data:
        if kline_data["trend"] == "多头":
            signals.append("🟢 技术面多头趋势")
        elif kline_data["trend"] == "空头":
            signals.append("🔴 技术面空头趋势")

    if signals:
        print(f"  {' | '.join(signals)}")
    else:
        print(f"  ⚪ 信号不明显，建议观望")

    # 止损止盈建议
    print(f"\n  📌 参考操作区间:")
    if kline_data:
        print(f"    支撑位: {kline_data.get('low_20', 0):.2f}")
        print(f"    压力位: {kline_data.get('high_20', 0):.2f}")

    print(f"\n  ⚠️ 分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 stock_analyze.py <股票名称或代码>")
        print("示例: python3 stock_analyze.py 600519")
        print("      python3 stock_analyze.py 铜陵有色")
        sys.exit(1)
    analyze_stock(sys.argv[1])
