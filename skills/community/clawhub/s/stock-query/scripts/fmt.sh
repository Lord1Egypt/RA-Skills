#!/usr/bin/env bash
# fmt.sh — stock-query 格式化输出工具
# 用法:
#   bash scripts/sq.sh get AAPL 00700 | bash scripts/fmt.sh
#   bash scripts/sq.sh get AAPL 00700 | bash scripts/fmt.sh --format table --detail
#   bash scripts/sq.sh hist 600519    | bash scripts/fmt.sh --format csv
#   bash scripts/sq.sh get AAPL      | bash scripts/fmt.sh --format json --detail
#
# --format / -f:  table（默认）| json | csv
# --detail / -d:  显示扩展字段（独立 boolean，与 --format 正交）
#
# 输入自动识别：JSON 数组 → sq get 行情；含 klines 字段的对象 → sq hist 历史K线

set -uo pipefail

FORMAT="table"
DETAIL="false"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --format|-f) FORMAT="${2:-table}"; shift 2 ;;
    --detail|-d) DETAIL="true"; shift ;;
    *) printf 'Usage: fmt.sh [--format table|json|csv] [--detail]\n' >&2; exit 1 ;;
  esac
done

if ! command -v python3 &>/dev/null; then
  printf 'Error: python3 is required\n' >&2; exit 1
fi

INPUT=$(cat)
[[ -z "$INPUT" ]] && exit 0

_PY=$(mktemp /tmp/sqfmt_XXXXXX.py)
trap 'rm -f "$_PY"' EXIT INT TERM

cat > "$_PY" << 'PYEOF'
import json, sys, unicodedata, io, csv as csv_mod

FMT    = sys.argv[1] if len(sys.argv) > 1 else 'table'
DETAIL = len(sys.argv) > 2 and sys.argv[2] == 'true'

text = sys.stdin.read()
data = json.loads(text, parse_float=str)

# ── Display utilities ──────────────────────────────────────────────────────────

def dw(s):
    w = 0
    for c in str(s):
        w += 2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1
    return w

def pad(s, width):
    s = str(s)
    return s + ' ' * max(0, width - dw(s))

def make_table(headers, rows):
    widths = [dw(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], dw(str(cell)))
    def render(cells):
        return '| ' + ' | '.join(pad(str(c), w) for c, w in zip(cells, widths)) + ' |'
    def sep():
        return '|' + '|'.join('-' * (w + 2) for w in widths) + '|'
    lines = [render(headers), sep()]
    for row in rows:
        lines.append(render(row))
    return '\n'.join(lines)

def make_csv(headers, rows):
    out = io.StringIO()
    w = csv_mod.writer(out)
    w.writerow(headers)
    w.writerows([[str(c) for c in row] for row in rows])
    return out.getvalue()

# ── Field formatters ───────────────────────────────────────────────────────────

def f_price(v):
    return '—' if v is None else str(v)

def f_pct(change_pct, direction, market, itype=None, is_estimate=None):
    if change_pct is None:
        return '—'
    pct_f = float(change_pct)
    if market in ('A股', '港股'):
        emoji = '🔴' if pct_f > 0 else ('🟢' if pct_f < 0 else '⚪')
    else:
        emoji = '🟩' if pct_f > 0 else ('🟥' if pct_f < 0 else '⚪')
    sign = '+' if pct_f >= 0 else ''
    r = f'{emoji} {sign}{pct_f:.2f}%'
    if itype == 'fund' and is_estimate is not None:
        r += '（估）' if is_estimate else '（净值）'
    return r

def f_change(v):
    if v is None:
        return '—'
    v_f = float(v)
    return ('+' if v_f >= 0 else '') + str(v)

def f_volume(v, market):
    if v is None:
        return '—'
    v_i = int(float(str(v)))
    if market in ('A股', '港股'):
        return f'{v_i / 10000:.1f}万手'
    return str(v_i)

def f_amount(v):
    if v is None:
        return '—'
    v_f = float(str(v))
    if v_f >= 10000:
        return f'{v_f / 10000:.2f}亿'
    return f'{v_f:,.0f}万'

def f_turnover(v):
    return '—' if v is None else f'{float(str(v)):.2f}%'

def f_datetime(v):
    if v is None:
        return '—'
    return v[:16] if len(v) == 19 else v

def f_ma(v):
    if v is None:
        return '—'
    return f'{float(v):.2f}' if isinstance(v, str) else f'{v:.2f}'

def f_vol_ma(v, mkt):
    if v is None:
        return '—'
    if mkt in ('A股', '港股'):
        return f'{float(v) / 10000:.1f}万手'
    return f'{float(v):.0f}'

# ── Detect input type ─────────────────────────────────────────────────────────

is_hist = isinstance(data, dict) and 'klines' in data

# ── Hist (sq hist) ────────────────────────────────────────────────────────────

