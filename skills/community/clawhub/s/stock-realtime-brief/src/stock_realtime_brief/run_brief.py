#!/usr/bin/env python3
"""v4.0 主路由 - 整合 smart_picker / price_watcher / disciplines"""
import sys
import os
from pathlib import Path

# v4.0 子命令路由
if len(sys.argv) > 1 and sys.argv[1] in ['pick', 'sectors', 'push', 'watch', 'rr', 'check', 'mainline', 'phase', 'endwave', 'shake']:
    SCRIPTS = Path(__file__).resolve().parent
    cmd = sys.argv[1]
    
    if cmd == 'pick':
        # 智能选股
        sys.argv = ['smart_picker.py'] + (sys.argv[2:] if len(sys.argv) > 2 else ['scan-all'])
        sys.path.insert(0, str(SCRIPTS))
        from smart_picker import main as picker_main
        picker_main()
        sys.exit(0)
    elif cmd == 'sectors':
        sys.argv = ['smart_picker.py', 'sectors']
        sys.path.insert(0, str(SCRIPTS))
        from smart_picker import main as picker_main
        picker_main()
        sys.exit(0)
    elif cmd == 'push':
        sys.argv = ['smart_picker.py', 'push']
        sys.path.insert(0, str(SCRIPTS))
        from smart_picker import main as picker_main
        picker_main()
        sys.exit(0)
    elif cmd == 'watch':
        sys.path.insert(0, str(SCRIPTS))
        from price_watcher import main_loop, check_rules, is_trading_time
        from datetime import datetime
        sub = sys.argv[2] if len(sys.argv) > 2 else 'check'
        if sub == 'start':
            print("🚀 启动盯盘 Agent 主循环...")
            main_loop()
        elif sub == 'check':
            print(f"📊 即时检查盯盘规则 - 北京时间 {datetime.now():%H:%M:%S}")
            check_rules()
        elif sub == 'status':
            print(f"交易时间: {is_trading_time()}")
        sys.exit(0)
    elif cmd == 'rr':
        # 风险收益比快速计算
        sys.path.insert(0, str(SCRIPTS))
        from disciplines import calculate_risk_reward, format_risk_reward
        if len(sys.argv) < 9:
            print("用法: rr <现价> <保守> <中性> <乐观> <技术止损> <硬止损> <极限止损>")
            sys.exit(1)
        result = calculate_risk_reward(
            float(sys.argv[2]),
            {
                'conservative_target': float(sys.argv[3]),
                'neutral_target': float(sys.argv[4]),
                'aggressive_target': float(sys.argv[5]),
                'tech_stop': float(sys.argv[6]),
                'hard_stop': float(sys.argv[7]),
                'extreme_stop': float(sys.argv[8]),
            }
        )
        print(format_risk_reward(result))
        sys.exit(0)
    elif cmd == 'mainline':
        sys.path.insert(0, str(SCRIPTS))
        from main_line_tracker import main as ml_main
        ml_main()
        sys.exit(0)
    elif cmd == 'phase':
        sys.path.insert(0, str(SCRIPTS))
        from market_phase import main as mp_main
        mp_main()
        sys.exit(0)
    elif cmd == 'endwave':
        sys.path.insert(0, str(SCRIPTS))
        from end_wave_detector import main as ew_main
        ew_main()
        sys.exit(0)
    elif cmd == 'shake':
        sys.argv = ['shake_vs_break.py'] + sys.argv[2:]
        sys.path.insert(0, str(SCRIPTS))
        from shake_vs_break import main as svb_main
        svb_main()
        sys.exit(0)
    elif cmd == 'check':
        # 纪律综合检查（演示模式）
        sys.path.insert(0, str(SCRIPTS))
        from disciplines import comprehensive_check, format_check_result
        result = comprehensive_check(
            sys.argv[2] if len(sys.argv) > 2 else '000000',
            'buy',
            {'using_leverage': '--leverage' in sys.argv}
        )
        print(format_check_result(result))
        sys.exit(0)

# 以下是 v3.x 原有逻辑

"""
A 股实时分析与操作建议生成器 — v2.2
支持三种模式：
  - portfolio (P): 持仓简报
  - single    (S): 单股深度
  - multi     (M): 多股对比
  - auto         : 根据输入数量自动判定 (1只→S，多只→M，有portfolio→P)

v2.8 → 增加机构研报扫描（目标价 / 评级 / 券商覆盖）
v2.7 → 增加回撤分析（最大回撤 / 当前回撤 / 风险等级）
v2.6 → 七维分析 + 业绩深挖
v2.5 → 解禁未来事件检测
v2.4 → TinyFish Search 集成
v2.2 → 公告拉取

依赖:
  - /home/work/.openclaw/workspace/stock-agents/data_fetcher.py
  - akshare
"""
import sys
import os
import argparse
import json
from datetime import datetime, timedelta

WORKSPACE = '/home/work/.openclaw/workspace'
sys.path.insert(0, os.path.join(WORKSPACE, 'stock-agents'))

try:
    from data_fetcher import _sina_batch_quotes, _tencent_realtime_quote
except Exception as e:
    print(f"[ERR] 无法加载 data_fetcher: {e}", file=sys.stderr)
    sys.exit(1)


# ============= 数据获取 =============

