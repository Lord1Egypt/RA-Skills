#!/usr/bin/env python3
"""
v20.45 v3: 修 alert log 路径
"""
import time, re, requests, json, os, sys
from datetime import datetime

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

METRICS_URL = 'http://<server-ip>:5000/metrics'
ALERT_LOG = '/home/ubuntu/star-search/logs/alerts.log'  # 修: ubuntu 可写
MONITOR_LOG = '/home/ubuntu/star-search/logs/monitor.log'
STATE_FILE = '/tmp/monitor-state.json'
CHECK_INTERVAL = 60

state = {
    'last_requests_total': 0,
    'consecutive_failures': 0,
    'alerts_sent': {},
}
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE) as f:
            state.update(json.load(f))
    except Exception:
        pass

def parse_metrics(text):
    metrics = {}
    for line in text.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'^([\w_]+)(?:\{[^}]*\})?\s+([\d\.\-eE\+]+)$', line)
        if m:
            metrics[m.group(1)] = float(m.group(2))
    return metrics

def log_msg(level, msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] [{level}] {msg}'
    print(line, flush=True)
    try:
        with open(MONITOR_LOG, 'a') as f:
            f.write(line + '\n')
    except Exception:
        pass

def log_alert(level, msg):
    log_msg(level, msg)
    if level == 'ALERT':
        try:
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(ALERT_LOG, 'a') as f:
                f.write(f'[{ts}] {msg}\n')
        except Exception as e:
            log_msg('ERROR', f'写 alert log 失败: {e}')

def check():
    try:
        r = requests.get(METRICS_URL, timeout=5)
        if r.status_code != 200:
            state['consecutive_failures'] += 1
            if state['consecutive_failures'] >= 3:
                log_alert('ALERT', f'metrics 端点返 {r.status_code} (连续 {state["consecutive_failures"]} 次)')
            return
        state['consecutive_failures'] = 0
        m = parse_metrics(r.text)

        # 1) 答案错误率
        answer_total = m.get('star_search_answer_total', 0)
        answer_errors = m.get('star_search_answer_errors_total', 0)
        if answer_total > 5:
            err_rate = answer_errors / answer_total * 100
            if err_rate > 20:
                key = f'err_{int(time.time()//300)}'
                if key not in state['alerts_sent']:
                    state['alerts_sent'][key] = True
                    log_alert('ALERT', f'答案错误率 {err_rate:.1f}% > 20%  errors={answer_errors}/{answer_total}')

        # 2) 缓存命中率
        cache_rate = m.get('star_search_cache_hit_rate', 0)
        search_total = m.get('star_search_search_total', 0)
        if search_total > 20 and cache_rate < 10:
            key = f'cache_{int(time.time()//1800)}'
            if key not in state['alerts_sent']:
                state['alerts_sent'][key] = True
                log_alert('ALERT', f'缓存命中率 {cache_rate:.1f}% < 10%')

        # 3) 健康摘要 5 min
        if int(time.time()) % 300 < 70:
            uptime = m.get('star_search_uptime_seconds', 0)
            reqs = m.get('star_search_requests_total', 0)
            log_msg('INFO', f'健康摘要: uptime={uptime:.0f}s reqs={reqs} cache={cache_rate:.1f}% errs={answer_errors}/{answer_total}')

    except Exception as e:
        state['consecutive_failures'] += 1
        if state['consecutive_failures'] >= 3:
            log_alert('ALERT', f'metrics 抓取失败: {e} (连续 {state["consecutive_failures"]} 次)')
        return

    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except Exception:
        pass

if __name__ == '__main__':
    log_msg('INFO', 'star_search_monitor v3 启动 (alert log: ' + ALERT_LOG + ')')
    while True:
        check()
        time.sleep(CHECK_INTERVAL)
