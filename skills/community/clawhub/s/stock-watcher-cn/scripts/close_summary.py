# -*- coding: utf-8 -*-
"""
收盘总结工具 - 两阶段执行
14:50 预收集数据，15:00 生成总结并推送
"""

import sys
import os
import json
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from monitor import StockAlert, WATCHLIST


def collect_pre_close_data():
    """14:50 收集收盘前数据并缓存"""
    print(f"[{datetime.now().strftime('%H:%M')}] 开始收集收盘前数据...")
    
    monitor = StockAlert()
    stocks_to_check = [s for s in WATCHLIST if s.get('focus', False)]
    
    if not stocks_to_check:
        print('[预收集] 没有关注的股票，跳过')
        return
    
    data_map = monitor.fetch_sina_realtime(stocks_to_check)
    
    # 收集每只股票的详细数据
    collected_data = {}
    for stock in stocks_to_check:
        code = stock['code']
        if code in data_map:
            data = data_map[code]
            alerts, level = monitor.check_alerts(stock, data)
            
            collected_data[code] = {
                'stock': stock,
                'data': data,
                'alerts': alerts,
                'level': level,
                'collected_at': datetime.now().isoformat()
            }
    
    # 保存到缓存文件
    cache_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, 'pre_close_data.json')
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(collected_data, f, ensure_ascii=False, indent=2)
    
    print(f'[预收集] 完成！已缓存 {len(collected_data)} 只股票数据')
    print(f'[预收集] 缓存文件：{cache_file}')
    return collected_data


def generate_close_summary():
    """15:00 生成收盘总结并推送"""
    print(f"[{datetime.now().strftime('%H:%M')}] 开始生成收盘总结...")
    
    # 读取缓存数据
    cache_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')
    cache_file = os.path.join(cache_dir, 'pre_close_data.json')
    
    if not os.path.exists(cache_file):
        print('[收盘总结] 未找到缓存数据，执行即时扫描')
        collect_pre_close_data()
    
    with open(cache_file, 'r', encoding='utf-8') as f:
        cached_data = json.load(f)
    
    # 补充最后数据（收盘价确认）
    monitor = StockAlert()
    summary_lines = []
    summary_lines.append('=' * 50)
    summary_lines.append(f'📊 收盘总结 ({datetime.now().strftime("%Y-%m-%d %H:%M")})')
    summary_lines.append('=' * 50)
    
    triggered_alerts = []
    
    for code, item in cached_data.items():
        stock = item['stock']
        data = item['data']
        alerts = item['alerts']
        level = item['level']
        
        # 获取最新价格（确认收盘价）
        latest = monitor.fetch_sina_realtime([stock])
        if code in latest:
            data = latest[code]
        
        change_pct = (data['price'] - data['prev_close']) / data['prev_close'] * 100 if data['prev_close'] else 0
        color_emoji = '🔴' if change_pct > 0 else '🟢' if change_pct < 0 else '⚪'
        
        summary_lines.append('')
        summary_lines.append(f'{color_emoji} {stock["name"]} ({code})')
        summary_lines.append(f'   收盘价：{data["price"]:.2f} 元 ({change_pct:+.2f}%)')
        summary_lines.append(f'   预警级别：{level}')
        
        if alerts:
            summary_lines.append(f'   触发预警 ({len(alerts)}项):')
            for _, text in alerts:
                summary_lines.append(f'     • {text}')
            triggered_alerts.append((stock, data, alerts, level))
        else:
            summary_lines.append(f'   无预警')
    
    summary_lines.append('')
    summary_lines.append('=' * 50)
    summary_lines.append('💡 明日关注:')
    summary_lines.append('   - 持续关注成交量异动股票')
    summary_lines.append('   - 关注操盘手习惯变化')
    summary_lines.append('=' * 50)
    
    # 输出总结
    summary_text = '\n'.join(summary_lines)
    print(summary_text)
    
    # 推送飞书（只推送有预警的股票）
    if triggered_alerts:
        push_msg = generate_push_message(triggered_alerts)
        print(f'\n[飞书推送]\n{push_msg}')
    
    return summary_text


def generate_push_message(triggered_alerts):
    """生成飞书推送消息"""
    lines = []
    lines.append('📊 【收盘总结】')
    lines.append('')
    
    for stock, data, alerts, level in triggered_alerts:
        code = stock['code']
        change_pct = (data['price'] - data['prev_close']) / data['prev_close'] * 100 if data['prev_close'] else 0
        color_emoji = '🔴' if change_pct > 0 else '🟢' if change_pct < 0 else '⚪'
        
        level_icon = '🚨' if level == 'critical' else '⚠️' if level == 'warning' else '📢'
        
        lines.append(f'{level_icon} {color_emoji} {stock["name"]} ({code})')
        lines.append(f'💰 收盘价：{data["price"]:.2f} 元 ({change_pct:+.2f}%)')
        lines.append(f'🎯 预警 ({len(alerts)}项):')
        for _, text in alerts:
            lines.append(f'  • {text}')
        lines.append('')
    
    return '\n'.join(lines)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == 'pre_close':
            collect_pre_close_data()
        elif mode == 'close_summary':
            generate_close_summary()
    else:
        print('用法：python close_summary.py [pre_close|close_summary]')
        print('  pre_close    - 14:50 预收集数据')
        print('  close_summary - 15:00 生成总结并推送')
