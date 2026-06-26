#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票量化监控系统 v6.0（通用版）
读取 config.yaml 获取股票池配置，无需硬编码
"""

import os
import sys
import time

# 确保时区正确（launchd 环境下不会继承用户时区设置）
try:
    from zoneinfo import ZoneInfo
    SH_TZ = ZoneInfo('Asia/Shanghai')
except ImportError:
    SH_TZ = None  # Python < 3.9， fallback 到系统时间

import yaml
import warnings
import requests
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta

def now_sh():
    """返回上海时区的当前时间（兼容 launchd 缺失时区环境）"""
    if 'SH_TZ' in globals() and SH_TZ is not None:
        return datetime.now(SH_TZ)
    return datetime.now()  # fallback：使用系统本地时间（无时区信息）

warnings.filterwarnings('ignore')

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
MARKER_FILE = os.path.join(SKILL_DIR, '.installed')


# ============================================================
# 自动安装（首次运行时自动触发）
# ============================================================

def check_and_install():
    """检查依赖并在必要时自动安装，无须用户手动操作"""
    if os.path.exists(MARKER_FILE):
        return True  # 已安装

    print("[INFO] 首次运行检查...", file=sys.stderr)

    # 1. 确保 pyyaml 可用（核心依赖）
    try:
        import yaml
    except ImportError:
        print("[INFO] 正在安装 pyyaml...", file=sys.stderr)
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'pyyaml', '--quiet'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print("[INFO] pyyaml 安装成功", file=sys.stderr)
        else:
            print(f"[WARN] pyyaml 安装失败: {result.stderr[:200]}", file=sys.stderr)

    # 2. 注册 launchd（macOS）
    if sys.platform == 'darwin':
        plist_path = os.path.expanduser('~/Library/LaunchAgents/com.openclaw.stock-monitor.plist')
        os.makedirs(os.path.dirname(plist_path), exist_ok=True)
        os.makedirs(os.path.join(SKILL_DIR, 'logs'), exist_ok=True)

        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.stock-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{SKILL_DIR}/push_stock_report.py</string>
        <string>morning</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>15</integer></dict>
        <dict><key>Hour</key><integer>10</integer><key>Minute</key><integer>30</integer></dict>
        <dict><key>Hour</key><integer>13</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Hour</key><integer>14</integer><key>Minute</key><integer>50</integer></dict>
    </array>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>{SKILL_DIR}/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>{SKILL_DIR}/logs/launchd.err</string>
</dict>
</plist>
"""
        try:
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            # 先尝试 load，如果失败（权限问题），给出明确指引
            load_result = subprocess.run(
                ['launchctl', 'load', plist_path],
                capture_output=True, text=True, timeout=10
            )
            if load_result.returncode != 0:
                # 检查是否是权限问题
                if 'Permission denied' in load_result.stderr or 'not loaded' in load_result.stderr:
                    print("[WARN] launchd 注册需要授权，请运行以下命令手动授权：", file=sys.stderr)
                    print(f"  launchctl load {plist_path}", file=sys.stderr)
                    print("[INFO] 或者手动在「系统设置 → 隐私与安全性 → 自动化」中授权", file=sys.stderr)
                else:
                    print(f"[WARN] launchd 注册失败: {load_result.stderr[:200]}", file=sys.stderr)
            else:
                print("[INFO] 定时任务已注册 (launchd)", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] launchd 注册异常: {e}", file=sys.stderr)

    # 3. 写 marker
    with open(MARKER_FILE, 'w') as f:
        f.write(now_sh().isoformat())
    print("[INFO] 安装完成", file=sys.stderr)
    return True


# ============================================================
# 配置加载
# ============================================================

def load_config():
    """加载配置文件（优先读 config.local.yaml，其次 config.yaml）"""
    local_path = os.path.join(SKILL_DIR, 'config.local.yaml')
    config_path = os.path.join(SKILL_DIR, 'config.yaml')

    # 优先使用本地配置（个人使用，不发布）
    if os.path.exists(local_path):
        config_path = local_path
    elif not os.path.exists(config_path):
        # 首次运行生成空白模板（不包含任何凭证，不会推送消息）
        default_config = """# 股票监控配置
# 请编辑此文件添加您的股票和飞书凭证
stocks: []

push:
  channel: "console"      # 暂时禁用推送，待配置凭证后改为 feishu
  times:
    - "09:15"
    - "10:00"
    - "13:00"
    - "14:50"

  feishu:
    app_id: ""
    app_secret: ""
    chat_id: ""

advanced:
  history_days: 60
"""
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(default_config)
        print(f"[INFO] 首次运行，配置文件已创建: {config_path}", file=sys.stderr)
        print("[INFO] 请编辑配置文件添加股票和飞书凭证后重新运行", file=sys.stderr)

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# ============================================================
# 数据采集层
# ============================================================