if is_hist:
    if data.get('error'):
        print(f'⚠ {data.get("code", "")}: {data["error"]}')
        sys.exit(0)

    code   = data.get('code', '')
    name   = data.get('name') or code
    market = data.get('market', '')
    period = data.get('period', 'day')
    fq     = data.get('fq', 'pre')
    klines = data.get('klines', [])

    dc = data.get('display_count') or 0
    display_klines = klines[-dc:] if (dc > 0 and dc < len(klines)) else klines

    period_label = {'day': '日K', 'week': '周K', 'month': '月K'}.get(period, period)
    fq_label     = {'pre': '前复权', 'post': '后复权', 'none': '不复权'}.get(fq, fq)

    # Compute MA5/MA10 on all klines (oldest → newest)
    closes_list = [float(str(k['close'])) for k in klines]
    volumes_list = [float(str(k['volume'])) if k.get('volume') is not None else None
                    for k in klines]

    def compute_ma(vals, idx, n):
        if idx + 1 < n:
            return None
        window = vals[idx - n + 1: idx + 1]
        if any(v is None for v in window):
            return None
        return round(sum(window) / n, 2)

    ma_by_idx = [{'ma5':     compute_ma(closes_list,  i, 5),
                  'ma10':    compute_ma(closes_list,  i, 10),
                  'vol_ma5': compute_ma(volumes_list, i, 5),
                  'vol_ma10':compute_ma(volumes_list, i, 10)}
                 for i in range(len(klines))]

    # ── Headers & row builder ──────────────────────────────────────────────────
    BASE_H    = ['日期', '收盘', '涨跌幅', 'MA5', 'MA10', '开盘', '最高', '最低', '成交量']
    DETAIL_H  = BASE_H + ['涨跌额', '振幅', '成交额', '换手率', '量MA5', '量MA10']
    headers   = DETAIL_H if DETAIL else BASE_H

    def hist_row(k, mas):
        cp   = k.get('change_pct')
        cp_f = float(cp) if cp is not None else None
        dir_ = ('up' if cp_f > 0 else ('down' if cp_f < 0 else 'flat')) if cp_f is not None else 'flat'
        row = [
            k.get('date') or '—',
            f_price(k.get('close')),
            f_pct(cp, dir_, market),
            f_ma(mas['ma5']),
            f_ma(mas['ma10']),
            f_price(k.get('open')),
            f_price(k.get('high')),
            f_price(k.get('low')),
            f_volume(k.get('volume'), market),
        ]
        if DETAIL:
            row += [
                f_change(k.get('change')),
                f_turnover(k.get('amplitude')),
                f_amount(k.get('amount')),
                f_turnover(k.get('turnover')),
                f_vol_ma(mas['vol_ma5'],  market),
                f_vol_ma(mas['vol_ma10'], market),
            ]
        return row

    if not display_klines:
        if FMT == 'json':
            print(json.dumps({'code': code, 'name': name, 'market': market,
                              'period': period, 'fq': fq, 'klines': []}, ensure_ascii=False))
        elif FMT == 'csv':
            print(make_csv(headers, []), end='')
        else:
            print(f'{name}（{code}）{period_label} · {fq_label} · 共0条\n\n（无数据）')
        sys.exit(0)

    rows = []
    for i, k in enumerate(reversed(display_klines)):
        orig_idx = len(klines) - 1 - i
        rows.append(hist_row(k, ma_by_idx[orig_idx]))

    if FMT == 'table':
        print(f'{name}（{code}）{period_label} · {fq_label} · 共{len(display_klines)}条\n')
        print(make_table(headers, rows))
        if len(display_klines) >= 2:
            first_c = float(str(display_klines[0]['close']))
            last_c  = float(str(display_klines[-1]['close']))
            rng     = (last_c - first_c) / first_c * 100
            sign    = '+' if rng >= 0 else ''
            closes  = [(float(str(k['close'])), k['date']) for k in display_klines]
            max_c, max_d = max(closes, key=lambda x: x[0])
            min_c, min_d = min(closes, key=lambda x: x[0])
            print(f'\n📊 区间统计：{display_klines[0]["date"]} ~ {display_klines[-1]["date"]}'
                  f' · 涨跌幅 {sign}{rng:.2f}%'
                  f' · 最高 {max_c}（{max_d[5:]}）'
                  f' · 最低 {min_c}（{min_d[5:]}）')

    elif FMT == 'csv':
        print(make_csv(headers, rows), end='')

    elif FMT == 'json':
        kline_dicts = []
        for i, k in enumerate(display_klines):
            orig_idx = len(klines) - len(display_klines) + i
            mas = ma_by_idx[orig_idx]
            d = {
                'date':       k.get('date'),
                'close':      k.get('close'),
                'change_pct': k.get('change_pct'),
                'ma5':        mas['ma5'],
                'ma10':       mas['ma10'],
                'open':       k.get('open'),
                'high':       k.get('high'),
                'low':        k.get('low'),
                'volume':     k.get('volume'),
            }
            if DETAIL:
                d['change']    = k.get('change')
                d['amplitude'] = k.get('amplitude')
                d['amount']    = k.get('amount')
                d['turnover']  = k.get('turnover')
                d['vol_ma5']   = mas['vol_ma5']
                d['vol_ma10']  = mas['vol_ma10']
            kline_dicts.append(d)
        print(json.dumps({'code': code, 'name': name, 'market': market,
                          'period': period, 'fq': fq, 'klines': kline_dicts},
                         ensure_ascii=False, indent=2))

    sys.exit(0)