# ============= 公告拉取 =============

def fetch_announcements(code, days=14):
    """拉个股近 N 天公告，重点识别减持/业绩/解禁/大股东以及其他利空关键词。
    返回: list of dict {date, title, url, level, tag}
    level: HIGH (明显利空代表词) / MED / LOW
    """
    keywords_HIGH = ['减持股份', '减持计划', '减持资产', '减股', '拟转让', '疑似错误', '立案', '被调查', '证监会', '警示', '业绩预减', '业绩老', '诉讼', '解禁', '限售解禁', '限售股解禁', '可流通', '限售股上市', '解禁股', '解禁日']
    keywords_MED = ['限售股', '收购', '重组', '股东大会', '定增', '发行', '业绩预告', '终止', '处罚', '调查', '震荡', '出售']
    keywords_LOW = ['业绩', '报告', '组织', '人事', '衇任', '会议', '取消', '继续', '占股底']

    out = []
    seen_titles = set()
    # 主接口：TinyFish Search（中文源更准，能抳雪球/知乎）、gsk 作为兑底
    queries = [
        f'{code} 减持 计划',
        f'{code} 业绩 预告 OR 预减',
        f'{code} 解禁',                      # v2.5: 简化查询，提升召回率
        f'{code} 限售股 解禁 日期',          # v2.5: 明确找解禁日期
        f'{code} 限售股 上市 可流通',        # v2.5: 找未来解禁
        f'{code} 处罚 OR 调查 OR 警示',
    ]
    # 加载 TinyFish 凭据
    tinyfish_key = None
    try:
        tf_env = '/home/work/.openclaw/secrets/tinyfish.env'
        if os.path.exists(tf_env):
            with open(tf_env) as f:
                for line in f:
                    if line.startswith('TINYFISH_API_KEY='):
                        tinyfish_key = line.split('=', 1)[1].strip()
    except Exception:
        pass
    
    def _extract_announcement_date(snippet, url, title):
        """从 snippet/url/title 中提取公告日期。返回 datetime 或 None。"""
        import re
        combined = f"{title} {snippet} {url}"
        if not combined.strip():
            return None
        # 1. 公告日期：XXXX-XX-XX
        m = re.search(r'公告日期[：:]\s*(\d{4})[-/](\d{1,2})[-/](\d{1,2})', combined)
        if m:
            try: return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except: pass
        # 2. AN东财公告号（前 8 位是日期）
        m = re.search(r'AN(\d{8})', combined)
        if m:
            s = m.group(1)
            try: return datetime(int(s[:4]), int(s[4:6]), int(s[6:8]))
            except: pass
        # 3. 'X月Y日'（按当前年）
        m = re.search(r'(\d{1,2})月(\d{1,2})日', combined)
        if m:
            try:
                now = datetime.now()
                d = datetime(now.year, int(m.group(1)), int(m.group(2)))
                if d > now: d = datetime(now.year - 1, int(m.group(1)), int(m.group(2)))
                return d
            except: pass
        # 4. 标准 ISO 65e5期 2026-04-14
        m = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', combined)
        if m:
            try: return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except: pass
        return None
    
    def _search_tinyfish(query):
        """用 TinyFish Search（中文效果最佳）"""
        if not tinyfish_key:
            return None
        try:
            import urllib.parse, urllib.request
            url = f'https://api.search.tinyfish.ai?query={urllib.parse.quote(query)}'
            req = urllib.request.Request(url, headers={'X-API-Key': tinyfish_key})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                # 转换为 gsk-兼容格式，主动提取日期
                items = []
                for r in data.get('results', []):
                    title = r.get('title', '')
                    snippet = r.get('snippet', '')
                    url_str = r.get('url', '')
                    date_obj = _extract_announcement_date(snippet, url_str, title)
                    date_str = date_obj.strftime('%Y-%m-%d') if date_obj else ''
                    items.append({
                        'title': title,
                        'link': url_str,
                        'snippet': snippet,
                        'site': r.get('site_name', ''),
                        'date': date_str,
                    })
                return items
        except Exception as e:
            return None
    
    def _search_gsk(query):
        """兑底：gsk web_search"""
        try:
            import subprocess
            r = subprocess.run(['gsk', 'search', query, '--output', 'json'],
                               capture_output=True, text=True, timeout=20)
            if r.returncode != 0 or not r.stdout: return []
            res = json.loads(r.stdout)
            data_payload = res.get('data', res) if isinstance(res, dict) else {}
            return data_payload.get('organic_results') or res.get('organic_results') or []
        except Exception:
            return []
    
    for q in queries:
        try:
            # 先试 TinyFish，拿不到兑底 gsk
            items = _search_tinyfish(q) or _search_gsk(q) or []
            for item in items[:8]:
                title = item.get('title', '')
                if not title or title in seen_titles: continue
                # 不过滤股票代码（同 query 搜，不会跨股混入）
                level = 'LOW'; tag = ''
                for kw in keywords_HIGH:
                    if kw in title:
                        level = 'HIGH'; tag = kw; break
                if level == 'LOW':
                    for kw in keywords_MED:
                        if kw in title:
                            level = 'MED'; tag = kw; break
                if level == 'LOW': continue
                # v2.5 时间过滤：HIGH 级支持"未来 30 天 + 过去 14 天"双向窗口
                # 因为解禁、定增上市等是未来事件，不应被"过去 N 天"过滤掉
                date_str = str(item.get('date', '')).strip()
                ok = False
                if not date_str:
                    continue  # 无日期一律跳过（防老公告混入）
                if 'ago' in date_str.lower():
                    try:
                        ds_low = date_str.lower()
                        digits = ''.join(c for c in date_str if c.isdigit())
                        if not digits: continue
                        n = int(digits)
                        # 转为天数
                        if 'hour' in ds_low or 'minute' in ds_low: days_eq = 1
                        elif 'day' in ds_low: days_eq = n
                        elif 'week' in ds_low: days_eq = n * 7
                        elif 'month' in ds_low: days_eq = n * 30
                        elif 'year' in ds_low: days_eq = n * 365
                        else: days_eq = n  # 默认当天数
                        if days_eq <= days: ok = True
                    except Exception:
                        continue
                else:
                    # 试图解析 ISO 或英文日期
                    try:
                        from email.utils import parsedate_to_datetime
                        d = None
                        for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%b %d, %Y'):
                            try:
                                from datetime import datetime as _dt
                                d = _dt.strptime(date_str[:11].strip(), fmt)
                                break
                            except Exception:
                                continue
                        if d:
                            delta = (datetime.now() - d).days
                            # v2.5: HIGH 级支持双向窗口（解禁等未来事件不该被滤）
                            # delta < 0 表示未来事件
                            if level == 'HIGH':
                                # HIGH: 过去 days 天 ~ 未来 30 天
                                if -30 <= delta <= days: ok = True
                            else:
                                # MED: 仅过去 days 天
                                if 0 <= delta <= days: ok = True
                    except Exception:
                        continue
                if not ok: continue
                out.append({'date': date_str, 'title': title,
                            'level': level, 'tag': tag,
                            'url': item.get('link', '')})
                seen_titles.add(title)
        except Exception:
            continue
    # 按重要度排序: HIGH 在前
    out.sort(key=lambda x: 0 if x['level'] == 'HIGH' else 1)
    return out[:6]  # 最多 6 条


