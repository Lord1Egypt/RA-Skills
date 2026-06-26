# -*- coding: utf-8 -*-
"""
A股持仓分析核心脚本（跨平台版）
每日分析流程的核心计算模块，供 skill 调用
支持 Windows / macOS / Linux
"""
import sys
import json
import os
import platform
from datetime import datetime
from pathlib import Path

# ---- 跨平台路径推断 ----
SKILL_DIR = Path(__file__).parent.resolve()   # .../stock-analysis-china/scripts/
SKILL_ROOT = SKILL_DIR.parent                  # .../stock-analysis-china/
SKILL_DATA = SKILL_ROOT / 'data'

# 用户主目录（跨平台）
HOME = Path.home()
SYSTEM = platform.system()  # 'Windows', 'Darwin' (macOS), 'Linux'

# 工作区路径（跨平台）
if SYSTEM == 'Windows':
    WORKSPACE_DIR = HOME / '.qclaw' / 'workspace'
else:
    # macOS / Linux
    WORKSPACE_DIR = HOME / '.qclaw' / 'workspace'

# Python site-packages 路径（自动推断）
def find_python_site():
    """跨平台查找 Python site-packages"""
    try:
        import site
        if site.getsitepackages():
            return Path(site.getsitepackages()[0])
    except:
        pass
    # 回退：使用当前 Python 的 site-packages
    return Path(sys.prefix) / 'lib' / f'python{sys.version_info.major}.{sys.version_info.minor}' / 'site-packages'

PYTHON_SITE = find_python_site()

# Python 可执行文件路径（跨平台）
def find_python():
    """跨平台查找 Python 解释器"""
    # 优先使用当前运行的 Python
    if sys.executable:
        return sys.executable
    # 回退：尝试系统 PATH 中的 python
    return 'python3' if SYSTEM != 'Windows' else 'python'

PYTHON_EXE = find_python()

def ensure_deps():
    """确保依赖已安装"""
    sys.path.insert(0, str(PYTHON_SITE))
    try:
        import akshare as ak
        import pandas as pd
        return True
    except ImportError:
        return False


def get_index_spot():
    """获取主要指数实时行情"""
    if not ensure_deps():
        return []
    import akshare as ak
    import pandas as pd
    indices = [('000001', '上证指数'), ('399001', '深证成指'),
               ('399006', '创业板指'), ('000300', '沪深300'),
               ('000016', '上证50'), ('000688', '科创50')]
    result = []
    try:
        df = ak.stock_zh_index_spot_em()
        for code, name in indices:
            row = df[df['代码'] == code]
            if not row.empty:
                r = row.iloc[0]
                pct = float(r['涨跌幅']) if pd.notna(r['涨跌幅']) else 0
                result.append({
                    'code': code, 'name': name,
                    'price': float(r['最新价']) if pd.notna(r['最新价']) else 0,
                    'change_pct': pct,
                    'trend': '▲' if pct > 0 else '▼' if pct < 0 else '-'
                })
    except Exception as e:
        print(f"[WARN] 指数数据获取失败: {e}")
    return result


def get_stock_spot(codes):
    """获取个股实时行情"""
    if not ensure_deps():
        return []
    import akshare as ak
    import pandas as pd
    results = []
    try:
        df = ak.stock_zh_a_spot_em()
        for code, name in codes:
            row = df[df['代码'] == code]
            if not row.empty:
                r = row.iloc[0]
                pct = float(r['涨跌幅']) if pd.notna(r['涨跌幅']) else 0
                results.append({
                    'code': code, 'name': name,
                    'price': float(r['最新价']) if pd.notna(r['最新价']) else 0,
                    'change_pct': pct,
                    'trend': '▲' if pct > 0 else '▼' if pct < 0 else '-',
                    'volume_ratio': float(r['量比']) if '量比' in df.columns and pd.notna(r['量比']) else None,
                    'pe': float(r['市盈率-动态']) if '市盈率-动态' in df.columns and pd.notna(r['市盈率-动态']) else None,
                })
            else:
                results.append({'code': code, 'name': name, 'price': None, 'change_pct': None})
    except Exception as e:
        print(f"[ERROR] 个股行情获取失败: {e}")
    return results


def get_kline(code, num=60):
    """获取K线数据"""
    if not ensure_deps():
        return None
    import akshare as ak
    try:
        df = ak.stock_zh_a_hist(symbol=code, period='daily',
                                  adjust='qfq',
                                  start_date='20250101',
                                  end_date=datetime.now().strftime('%Y%m%d'))
        if not df.empty and len(df) >= 10:
            return {
                'dates': df['日期'].tolist()[-num:],
                'closes': [float(x) for x in df['收盘'].tolist()[-num:]],
                'highs': [float(x) for x in df['最高'].tolist()[-num:]],
                'lows': [float(x) for x in df['最低'].tolist()[-num:]],
                'volumes': [float(x) for x in df['成交量'].tolist()[-num:]] if '成交量' in df.columns else [],
            }
    except Exception as e:
        print(f"[WARN] K线获取失败 {code}: {e}")
    return None


