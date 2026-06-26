#!/usr/bin/env python3
"""
股票分析工具
支持技术指标计算、基本面分析、价格预测
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
except ImportError as e:
    print(f"❌ 缺少依赖库: {e}")
    print("请安装: pip install yfinance pandas numpy matplotlib")
    sys.exit(1)

# 配置文件路径
CONFIG_PATH = Path.home() / ".openclaw" / "secrets" / "stock-analyzer.json"

def load_config():
    """加载配置文件"""
    default_config = {
        "default_period": "6mo",
        "default_indicators": ["ma", "rsi", "macd", "bbands"],
        "chart_style": "dark",
        "output_dir": "./reports"
    }
    
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            print(f"⚠️  配置文件加载失败，使用默认配置: {e}")
    
    return default_config

def fetch_stock_data(symbol: str, period: str):
    """获取股票数据"""
    try:
        ticker = yf.Ticker(symbol)
        
        # 获取历史数据
        hist = ticker.history(period=period)
        if hist.empty:
            print(f"❌ 未找到股票 {symbol} 的数据")
            sys.exit(1)
        
        # 获取基本信息
        info = ticker.info
        
        return hist, info
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        sys.exit(1)

def calculate_indicators(df):
    """计算技术指标"""
    # 移动平均线
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA60'] = df['Close'].rolling(window=60).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    
    # 布林带
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    bb_std = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
    df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
    
    return df

def analyze_technical(df, indicators):
    """分析技术指标"""
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    signals = []
    
    # MA 分析
    if 'ma' in indicators:
        ma20 = latest['MA20']
        ma60 = latest['MA60']
        close = latest['Close']
        
        if close > ma20 and ma20 > ma60:
            signals.append(("✅", "短期上涨趋势（MA20 > MA60，价格在均线上方）"))
        elif close < ma20 and ma20 < ma60:
            signals.append(("⚠️", "短期下跌趋势（MA20 < MA60，价格在均线下方）"))
        else:
            signals.append(("⚪", "均线交织，方向不明"))
    
    # RSI 分析
    if 'rsi' in indicators:
        rsi = latest['RSI']
        if rsi > 70:
            signals.append(("⚠️", f"RSI={rsi:.1f}，超买，可能回调"))
        elif rsi < 30:
            signals.append(("✅", f"RSI={rsi:.1f}，超卖，可能反弹"))
        else:
            signals.append(("⚪", f"RSI={rsi:.1f}，中性"))
    
    # MACD 分析
    if 'macd' in indicators:
        macd = latest['MACD']
        signal = latest['Signal_Line']
        hist = latest['MACD_Histogram']
        prev_hist = prev['MACD_Histogram']
        
        if macd > signal and hist > 0:
            if hist > prev_hist:
                signals.append(("✅", "MACD 金叉且柱状图扩大，看涨"))
            else:
                signals.append(("⚪", "MACD 金叉但柱状图缩小，谨慎看涨"))
        elif macd < signal and hist < 0:
            if hist < prev_hist:
                signals.append(("⚠️", "MACD 死叉且柱状图扩大，看跌"))
            else:
                signals.append(("⚪", "MACD 死叉但柱状图缩小，谨慎看跌"))
        else:
            signals.append(("⚪", "MACD 信号不明确"))
    
    # 布林带分析
    if 'bbands' in indicators:
        close = latest['Close']
        upper = latest['BB_Upper']
        lower = latest['BB_Lower']
        
        if close > upper:
            signals.append(("⚠️", "价格触及布林带上轨，可能超买"))
        elif close < lower:
            signals.append(("✅", "价格触及布林带下轨，可能超卖"))
        else:
            signals.append(("⚪", "价格在布林带中轨附近"))
    
    return signals

def generate_report(symbol, df, info, signals, config):
    """生成分析报告"""
    latest = df.iloc[-1]
    
    report = []
    report.append(f"# {symbol} 股票分析报告")
    report.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    report.append("")
    
    # 基本信息
    report.append("## 基本信息")
    company_name = info.get('longName', symbol)
    current_price = latest['Close']
    prev_close = df.iloc[-2]['Close']
    change = current_price - prev_close
    change_pct = (change / prev_close) * 100
    
    report.append(f"- **公司**: {company_name}")
    report.append(f"- **当前价格**: ${current_price:.2f}")
    report.append(f"- **涨跌**: {change:+.2f} ({change_pct:+.1f}%)")
    
    if 'marketCap' in info:
        market_cap = info['marketCap']
        if market_cap > 1e12:
            cap_str = f"${market_cap/1e12:.2f}T"
        elif market_cap > 1e9:
            cap_str = f"${market_cap/1e9:.1f}B"
        else:
            cap_str = f"${market_cap/1e6:.1f}M"
        report.append(f"- **市值**: {cap_str}")
    
    if 'trailingPE' in info:
        report.append(f"- **PE**: {info['trailingPE']:.2f}")
    if 'priceToBook' in info:
        report.append(f"- **PB**: {info['priceToBook']:.2f}")
    report.append("")
    
    # 技术指标
    report.append("## 技术指标")
    if 'ma' in config['default_indicators']:
        report.append(f"- **MA20**: ${latest['MA20']:.2f}")
        report.append(f"- **MA60**: ${latest['MA60']:.2f}")
    if 'rsi' in config['default_indicators']:
        report.append(f"- **RSI(14)**: {latest['RSI']:.2f}")
    if 'macd' in config['default_indicators']:
        report.append(f"- **MACD**: {latest['MACD']:.4f}")
        report.append(f"- **Signal**: {latest['Signal_Line']:.4f}")
    report.append("")
    
    # 信号汇总
    report.append("## 信号汇总")
    for emoji, text in signals:
        report.append(f"{emoji} {text}")
    report.append("")
    
    # 建议
    report.append("## 投资建议")
    bullish_count = sum(1 for e, _ in signals if e == "✅")
    warning_count = sum(1 for e, _ in signals if e == "⚠️")
    
    if bullish_count > warning_count:
        report.append("**短期**: 持有/买入")
        report.append("**中期**: 看涨")
        report.append("**风险等级**: 低-中等")
    elif warning_count > bullish_count:
        report.append("**短期**: 谨慎/观望")
        report.append("**中期**: 中性")
        report.append("**风险等级**: 中等")
    else:
        report.append("**短期**: 持币观望")
        report.append("**中期**: 方向不明")
        report.append("**风险等级**: 中等")
    
    report.append("")
    report.append("---")
    report.append("*免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。*")
    
    return "\n".join(report)

def generate_charts(df, symbol, output_dir):
    """生成图表"""
    Path(output_dir).mkdir(exist_ok=True)
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # 价格 + MA + 布林带
    ax1 = axes[0]
    ax1.plot(df.index, df['Close'], label='收盘价', alpha=0.7)
    ax1.plot(df.index, df['MA20'], label='MA20', alpha=0.7)
    ax1.plot(df.index, df['BB_Upper'], label='布林带上轨', alpha=0.5, linestyle='--')
    ax1.plot(df.index, df['BB_Lower'], label='布林带下轨', alpha=0.5, linestyle='--')
    ax1.fill_between(df.index, df['BB_Lower'], df['BB_Upper'], alpha=0.1)
    ax1.set_title(f'{symbol} - 价格与布林带')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # RSI
    ax2 = axes[1]
    ax2.plot(df.index, df['RSI'], label='RSI', color='purple', alpha=0.7)
    ax2.axhline(y=70, color='r', linestyle='--', alpha=0.5)
    ax2.axhline(y=30, color='g', linestyle='--', alpha=0.5)
    ax2.fill_between(df.index, 30, 70, alpha=0.1)
    ax2.set_title('RSI 指标')
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # MACD
    ax3 = axes[2]
    ax3.plot(df.index, df['MACD'], label='MACD', color='blue', alpha=0.7)
    ax3.plot(df.index, df['Signal_Line'], label='Signal', color='orange', alpha=0.7)
    ax3.bar(df.index, df['MACD_Histogram'], label='Histogram', alpha=0.5)
    ax3.set_title('MACD 指标')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    chart_path = Path(output_dir) / f"{symbol}_analysis_{datetime.now().strftime('%Y%m%d')}.png"
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return chart_path

def predict_price(df, days: int):
    """简单线性回归预测"""
    # 准备数据
    prices = df['Close'].values
    x = np.arange(len(prices)).reshape(-1, 1)
    y = prices
    
    # 线性回归
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(x, y)
    
    # 预测未来
    last_idx = len(prices) - 1
    future_idx = np.arange(last_idx + 1, last_idx + days + 1).reshape(-1, 1)
    predictions = model.predict(future_idx)
    
    # 计算趋势
    slope = model.coef_[0]
    if slope > 0:
        trend = "上涨"
    elif slope < 0:
        trend = "下跌"
    else:
        trend = "横盘"
    
    return predictions, trend, model.score(x, y)

def cmd_analyze(args):
    """分析命令"""
    config = load_config()
    
    print(f"🔍 获取 {args.symbol} 数据...")
    df, info = fetch_stock_data(args.symbol, args.period)
    
    print("📊 计算技术指标...")
    df = calculate_indicators(df)
    
    print("📈 分析信号...")
    signals = analyze_technical(df, args.indicators)
    
    print("📄 生成报告...")
    report = generate_report(args.symbol, df, info, signals, config)
    
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    if args.charts:
        print("\n🖼️  生成图表...")
        output_dir = config['output_dir']
        chart_path = generate_charts(df, args.symbol, output_dir)
        print(f"✅ 图表已保存: {chart_path}")
    
    # 保存报告到文件
    report_file = Path(config['output_dir']) / f"{args.symbol}_report_{datetime.now().strftime('%Y%m%d')}.md"
    report_file.parent.mkdir(exist_ok=True)
    report_file.write_text(report, encoding='utf-8')
    print(f"✅ 报告已保存: {report_file}")

def cmd_fundamentals(args):
    """基本面分析命令"""
    print(f"🔍 获取 {args.symbol} 基本面数据...")
    try:
        ticker = yf.Ticker(args.symbol)
        info = ticker.info
        
        print("\n" + "="*60)
        print(f"# {args.symbol} 基本面分析")
        print("="*60)
        
        fields = [
            ('longName', '公司名称'),
            ('industry', '行业'),
            ('sector', '板块'),
            ('marketCap', '市值'),
            ('trailingPE', 'PE (TTM)'),
            ('forwardPE', 'PE (预期)'),
            ('priceToBook', 'PB'),
            ('trailingEps', 'EPS (TTM)'),
            ('forwardEps', 'EPS (预期)'),
            ('revenueGrowth', '营收增长率'),
            ('earningsGrowth', '利润增长率'),
            ('dividendYield', '股息率'),
            ('beta', 'Beta'),
        ]
        
        for key, label in fields:
            if key in info and info[key] is not None:
                value = info[key]
                if isinstance(value, (int, float)):
                    if key in ['marketCap']:
                        if value > 1e12:
                            value = f"${value/1e12:.2f}T"
                        elif value > 1e9:
                            value = f"${value/1e9:.1f}B"
                        else:
                            value = f"${value/1e6:.1f}M"
                    elif key in ['dividendYield']:
                        value = f"{value*100:.2f}%"
                    elif key in ['revenueGrowth', 'earningsGrowth']:
                        value = f"{value*100:.1f}%"
                print(f"- **{label}**: {value}")
        
        print("="*60)
    except Exception as e:
        print(f"❌ 获取基本面数据失败: {e}")
        sys.exit(1)

def cmd_predict(args):
    """预测命令"""
    config = load_config()
    
    print(f"🔍 获取 {args.symbol} 历史数据...")
    df, info = fetch_stock_data(args.symbol, "2y")
    
    print("🧮 计算预测模型...")
    try:
        predictions, trend, r2 = predict_price(df, args.days)
    except ImportError:
        print("❌ 需要安装 scikit-learn: pip install scikit-learn")
        sys.exit(1)
    
    print("\n" + "="*60)
    print(f"# {args.symbol} 价格预测")
    print("="*60)
    print(f"**模型**: 线性回归")
    print(f"**R²**: {r2:.4f}")
    print(f"**趋势**: {trend}")
    print(f"**预测天数**: {args.days}")
    print("")
    print("**预测价格**:")
    
    current_price = df['Close'].iloc[-1]
    for i, price in enumerate(predictions, 1):
        change = price - current_price
        change_pct = (change / current_price) * 100
        print(f"- 第{i}天: ${price:.2f} ({change:+.2f}, {change_pct:+.1f}%)")
    
    print("="*60)
    print("⚠️  免责声明：预测仅供参考，不构成投资建议。")

def main():
    parser = argparse.ArgumentParser(description="股票分析工具")
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # analyze 命令
    parser_analyze = subparsers.add_parser('analyze', help='股票技术分析')
    parser_analyze.add_argument('--symbol', '-s', required=True, help='股票代码')
    parser_analyze.add_argument('--period', '-p', default='6mo', 
                                choices=['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y'],
                                help='数据周期')
    parser_analyze.add_argument('--indicators', '-i', default='ma,rsi,macd,bbands',
                                help='技术指标列表，逗号分隔')
    parser_analyze.add_argument('--report', '-r', default='summary',
                                choices=['summary', 'full'],
                                help='报告类型')
    parser_analyze.add_argument('--charts', '-c', action='store_true',
                                help='生成图表')
    
    # fundamentals 命令
    parser_fund = subparsers.add_parser('fundamentals', help='基本面分析')
    parser_fund.add_argument('--symbol', '-s', required=True, help='股票代码')
    parser_fund.add_argument('--locale', default='en', choices=['zh', 'en'],
                             help='数据语言')
    
    # predict 命令
    parser_predict = subparsers.add_parser('predict', help='价格预测')
    parser_predict.add_argument('--symbol', '-s', required=True, help='股票代码')
    parser_predict.add_argument('--days', '-d', type=int, default=5,
                               help='预测天数 (1-30)')
    parser_predict.add_argument('--method', '-m', default='linear',
                               choices=['linear', 'prophet'],
                               help='预测方法')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'analyze':
            args.indicators = [i.strip() for i in args.indicators.split(',')]
            cmd_analyze(args)
        elif args.command == 'fundamentals':
            cmd_fundamentals(args)
        elif args.command == 'predict':
            if args.days < 1 or args.days > 30:
                print("❌ 预测天数必须在 1-30 之间")
                sys.exit(1)
            cmd_predict(args)
    except KeyboardInterrupt:
        print("\n\n⚠️  已取消")
        sys.exit(130)
    except Exception as e:
        print(f"❌ 错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()