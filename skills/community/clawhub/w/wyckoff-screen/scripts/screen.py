"""
Wyckoff 2.0 选股扫描
每天收盘后运行，扫描全市场，找出积累末期候选股

用法:
  python screen.py               # 右侧趋势筛选（默认）
  python screen.py --left         # 左侧积累筛选
  python screen.py --mode left    # 同上
  python screen.py --mode both    # 两种都跑
"""

import sys
import time
import sqlite3
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wyckoff_engine import calculate_vp, detect_phase, score_stock
from screen_data import fetch_stock_data

import akshare as ak
import pandas as pd

# ========== 配置 ==========
DB_PATH = Path(__file__).parent.parent / 'data' / 'stocks.db'
LOOKBACK = 120
TOP_N = 20
REQUEST_DELAY = 0.3
BATCH_SLEEP = 2
BATCH_SIZE = 100

# 右侧阈值（趋势确认后买）
RIGHT_SCORE_THRESHOLD = 60
# 左侧阈值（低位埋伏）
LEFT_SCORE_THRESHOLD = 55


def init_db():
    """初始化SQLite数据库"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stock_daily (
            code TEXT, date TEXT,
            open REAL, close REAL, high REAL, low REAL,
            volume INTEGER, amount REAL,
            PRIMARY KEY (code, date)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS screening_results (
            date TEXT, rank INTEGER,
            code TEXT, name TEXT,
            side TEXT,
            phase TEXT, phase_dir TEXT,
            score INTEGER, signals TEXT,
            vpoc REAL, cur_price REAL,
            position TEXT,
            PRIMARY KEY (date, side, rank)
        )
    ''')
    conn.commit()
    return conn


def get_all_codes() -> list:
    """获取A股代码（仅深交所主板+中小企业板）"""
    df = ak.stock_info_a_code_name()
    all_codes = df['code'].tolist()
    szse_patterns = ('000', '001', '002')
    codes = [c for c in all_codes if str(c).startswith(szse_patterns)]
    codes = [c for c in codes if not str(c).startswith(('4', '8'))]
    print(f'  A股总数: {len(all_codes)} -> 筛选后: {len(codes)}（深交所主板+中小企业板）')
    return codes


def update_daily_data(conn: sqlite3.Connection, force: bool = False):
    """拉取/更新日线数据到SQLite"""
    codes = get_all_codes()
    today = pd.Timestamp.today().strftime('%Y-%m-%d')
    done, errors = 0, 0

    print(f'  开始更新日线数据（{len(codes)}只）...')
    for i, code in enumerate(codes):
        if i % 20 == 0:
            print(f'  进度: {i}/{len(codes)}...')
        if not force:
            c = conn.cursor()
            c.execute('SELECT 1 FROM stock_daily WHERE code=? AND date=?', (code, today))
            if c.fetchone():
                done += 1
                continue
        try:
            df = ef.stock.get_quote_history(code, beg='20230101', end='20500101', klt=101, fqt=1)
            time.sleep(REQUEST_DELAY)
            if df is None or len(df) == 0:
                continue
            df = df.rename(columns={
                '股票代码': 'code', '日期': 'date',
                '开盘': 'open', '收盘': 'close',
                '最高': 'high', '最低': 'low',
                '成交量': 'volume', '成交额': 'amount'
            })
            rows = df[['code', 'date', 'open', 'close', 'high', 'low', 'volume', 'amount']].values.tolist()
            conn.executemany('INSERT OR REPLACE INTO stock_daily VALUES (?,?,?,?,?,?,?,?)', rows)
            done += 1
        except Exception:
            errors += 1
            time.sleep(REQUEST_DELAY)
            continue
        if (i + 1) % BATCH_SIZE == 0:
            time.sleep(BATCH_SLEEP)

    conn.commit()
    print(f'  更新完成: {done}只成功, {errors}只失败')


def screen(conn: sqlite3.Connection, mode: str = 'right', top_n: int = TOP_N) -> pd.DataFrame:
    """
    执行选股扫描
    mode='right' → 右侧趋势筛选（突破确认后买）
    mode='left'  → 左侧积累筛选（低位埋伏）
    """
    threshold = LEFT_SCORE_THRESHOLD if mode == 'left' else RIGHT_SCORE_THRESHOLD
    mode_label = '左侧积累' if mode == 'left' else '右侧趋势'

    today = pd.Timestamp.today().strftime('%Y-%m-%d')
    c = conn.cursor()
    c.execute('SELECT DISTINCT code FROM stock_daily')
    all_codes = [r[0] for r in c.fetchall()]

    results = []
    print(f'  [{mode_label}] 开始扫描 {len(all_codes)} 只股票...')

    for i, code in enumerate(all_codes):
        if i % 50 == 0:
            print(f'  进度: {i}/{len(all_codes)}...')
        try:
            df = fetch_stock_data(code)
            time.sleep(REQUEST_DELAY)
            if df is None or len(df) < 60:
                continue
        except:
            time.sleep(REQUEST_DELAY)
            continue

        if (i + 1) % BATCH_SIZE == 0:
            time.sleep(BATCH_SLEEP)

        r = score_stock(df, mode=mode)
        if not r['pass']:
            continue

        name = code

        results.append({
            'code': code,
            'name': name,
            'side': mode,
            'phase': r['phase']['phase'],
            'phase_dir': r['phase']['dir'],
            'score': r['score'],
            'rating': r['rating'],
            'signals': ' | '.join(r['signals']),
            'vpoc': r['profile']['vpoc'],
            'cur': r['profile']['cur'],
            'position': r['profile']['position'],
            'verdict': r['verdict'],
        })

    df_result = pd.DataFrame(results)
    if len(df_result) == 0:
        print(f'  [{mode_label}] 没有找到符合条件的股票（阈值≥{threshold}）')
        return pd.DataFrame()

    df_result = df_result.sort_values('score', ascending=False).head(top_n)
    df_result = df_result.reset_index(drop=True)
    df_result.index = df_result.index + 1
    df_result.index.name = 'rank'

    # 存库
    c.execute('DELETE FROM screening_results WHERE date=? AND side=?', (today, mode))
    for rank, row in df_result.iterrows():
        c.execute('''
            INSERT INTO screening_results VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (today, rank, row['code'], row['name'], row['side'],
              row['phase'], row['phase_dir'], row['score'],
              row['signals'], row['vpoc'], row['cur'], row['position']))
    conn.commit()

    print(f'  [{mode_label}] 扫描完成，找到 {len(df_result)} 只候选股（阈值≥{threshold}）')
    return df_result


def format_result(df: pd.DataFrame, mode: str = 'right') -> str:
    """格式化输出"""
    if len(df) == 0:
        return '今日无符合条件的股票'

    mode_label = '左侧积累' if mode == 'left' else '右侧趋势'
    threshold = LEFT_SCORE_THRESHOLD if mode == 'left' else RIGHT_SCORE_THRESHOLD
    today = pd.Timestamp.today().strftime('%Y-%m-%d')

    # 侧栏宽度
    W = 64
    sep = '━' * W

    lines = []
    lines.append(f'{"┌"}{"─"*W}{"┐"}')
    lines.append(f'│{" Wyckoff 2.0 选股结果 ".center(W)}│')
    lines.append(f'│{" "+today+" | "+mode_label+" | 阈值"+str(threshold)+" ".center(W)}│')
    lines.append(f'{"└"}{"─"*W}{"┘"}')

    for rank, row in df.iterrows():
        rating_icon = {'S': '🅖', 'A': '✅', 'B': '🅑', 'C': '⚠️', 'D': '🅕'}.get(row.get('rating', ''), '?')

        lines.append(f'  {sep}')
        lines.append(f'  #{rank}  {row["name"]} ({row["code"]})  {rating_icon} {row.get("rating","?")}')
        lines.append(f'  {sep}')
        lines.append(f'   Phase : {row["phase"]} / {row["phase_dir"]}')
        lines.append(f'   评分  : {row["score"]}/100')
        lines.append(f'   现价  : {row["cur"]}  |  VPOC: {row["vpoc"]}  |  位置: {row["position"]}')
        verdict = row.get('verdict', '')
        if verdict:
            lines.append(f'   结论  : {verdict}')
        signals = row['signals']
        if len(signals) > 80:
            # 分行显示信号
            parts = signals.split(' | ')
            line = '   信号  : '
            for p in parts:
                if len(line + p) > W + 8:
                    lines.append(line.rstrip(' ,'))
                    line = '          ' + p + ' | '
                else:
                    line += p + ' | '
            lines.append(line.rstrip(' |'))
        else:
            lines.append(f'   信号  : {signals}')

    lines.append(f'  {"━"*W}')
    lines.append(f'   共 {len(df)} 只候选股  |  规则: 评分≥{threshold} + Wyckoff {mode_label}结构')
    lines.append(f'  {"━"*W}')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Wyckoff 2.0 选股系统')
    parser.add_argument('--mode', default='right',
                        choices=['right', 'left', 'both'],
                        help='right=右侧趋势筛选, left=左侧积累筛选, both=两种都跑')
    parser.add_argument('--top', type=int, default=TOP_N, help=f'输出前N只（默认{TOP_N}）')
    parser.add_argument('--force-update', action='store_true', help='强制全量更新日线数据')
    args = parser.parse_args()

    print('=' * 60)
    print('  Wyckoff 2.0 选股系统')
    print(f'  模式: {args.mode}')
    print('=' * 60)

    conn = init_db()
    update_daily_data(conn, force=args.force_update)

    all_results = {}
    modes = ['right', 'left'] if args.mode == 'both' else [args.mode]

    for mode in modes:
        result = screen(conn, mode=mode, top_n=args.top)
        all_results[mode] = result

    print()
    for mode, result in all_results.items():
        txt = format_result(result, mode=mode)
        print(txt)
        print()

    # 保存
    today = pd.Timestamp.today().strftime('%Y-%m-%d')
    out_path = Path(__file__).parent.parent / 'data' / f'screen_{today}.txt'
    with open(out_path, 'w', encoding='utf-8') as f:
        for mode, result in all_results.items():
            f.write(format_result(result, mode=mode) + '\n\n')
    print(f'结果已保存: {out_path}')


if __name__ == '__main__':
    main()