def _name_likely_in_title(title, code):
    # 简单判断：常见股票名会以股票代码出现。如果标题里有明显公告关键词且代码不在里，可能是同名公司。
    return False


def fetch_realtime(codes):
    """优先腾讯（最稳）→ 新浪批量兜底"""
    out = {}
    # 先尝试新浪批量（一次拿多只，省时间）
    try:
        sina = _sina_batch_quotes(codes)
        for c in codes:
            if sina.get(c):
                out[c] = sina[c]
    except Exception:
        pass
    # 缺的用腾讯补
    for c in codes:
        if c not in out:
            try:
                q = _tencent_realtime_quote(c)
                if q:
                    out[c] = {
                        'name': q.get('名称'),
                        'price': q.get('最新价'),
                        'pct_change': q.get('涨跌幅'),
                        'open': q.get('今开'),
                        'high': q.get('最高'),
                        'low': q.get('最低'),
                        'prev_close': q.get('昨收'),
                        'amount': q.get('成交额'),
                        'turnover_rate': q.get('换手率'),
                        'volume': q.get('成交量'),
                    }
            except Exception:
                pass
    return out


def _fetch_hist_tencent(code):
    """备用：腾讯日 K 线接口（更稳）"""
    import urllib.request, json as _json
    # 腾讯前复权日 K：sh600519 / sz000858 / sz300757
    if code.startswith(('60', '68', '90')):
        sym = 'sh' + code
    else:
        sym = 'sz' + code
    url = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,90,qfq'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = _json.loads(resp.read().decode('utf-8'))
        # 数据路径: data.data.{sym}.qfqday
        kline = data.get('data', {}).get(sym, {}).get('qfqday', [])
        if not kline:
            kline = data.get('data', {}).get(sym, {}).get('day', [])
        # 每条: [日期, 开, 收, 高, 低, 成交量, ...]
        rows = []
        for r in kline:
            try:
                rows.append({
                    '日期': r[0],
                    '开盘': float(r[1]),
                    '收盘': float(r[2]),
                    '最高': float(r[3]),
                    '最低': float(r[4]),
                    '成交量': float(r[5]) if len(r) > 5 else 0,
                })
            except Exception:
                continue
        import pandas as pd
        if rows:
            return pd.DataFrame(rows)
        return None
    except Exception:
        return None


def _calc_drawdown(closes):
    """v2.7: 回撤分析
    
    返回 max_drawdown / current_drawdown / 历史高点 / 风险等级
    """
    if not closes or len(closes) < 2:
        return None
    try:
        peak = closes[0]
        max_dd = 0.0
        max_dd_peak = peak
        for c in closes[1:]:
            if c > peak:
                peak = c
            dd = (peak - c) / peak * 100
            if dd > max_dd:
                max_dd = dd
                max_dd_peak = peak
        peak_global = max(closes)
        peak_idx = closes.index(peak_global)
        current_dd = (peak_global - closes[-1]) / peak_global * 100
        days_since = len(closes) - 1 - peak_idx
        return {
            'max_drawdown_pct': round(max_dd, 2),
            'max_drawdown_peak': round(max_dd_peak, 2),
            'current_drawdown_pct': round(current_dd, 2),
            'peak_price': round(peak_global, 2),
            'days_since_peak': days_since,
            'risk_level': _drawdown_risk_level(current_dd),
        }
    except Exception:
        return None