SINA_HQ_HEADERS = {'Referer': 'https://finance.sina.com.cn'}


def get_realtime_sina(codes_markets):
    """新浪HQ接口获取实时行情"""
    if not codes_markets:
        return {}
    symbols = ','.join([f'{m}{c}' for c, m in codes_markets])
    try:
        url = f'https://hq.sinajs.cn/list={symbols}'
        r = requests.get(url, headers=SINA_HQ_HEADERS, timeout=10)
        r.encoding = 'gbk'
        # 检查是否返回403
        if r.status_code != 200:
            print(f"[WARN] Sina接口返回状态码 {r.status_code}", file=sys.stderr)
            return {}
        lines = r.text.strip().split('\n')
        result = {}
        for line in lines:
            match = line.split('=')
            if len(match) < 2:
                continue
            key = match[0].split('_')[-1]
            vals = match[1].replace('"', '').split(',')
            if len(vals) < 10:
                continue
            try:
                result[key] = {
                    'name': vals[0],
                    'open': float(vals[1]),
                    'prev_close': float(vals[2]),
                    'current': float(vals[3]),
                    'high': float(vals[4]),
                    'low': float(vals[5]),
                    'volume': float(vals[8]),
                    'amount': float(vals[9]),
                    'pct': 0.0
                }
                pc = result[key]['prev_close']
                cur = result[key]['current']
                result[key]['pct'] = round((cur - pc) / pc * 100, 2) if pc else 0
            except (ValueError, IndexError):
                continue
        return result
    except Exception as e:
        print(f"[WARN] get_realtime_sina failed: {e}", file=sys.stderr)
        return {}


def get_realtime_tencent(codes_markets):
    """腾讯行情接口获取实时行情（新浪备用）"""
    if not codes_markets:
        return {}
    symbols = ','.join([f'{m}{c}' for c, m in codes_markets])
    try:
        url = f'https://qt.gtimg.cn/q={symbols}'
        r = requests.get(url, timeout=10)
        r.encoding = 'gbk'
        text = r.text
        result = {}
        for line in text.strip().split('\n'):
            if '~' not in line:
                continue
            # v_sz000001="51~平安银行~000001~10.50~10.45~..."
            parts = line.split('~')
            if len(parts) < 37:
                continue
            try:
                # 从变量名提取市场前缀: v_sz000001 -> sz000001
                var_match = line.split('=')[0] if '=' in line else ''
                key = var_match.replace('v_', '').strip()  # e.g. "sz000001"
                market_code = parts[0]  # 51=深圳, 1=上海
                name = parts[1]
                code = parts[2]
                current = float(parts[3])
                prev_close = float(parts[4])
                open_price = float(parts[5])
                high = float(parts[33])  # 当日高点
                low = float(parts[34])    # 当日低点
                
                result[key] = {
                    'name': name,
                    'open': open_price,
                    'prev_close': prev_close,
                    'current': current,
                    'high': high,
                    'low': low,
                    'volume': float(parts[6]) if parts[6] else 0,
                    'amount': float(parts[37]) if parts[37] else 0,
                    'pct': 0.0
                }
                pc = prev_close
                result[key]['pct'] = round((current - pc) / pc * 100, 2) if pc else 0
            except (ValueError, IndexError):
                continue
        return result
    except Exception as e:
        print(f"[WARN] get_realtime_tencent failed: {e}", file=sys.stderr)
        return {}


def get_realtime_fund_tiantian(fund_code):
    """天天基金网接口获取实时估算净值（基金监控）"""
    try:
        url = f'http://fundgz.1234567.com.cn/js/{fund_code}.js?rt={int(time.time())}'
        r = requests.get(url, timeout=8)
        text = r.text.strip()
        if not text or text.startswith('jsonpgz({'):
            # 解析 jsonpgz({...}) 格式
            json_str = text.replace('jsonpgz(', '').rstrip(');')
            data = json.loads(json_str)
            return {
                'fund_code': data.get('fundcode', ''),
                'name': data.get('name', ''),
                'nav_date': data.get('jzrq', ''),        # 净值日期
                'nav': float(data.get('dwjz', 0)),       # 单位净值
                'estimated_nav': float(data.get('gsz', 0)),  # 估算净值
                'estimated_change': float(data.get('gszzl', 0)),  # 估算增长率%
                'estimated_time': data.get('gztime', '')
            }
        return None
    except Exception as e:
        print(f"[WARN] get_realtime_fund_tiantian {fund_code} failed: {e}", file=sys.stderr)
        return None