# ── Get (sq get / sq fund) ────────────────────────────────────────────────────

items  = data if isinstance(data, list) else [data]
valid  = [it for it in items if not it.get('error')]
errors = [it for it in items if it.get('error')]

BASE_H   = ['代码', '名称', '市场', '最新价', '昨收', '涨跌幅', '最高', '最低', '币种', '更新时间']
DETAIL_H = ['代码', '名称', '市场', '最新价', '昨收', '今开', '涨跌幅', '涨跌额',
            '最高', '最低', '成交量', '成交额', '换手率', '市盈率PE',
            '52W最高', '52W最低', 'MA5', 'MA10', '量MA5', '量MA10', '币种', '更新时间']
headers = DETAIL_H if DETAIL else BASE_H

def get_row(it):
    market = it.get('market') or '—'
    pct    = it.get('change_pct')
    dir_   = it.get('direction', 'flat')
    itype  = it.get('type')
    is_est = it.get('is_estimate')
    if DETAIL:
        return [
            it.get('code') or '—',
            it.get('name') or '—',
            market,
            f_price(it.get('price')),
            f_price(it.get('prev_close')),
            f_price(it.get('open')),
            f_pct(pct, dir_, market, itype, is_est),
            f_change(it.get('change')),
            f_price(it.get('high')),
            f_price(it.get('low')),
            f_volume(it.get('volume'), market),
            f_amount(it.get('amount')),
            f_turnover(it.get('turnover')),
            f_price(it.get('pe')),
            f_price(it.get('week52_high')),
            f_price(it.get('week52_low')),
            f_ma(it.get('ma5')),
            f_ma(it.get('ma10')),
            f_vol_ma(it.get('vol_ma5'),  market),
            f_vol_ma(it.get('vol_ma10'), market),
            it.get('currency') or '—',
            f_datetime(it.get('datetime')),
        ]
    return [
        it.get('code') or '—',
        it.get('name') or '—',
        market,
        f_price(it.get('price')),
        f_price(it.get('prev_close')),
        f_pct(pct, dir_, market, itype, is_est),
        f_price(it.get('high')),
        f_price(it.get('low')),
        it.get('currency') or '—',
        f_datetime(it.get('datetime')),
    ]

rows = [get_row(it) for it in valid]

def item_to_dict(it):
    market = it.get('market')
    base = {
        'code':       it.get('code'),
        'name':       it.get('name'),
        'market':     market,
        'price':      it.get('price'),
        'prev_close': it.get('prev_close'),
        'change_pct': it.get('change_pct'),
        'high':       it.get('high'),
        'low':        it.get('low'),
        'currency':   it.get('currency'),
        'datetime':   it.get('datetime'),
    }
    if DETAIL:
        base.update({
            'open':        it.get('open'),
            'change':      it.get('change'),
            'volume':      it.get('volume'),
            'amount':      it.get('amount'),
            'turnover':    it.get('turnover'),
            'pe':          it.get('pe'),
            'week52_high': it.get('week52_high'),
            'week52_low':  it.get('week52_low'),
            'ma5':         it.get('ma5'),
            'ma10':        it.get('ma10'),
            'vol_ma5':     it.get('vol_ma5'),
            'vol_ma10':    it.get('vol_ma10'),
        })
    return base

if FMT == 'table':
    if rows:
        print(make_table(headers, rows))
    for it in errors:
        print(f'\n⚠ {it["code"]}: {it["error"]}')

elif FMT == 'csv':
    print(make_csv(headers, rows), end='')

elif FMT == 'json':
    out = [item_to_dict(it) for it in valid]
    for it in errors:
        out.append({'code': it.get('code'), 'error': it.get('error')})
    print(json.dumps(out, ensure_ascii=False, indent=2))

# Annotations (table / csv only)
if FMT in ('table', 'csv'):
    qdii = [it for it in valid if it.get('is_qdii')]
    if qdii:
        codes = ', '.join(it['code'] for it in qdii)
        print(f'\n⏳ QDII基金，净值公布有 T+2~T+7 延迟：{codes}')
PYEOF

printf '%s' "$INPUT" | python3 "$_PY" "$FORMAT" "$DETAIL"