def _drawdown_risk_level(dd_pct):
    """根据当前回撤幅度返回风险等级"""
    if dd_pct is None:
        return '?'
    if dd_pct < 5:
        return '🟢 新高附近'
    elif dd_pct < 10:
        return '🟢 健康回调'
    elif dd_pct < 20:
        return '🟡 中度回调'
    elif dd_pct < 30:
        return '🟠 深度回调'
    elif dd_pct < 50:
        return '🔴 重度下跌'
    else:
        return '⚫ 腰斩级'



def fetch_hist_ma(code, days_back=120, retry=2):
    """拉历史 K 线（AKShare 主源 + 腾讯备源 + 重试），算 MA5/10/20/30 + N 日高低"""
    df = None
    # 先尝试 AKShare（带重试）
    for attempt in range(retry):
        try:
            import akshare as ak
            end = datetime.now().strftime('%Y%m%d')
            start = (datetime.now() - timedelta(days=days_back)).strftime('%Y%m%d')
            df = ak.stock_zh_a_hist(symbol=code, period='daily',
                                    start_date=start, end_date=end, adjust='qfq')
            if df is not None and not df.empty:
                break
        except Exception:
            pass
    # AKShare 失败 → 切腾讯
    if df is None or df.empty:
        df = _fetch_hist_tencent(code)
    if df is None or df.empty:
        return None
    try:
        closes = df['收盘'].tolist()
        last = closes[-1] if closes else None
        ma = {}
        for n in (5, 10, 20, 30):
            if len(closes) >= n:
                ma[f'ma{n}'] = round(sum(closes[-n:]) / n, 2)
        # 近 5 日均量（用于量比判断）
        vols = df['成交量'].tolist() if '成交量' in df.columns else []
        avg_vol5 = round(sum(vols[-5:]) / 5, 0) if len(vols) >= 5 else None
        # 40 日涨幅
        pct40 = None
        if len(closes) >= 40:
            pct40 = round((closes[-1] - closes[-40]) / closes[-40] * 100, 2)
        # v2.7: 回撤分析（最大回撤 / 当前回撤 / 历史高点位置）
        drawdown = _calc_drawdown(closes)
        cols = ['日期', '收盘']
        if '涨跌幅' in df.columns: cols.append('涨跌幅')
        if '换手率' in df.columns: cols.append('换手率')
        return {
            'last': last,
            **ma,
            'high_n': round(max(closes), 2) if closes else None,
            'low_n': round(min(closes), 2) if closes else None,
            'avg_vol5': avg_vol5,
            'pct_40d': pct40,
            'drawdown': drawdown,  # v2.7
            'recent6': df.tail(6)[cols].to_dict(orient='records'),
        }
    except Exception as e:
        return {'error': str(e)}


# ============= 分析逻辑 =============

def derive_stop_loss(rt, hist, is_heavy=False, has_margin=False, cost=None):
    """三档硬止损。
    原则：
    - 预警线 = MA5 (强势) / MA10 (重仓)
    - 风控线 = MA10 (一般) / MA20 (重仓) / max(MA20, 成本-15%) (重仓亏损)
      → 盈利股不用“成本-15%”，避免风控线跑到当前价以下 20%+
    - 清仓线 = MA20 或 成本-25% (亏损股)
    - 盈利 > 30% 的股额外提供“利润保护位” (现价-回吐 25% 利润)
    """
    last = rt.get('price') if rt else None
    if not last or not hist:
        return None
    ma5 = hist.get('ma5'); ma10 = hist.get('ma10'); ma20 = hist.get('ma20')

    # 是否处于明显盈利
    pnl_pct = ((last - cost) / cost * 100) if cost else 0
    is_profit = pnl_pct > 30
    is_loss_state = pnl_pct < 0

    # 预警线
    if is_heavy:
        warn = ma10 or ma5
    else:
        warn = ma5 or ma10

    # 风控线
    if is_loss_state and is_heavy and cost:
        # 重仓亏损：成本-15% 与 MA20 中高者 (先触发者先减)
        risk = max(round(cost * 0.85, 2), ma20 or 0)
    else:
        risk = ma20 or ma10

    # 清仓线
    if is_loss_state and cost:
        cut = round(cost * 0.75, 2)
    else:
        cut = ma20 or ma10
        # 不能比风控线高
        if risk and cut and cut >= risk:
            cut = round(risk * 0.97, 2)

    # 盈利股额外提供“利润保护位”
    profit_lock = None
    if is_profit:
        # 现价回吐 25% 利润
        give_back = (last - cost) * 0.25
        profit_lock = round(last - give_back, 2)
        # 如果利润保护位高于预警线，提升预警线
        if warn and profit_lock > warn:
            warn = profit_lock

    if has_margin:
        if warn: warn = round(warn * 1.03, 2)
        if risk: risk = round(risk * 1.03, 2)

    return {
        'warn_line': warn, 'warn_action': '减 1/3',
        'risk_line': risk, 'risk_action': '再减 1/3',
        'cut_line': cut, 'cut_action': '清掉剩余',
        'profit_lock': profit_lock,
    }


