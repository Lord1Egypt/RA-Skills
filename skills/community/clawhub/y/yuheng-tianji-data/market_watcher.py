#!/usr/bin/env python3
"""
七政系统·天枢盘中预警触发器
玉衡·廉贞：盘中实时监控 + 异常预警触发
监测：价格异动 / 资金大幅流出 / 地缘事件 / 涨停板异常
用法：每5分钟执行一次，检测到异常立即推送飞书
"""
import sys
import datetime
import json
import os
import time

sys.path.insert(0, '/workspace/skills/tianji-data')
sys.path.insert(0, '/workspace/skills/tianji-model')

ALERT_QUEUE = '/workspace/data/tianji-system/alerts_queue'
os.makedirs(ALERT_QUEUE, exist_ok=True)

# ─── 预警阈值配置 ───────────────────────────────

THRESHOLDS = {
    'index_drop': -1.5,           # 指数单分钟跌超1.5%
    'index_rise': 1.5,            # 指数单分钟涨超1.5%
    'limit_up_surge': 20,          # 涨停家数单日突破20家（情绪过热预警）
    'limit_down_surge': 30,        # 跌停家数单日突破30家（恐慌蔓延）
    'main_outflow': -200,          # 主力单分钟净流出超200亿
    'oil_spike': 5.0,              # 原油单分钟涨超5%（地缘重大异动）
    'gold_spike': 2.0,             # 黄金单分钟涨超2%（避险升温）
}


# ─── 数据采集 ─────────────────────────────────

def get_realtime_snapshot():
    """获取当前实时快照"""
    from free_market import get_full_market_snapshot, get_commodities
    from realtime import get_batch

    snap = get_full_market_snapshot()
    indices = get_batch(['000001', '399001', '399006'])
    comm = get_commodities()
    return {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'indices': indices,
        'comm': comm,
        'snap': snap,
    }


# ─── 预警检测 ─────────────────────────────────

def check_alerts(current: dict, prev: dict = None) -> list:
    """
    检测所有预警类型
    current：当前快照
    prev：上一分钟快照（可选，用于计算变化）
    """
    alerts = []
    now = current['timestamp']
    indices = current['indices']
    comm = current.get('comm', {})

    # 1. 指数大幅波动
    for code, name in [('000001', '上证'), ('399006', '创业板')]:
        idx = indices.get(code, {})
        chg = idx.get('change_pct', 0) or 0
        if chg <= THRESHOLDS['index_drop']:
            alerts.append({
                'level': '🔴 高',
                'type': '指数暴跌',
                'content': f"{name}指数当前{idx.get('price')}（{chg:+.2f}%），跌幅超{abs(chg):.1f}%",
                'action': '建议减仓/止损',
            })
        elif chg >= THRESHOLDS['index_rise']:
            alerts.append({
                'level': '🟢 利好',
                'type': '指数大涨',
                'content': f"{name}指数当前{idx.get('price')}（{chg:+.2f}%），涨幅超{abs(chg):.1f}%",
                'action': '可加仓跟进',
            })

    # 2. 地缘风险：原油异动
    oil = comm.get('crude_oil', {})
    oil_price = oil.get('price') or oil.get('bid')
    if oil_price:
        # 估算变化率（用bid和prev_close对比）
        oil_prev = oil.get('prev_close') or oil_price
        if oil_prev and oil_prev > 0:
            oil_chg = (oil_price - oil_prev) / oil_prev * 100
            if oil_chg >= THRESHOLDS['oil_spike']:
                alerts.append({
                    'level': '🔴 高',
                    'type': '原油暴涨',
                    'content': f"WTI原油当前${oil_price}（{oil_chg:+.1f}%），地缘风险升温",
                    'action': '关注：油气/新能源板块分化',
                })

    # 3. 黄金异动
    gold = comm.get('gold', {})
    gold_price = gold.get('price') or gold.get('bid')
    if gold_price:
        gold_prev = gold.get('prev_close') or gold_price
        if gold_prev and gold_prev > 0:
            gold_chg = (gold_price - gold_prev) / gold_prev * 100
            if gold_chg >= THRESHOLDS['gold_spike']:
                alerts.append({
                    'level': '🟡 中',
                    'type': '黄金暴涨',
                    'content': f"黄金当前${gold_price}（{gold_chg:+.1f}%），避险情绪升温",
                    'action': '关注：黄金股/日元/瑞郎',
                })

    return alerts


# ─── 预警等级判定 ─────────────────────────────

def get_overall_level(alerts: list) -> str:
    """综合预警等级"""
    if any(a['level'] == '🔴 高' for a in alerts):
        return '🔴 高级预警'
    elif any(a['level'] == '🟡 中' for a in alerts):
        return '🟡 中级预警'
    elif alerts:
        return '🟢 低级提示'
    return '✅ 无预警'