# ---- 技术指标计算 ----

def calc_sma(data, n):
    if len(data) < n: return None
    return sum(data[-n:]) / n


def calc_rsi(closes, period=14):
    if len(closes) < period + 1: return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i-1]
        gains.append(d if d > 0 else 0)
        losses.append(abs(d) if d < 0 else 0)
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0: return 100
    return 100 - (100 / (1 + avg_gain / avg_loss))


def calc_macd(closes, fast=12, slow=26, signal=9):
    if len(closes) < slow + signal: return None
    def ema(data, n):
        k = 2 / (n + 1)
        e = data[0]
        for d in data[1:]: e = d * k + e * (1 - k)
        return e
    ef = ema(closes, fast)
    es = ema(closes, slow)
    dif = ef - es
    return {'dif': round(dif, 4), 'dea': round(dif * 0.9, 4), 'hist': round(dif * 2, 4)}


def calc_boll(closes, period=20):
    if len(closes) < period: return None
    recent = closes[-period:]
    mid = sum(recent) / period
    std = (sum((x - mid)**2 for x in recent) / period) ** 0.5
    return {'upper': round(mid + 2*std, 4), 'mid': round(mid, 4), 'lower': round(mid - 2*std, 4)}


def calc_kdj(highs, lows, closes, n=9, m1=3, m2=3):
    if len(closes) < n: return None
    k, d = 50, 50
    for i in range(n-1, len(closes)):
        hh = max(highs[max(0,i-n+1):i+1]) if highs else closes[i]
        ll = min(lows[max(0,i-n+1):i+1]) if lows else closes[i]
        rsv = (closes[i] - ll) / (hh - ll) * 100 if hh != ll else 50
        k = (2/3) * k + (1/3) * rsv
        d = (2/3) * d + (1/3) * k
    j = 3 * k - 2 * d
    return {'K': round(k, 2), 'D': round(d, 2), 'J': round(j, 2)}


