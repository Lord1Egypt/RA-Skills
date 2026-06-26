"""
Wyckoff 2.0 诊股系统 v4
- 支持 --side left/right/both 双视角分析
- 默认同时输出右侧趋势 + 左侧积累两份报告
- 失败自动重试（指数退避，最多3次）
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from wyckoff_engine import calculate_vp, detect_phase, score_stock, detect_columns
import efinance as ef
import pandas as pd
from bs_data import get_quote_history_bs
from ts_data import get_quote_history_ts


REQUEST_DELAY = 0.5
MAX_RETRIES = 2
RETRY_BASE_DELAY = 3


def diagnose_with_retry(code: str, delay: float = REQUEST_DELAY) -> dict:
    """诊股：三源优先级 tushare → baostock → efinance"""
    last_err = ''

    # 方法1: tushare（最全）
    for attempt in range(2):
        try:
            df, name = get_quote_history_ts(code, start_date='20200101', end_date='20500101')
            if df is not None and len(df) >= 60:
                return {'ok': True, 'result': None, 'code': code, 'name': name, 'df': df}
            last_err = f'数据不足（{len(df) if df is not None else 0}条K线）'
        except Exception as e:
            last_err = str(e)
        if attempt == 0:
            print(f'  [{code}] tushare 失败，尝试 baostock... ({last_err})')
            time.sleep(0.5)

    # 方法2: baostock
    for attempt in range(2):
        try:
            df, name = get_quote_history_bs(code, start_date='2020-01-01', end_date='2050-01-01')
            if df is not None and len(df) >= 60:
                return {'ok': True, 'result': None, 'code': code, 'name': name, 'df': df}
            last_err = f'数据不足（{len(df) if df is not None else 0}条K线）'
        except Exception as e:
            last_err = str(e)
        if attempt == 0:
            print(f'  [{code}] baostock 失败，尝试 efinance... ({last_err})')
            time.sleep(0.5)

    # 方法3: efinance
    for attempt in range(2):
        try:
            df = ef.stock.get_quote_history(
                code, beg='20220101', end='20500101', klt=101, fqt=1
            )
            if df is not None and len(df) >= 60:
                cols = detect_columns(df)
                name = df[cols.get('name', 'name')].iloc[-1] if cols.get('name') else code
                return {'ok': True, 'result': None, 'code': code, 'name': name, 'df': df}
            last_err = f'数据不足（{len(df) if df is not None else 0}条K线）'
        except Exception as e:
            last_err = str(e)
        if attempt == 0:
            print(f'  [{code}] efinance 失败，重试... ({last_err})')
            time.sleep(2)

    return {'ok': False, 'result': f'{code}: 三源均不可用: {last_err}'}


def format_side_report(sc: dict) -> str:
    """格式化单侧评分报告片段"""
    rating_map = {
        'S': '🅢 强烈推荐', 'A': '🄰 重点关注',
        'B': '🄱 观察', 'C': '🄲 不建议',
        'D': '🄳 回避', 'N': '未知',
    }
    side_label = '左侧积累' if sc['side'] == 'left' else '右侧趋势'
    icon = '📍' if sc['side'] == 'left' else '🚀'

    lines = []
    lines.append(f"  {icon} 【{side_label}】{rating_map.get(sc.get('rating', 'N'), sc.get('rating', 'N'))}  {sc.get('verdict', '')}")
    lines.append(f"     评分: {sc.get('score', 0)}/100")

    # 信号
    for g in sc.get('green_flags', []):
        lines.append(f"    {g}")
    for r in sc.get('red_flags', []):
        lines.append(f"    {r}")

    return '\n'.join(lines)


def format_report(code: str, name: str, df: pd.DataFrame, side: str = 'both') -> str:
    """
    格式化完整诊股报告
    side='right'  → 仅右侧趋势报告
    side='left'    → 仅左侧积累报告
    side='both'   → 双视角都输出
    """
    phase_desc = {
        'A': '筑底/筑顶（趋势停止）', 'B': '横盘（积累/派发区间）',
        'C': '测试（Spring/Upthrust）', 'D': '突破（趋势启动）',
        'E': '趋势运行中', 'unknown': '信号不足',
    }
    dir_desc = {
        'accumulation': '积累（看多✅）', 'distribution': '派发（看空🔴）',
        'spring_test': 'Spring测试（待确认⚠️）', 'upthrust_test': 'Upthrust测试（诱多🔴）',
        'uptrend': '上涨趋势✅', 'downtrend': '下跌趋势🔴',
        'uptrend_pullback': '上涨趋势回踩（正常⚠️）',
        'downtrend_pullback': '下跌趋势反弹',
        'stopping': '趋势停止',
        'breakout_up': '向上突破✅', 'breakout_down': '向下突破🔴',
    }

    prof = calculate_vp(df)
    ph = detect_phase(df)

    sides_to_run = ['right', 'left'] if side == 'both' else [side]
    side_scores = {}
    for s in sides_to_run:
        side_scores[s] = score_stock(df, mode=s)

    W = 58
    sep = '─' * W

    lines = []
    lines.append(f'┌{sep}┐')
    lines.append(f'│{" Wyckoff 诊股报告 ".center(W)}│')
    lines.append(f'│{name} ({code}){"".center(W - len(name) - len(code) - 4)}│')
    lines.append(f'└{sep}┘')

    # Phase 状态（共用）
    lines.append(f'\n【当前状态】（左🅻右🅡 双视角共用）')
    lines.append(f'  Phase: {ph["phase"]} - {phase_desc.get(ph["phase"], ph["phase"])}')
    lines.append(f'  方向: {ph["dir"]} - {dir_desc.get(ph["dir"], ph["dir"])}')
    lines.append(f'  置信度: {ph["conf"]}%')

    # 关键价位
    if prof:
        lines.append(f'\n【关键价位】')
        lines.append(f'  VPOC: {prof["vpoc"]}（控制点/重心）')
        lines.append(f'  VAH:  {prof["vah"]}（价值区上沿）')
        lines.append(f'  VAL:  {prof["val"]}（价值区下沿）')
        lines.append(f'  现价:  {prof["cur"]}  位置: {prof["position"]}')
        pos_emoji = '✅' if 'above' in prof['position'] else ('🔴' if 'below' in prof['position'] else '⚠️')
        lines.append(f'  {pos_emoji} 价格相对VPOC: {prof["position"]}')
        if prof.get('lvn'):
            lvn_str = ', '.join([f'LVN@{l["price"]}' for l in prof['lvn'][:3]])
            lines.append(f'  支撑（LVN）: {lvn_str}')
        if prof.get('hvn'):
            hvn_str = ', '.join([f'HVN@{h["price"]}' for h in prof['hvn'][:3]])
            lines.append(f'  阻力（HVN）: {hvn_str}')

    # 双视角评分
    lines.append(f'\n{sep}')
    lines.append(f'  📊 双视角评分')
    lines.append(f'{sep}')

    for s in sides_to_run:
        sc = side_scores[s]
        lines.append(f'\n{format_side_report(sc)}')

    # 阻力/支撑小结
    if prof:
        cur = prof['cur']
        vah = prof['vah']
        val = prof['val']
        vpoc = prof['vpoc']

        if side == 'both':
            r_sc = side_scores.get('right', {})
            l_sc = side_scores.get('left', {})
            r_rating = r_sc.get('rating', 'N')
            l_rating = l_sc.get('rating', 'N')

            lines.append(f'\n{sep}')
            lines.append(f'  📋 双视角综览')
            lines.append(f'{sep}')
            lines.append(f'  右侧🅡: {r_rating} | 左侧🅻: {l_rating} | 现价: {cur}')
            lines.append(f'  阻力区: {vah}~{prof["max_p"]}  |  支撑区: {prof["min_p"]}~{val}')

            # 综合建议
            if r_rating in ['S', 'A'] and l_rating in ['S', 'A']:
                lines.append(f'\n  ✅✅ 双重共振！右侧+左侧同时满足买入条件，重点关注！')
                lines.append(f'     止损: {val}  目标: {vah}')
            elif r_rating in ['S', 'A']:
                lines.append(f'\n  🚀 右侧趋势满足条件，等待回踩或突破确认后再买')
                lines.append(f'     止损: {val}  目标: {vah}')
            elif l_rating in ['S', 'A']:
                lines.append(f'\n  📍 左侧积累满足条件，耐心等待启动信号（放量阳线突破VPOC）')
                lines.append(f'     关注区间: {prof["min_p"]}~{val}  突破标志: 放量收复VPOC({vpoc})')
            else:
                verdict = r_sc.get('verdict', l_sc.get('verdict', ''))
                lines.append(f'\n  ⚠️ {verdict}')

    lines.append(f'\n{sep}')
    lines.append(f'  ⚠️ 本报告仅供参考，不构成投资建议')
    lines.append(f'{sep}')

    return '\n'.join(lines)


def diagnose_batch(codes: list, side: str = 'both'):
    """批量诊股"""
    results = []
    total = len(codes)
    for i, code in enumerate(codes):
        code = code.strip()
        if not code:
            continue
        print(f'\n[{i+1}/{total}] 正在诊断 {code}...')
        result = diagnose_with_retry(code)
        if result['ok']:
            text = format_report(result['code'], result['name'], result['df'], side=side)
            results.append({'ok': True, 'text': text})
        else:
            results.append({'ok': False, 'text': result['result']})
        if i < total - 1:
            time.sleep(REQUEST_DELAY)
    return results


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Wyckoff 诊股系统 v4')
    parser.add_argument('codes', nargs='*', help='股票代码（可多个）')
    parser.add_argument('-f', '--file', help='从文件批量读取股票代码（每行一个）')
    parser.add_argument('--side', default='both',
                        choices=['right', 'left', 'both'],
                        help='right=右侧趋势, left=左侧积累, both=两者都输出（默认both）')
    parser.add_argument('--delay', type=float, default=REQUEST_DELAY,
                        help=f'请求间隔秒数（默认{REQUEST_DELAY}s）')
    args = parser.parse_args()
    REQUEST_DELAY = args.delay

    codes = []
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            codes = [line.strip() for line in f if line.strip()]
    codes += [c.strip() for c in args.codes if c.strip()]

    if not codes:
        print('用法: python diagnose.py 000001')
        print('   python diagnose.py 000001 --side left')
        print('   python diagnose.py -f stocks.txt --side both')
        sys.exit(0)

    print(f'=' * 60)
    print(f'  Wyckoff 诊股系统 v4  |  共 {len(codes)} 只')
    print(f'  视角: {args.side}  |  间隔: {REQUEST_DELAY}s')
    print(f'=' * 60)

    results = diagnose_batch(codes, side=args.side)

    print(f'\n\n{"=" * 60}')
    print(f'  完成 | 成功: {sum(1 for r in results if r["ok"])} | 失败: {sum(1 for r in results if not r["ok"])}')
    print(f'{"=" * 60}\n')

    for r in results:
        print(r['text'])
        print()
