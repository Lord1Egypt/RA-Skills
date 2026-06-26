"""
Wyckoff 2.0 选股扫描 - 深市主板专用版(000xxx + 001xxx)
"""

import sys
import time
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wyckoff_engine import calculate_vp, detect_phase, score_stock

import efinance as ef
import akshare as ak
import pandas as pd

# ========== 配置 ==========
DB_PATH = Path(__file__).parent.parent / 'data' / 'stocks_sz_mainboard.db'
LOOKBACK = 120
TOP_N = 20
REQUEST_DELAY = 0.5  # 每次请求间隔0.5秒，防限流


def init_db():
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
            phase TEXT, phase_dir TEXT,
            score INTEGER, signals TEXT,
            vpoc REAL, cur_price REAL,
            reason TEXT,
            PRIMARY KEY (date, rank)
        )
    ''')
    conn.commit()
    return conn


def get_sz_mainboard_codes() -> list:
    """获取深市主板代码(000xxx + 001xxx)"""
    df = ak.stock_info_a_code_name()
    codes = df['code'].tolist()
    # 过滤深市主板: 000xxx 和 001xxx
    sz_mainboard = [c for c in codes if c.startswith('000') or c.startswith('001')]
    print(f'  深市主板总数: {len(sz_mainboard)}')
    return sz_mainboard


def update_daily_data(conn: sqlite3.Connection, force: bool = False):
    codes = get_sz_mainboard_codes()
    today = pd.Timestamp.today().strftime('%Y-%m-%d')

    done = 0
    errors = 0
    skipped = 0

    print(f'  开始更新日线数据（{len(codes)}只）...')

    for i, code in enumerate(codes):
        if i % 50 == 0:
            print(f'  进度: {i}/{len(codes)}...')

        # 查是否已有今日数据（有缓存且非force，直接跳过）
        if not force:
            c = conn.cursor()
            c.execute('SELECT 1 FROM stock_daily WHERE code=? AND date=?', (code, today))
            if c.fetchone():
                skipped += 1
                continue

        try:
            df = ef.stock.get_quote_history(
                code,
                beg='20230101',
                end='20500101',
                klt=101,
                fqt=1
            )
            if df is None or len(df) == 0:
                errors += 1
                time.sleep(REQUEST_DELAY)
                continue

            df = df.rename(columns={
                '股票代码': 'code', '日期': 'date',
                '开盘': 'open', '收盘': 'close',
                '最高': 'high', '最低': 'low',
                '成交量': 'volume', '成交额': 'amount'
            })

            rows = df[['code', 'date', 'open', 'close', 'high', 'low', 'volume', 'amount']].values.tolist()
            conn.executemany(
                'INSERT OR REPLACE INTO stock_daily VALUES (?,?,?,?,?,?,?,?)', rows
            )
            done += 1
            time.sleep(REQUEST_DELAY)  # 防限流
        except Exception as e:
            errors += 1
            time.sleep(REQUEST_DELAY)
            continue

    conn.commit()
    print(f'  更新完成: {done}只成功, {errors}只失败, {skipped}只跳过(已有缓存)')


def screen(conn: sqlite3.Connection) -> pd.DataFrame:
    today = pd.Timestamp.today().strftime('%Y-%m-%d')
    c = conn.cursor()

    c.execute('SELECT DISTINCT code FROM stock_daily')
    all_codes = [r[0] for r in c.fetchall()]

    results = []
    print(f'  开始扫描 {len(all_codes)} 只股票...')

    for i, code in enumerate(all_codes):
        if i % 50 == 0:
            print(f'  进度: {i}/{len(all_codes)}...')

        try:
            df = ef.stock.get_quote_history(
                code,
                beg='20230101',
                end='20500101',
                klt=101,
                fqt=1
            )
            if df is None or len(df) < 60:
                continue
            df = df.rename(columns={
                '股票代码': 'code', '日期': 'date',
                '开盘': 'open', '收盘': 'close',
                '最高': 'high', '最低': 'low',
                '成交量': 'volume', '成交额': 'amount'
            })
        except:
            continue

        r = score_stock(df)
        if not r['pass']:
            continue

        try:
            name = df['股票名称'].iloc[-1] if '股票名称' in df.columns else code
        except:
            name = code

        results.append({
            'code': code,
            'name': name,
            'phase': r['phase']['phase'],
            'phase_dir': r['phase']['dir'],
            'score': r['score'],
            'signals': ' | '.join(r['signals']),
            'vpoc': r['profile']['vpoc'],
            'cur': r['profile']['cur'],
            'position': r['profile']['position'],
        })
        time.sleep(REQUEST_DELAY)

    df_result = pd.DataFrame(results)
    if len(df_result) == 0:
        print('  没有找到符合条件的股票')
        return pd.DataFrame()

    df_result = df_result.sort_values('score', ascending=False).head(TOP_N)
    df_result = df_result.reset_index(drop=True)
    df_result.index = df_result.index + 1
    df_result.index.name = 'rank'

    c.execute('DELETE FROM screening_results WHERE date=?', (today,))
    for rank, row in df_result.iterrows():
        c.execute('''
            INSERT INTO screening_results VALUES (?,?,?,?,?,?,?,?,?,?,?)
        ''', (today, rank, row['code'], row['name'],
              row['phase'], row['phase_dir'], row['score'],
              row['signals'], row['vpoc'], row['cur'], row['position']))
    conn.commit()

    print(f'  扫描完成，找到 {len(df_result)} 只候选股')
    return df_result


def format_result(df: pd.DataFrame) -> str:
    if len(df) == 0:
        return '今日无符合条件的股票'

    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"  Wyckoff 选股结果 - 深市主板  ({pd.Timestamp.today().strftime('%Y-%m-%d')})")
    lines.append(f"{'='*60}")

    for rank, row in df.iterrows():
        lines.append(f"\n#{rank}  {row['name']} ({row['code']})")
        lines.append(f"   Phase: {row['phase']} | {row['phase_dir']} | 评分: {row['score']}/100")
        lines.append(f"   现价: {row['cur']}  |  VPOC: {row['vpoc']}  |  位置: {row['position']}")
        lines.append(f"   信号: {row['signals']}")

    lines.append(f"\n{'='*60}")
    lines.append(f"  共 {len(df)} 只候选股 | 规则: 评分≥60 + Wyckoff积累/突破结构")
    lines.append(f"{'='*60}")
    return '\n'.join(lines)


if __name__ == '__main__':
    print('Wyckoff 选股系统 - 深市主板 启动...')

    conn = init_db()
    update_daily_data(conn)
    result = screen(conn)

    txt = format_result(result)
    print('\n' + txt)

    today = pd.Timestamp.today().strftime('%Y-%m-%d')
    out_path = Path(__file__).parent.parent / 'data' / f'screen_sz_{today}.txt'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    print(f'\n结果已保存: {out_path}')
