#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T+0 基金实时监控 - 健壮版（带日志、重试、进程守护）
"""

import os
import sys
import json
import yaml
import time
import argparse
import signal
import logging
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
from apscheduler.schedulers.background import BackgroundScheduler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetch import get_fund_realtime, get_fund_1min_kline, get_fund_5min_kline
from indicators import calculate_indicators, get_latest_indicators
from signals import generate_signals, format_signal, process_signal, get_trade_history, format_trade, load_trades
from notifier import notify

# 基础路径
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = BASE_DIR / 'data'
CONFIG_DIR = BASE_DIR / 'config'
LOGS_DIR = BASE_DIR / 'logs'

# 日志文件
LOG_FILE = LOGS_DIR / 'monitor.log'

# 确保目录存在
for d in [DATA_DIR, CONFIG_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 配置日志
def setup_logging():
    """配置日志系统"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 文件处理器（带轮转）
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

# 数据文件
WATCHLIST_FILE = DATA_DIR / 'watchlist.json'
SIGNALS_FILE = DATA_DIR / 'signals.json'
CONFIG_FILE = CONFIG_DIR / 'default.yaml'
PID_FILE = DATA_DIR / 'monitor.pid'

# 全局变量
scheduler = None
monitoring = False
fast_mode = False
shutdown_requested = False

# 信号处理
def signal_handler(signum, frame):
    """处理退出信号"""
    global shutdown_requested
    logger.info(f"收到信号 {signum}，准备退出...")
    shutdown_requested = True
    if scheduler:
        scheduler.shutdown()
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def save_pid():
    """保存 PID 文件"""
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

def load_config() -> dict:
    """加载配置（带默认值）"""
    default_config = {
        'monitor': {
            'interval': 60,
            'market_hours': {'start': '09:30', 'end': '15:00', 'noon_break': {'start': '11:30', 'end': '13:00'}},
            'fast_mode': True
        },
        'indicators': {
            'macd': {'fast': 12, 'slow': 26, 'signal': 9},
            'kdj': {'n': 9, 'm1': 3, 'm2': 3}
        },
        'signals': {
            'buy': {'kdj_max': 20, 'volume_ratio': 1.2, 'kdj_early': 30},
            'sell': {'kdj_min': 80},
            'stop_loss': 2,
            'take_profit': 3
        },
        'notify': {
            'dingtalk': {'enabled': False, 'webhook': ''},
            'wechat': {'enabled': False, 'key': ''},
            'terminal': {'enabled': True, 'sound': True}
        }
    }
    
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    for key in user_config:
                        if isinstance(user_config[key], dict) and key in default_config:
                            default_config[key].update(user_config[key])
                        else:
                            default_config[key] = user_config[key]
    except Exception as e:
        logger.error(f"加载配置失败：{e}")
    
    return default_config

def load_watchlist() -> list:
    """加载监控列表（带异常处理）"""
    try:
        if WATCHLIST_FILE.exists():
            with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception as e:
        logger.error(f"加载监控列表失败：{e}")
    return []

def is_market_hours() -> bool:
    """判断是否在交易时间"""
    try:
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        config = load_config()
        market = config['monitor']['market_hours']
        
        if now.weekday() >= 5:
            return False
        if current_time < market['start'] or current_time >= market['end']:
            return False
        noon = market['noon_break']
        if noon['start'] <= current_time < noon['end']:
            return False
        return True
    except Exception as e:
        logger.error(f"判断交易时间失败：{e}")
        return False

def check_single_fund(code: str, config: dict, use_fast_mode: bool = False) -> list:
    """检查单只基金（带异常处理）"""
    results = []
    try:
        realtime = get_fund_realtime(code)
        if not realtime:
            return results
        
        if use_fast_mode:
            kline = get_fund_1min_kline(code, periods=60)
        else:
            kline = get_fund_5min_kline(code, periods=100)
        
        if kline is None or len(kline) < 30:
            return results
        
        kline_with_indicators = calculate_indicators(kline, config.get('indicators'), fast_mode=use_fast_mode)
        if kline_with_indicators is None:
            return results
        
        indicators = get_latest_indicators(kline_with_indicators)
        if indicators is None:
            return results
        
        fund_signals = generate_signals(code, realtime['name'], indicators, config.get('signals'), fast_mode=use_fast_mode)
        
        for signal in fund_signals:
            signal['realtime'] = realtime
            result = process_signal(signal)
            results.append(result)
        
        return results
    except Exception as e:
        logger.error(f"检查基金 {code} 失败：{e}", exc_info=True)
        return results