def get_gold_spot_price():
    """获取国际黄金现货价格（Yahoo Finance）"""
    try:
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/GC%3DF'
        r = requests.get(url, timeout=6)
        r.raise_for_status()
        data = r.json()
        result = data.get('chart', {}).get('result', [])
        if not result:
            return None
        quotes = result[0].get('indicators', {}).get('quote', [{}])[0]
        closes = quotes.get('close', [])
        if len(closes) < 2:
            return None
        current = float(closes[-1])
        prev = float(closes[-2])
        pct = round((current - prev) / prev * 100, 2)
        return {'price': current, 'pct': pct}
    except Exception as e:
        print(f"[WARN] get_gold_spot_price failed: {e}", file=sys.stderr)
        return None


def get_fund_hist_eastmoney(fund_code, days=60):
    """东方财富获取基金历史净值"""
    try:
        url = f'https://api.fund.eastmoney.com/f10/lsjz'
        params = {
            'callback': 'jQuery',
            'fundCode': fund_code,
            'pageIndex': 1,
            'pageSize': days,
            'startDate': '',
            'endDate': ''
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        text = r.text
        # jQuery({...})
        json_str = text[7:-1] if text.startswith('jQuery') else text
        data = json.loads(json_str)
        records = data.get('Data', {}).get('LSJZList', [])
        if not records:
            return None
        result = []
        for rec in reversed(records[-days:]):
            result.append({
                'date': rec.get('FSRQ', ''),
                'nav': float(rec.get('DWJZ', 0)),
                'accumulated_nav': float(rec.get('LJJZ', 0))
            })
        return result
    except Exception as e:
        print(f"[WARN] get_fund_hist_eastmoney {fund_code} failed: {e}", file=sys.stderr)
        return None


def get_market_index_sina():
    """获取大盘指数"""
    try:
        url = 'https://hq.sinajs.cn/list=sh000001,sz399001,sz399006,sh000688'
        r = requests.get(url, headers=SINA_HQ_HEADERS, timeout=10)
        r.encoding = 'gb18030'
        text = r.text
        result = {}
        mappings = {
            'sh000001': '上证指数',
            'sz399001': '深证成指',
            'sz399006': '创业板指',
            'sh000688': '科创50'
        }
        for mcode, name in mappings.items():
            try:
                key = f'hq_str_{mcode}='
                idx = text.find(key)
                if idx == -1:
                    continue
                start = idx + len(key) + 1  # skip ="
                end = text.find('"', start)
                if end == -1:
                    continue
                vals = text[start:end].split(',')
                if len(vals) < 6:
                    continue
                current = float(vals[3])
                prev_close = float(vals[2])
                pct = round((current - prev_close) / prev_close * 100, 2) if prev_close else 0
                result[name] = {'price': current, 'pct': pct}
            except Exception:
                continue
        return result
    except Exception as e:
        print(f"[WARN] get_market_index_sina failed: {e}", file=sys.stderr)
        return {}


def get_hist_from_sina(code, market, days=60):
    """获取历史K线数据（新浪快接口，并发安全）"""
    import pandas as pd
    symbol = f'{market}{code}'
    try:
        # 新浪日K接口，scale=240代表240分钟(=日K)，ma为均线周期
        url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'
        params = {'symbol': symbol, 'scale': '240', 'ma': 'no', 'datalen': days}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        df = pd.DataFrame(data)
        df = df.rename(columns={'day': 'date', 'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close', 'volume': 'volume'})
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        return df
    except Exception as e:
        print(f"[WARN] get_hist_from_sina {symbol} failed: {e}", file=sys.stderr)
        return None


def get_us_index_sina():
    """获取隔夜美股（Yahoo Finance极速版）"""
    import json

    def fetch_yahoo(symbol, name):
        try:
            url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
            r = requests.get(url, timeout=6)
            r.raise_for_status()
            data = r.json()
            result = data.get('chart', {}).get('result', [])
            if not result:
                return name, None
            meta = result[0]
            quotes = meta.get('indicators', {}).get('quote', [{}])[0]
            closes = quotes.get('close', [])
            if len(closes) < 2:
                return name, None
            last = float(closes[-1])
            prev = float(closes[-2])
            pct = round((last - prev) / prev * 100, 2)
            return name, pct
        except Exception:
            return name, None

    indices = [('^DJI', '道琼斯'), ('^IXIC', '纳斯达克'), ('^GSPC', '标普500')]
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(lambda x: fetch_yahoo(*x), indices))

    return {name: pct for name, pct in results if pct is not None}


def get_sector_tencent():
    """腾讯行情获取行业板块涨跌"""
    try:
        import akshare as ak
        df = ak.stock_sector_spot()
        if df is None or df.empty:
            return {}
        if '板块' not in df.columns or '涨跌幅' not in df.columns:
            return {}
        df = df.sort_values('涨跌幅', ascending=False)
        top = df.head(5)
        bottom = df.tail(5)
        return {
            'top': [(str(row['板块']), round(float(row['涨跌幅']), 2)) for _, row in top.iterrows()],
            'bottom': [(str(row['板块']), round(float(row['涨跌幅']), 2)) for _, row in bottom.iterrows()]
        }
    except Exception as e:
        print(f"[WARN] get_sector_tencent failed: {e}", file=sys.stderr)
        return {}