def derive_operation_levels(rt, hist):
    """单股操作位推算 (模式 S)"""
    last = rt.get('price') if rt else None
    if not last or not hist:
        return None
    ma5, ma10, ma20 = hist.get('ma5'), hist.get('ma10'), hist.get('ma20')
    high_n = hist.get('high_n')
    return {
        '介入位': ma10,
        '加仓位': high_n,
        '止损位': ma20,
        '止盈位_短线': round(last * 1.10, 2) if last else None,
        '止盈位_波段': round(last * 1.20, 2) if last else None,
    }


def calc_score(rt, hist):
    """多股对比的轻量综合打分 (模式 M)"""
    if not rt or not hist or not hist.get('last'):
        return 0
    last = hist['last']
    score = 0
    # 当日涨跌幅 ÷ 2
    pct = rt.get('pct_change') or 0
    score += pct / 2
    # MA5 偏离度 × 1.5（短期强弱）
    if hist.get('ma5'):
        score += (last - hist['ma5']) / hist['ma5'] * 100 * 1.5
    # MA20 偏离度 × 1（中期趋势）
    if hist.get('ma20'):
        score += (last - hist['ma20']) / hist['ma20'] * 100
    # 量价共振分
    vol = rt.get('volume') or 0
    avg_v5 = hist.get('avg_vol5') or 1
    vol_ratio = vol / avg_v5 if avg_v5 else 1
    if pct > 0 and vol_ratio > 1.2:   # 放量涨
        score += 2
    elif pct < 0 and vol_ratio > 1.2: # 放量跌
        score -= 2
    return round(score, 2)


def judge_stance(rt, hist):
    """态势速判一句话 (模式 S)"""
    if not rt or not hist:
        return "数据不足"
    last = rt.get('price')
    pct = rt.get('pct_change') or 0
    ma5, ma10, ma20 = hist.get('ma5'), hist.get('ma10'), hist.get('ma20')
    if not all([last, ma5, ma10, ma20]):
        return "数据不全，谨慎判断"
    # 趋势判断
    if last > ma5 > ma10 > ma20:
        if pct > 3:
            return "🚀 强势上攻，多头排列加速"
        return "📈 多头排列，趋势向上"
    if last < ma5 < ma10 < ma20:
        if pct < -3:
            return "⚠️ 加速下跌，空头排列扩散"
        return "📉 空头排列，趋势向下"
    if last > ma20 and ma5 > ma10:
        return "🔵 中期向上，短期偏强"
    if abs(pct) < 1 and abs(last - ma20) / ma20 < 0.02:
        return "⚪ 低波动震荡"
    return "🟡 多空交错，方向不明"


# ============= 输出渲染 =============