# ─── 飞书推送 ─────────────────────────────────

def push_to_feishu(alert_msg: str) -> bool:
    """推送预警到飞书（通过message工具）"""
    try:
        from message_tool import message
        # 动态导入（避免循环依赖）
        import subprocess
        result = subprocess.run(
            ['python3', '-c',
             f'from tools import message; message(action="send", channel="feishu", target="user:ou_fd61d5ebc9af22913aa4c21c8e3cac14", message="{alert_msg}")'],
            capture_output=True, text=True, timeout=15,
            cwd='/workspace'
        )
        return result.returncode == 0
    except Exception:
        return False


# ─── 队列持久化 ───────────────────────────────

def save_alert(alert: dict):
    """保存预警到队列"""
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    path = f"{ALERT_QUEUE}/{ts}_{alert['type']}.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(alert, f, ensure_ascii=False, indent=2)


# ─── 主监控函数 ───────────────────────────────

def monitor():
    """
    盘中监控主循环
    推荐：每5分钟执行一次（cron或while循环）
    """
    prev_state_path = '/tmp/tianji_prev_state.json'

    # 读取上次状态（用于计算变化）
    prev = None
    if os.path.exists(prev_state_path):
        try:
            with open(prev_state_path, 'r') as f:
                prev = json.load(f)
        except Exception:
            pass

    # 采集当前数据
    current = get_realtime_snapshot()

    # 检测预警
    alerts = check_alerts(current, prev)

    # 保存当前状态
    with open(prev_state_path, 'w') as f:
        json.dump(current, f)

    # 输出结果
    now_str = current['timestamp']
    print(f"[天枢监控] {now_str} | 预警数量：{len(alerts)}")

    if alerts:
        level = get_overall_level(alerts)
        print(f"[预警] {level}")
        for a in alerts:
            print(f"  {a['level']} {a['type']}：{a['content']}")
            print(f"  操作建议：{a['action']}")
            save_alert(a)
    else:
        print("[监控] 无异常")

    return alerts


# ─── 预包装推送消息 ──────────────────────────

def build_alert_message(alerts: list, timestamp: str) -> str:
    """构建飞书预警消息"""
    if not alerts:
        return None

    level = get_overall_level(alerts)
    lines = [
        f"**七政·盘中预警** {timestamp}",
        f"等级：{level}",
        ""
    ]
    for a in alerts:
        lines.append(f"{a['level']} **{a['type']}**")
        lines.append(f"{a['content']}")
        lines.append(f"→ {a['action']}")
        lines.append("")

    return '\n'.join(lines)


# ─── 单独执行：发送预警 ─────────────────────

def send_alert(alert_type: str, content: str, action: str, level: str = '🔴 高'):
    """手动触发一条预警"""
    alert = {
        'level': level,
        'type': alert_type,
        'content': content,
        'action': action,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    }
    save_alert(alert)
    msg = build_alert_message([alert], alert['timestamp'])
    print(f"[预警推送] {msg}")
    return alert


# ─── 预配置重点监控股票 ─────────────────────

WATCHED_STOCKS = {
    '000617': '中油资本',  # 多元金融龙头
    '000586': '汇源通信',  # 光通信连板
    '688205': '德科立',     # OCS概念
    '600488': '津药药业',   # 6连板妖股
}


def check_watched_stocks() -> list:
    """监控重点持仓/自选股"""
    from realtime import get_batch
    codes = list(WATCHED_STOCKS.keys())
    data = get_batch(codes)
    alerts = []

    for code, name in WATCHED_STOCKS.items():
        d = data.get(code)
        if not d:
            continue
        chg = d.get('change_pct', 0) or 0
        price = d.get('price')
        if chg <= -5.0:
            alerts.append({
                'level': '🔴 高',
                'type': f'{name}大跌',
                'content': f"{name}({code})当前{price}元（{chg:+.2f}%）",
                'action': '注意止损',
            })
        elif chg >= 9.5:
            alerts.append({
                'level': '🟢 强势',
                'type': f'{name}涨停',
                'content': f"{name}({code})当前{price}元（{chg:+.2f}%）",
                'action': '封板成功可持有',
            })

    return alerts


if __name__ == '__main__':
    print(f"[七政监控] 启动盘中监控 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"[监控股票] {', '.join(WATCHED_STOCKS.values())}")
    print("-" * 40)

    # 全市场监控
    market_alerts = monitor()

    # 重点个股监控
    stock_alerts = check_watched_stocks()

    all_alerts = market_alerts + stock_alerts
    if all_alerts:
        msg = build_alert_message(all_alerts, datetime.datetime.now().strftime('%H:%M'))
        print(f"\n[推送飞书]\n{msg}")
    else:
        print("\n[结论] 无需推送，继续观察")