def get_north_money():
    """北向资金（东方财富直接API版）"""
    try:
        url = 'https://push2.eastmoney.com/api/qt/kamt.rtmin/get'
        params = {'fields': 'f12,f13,f14,f62', '_': '1700000000000'}
        r = requests.get(url, params=params, timeout=6)
        r.raise_for_status()
        data = r.json()
        # 北向资金净买入额在东方财富没找到简洁接口，用腾讯行情代替
    except Exception:
        pass
    # 降级：用腾讯北向数据
    try:
        url2 = 'https://proxy.finance.qq.com/ifzqgtimg/appstock/app/rank/getRankByType'
        params2 = {'type': 'hgt', 'page': 0, 'pageSize': 5}
        r2 = requests.get(url2, timeout=6)
        r2.raise_for_status()
    except Exception:
        pass
    return {}


def get_stock_news(code, count=3):
    """获取个股新闻（新浪快接口）"""
    try:
        url = 'https://feed.mix.sina.com.cn/api/roll/get'
        params = {'pageid': 153, 'lid': 2516, 'k': code, 'num': count, 'page': 1}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        json_data = r.json()
        items = json_data.get('result', {}).get('data', [])
        news = []
        for item in items[:count]:
            title = item.get('title', '')
            ctime_str = item.get('ctime', '')
            # 转换 Unix 时间戳为可读日期
            try:
                ts = int(str(ctime_str)[:10])
                date_str = datetime.fromtimestamp(ts).strftime('%m-%d %H:%M')
            except Exception:
                date_str = ctime_str[:8]
            if title:
                news.append(f"• {date_str} {title[:28]}")
        return news
    except Exception as e:
        print(f"[WARN] get_stock_news {code} failed: {e}", file=sys.stderr)
        return []


# ============================================================
# 技术指标层
# ============================================================

def calc_ma(close, periods=[5, 10, 20, 60]):
    return {f'ma{p}': round(float(close.tail(p).mean()), 2) for p in periods}


def calc_macd(close, fast=12, slow=26, signal=9):
    s = close.astype(float)
    ema_fast = s.ewm(span=fast, adjust=False).mean()
    ema_slow = s.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd_hist = (dif - dea) * 2
    dif_v = round(float(dif.iloc[-1]), 3)
    dea_v = round(float(dea.iloc[-1]), 3)
    hist_v = round(float(macd_hist.iloc[-1]), 3)
    cross = 'none'
    if len(dif) >= 2:
        cross = 'gold' if float(dif.iloc[-2]) < float(dea.iloc[-2]) and dif_v >= dea_v else \
                'death' if float(dif.iloc[-2]) > float(dea.iloc[-2]) and dif_v <= dea_v else 'none'
    return {'dif': dif_v, 'dea': dea_v, 'hist': hist_v, 'cross': cross}