def render_portfolio(holdings, total_mv, total_margin):
    """模式 P：持仓简报。holdings 已拿到实时数据 + hist + sl + 个股浮盈。"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    md = [f"# 📊 盘前持仓简报 — {now}\n"]

    # 担保比例
    guarantee_ratio = round(total_mv / total_margin * 100, 1) if total_margin else None
    md.append(f"**总市值**：¥{total_mv:,.0f} · **融资余额**：¥{total_margin:,.0f} · **担保比例**：**{guarantee_ratio}%**\n" if guarantee_ratio else f"**总市值**：¥{total_mv:,.0f}\n")

    # 担保比例分级
    if guarantee_ratio:
        if guarantee_ratio < 150:
            warn = '🚨🚨🚨 **接近强平区！立即降仓**'
        elif guarantee_ratio < 160:
            warn = '🚨 **强警告：尽快降杠杆**'
        elif guarantee_ratio < 170:
            warn = '⚠️ **警戒区：建议主动降仓**'
        elif guarantee_ratio < 200:
            warn = '🟡 **可控区：仍需关注**'
        else:
            warn = '✅ **安全区**'
        md.append(f"### 担保比例评估: {warn}\n")

    # 按风险排序：亏损 × 融资 × 跌破MA20 × 重仓
    def _risk_rank(h):
        s = 0
        if h.get('is_loss'): s += 2
        if h.get('has_margin'): s += 3
        if h.get('is_heavy'): s += 1
        hist = h.get('hist') or {}
        if hist.get('last') and hist.get('ma20') and hist['last'] < hist['ma20']:
            s += 2
        return -s
    holdings = sorted(holdings, key=_risk_rank)

    # 一、实时态势
    md.append("## 一、持仓实时态势\n")
    md.append("| 股票 | 现价 | 涨跌幅 | 成本 | 浮盈% | 仓位% | 赛道 |")
    md.append("|------|-----:|-------:|-----:|------:|------:|------|")
    for h in holdings:
        rt = h.get('rt') or {}
        marks = []
        if h.get('is_heavy'): marks.append('🎯')
        if h.get('has_margin'): marks.append('🔥')
        if h.get('is_loss'): marks.append('📉')
        prefix = ''.join(marks) or '🔵'
        pnl_pct = h.get('pnl_pct')
        pnl_str = f"+{pnl_pct}%" if pnl_pct is not None and pnl_pct >= 0 else f"{pnl_pct}%"
        md.append(f"| {prefix} {h['name']} {h['code']} | {h.get('price','-')} | "
                  f"{rt.get('pct_change','-')}% | {h.get('cost','-')} | {pnl_str} | "
                  f"{h.get('weight','-')}% | {h.get('sector','')} |")
    md.append("")

    # 公告集中告警（最重要，置顶）
    has_high = any(a.get('level') == 'HIGH' for h in holdings for a in (h.get('announce') or []))
    has_med = any(a.get('level') == 'MED' for h in holdings for a in (h.get('announce') or []))
    if has_high or has_med:
        md.append("## 📢 近 14 日重要公告告警\n")
        for h in holdings:
            ann = h.get('announce') or []
            if not ann: continue
            for a in ann:
                emoji = '🔴' if a['level'] == 'HIGH' else '🟡'
                md.append(f"- {emoji} **{h['name']}** [{a.get('date','?')}] [{a.get('tag','')}] {a['title']}")
        md.append("")
        md.append("> ⚠️ **以上公告可能影响评估，建议在下面的技术面之上调整出手节奏。**\n")

    # 二、关键均线 + 三档硬止损
    md.append("## 二、关键均线 + 三档硬止损\n")
    for h in holdings:
        hist = h.get('hist') or {}
        sl = h.get('sl') or {}
        flag = '🎯' if h.get('is_heavy') else ('🔥' if h.get('has_margin') else '🔵')
        pnl_pct = h.get('pnl_pct')
        pnl_str = f"+{pnl_pct}%" if pnl_pct is not None and pnl_pct >= 0 else f"{pnl_pct}%"
        md.append(f"### {flag} {h['name']} {h['code']} — 成本 {h.get('cost','-')} / 浮盈 {pnl_str}")
        if hist.get('last'):
            ma20 = hist.get('ma20'); last = hist.get('last')
            pos_state = ''
            if ma20 and last:
                pos_state = '✅ 站上 MA20' if last > ma20 else '⚠️ 跌破 MA20'
            md.append(f"- 现价 **{hist.get('last')}** {pos_state} | "
                      f"MA5={hist.get('ma5','-')} MA10={hist.get('ma10','-')} "
                      f"MA20={hist.get('ma20','-')} MA30={hist.get('ma30','-')}")
            if hist.get('pct_40d') is not None:
                md.append(f"- 40 日涨幅 **{hist.get('pct_40d')}%** | 区间 {hist.get('low_n','-')} ~ {hist.get('high_n','-')}")
        # v2.7 回撤分析
        dd = hist.get('drawdown')
        if dd:
            md.append(f"- 📉 当前回撤 **{dd['current_drawdown_pct']}%** {dd['risk_level']} | 距高点 {dd['peak_price']} ({dd['days_since_peak']} 日) | 区间最大回撤 {dd['max_drawdown_pct']}%")
        if sl:
            md.append(f"- 🚨 预警 **{sl.get('warn_line','-')}** → {sl.get('warn_action')}")
            md.append(f"- 🚨 风控 **{sl.get('risk_line','-')}** → {sl.get('risk_action')}")
            md.append(f"- 🚨 清仓 **{sl.get('cut_line','-')}** → {sl.get('cut_action')}")
        md.append("")

    # 三、操作清单
    md.append("## 三、📋 今早可执行的条件单\n")
    md.append("✅ **开盘前 5 分钟内设好**：")
    md.append("| 优先级 | 股票 | 触发位 | 动作 |")
    md.append("|:---:|------|-------:|------|")
    for h in holdings:
        sl = h.get('sl') or {}
        if not sl.get('risk_line'): continue
        # 优先级：亏损融资 P0 / 重仓 P1 / 其他 P2
        if h.get('is_loss') and h.get('has_margin'): pri = 'P0 🚨'
        elif h.get('is_heavy'): pri = 'P1 🎯'
        elif h.get('has_margin'): pri = 'P1 🔥'
        else: pri = 'P2'
        md.append(f"| {pri} | {h['name']} | {sl['risk_line']} | {sl['risk_action']} |")
    md.append("")
    md.append("🔥 **融资管理**：担保比例 < 170% 主动降仓 / 优先还亏损票 / 强势票暂不还")
    md.append("")
    md.append("## 四、今晚问自己 3 个问题")
    md.append("1. 已经赚多少？是否到落袋点？")
    md.append("2. 哪只技术位最弱？能不能借反弹减？")
    md.append("3. 担保比例够不够安全？")
    return '\n'.join(md)


def load_portfolio(path):
    """读取 portfolio.json 并读出 positions 格式（合并同一股票多账户、算加权成本、型联融资标记）"""
    with open(path) as f:
        pf = json.load(f)
    total_margin = pf.get('margin_debt', 0)
    agg = {}
    # 兼容 holdings/positions 两种字段名
    raw = pf.get('positions') or pf.get('holdings') or []
    for p in raw:
        code = p.get('code') or p.get('symbol')
        if not code: continue
        if code not in agg:
            agg[code] = {
                'code': code, 'name': p.get('name', code),
                'sector': p.get('sector', ''),
                'amount': 0, 'cost_total': 0,
                'has_margin': False,
            }
        amt = p.get('amount') or p.get('shares') or 0
        cost_each = p.get('buy_price') or p.get('cost') or 0
        agg[code]['amount'] += amt
        agg[code]['cost_total'] += cost_each * amt
        if p.get('account') == '融资' or p.get('has_margin'):
            agg[code]['has_margin'] = True
    holdings = []
    for code, x in agg.items():
        if x['amount'] <= 0: continue
        avg_cost = round(x['cost_total'] / x['amount'], 2)
        holdings.append({
            'code': code, 'name': x['name'], 'sector': x['sector'],
            'cost': avg_cost, 'amount': x['amount'],
            'has_margin': x['has_margin'],
        })
    return holdings, total_margin


def render_single(code, data):
    """模式 S：单股深度"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    rt = data.get('rt') or {}
    hist = data.get('hist') or {}
    name = rt.get('name', code)
    md = [f"# 🔍 {name} {code} 实时分析 — {now}\n"]

    md.append("## 一、态势速判\n")
    md.append(f"**{judge_stance(rt, hist)}**\n")

    md.append("## 二、技术面\n")
    if rt:
        md.append(f"- 现价: **{rt.get('price','-')}** | "
                  f"涨跌幅: **{rt.get('pct_change','-')}%** | "
                  f"换手: {rt.get('turnover_rate','-')}% | "
                  f"成交额: {rt.get('amount','-')}")
    if hist.get('ma5'):
        md.append(f"- 均线: MA5={hist.get('ma5')} MA10={hist.get('ma10')} "
                  f"MA20={hist.get('ma20')} MA30={hist.get('ma30')}")
    if hist.get('high_n'):
        md.append(f"- 近 N 日: 高 **{hist.get('high_n')}** / 低 **{hist.get('low_n')}**")
    if hist.get('pct_40d') is not None:
        md.append(f"- 40 日涨幅: **{hist.get('pct_40d')}%**")
        # v2.7 回撤分析
        dd = hist.get('drawdown')
        if dd:
            md.append(f"- 📉 当前回撤: **{dd['current_drawdown_pct']}%** {dd['risk_level']}")
            md.append(f"- 历史高点: ¥{dd['peak_price']}（{dd['days_since_peak']} 个交易日前）")
            md.append(f"- 区间最大回撤: {dd['max_drawdown_pct']}%")
    md.append("")

    md.append("## 三、操作位建议\n")
    levels = derive_operation_levels(rt, hist)
    sl = derive_stop_loss(rt, hist)
    if levels:
        md.append("| 类型 | 价位 | 触发动作 |")
        md.append("|------|-----:|---------|")
        md.append(f"| 介入位（MA10）| {levels.get('介入位','-')} | 站稳后小仓位试探 |")
        md.append(f"| 加仓位（前高）| {levels.get('加仓位','-')} | 突破前高确认 |")
        md.append(f"| 止损位（MA20）| {levels.get('止损位','-')} | 跌破后减仓 |")
        md.append(f"| 短线止盈位 | {levels.get('止盈位_短线','-')} | 触及落袋 1/3 |")
        md.append(f"| 波段止盈位 | {levels.get('止盈位_波段','-')} | 触及落袋 1/2 |")
    if sl:
        md.append(f"\n**止损三档**：预警 {sl['warn_line']} → 风控 {sl['risk_line']} → 清仓 {sl['cut_line']}")
    md.append("")

    md.append("## 四、跟踪要点\n")
    md.append("- 关注是否站稳/跌破上方关键均线")
    md.append("- 关注量价是否共振（放量上涨为多头信号，缩量上涨警惕）")
    md.append("- 关注大盘环境与板块联动")
    return '\n'.join(md)