def run_check():
    """执行一次监控检查"""
    global fast_mode
    
    try:
        if not is_market_hours():
            logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] 非交易时间，跳过")
            return
        
        config = load_config()
        watchlist = load_watchlist()
        fast_mode = config['monitor'].get('fast_mode', True)
        
        mode_str = "⚡快速" if fast_mode else "📊标准"
        logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] {mode_str} - 检查 {len(watchlist)} 只基金...")
        
        new_results = []
        success_count = 0
        
        for code in watchlist:
            results = check_single_fund(code, config, use_fast_mode=fast_mode)
            if results:
                new_results.extend(results)
                success_count += 1
        
        if new_results:
            for result in new_results:
                signal = result['signal']
                notify(signal, config)
                
                if result['profit']:
                    profit_pct = result['profit']['profit_pct']
                    profit_emoji = "🟢" if profit_pct > 0 else "🔴"
                    logger.info(f"{profit_emoji} 完成交易！盈亏：{profit_pct:+.2f}% - {signal['code']}")
            
            logger.info(f"✨ 发现 {len(new_results)} 个新信号!")
            # 输出详细信号信息
            for sig in new_results:
                signal = sig.get('signal', {})
                signal_type = "🟢 买入" if signal.get('type') == 'BUY' else "🔴 卖出"
                code = signal.get('code', 'UNKNOWN')
                name = signal.get('name', '')
                price = signal.get('price', 0)
                reason = signal.get('reason', 'N/A')
                logger.info(f"  {signal_type} {code} {name} @ {price} - {reason}")
        else:
            logger.info("无新信号")
        
        logger.info(f"检查完成 - 成功：{success_count}/{len(watchlist)}")
        
    except Exception as e:
        logger.error(f"监控检查失败：{e}", exc_info=True)

def cmd_add(args):
    """添加基金"""
    try:
        codes = [c.strip() for c in args.codes.replace(',', ' ').split()]
        watchlist = load_watchlist()
        added = [c for c in codes if c not in watchlist]
        watchlist.extend(added)
        
        with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(watchlist, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 已添加 {len(added)} 只基金：{', '.join(added)}")
        logger.info(f"监控列表共 {len(watchlist)} 只")
    except Exception as e:
        logger.error(f"添加失败：{e}")

def cmd_remove(args):
    """移除基金"""
    try:
        watchlist = load_watchlist()
        if args.code in watchlist:
            watchlist.remove(args.code)
            with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
                json.dump(watchlist, f, ensure_ascii=False, indent=2)
            logger.info(f"✅ 已移除 {args.code}")
        else:
            logger.info(f"❌ {args.code} 不在监控列表中")
    except Exception as e:
        logger.error(f"移除失败：{e}")

def cmd_list(args):
    """显示监控列表"""
    try:
        watchlist = load_watchlist()
        if not watchlist:
            logger.info("监控列表为空")
            return
        
        logger.info(f"📊 监控列表 ({len(watchlist)}只):\n")
        for i, code in enumerate(watchlist, 1):
            realtime = get_fund_realtime(code)
            if realtime:
                change_color = "🟢" if realtime['change_pct'] >= 0 else "🔴"
                logger.info(f"{i}. {code} - {realtime['name']} - {realtime['price']:.3f} {change_color} {realtime['change_pct']:+.2f}%")
            else:
                logger.info(f"{i}. {code} - 获取行情失败")
    except Exception as e:
        logger.error(f"显示列表失败：{e}")

def cmd_start(args):
    """启动监控"""
    global scheduler, monitoring, fast_mode
    
    try:
        # 检查是否已在运行
        if os.path.exists(PID_FILE):
            with open(PID_FILE, 'r') as f:
                old_pid = int(f.read().strip())
            try:
                os.kill(old_pid, 0)
                logger.info(f"⚠️ 监控已在运行中 (PID: {old_pid})")
                return
            except ProcessLookupError:
                logger.info("检测到残留 PID 文件，清理中...")
                os.remove(PID_FILE)
        
        watchlist = load_watchlist()
        if not watchlist:
            logger.info("❌ 监控列表为空")
            return
        
        config = load_config()
        interval = config['monitor']['interval']
        fast_mode = config['monitor'].get('fast_mode', True)
        
        mode_str = "⚡快速模式 (1 分钟)" if fast_mode else "📊标准模式 (5 分钟)"
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_check, 'interval', seconds=interval)
        scheduler.start()
        
        monitoring = True
        save_pid()
        
        logger.info(f"✅ 监控已启动 - {mode_str}")
        logger.info(f"   监控基金：{len(watchlist)}只")
        logger.info(f"   检查间隔：{interval}秒")
        logger.info(f"   交易时间：09:30-11:30, 13:00-15:00")
        logger.info(f"   日志文件：{LOG_FILE}")
        logger.info(f"   PID: {os.getpid()}")
        logger.info(f"\n按 Ctrl+C 停止监控")
        
        while monitoring and not shutdown_requested:
            time.sleep(1)
    except Exception as e:
        logger.error(f"启动失败：{e}", exc_info=True)
    finally:
        cmd_stop(args)

