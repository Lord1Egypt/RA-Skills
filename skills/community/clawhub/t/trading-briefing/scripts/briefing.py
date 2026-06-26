#!/usr/bin/env python3
"""
Trading Briefing - 一站式交易系统简报
聚合市场行情、机器人状态、持仓、系统健康、策略发现
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = "/root/.openclaw/workspace"
LIVE_DIR = os.path.join(WORKSPACE, "live_trading")
BACKTEST_DIR = os.path.join(WORKSPACE, "backtest")

def get_market_data():
    """获取市场行情"""
    try:
        import ccxt
        exchange = ccxt.okx({'enableRateLimit': True})
        
        symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT']
        results = []
        
        for symbol in symbols:
            try:
                ticker = exchange.fetch_ticker(symbol)
                price = ticker['last']
                change = ticker.get('percentage', 0) or 0
                vol = ticker.get('quoteVolume', 0) or 0
                
                emoji = "🟢" if change >= 0 else "🔴"
                results.append({
                    'symbol': symbol,
                    'price': price,
                    'change': change,
                    'volume': vol,
                    'emoji': emoji
                })
            except:
                continue
        
        return results
    except ImportError:
        return None

def get_bot_status():
    """获取机器人状态"""
    state_file = os.path.join(LIVE_DIR, "state.json")
    log_file = os.path.join(LIVE_DIR, "trading.log")
    
    status = {
        'running': False,
        'positions': {},
        'daily_pnl': 0,
        'total_trades': 0,
        'win_rate': 0,
        'last_trade': None
    }
    
    # 检查进程
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'bot.py'],
            capture_output=True, text=True, timeout=5
        )
        status['running'] = result.returncode == 0
    except:
        pass
    
    # 读取状态
    if os.path.exists(state_file):
        try:
            with open(state_file) as f:
                state = json.load(f)
            status['positions'] = state.get('positions', {})
            status['daily_pnl'] = state.get('daily_pnl', 0)
            status['total_trades'] = state.get('total_trades', 0)
            wins = state.get('winning_trades', 0)
            if status['total_trades'] > 0:
                status['win_rate'] = wins / status['total_trades'] * 100
        except:
            pass
    
    # 获取最后交易时间
    if os.path.exists(log_file):
        try:
            result = subprocess.run(
                ['tail', '-20', log_file],
                capture_output=True, text=True, timeout=5
            )
            for line in reversed(result.stdout.split('\n')):
                if '买入' in line or '卖出' in line or '开仓' in line or '平仓' in line:
                    status['last_trade'] = line.strip()[:80]
                    break
        except:
            pass
    
    return status

def get_positions_pnl():
    """获取持仓盈亏"""
    state_file = os.path.join(LIVE_DIR, "state.json")
    
    if not os.path.exists(state_file):
        return {}
    
    try:
        with open(state_file) as f:
            state = json.load(f)
        return state.get('positions', {})
    except:
        return {}

def get_system_health():
    """获取系统健康状态"""
    health = {}
    
    # 磁盘
    try:
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            health['disk_used'] = parts[4] if len(parts) > 4 else 'N/A'
            health['disk_avail'] = parts[3] if len(parts) > 3 else 'N/A'
    except:
        health['disk_used'] = 'N/A'
    
    # 内存
    try:
        result = subprocess.run(['free', '-h'], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            health['mem_used'] = parts[2] if len(parts) > 2 else 'N/A'
            health['mem_total'] = parts[1] if len(parts) > 1 else 'N/A'
    except:
        health['mem_used'] = 'N/A'
    
    # 关键进程
    processes = {
        'openclaw-gateway': 'OpenClaw网关',
        'bot.py': '交易机器人',
        'strategy_discovery.py': '策略发现'
    }
    
    health['processes'] = {}
    for proc, name in processes.items():
        try:
            result = subprocess.run(
                ['pgrep', '-f', proc],
                capture_output=True, text=True, timeout=5
            )
            health['processes'][name] = result.returncode == 0
        except:
            health['processes'][name] = False
    
    return health

def get_discovery_status():
    """获取策略发现引擎状态"""
    best_file = os.path.join(BACKTEST_DIR, "current_best.json")
    log_file = os.path.join(BACKTEST_DIR, "discovery.log")
    
    status = {
        'running': False,
        'best_strategy': None,
        'best_sharpe': 0,
        'best_return': 0
    }
    
    # 检查进程
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'strategy_discovery.py'],
            capture_output=True, text=True, timeout=5
        )
        status['running'] = result.returncode == 0
    except:
        pass
    
    # 读取最佳策略
    if os.path.exists(best_file):
        try:
            with open(best_file) as f:
                best = json.load(f)
            status['best_strategy'] = best.get('strategy', 'N/A')
            status['best_sharpe'] = best.get('sharpe', 0)
            status['best_return'] = best.get('return', 0)
        except:
            pass
    
    return status

def format_price(price):
    """格式化价格"""
    if price >= 1000:
        return f"${price:,.0f}"
    elif price >= 1:
        return f"${price:,.2f}"
    else:
        return f"${price:.4f}"

def generate_report():
    """生成完整简报"""
    now = datetime.now(CST)
    
    lines = []
    lines.append("=" * 40)
    lines.append(f"📊 交易简报")
    lines.append(f"   {now.strftime('%Y-%m-%d %H:%M')} CST")
    lines.append("=" * 40)
    
    # 1. 市场行情
    lines.append("")
    lines.append("📈 市场行情")
    lines.append("-" * 30)
    
    market = get_market_data()
    if market:
        for item in market:
            sign = "+" if item['change'] >= 0 else ""
            lines.append(
                f"  {item['emoji']} {item['symbol']:8s} "
                f"{format_price(item['price']):>12s}  "
                f"{sign}{item['change']:.1f}%"
            )
    else:
        lines.append("  ⚠️ 无法获取行情数据")
    
    # 2. 机器人状态
    lines.append("")
    lines.append("🤖 交易机器人")
    lines.append("-" * 30)
    
    bot = get_bot_status()
    if bot['running']:
        lines.append("  ✅ 运行中")
    else:
        lines.append("  ❌ 未运行")
    
    lines.append(f"  📊 今日交易: {bot['total_trades']} 笔")
    if bot['total_trades'] > 0:
        lines.append(f"  🎯 胜率: {bot['win_rate']:.1f}%")
    lines.append(f"  💵 今日盈亏: {bot['daily_pnl']:+.2f} USDT")
    
    if bot['last_trade']:
        lines.append(f"  🕐 最近交易: {bot['last_trade'][:50]}...")
    
    # 3. 持仓
    positions = get_positions_pnl()
    if positions:
        lines.append("")
        lines.append("💰 当前持仓")
        lines.append("-" * 30)
        for symbol, pos in positions.items():
            side = pos.get('side', '?')
            size = pos.get('size', 0)
            pnl = pos.get('unrealized_pnl', 0)
            emoji = "🟢" if pnl >= 0 else "🔴"
            lines.append(f"  {emoji} {symbol} {side} {size} | 盈亏: {pnl:+.2f}")
    
    # 4. 系统健康
    lines.append("")
    lines.append("⚙️ 系统状态")
    lines.append("-" * 30)
    
    health = get_system_health()
    lines.append(f"  💾 磁盘: {health.get('disk_used', 'N/A')} 已用")
    lines.append(f"  🧠 内存: {health.get('mem_used', 'N/A')} / {health.get('mem_total', 'N/A')}")
    
    for name, running in health.get('processes', {}).items():
        emoji = "✅" if running else "❌"
        lines.append(f"  {emoji} {name}")
    
    # 5. 策略发现
    lines.append("")
    lines.append("🧠 策略发现")
    lines.append("-" * 30)
    
    discovery = get_discovery_status()
    if discovery['running']:
        lines.append("  ✅ 引擎运行中")
    else:
        lines.append("  ⚠️ 引擎未运行")
    
    if discovery['best_strategy']:
        lines.append(f"  📋 最佳策略: {discovery['best_strategy']}")
        lines.append(f"  📊 夏普比率: {discovery['best_sharpe']:.2f}")
        lines.append(f"  💰 策略收益: {discovery['best_return']:.1%}")
    
    lines.append("")
    lines.append("=" * 40)
    
    return "\n".join(lines)

if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # 可选：保存到文件
    if "--save" in sys.argv:
        report_file = os.path.join(WORKSPACE, "daily_briefing.md")
        with open(report_file, "w") as f:
            f.write(f"# 每日简报 - {datetime.now(CST).strftime('%Y-%m-%d')}\n\n")
            f.write("```\n")
            f.write(report)
            f.write("\n```\n")
        print(f"\n📄 报告已保存到 {report_file}")