def render_multi(codes, data):
    """模式 M：多股对比"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    md = [f"# 📊 多股对比分析 — {now}\n"]

    rows = []
    for c in codes:
        rt = data.get(c, {}).get('rt') or {}
        hist = data.get(c, {}).get('hist') or {}
        if not rt or not hist:
            continue
        last = hist.get('last') or rt.get('price') or 0
        ma5 = hist.get('ma5') or last
        ma20 = hist.get('ma20') or last
        ma5_dev = round((last - ma5) / ma5 * 100, 2) if ma5 else 0
        ma20_dev = round((last - ma20) / ma20 * 100, 2) if ma20 else 0
        score = calc_score(rt, hist)
        rows.append({
            'code': c,
            'name': rt.get('name', c),
            'price': rt.get('price'),
            'pct': rt.get('pct_change'),
            'ma5_dev': ma5_dev,
            'ma20_dev': ma20_dev,
            'turnover': rt.get('turnover_rate'),
            'pct_40d': hist.get('pct_40d'),
            'score': score,
        })
    rows.sort(key=lambda x: -x['score'])

    md.append("## 一、横向对比表\n")
    md.append("| 排名 | 股票 | 现价 | 涨跌幅 | MA5偏离 | MA20偏离 | 换手% | 40日涨幅 | 综合分 | 标签 |")
    md.append("|:---:|------|-----:|-------:|--------:|---------:|------:|---------:|-------:|------|")
    for i, r in enumerate(rows, 1):
        if i == 1 and r['score'] > 3:
            tag = '⭐'
        elif r['score'] < -3:
            tag = '⚠️'
        else:
            tag = '🟡'
        md.append(f"| {i} | {r['name']} {r['code']} | {r['price']} | "
                  f"{r['pct']}% | {r['ma5_dev']}% | {r['ma20_dev']}% | "
                  f"{r['turnover']}% | {r['pct_40d']}% | {r['score']} | {tag} |")
    md.append("")

    md.append("## 二、关键差异点\n")
    if len(rows) >= 2:
        top, bot = rows[0], rows[-1]
        md.append(f"- **{top['name']} vs {bot['name']}**：")
        md.append(f"  - {top['name']} 综合分 {top['score']}（强势特征：MA5偏离 {top['ma5_dev']}% / 40日涨幅 {top['pct_40d']}%）")
        md.append(f"  - {bot['name']} 综合分 {bot['score']}（偏弱：MA20偏离 {bot['ma20_dev']}%）")
    md.append("")

    md.append("## 三、判断（不构成投资建议）\n")
    if rows:
        md.append(f"- ⭐ **优势更明显**：{rows[0]['name']}")
        md.append(f"  理由：综合分 {rows[0]['score']}，量价/趋势/动能综合最优")
        if len(rows) > 2:
            md.append(f"- 🟡 **保持观察**：{rows[1]['name']}（综合分 {rows[1]['score']}）")
        if rows[-1]['score'] < 0:
            md.append(f"- ⚠️ **谨慎对待**：{rows[-1]['name']}（综合分 {rows[-1]['score']}）")
    return '\n'.join(md)


# ============= 主流程 =============

def main():
    ap = argparse.ArgumentParser(description='A 股实时分析与操作建议（v2.0）')
    ap.add_argument('--mode', choices=['portfolio', 'single', 'multi', 'auto'],
                    default='auto', help='模式：persona(P)/single(S)/multi(M)/auto')
    ap.add_argument('--portfolio', help='portfolio.json 路径（模式 P）')
    ap.add_argument('--code', help='股票代码（模式 S）')
    ap.add_argument('--codes', help='股票代码列表，逗号分隔（模式 M / S 多选）')
    ap.add_argument('--names', help='股票名称列表，逗号分隔（与 codes 对应）')
    ap.add_argument('--skip-announce', action='store_true', help='跳过公告拉取（提速）')
    args = ap.parse_args()

    # ===== 模式判定 =====
    mode = args.mode
    if mode == 'auto':
        if args.portfolio:
            mode = 'portfolio'
        elif args.code:
            mode = 'single'
        elif args.codes:
            n = len([c for c in args.codes.split(',') if c.strip()])
            mode = 'single' if n == 1 else 'multi'
        else:
            print("ERR: 需要 --portfolio / --code / --codes 之一", file=sys.stderr)
            sys.exit(1)

    # ===== 模式 P =====
    if mode == 'portfolio':
        # portfolio 路径默认 → stock-agents/data/portfolio.json
        pf_path = args.portfolio or '/home/work/.openclaw/workspace/stock-agents/data/portfolio.json'
        if not os.path.exists(pf_path):
            print(f"ERR: 未找到 portfolio 文件：{pf_path}", file=sys.stderr)
            sys.exit(1)
        holdings, total_margin = load_portfolio(pf_path)
        codes = [h['code'] for h in holdings]
        print(f"[i] 持仓 {len(holdings)} 只: {codes} | 融资余额 ¥{total_margin:,.0f}", file=sys.stderr)
        rt = fetch_realtime(codes)
        # 补齐实时 + hist + 浮盈 + 仓位
        total_mv = 0
        for h in holdings:
            r = rt.get(h['code']) or {}
            price = r.get('price') or h['cost']
            h['price'] = price
            h['rt'] = r
            h['mv'] = round(price * h['amount'], 0)
            h['pnl'] = round((price - h['cost']) * h['amount'], 0)
            h['pnl_pct'] = round((price - h['cost']) / h['cost'] * 100, 2) if h['cost'] else 0
            h['is_loss'] = h['pnl'] < 0
            total_mv += h['mv']
        for h in holdings:
            h['weight'] = round(h['mv'] / total_mv * 100, 2) if total_mv else 0
            h['is_heavy'] = h['weight'] >= 25
            hist = fetch_hist_ma(h['code'])
            h['hist'] = hist
            h['sl'] = derive_stop_loss(h['rt'], hist,
                                       is_heavy=h['is_heavy'],
                                       has_margin=h['has_margin'],
                                       cost=h['cost'])
            # 拉近 14 日公告（只保留 HIGH/MED 重要级）
            if not args.skip_announce:
                ann = fetch_announcements(h['code'], days=14)
                h['announce'] = [a for a in ann if a.get('level') in ('HIGH', 'MED')]
            else:
                h['announce'] = []
        print(render_portfolio(holdings, total_mv, total_margin))

    # ===== 模式 S =====
    elif mode == 'single':
        code = args.code or args.codes.split(',')[0].strip()
        rt = fetch_realtime([code])
        hist = fetch_hist_ma(code)
        data = {'rt': rt.get(code), 'hist': hist}
        print(render_single(code, data))

    # ===== 模式 M =====
    elif mode == 'multi':
        codes = [c.strip() for c in args.codes.split(',') if c.strip()]
        rt = fetch_realtime(codes)
        data = {}
        for c in codes:
            hist = fetch_hist_ma(c)
            data[c] = {'rt': rt.get(c), 'hist': hist}
        print(render_multi(codes, data))


if __name__ == '__main__':
    main()