def calc_rsi(close, period=14):
    try:
        s = close.astype(float).diff()
        gain = s.where(s > 0, 0).rolling(window=period).mean()
        loss = (-s.where(s < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        if rs.iloc[-1] == 0 or (rs == float('inf')).any():
            return 50.0  # 无涨跌时返回中性值
        return round(float((100 - 100 / (1 + rs)).iloc[-1]), 1)
    except Exception:
        return 50.0


def calc_bollinger(close, period=20):
    s = close.astype(float)
    mid = s.rolling(window=period).mean()
    std = s.rolling(window=period).std()
    upper, lower = mid + 2*std, mid - 2*std
    cur = float(s.iloc[-1])
    pos = 'lower' if cur <= float(lower.iloc[-1]) else 'upper' if cur >= float(upper.iloc[-1]) else 'middle'
    return {
        'upper': round(float(upper.iloc[-1]), 2),
        'mid': round(float(mid.iloc[-1]), 2),
        'lower': round(float(lower.iloc[-1]), 2),
        'position': pos
    }


def calc_vol_ratio(volumes, period=5):
    s = volumes.astype(float)
    avg = float(s.tail(period+1).iloc[:-1].mean())
    today = float(s.iloc[-1])
    return round(today/avg, 2) if avg > 0 else 1.0


def calc_support_resistance(highs, lows, period=20):
    h = highs.astype(float)
    l = lows.astype(float)
    return {
        'resistance': round(float(h.tail(period).max()), 2),
        'support': round(float(l.tail(period).min()), 2)
    }


def score_stock(ma, macd, rsi, bollinger, vol_ratio, pct_change):
    score = 0
    if ma['ma5'] > ma['ma10'] > ma['ma20'] > ma['ma60']: score += 2
    elif ma['ma5'] < ma['ma10'] < ma['ma20'] < ma['ma60']: score -= 2
    elif ma['ma5'] > ma['ma10']: score += 1
    else: score -= 1

    if macd['cross'] == 'gold': score += 2
    elif macd['cross'] == 'death': score -= 2
    elif macd['hist'] > 0: score += 1
    else: score -= 1

    if rsi < 35: score += 2
    elif rsi > 65: score -= 2
    elif rsi < 45: score += 1
    elif rsi > 55: score += 1

    if bollinger['position'] == 'lower': score += 2
    elif bollinger['position'] == 'upper': score -= 2

    if pct_change > 0 and vol_ratio > 1.3: score += 1
    elif pct_change < 0 and vol_ratio < 0.7: score -= 1

    return max(-10, min(10, score))


def get_signal_info(score):
    if score >= 7: return '🟢 强烈买入', score
    elif score >= 4: return '🟢 买入', score
    elif score >= -3: return '🟡 持有', score
    elif score >= -6: return '🔴 卖出', score
    else: return '🔴 强烈卖出', score


# ============================================================
# 报告生成层
# ============================================================

def generate_suggestion(score, macd, rsi, bollinger, position, current_price):
    """生成具体可操作建议（每条结论必须有价格依据）"""
    parts = []
    lower = bollinger['lower']
    upper = bollinger['upper']
    mid = bollinger['mid']

    # ---- 持仓相关 ----
    has_position = position and current_price > 0 and position.get('cost', 0) > 0

    if has_position:
        cost = position['cost']
        qty = position['quantity']
        profit = (current_price - cost) * qty
        profit_pct = (current_price - cost) / cost * 100
        is_profit = profit >= 0

        if is_profit:
            # 赚钱时：给止盈价位
            upside = (upper - current_price) / current_price * 100
            parts.append(f"持仓盈利+{profit_pct:.0f}%，向上还有{upside:.0f}%空间至{upper}")
            if current_price >= upper:
                parts.append(f"价格已触布林上轨{upper}，建议减仓1/3，落袋")
            else:
                parts.append(f"若反弹至中轨{mid:.2f}，可减半仓")
        else:
            # 亏钱时：给止损价位
            if abs(profit_pct) > 20:
                parts.append(f"深套{abs(profit_pct):.0f}%，若跌破{lower}元清仓止损")
                parts.append("大盘弱势，不加仓")
            elif abs(profit_pct) > 10:
                parts.append(f"亏损{abs(profit_pct):.0f}%，若跌破{lower}考虑止损")
            else:
                parts.append(f"微亏{abs(profit_pct):.0f}%，持有观察，止损{lower}")

    # ---- 无持仓时的纯技术建议 ----
    if not has_position:
        if rsi < 35:
            parts.append(f"RSI={rsi}超卖，激进者可轻仓试探，止损{lower}")
        elif rsi > 65:
            parts.append(f"RSI={rsi}偏高，谨慎追高，观望为宜")
        elif current_price <= lower:
            parts.append(f"价格跌破布林下轨{lower}，若无快速收复，观望")
        elif current_price >= upper:
            parts.append(f"价格突破布林上轨{upper}，有回调压力，慎追")

    # ---- MACD ----
    if macd['cross'] == 'gold':
        parts.append("MACD刚金叉，短线偏多")
    elif macd['cross'] == 'death':
        parts.append("MACD刚死叉，短线偏空")

    # 返回前两条（不贪多）
    return '\n'.join([f"   → {p}" for p in parts[:2]])


def analyze_stock(stock, realtime, hist):
    """生成单个股票分析（精简版）"""
    code = stock['code']
    name = stock['name']
    emoji = stock.get('emoji', '📊')
    position = stock.get('position')

    if not realtime:
        return f"{emoji} {name}（{code}）- 实时数据获取失败\n"

    current = realtime.get('current', 0)
    pct = realtime.get('pct', 0)
    pct_str = f"+{pct:.2f}%" if pct >= 0 else f"{pct:.2f}%"

    lines = []
    lines.append(f"{emoji} {name}（{code}）")
    lines.append(f"   现价: {current:.2f}  今日: {pct_str}")

    if hist is not None and len(hist) >= 20:
        # ===== 有历史K线，完整分析 =====
        close = hist['close']
        volume = hist['volume']

        ma = calc_ma(close)
        macd = calc_macd(close)
        rsi = calc_rsi(close)
        bollinger = calc_bollinger(close)
        vol_ratio = calc_vol_ratio(volume)

        score = score_stock(ma, macd, rsi, bollinger, vol_ratio, pct)
        signal_emoji, score_val = get_signal_info(score)

        lines.append(f"   信号: {signal_emoji} ({score_val:+.0f}分)  RSI:{rsi}  量比:{vol_ratio}")
        lines.append(f"   布林: {bollinger['lower']}~{bollinger['upper']}（中轨{bollinger['mid']:.2f}）")

        # 持仓盈亏
        has_pos = position and current > 0 and position.get('cost', 0) > 0
        if has_pos:
            cost = position['cost']
            qty = position['quantity']
            profit = (current - cost) * qty
            profit_pct = (current - cost) / cost * 100
            profit_str = f"+{profit:.0f}元" if profit >= 0 else f"{profit:.0f}元"
            pct_str2 = f"+{profit_pct:.1f}%" if profit_pct >= 0 else f"{profit_pct:.1f}%"
            lines.append(f"   💰 持仓: 成本{cost:.2f} | {profit_str}({pct_str2})")

        # 可操作建议
        suggestion = generate_suggestion(score, macd, rsi, bollinger, position, current)
        if suggestion:
            lines.append(suggestion)

    else:
        # ===== 无历史K线，简化版 =====
        if position and current > 0 and position.get('cost', 0) > 0:
            cost = position['cost']
            qty = position['quantity']
            profit = (current - cost) * qty
            profit_pct = (current - cost) / cost * 100
            profit_str = f"+{profit:.0f}元" if profit >= 0 else f"{profit:.0f}元"
            pct_str2 = f"+{profit_pct:.1f}%" if profit_pct >= 0 else f"{profit_pct:.1f}%"
            lines.append(f"   💰 持仓: 成本{cost:.2f} | {profit_str}({pct_str2})")
        lines.append(f"   ⚠️ 历史K线获取超时，仅展示实时数据")

    return '\n'.join(lines) + '\n'


def analyze_fund(fund, fund_data, gold):
    """生成基金分析（不同于股票，基金主要看净值和黄金走势）"""
    code = fund['code']
    name = fund.get('name', fund_data.get('name', code))
    emoji = fund.get('emoji', '🥇')
    position = fund.get('position')

    lines = []
    lines.append(f"{emoji} {name}（{code}）")

    # 估算净值数据
    estimated_nav = fund_data.get('estimated_nav', 0)
    estimated_change = fund_data.get('estimated_change', 0)
    nav_date = fund_data.get('nav_date', '')
    est_time = fund_data.get('estimated_time', '')

    if estimated_nav > 0:
        change_str = f"+{estimated_change:.2f}%" if estimated_change >= 0 else f"{estimated_change:.2f}%"
        lines.append(f"   估算净值: {estimated_nav:.4f}  今日: {change_str}")
        if est_time:
            lines.append(f"   更新时间: {est_time}")
    else:
        # 盘中未更新，显示昨日净值
        nav = fund_data.get('nav', 0)
        if nav > 0:
            lines.append(f"   单位净值: {nav:.4f}（昨日）")

    # 持仓盈亏（如有）
    has_pos = position and estimated_nav > 0 and position.get('cost', 0) > 0
    if has_pos:
        cost = position['cost']
        qty = position['quantity']
        profit = (estimated_nav - cost) * qty
        profit_pct = (estimated_nav - cost) / cost * 100
        profit_str = f"+{profit:.0f}元" if profit >= 0 else f"{profit:.0f}元"
        pct_str = f"+{profit_pct:.1f}%" if profit_pct >= 0 else f"{profit_pct:.1f}%"
        lines.append(f"   💰 持仓: 成本{cost:.4f} | {profit_str}({pct_str})")

    # 黄金走势参考（如有）
    if gold:
        gold_pct = gold.get('pct', 0)
        fund_pct = estimated_change
        diff = fund_pct - gold_pct
        diff_str = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
        lines.append(f"   📊 黄金参考: {gold_pct:+.2f}% | 基金跑赢: {diff_str}")

    # 简单建议
    if estimated_change < -2:
        lines.append(f"   → 黄金大跌，注意止损")
    elif estimated_change > 2:
        lines.append(f"   → 黄金大涨，持有的可适度减仓")
    else:
        lines.append(f"   → 变动正常，持有观望")

    return '\n'.join(lines) + '\n'


def generate_report(config, mode='auto'):
    """生成完整分析报告（并发优化版）"""
    today = now_sh().strftime("%Y-%m-%d")
    hour = now_sh().hour
    if hour < 10: period = "开盘前"
    elif hour < 12: period = "早盘"
    elif hour < 14: period = "午后"
    else: period = "尾盘"
    if mode != 'auto':
        period = {'morning': '开盘前', 'noon': '早盘', 'afternoon': '午后', 'evening': '尾盘'}.get(mode, period)

    stocks_cfg = config.get('stocks', [])
    if not stocks_cfg:
        return "⚠️ 股票池为空，请先在 config.yaml 中添加股票。"

    # 分离基金和股票
    funds_cfg = [s for s in stocks_cfg if s.get('type') == 'fund']
    stocks_only = [s for s in stocks_cfg if s.get('type') != 'fund']

    lines = []
    lines.append(f"📊 参考 - {period} {today}")
    lines.append("━" * 20)

    # 股票-only 的 codes_markets（排除基金）
    codes_markets = [(s['code'], s['market']) for s in stocks_only]
    history_days = config.get('advanced', {}).get('history_days', 60)

    # ========== 第一波：并发获取所有共享数据 ==========
    with ThreadPoolExecutor(max_workers=6) as executor:
        f_realtime = executor.submit(get_realtime_sina, codes_markets)
        f_market   = executor.submit(get_market_index_sina)
        f_sectors  = executor.submit(get_sector_tencent)
        f_us       = executor.submit(get_us_index_sina)
        f_north    = executor.submit(get_north_money)

        rt_raw  = f_realtime.result()
        market  = f_market.result()
        sectors = f_sectors.result()
        us_index = f_us.result()
        north   = f_north.result()

    # 处理实时数据
    realtime = {}
    for key, val in rt_raw.items():
        code = key.replace('sz', '').replace('sh', '')
        realtime[code] = val

    # 数据质量检查：所有股票价格都是0说明数据异常，尝试腾讯行情备用接口
    valid_prices = [v['current'] for v in realtime.values() if v.get('current', 0) > 0]
    if len(valid_prices) == 0 and len(realtime) > 0:
        print(f"[WARN] Sina接口返回空，尝试腾讯行情备用...", file=sys.stderr)
        rt_tencent = get_realtime_tencent(codes_markets)
        valid_prices = [v['current'] for v in rt_tencent.values() if v.get('current', 0) > 0]
        if len(valid_prices) > 0:
            for key, val in rt_tencent.items():
                code = key.replace('sz', '').replace('sh', '')
                realtime[code] = val
            print(f"[INFO] 腾讯行情备用成功，获取 {len(valid_prices)} 只股票数据", file=sys.stderr)
        else:
            warning_msg = (
                f"⚠️ 数据异常提醒 - {today} {now_sh().strftime('%H:%M:%S')}\n"
                f"原因：实时行情接口返回价格为空（股票可能停牌或接口暂时不可用）\n"
                f"下次定时推送将自动恢复"
            )
            print(f"[WARN] {warning_msg}", file=sys.stderr)
            return warning_msg

    # 如果新浪接口返回异常数据（价格为0或负数），强制使用腾讯接口
    problematic_codes = [k for k, v in rt_raw.items() if v.get('current', 0) <= 0]
    if problematic_codes:
        print(f"[WARN] Sina接口对 {len(problematic_codes)} 只股票返回异常数据，强制使用腾讯接口...", file=sys.stderr)
        rt_tencent = get_realtime_tencent(codes_markets)
        for key, val in rt_tencent.items():
            code = key.replace('sz', '').replace('sh', '')
            realtime[code] = val
        print(f"[INFO] 腾讯接口数据已更新", file=sys.stderr)
    # 如果新浪接口返回空或403，强制使用腾讯接口
    elif not rt_raw or len(rt_raw) == 0:
        print(f"[WARN] Sina接口返回空，强制使用腾讯接口...", file=sys.stderr)
        rt_tencent = get_realtime_tencent(codes_markets)
        for key, val in rt_tencent.items():
            code = key.replace('sz', '').replace('sh', '')
            realtime[code] = val
        print(f"[INFO] 腾讯接口数据已更新", file=sys.stderr)

    # 输出大盘/美股/板块/北向
    if market:
        mkt_str = ' | '.join([f"{k} {v['price']:.0f}({v['pct']:+.1f}%)" for k, v in market.items()])
        lines.append(f"📊 A股大盘: {mkt_str}")

    if us_index:
        us_str = ' | '.join([f"{k} {v:+.1f}%" for k, v in us_index.items()])
        lines.append(f"🌏 昨夜美股: {us_str}")

    if sectors:
        top3 = sectors.get('top', [])[:3]
        if top3:
            lines.append(f"📈 强势板块: " + ' | '.join([f"{n}({p:+.1f}%)" for n, p in top3]))
        bot3 = sectors.get('bottom', [])[:3]
        if bot3:
            lines.append(f"📉 弱势板块: " + ' | '.join([f"{n}({p:+.1f}%)" for n, p in bot3]))

    if north:
        total = north.get('total', 0)
        direction = "净买入" if total > 0 else "净卖出"
        lines.append(f"📊 北向资金: {direction} {abs(total)}亿")

    if market or us_index or sectors or north:
        lines.append("━" * 20)

    # ========== 第二波：并发获取每只股票的历史+新闻 ==========
    def fetch_one_stock(stock):
        code = stock['code']
        market_code = stock['market']
        rt = realtime.get(code, {})
        hist = get_hist_from_sina(code, market_code, days=history_days)
        return analyze_stock(stock, rt, hist)

    # 只有股票才获取历史K线，基金不需要
    if stocks_only:
        with ThreadPoolExecutor(max_workers=len(stocks_only)) as executor:
            stock_results = list(executor.map(fetch_one_stock, stocks_only))
        lines.extend(stock_results)

    # ========== 第三波：基金数据（独立接口） ==========
    if funds_cfg:
        # 获取黄金价格（基金对标）
        gold = get_gold_spot_price()
        if gold:
            gold_str = f"${gold['price']:.1f}({gold['pct']:+.1f}%)"
            lines.append(f"🥇 国际黄金: {gold_str}")

        # 并发获取所有基金实时数据
        def fetch_one_fund(fund):
            code = fund['code']
            fund_data = get_realtime_fund_tiantian(code)
            emoji = fund.get('emoji', '🥇')
            name = fund.get('name', code)
            if not fund_data:
                return f"{emoji} {name}（{code}）- 数据获取失败\n"
            return analyze_fund(fund, fund_data, gold)
        with ThreadPoolExecutor(max_workers=len(funds_cfg)) as executor:
            fund_results = list(executor.map(fetch_one_fund, funds_cfg))
        lines.append("━" * 20)
        lines.extend(fund_results)

    lines.append("━" * 20)
    lines.append("⚠️ 仅供参考，不构成投资建议")
    lines.append(f"生成时间: {now_sh().strftime('%H:%M:%S')}")

    return '\n'.join(lines)


# ============================================================
# 推送层
# ============================================================

def push_report(report_text, config):
    """推送报告到指定渠道"""
    channel = config.get('push', {}).get('channel', 'console')

    if channel == 'console':
        print(report_text)
        return

    elif channel == 'feishu':
        feishu_cfg = config.get('push', {}).get('feishu', {})
        app_id = feishu_cfg.get('app_id', '')
        app_secret = feishu_cfg.get('app_secret', '')
        chat_id = feishu_cfg.get('chat_id', '')

        # 凭证不完整时给出明确提示
        if not app_id or not app_secret or not chat_id:
            missing = []
            if not app_id: missing.append('app_id')
            if not app_secret: missing.append('app_secret')
            if not chat_id: missing.append('chat_id')
            print(f"[ERROR] 飞书推送配置不完整，缺少: {', '.join(missing)}", file=sys.stderr)
            print("[ERROR] 请在 config.yaml 或 config.local.yaml 中填写飞书凭证", file=sys.stderr)
            print("[ERROR] 参见 SKILL.md 的「飞书推送配置」章节", file=sys.stderr)
            print(report_text)  # 降级到控制台输出
            return

        try:
            # 1. 获取 tenant_access_token
            token_resp = requests.post(
                'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
                json={'app_id': app_id, 'app_secret': app_secret},
                timeout=10
            )
            token_resp.raise_for_status()
            access_token = token_resp.json().get('tenant_access_token', '')
            if not access_token:
                raise ValueError("No access_token returned")

            # 2. 发送消息到 chat_id
            msg_resp = requests.post(
                'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id',
                headers={'Authorization': f'Bearer {access_token}'},
                json={
                    'receive_id': chat_id,
                    'msg_type': 'text',
                    'content': json.dumps({'text': report_text})
                },
                timeout=10
            )
            msg_resp.raise_for_status()
            return
        except Exception as e:
            print(f"[WARN] Feishu push failed: {e}", file=sys.stderr)
        print(report_text)
        return

    elif channel == 'telegram':
        tg_cfg = config.get('push', {}).get('telegram', {})
        bot_token = tg_cfg.get('bot_token', os.environ.get('TG_BOT_TOKEN', ''))
        chat_id = tg_cfg.get('chat_id', os.environ.get('TG_CHAT_ID', ''))
        if bot_token and chat_id:
            try:
                requests.post(
                    f'https://api.telegram.org/bot{bot_token}/sendMessage',
                    json={'chat_id': chat_id, 'text': report_text},
                    timeout=10
                )
                return
            except Exception as e:
                print(f"[WARN] Telegram push failed: {e}")
        print(report_text)
        return

    else:
        print(report_text)


# ============================================================
# 主入口
# ============================================================

def main():
    # 首次运行自动安装（安装过则跳过）
    check_and_install()

    mode = sys.argv[1] if len(sys.argv) > 1 else 'auto'
    config = load_config()
    report = generate_report(config, mode)
    push_report(report, config)


if __name__ == '__main__':
    main()