def cmd_stop(args):
    """停止监控"""
    global scheduler, monitoring
    
    try:
        if scheduler:
            scheduler.shutdown()
            scheduler = None
        monitoring = False
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        logger.info("✅ 监控已停止")
    except Exception as e:
        logger.error(f"停止失败：{e}")

def cmd_trades(args):
    """显示交易历史"""
    try:
        limit = getattr(args, 'limit', 20) if hasattr(args, 'limit') else 20
        trades = get_trade_history(limit)
        
        if not trades:
            logger.info("暂无完整交易记录")
            return
        
        logger.info(f"📊 交易历史 (最近 {len(trades)}笔)\n")
        logger.info("=" * 70)
        
        total_profit = 0
        winning_trades = 0
        
        for trade in trades:
            logger.info(format_trade(trade))
            total_profit += trade['profit_pct']
            if trade['profit_pct'] > 0:
                winning_trades += 1
        
        logger.info("=" * 70)
        logger.info(f"📈 统计:")
        logger.info(f"   总交易：{len(trades)} | 胜率：{winning_trades/len(trades)*100:.1f}% | 累计：{total_profit:+.2f}% | 场均：{total_profit/len(trades):+.2f}%")
    except Exception as e:
        logger.error(f"显示交易失败：{e}")

def cmd_status(args):
    """显示监控状态"""
    try:
        watchlist = load_watchlist()
        trades = load_trades()
        open_positions = [t for t in trades if t.get('status') == 'OPEN']
        closed_trades = [t for t in trades if t.get('status') == 'CLOSED' and t['type'] == 'SELL']
        
        logger.info("📊 监控状态")
        logger.info("=" * 50)
        logger.info(f"监控基金：{len(watchlist)}只")
        logger.info(f"总交易：{len(trades)} | 未平仓：{len(open_positions)} | 已完成：{len(closed_trades)}")
        # 检查实际进程是否存在
        process_running = False
        if os.path.exists(PID_FILE):
            try:
                with open(PID_FILE, 'r') as f:
                    pid = int(f.read().strip())
                import subprocess
                result = subprocess.run(['ps', '-p', str(pid)], capture_output=True)
                process_running = (result.returncode == 0)
            except:
                process_running = False
        
        logger.info(f"运行状态：{'🟢 运行中' if process_running else '🔴 已停止'}")
        
        if process_running:
            logger.info(f"进程 PID: {pid}")
        
        if open_positions:
            logger.info(f"\n📍 未平仓头寸 ({len(open_positions)}个):")
            for pos in open_positions[:5]:
                logger.info(f"   {pos['code']} - 买入：{pos['price']:.3f} @ {pos['time']}")
        
        if closed_trades:
            total_profit = sum(t['profit_pct'] for t in closed_trades)
            winning = sum(1 for t in closed_trades if t['profit_pct'] > 0)
            logger.info(f"\n📈 表现：胜率 {winning/len(closed_trades)*100:.1f}% | 累计 {total_profit:+.2f}%")
    except Exception as e:
        logger.error(f"显示状态失败：{e}")

def main():
    parser = argparse.ArgumentParser(description='T+0 基金实时监控')
    subparsers = parser.add_subparsers(dest='command')
    
    add_p = subparsers.add_parser('add', help='添加基金')
    add_p.add_argument('codes')
    add_p.set_defaults(func=cmd_add)
    
    remove_p = subparsers.add_parser('remove', help='移除基金')
    remove_p.add_argument('code')
    remove_p.set_defaults(func=cmd_remove)
    
    subparsers.add_parser('list', help='监控列表').set_defaults(func=cmd_list)
    subparsers.add_parser('start', help='启动监控').set_defaults(func=cmd_start)
    subparsers.add_parser('stop', help='停止监控').set_defaults(func=cmd_stop)
    subparsers.add_parser('trades', help='交易历史').set_defaults(func=cmd_trades)
    subparsers.add_parser('status', help='监控状态').set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return
    args.func(args)

if __name__ == '__main__':
    main()