def analyze(code, name, portfolio=None):
    """综合技术分析"""
    kdata = get_kline(code)
    r = {'code': code, 'name': name}
    if portfolio:
        r['cost'] = portfolio.get('cost_price')
        r['qty'] = portfolio.get('quantity')
        r['cost_pct'] = portfolio.get('profit_pct')
        r['market_value'] = portfolio.get('market_value')

    if not kdata or len(kdata['closes']) < 20:
        r['status'] = '数据不足'
        return r

    closes = kdata['closes']
    highs = kdata['highs']
    lows = kdata['lows']
    latest = closes[-1]

    ma5 = calc_sma(closes, 5)
    ma10 = calc_sma(closes, 10)
    ma20 = calc_sma(closes, 20)
    ma60 = calc_sma(closes, 60) if len(closes) >= 60 else None
    rsi = calc_rsi(closes)
    macd = calc_macd(closes)
    boll = calc_boll(closes)
    kdj = calc_kdj(highs, lows, closes)

    signals = []

    # RSI
    if rsi:
        if rsi > 75: signals.append({'type': 'risk', 'label': 'RSI超买', 'detail': f'RSI={rsi:.1f}'})
        elif rsi < 25: signals.append({'type': 'opportunity', 'label': 'RSI超卖', 'detail': f'RSI={rsi:.1f}'})
        elif rsi > 60: signals.append({'type': 'bullish', 'label': 'RSI偏强', 'detail': f'RSI={rsi:.1f}'})
        elif rsi < 40: signals.append({'type': 'bearish', 'label': 'RSI偏弱', 'detail': f'RSI={rsi:.1f}'})
        else: signals.append({'type': 'neutral', 'label': 'RSI中性', 'detail': f'RSI={rsi:.1f}'})

    # MACD
    if macd:
        if macd['dif'] > 0: signals.append({'type': 'bullish', 'label': 'MACD多头', 'detail': 'DIF>0'})
        else: signals.append({'type': 'bearish', 'label': 'MACD空头', 'detail': 'DIF<0'})
        if macd['hist'] > 0: signals.append({'type': 'bullish', 'label': '红柱扩张', 'detail': 'MACD柱>0'})
        else: signals.append({'type': 'bearish', 'label': '绿柱扩张', 'detail': 'MACD柱<0'})

    # 布林带
    if boll:
        if latest > boll['upper']: signals.append({'type': 'risk', 'label': '突破布林上轨', 'detail': f'注意回调风险'})
        elif latest < boll['lower']: signals.append({'type': 'opportunity', 'label': '跌破布林下轨', 'detail': f'超跌关注反弹'})
        elif latest > boll['mid']: signals.append({'type': 'bullish', 'label': '价格>布林中轨', 'detail': f"mid={boll['mid']:.2f}"})
        else: signals.append({'type': 'bearish', 'label': '价格<布林中轨', 'detail': f"mid={boll['mid']:.2f}"})

    # KDJ
    if kdj:
        if kdj['K'] > 80 or kdj['J'] > 100: signals.append({'type': 'risk', 'label': 'KDJ超买', 'detail': f"K={kdj['K']:.0f}"})
        elif kdj['K'] < 20 or kdj['J'] < 0: signals.append({'type': 'opportunity', 'label': 'KDJ超卖', 'detail': f"K={kdj['K']:.0f}"})
        elif kdj['K'] > kdj['D']: signals.append({'type': 'bullish', 'label': 'KDJ金叉', 'detail': f"K={kdj['K']:.0f}>D={kdj['D']:.0f}"})
        else: signals.append({'type': 'bearish', 'label': 'KDJ死叉', 'detail': f"K={kdj['K']:.0f}<D={kdj['D']:.0f}"})

    # 均线排列
    if all([ma5, ma10, ma20, ma60]):
        if ma5 > ma10 > ma20 > ma60: signals.append({'type': 'bullish', 'label': '均线多头排列', 'detail': '强势上升趋势'})
        elif ma5 < ma10 < ma20 < ma60: signals.append({'type': 'bearish', 'label': '均线空头排列', 'detail': '弱势下降趋势'})
        elif ma5 > ma10 > ma20: signals.append({'type': 'bullish', 'label': '短期均线多头', 'detail': '短期偏强'})
        elif ma5 < ma10 < ma20: signals.append({'type': 'bearish', 'label': '短期均线空头', 'detail': '短期偏弱'})

    # 趋势判断
    bullish = sum(1 for s in signals if s['type'] in ('bullish', 'opportunity'))
    bearish = sum(1 for s in signals if s['type'] in ('bearish', 'risk'))
    if bullish > bearish + 2: tech_view = '偏多'
    elif bearish > bullish + 2: tech_view = '偏空'
    else: tech_view = '中性'

    r['signals'] = signals
    r['tech_view'] = tech_view
    r['rsi'] = round(rsi, 1) if rsi else None
    r['macd'] = macd
    r['boll'] = boll
    r['kdj'] = kdj
    r['ma'] = {
        'MA5': round(ma5, 3) if ma5 else None,
        'MA10': round(ma10, 3) if ma10 else None,
        'MA20': round(ma20, 3) if ma20 else None,
        'MA60': round(ma60, 3) if ma60 else None,
    }
    r['latest_price'] = latest
    r['latest_date'] = kdata['dates'][-1] if kdata['dates'] else None

    # 持仓综合建议
    if portfolio and signals:
        risk_signals = [s for s in signals if s['type'] in ('risk', 'bearish')]
        opp_signals = [s for s in signals if s['type'] in ('opportunity', 'bullish')]
        if risk_signals and not opp_signals and tech_view == '偏空':
            r['action'] = '减仓/止损'
        elif opp_signals and not risk_signals and tech_view == '偏多':
            r['action'] = '持有/关注加仓机会'
        elif tech_view == '中性':
            r['action'] = '持有观望'
        else:
            r['action'] = '持有'
    else:
        r['action'] = '数据不足'

    return r


def run_analysis(portfolio_path=None):
    """运行完整分析"""
    if not portfolio_path:
        # 优先读 skill 内置 data/（跟随 skill 更新）
        # 若不存在则读用户工作区（升级保护，数据持久化）
        skill_data_file = SKILL_DATA / 'positions_portfolio.json'
        workspace_data_file = WORKSPACE_DIR / 'data' / 'positions_portfolio.json'
        if skill_data_file.exists():
            portfolio_path = skill_data_file
        else:
            portfolio_path = workspace_data_file

    print('=' * 60)
    print(f'A股持仓分析 - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'系统: {SYSTEM} | Python: {PYTHON_EXE}')
    print('=' * 60)

    # 指数
    print('\n>>> 主要指数 <<<')
    indices = get_index_spot()
    for idx in indices:
        print(f"  {idx['name']}: {idx['price']} {idx['trend']}{abs(idx['change_pct']):.2f}%")

    # 持仓分析
    portfolio = []
    portfolio_path = Path(portfolio_path) if isinstance(portfolio_path, str) else portfolio_path
    if portfolio_path.exists():
        with open(portfolio_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            portfolio = data.get('portfolio', [])

    print(f'\n>>> 持仓分析（共{len(portfolio)}只证券）<<<\n')
    results = []
    for item in portfolio:
        code = item.get('code', '')
        name = item.get('name', '')
        print(f'  分析: {name}({code}) ...')
        result = analyze(code, name, item)
        results.append(result)
        for sig in (result.get('signals') or []):
            t = sig['type'].upper()
            print(f"    [{t:10}] {sig['label']}: {sig['detail']}")
        action = result.get('action', '')
        print(f"    → 综合建议: {action}")
        print()

    return {'indices': indices, 'portfolio_analysis': results}


if __name__ == '__main__':
    run_analysis()
