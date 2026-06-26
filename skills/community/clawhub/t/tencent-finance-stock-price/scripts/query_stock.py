#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Universal stock data query tool via Tencent Finance API (qt.gtimg.cn).
Supports A-shares, HK stocks, and US stocks. No API key required.

Usage:
  uv run query_stock.py [--detail] <code1> [code2] ...
  uv run query_stock.py --help

Codes: sh000001 (上证指数), hkHSI (恒生指数), usINX (标普500)
       sh688008 (澜起科技), hk02026 (小马智行), usWOLF (Wolfspeed)
       Or raw: 688008, 02026
"""

import sys
import io

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

import urllib.request
import urllib.parse
import re

# ==========================================
# Code auto-prefix logic (no hardcoded names)
# ==========================================
def resolve_code(code):
    """Auto-prefix raw codes. Already-prefixed codes pass through."""
    if code.startswith(('sh', 'sz', 'hk', 'us')) and len(code) > 2:
        return code
    if code.isdigit():
        if len(code) == 6:
            if code.startswith(('6', '0')) and code[0] != '0':
                return f'sh{code}'
            if code.startswith(('0', '3')):
                return f'sz{code}'
        if len(code) == 5 and code.startswith('0'):
            return f'hk{code}'
    return code


def query_stocks(codes):
    resolved = [resolve_code(c) for c in codes]
    url = f"http://qt.gtimg.cn/q={urllib.parse.quote(','.join(resolved))}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            raw = resp.read()
    except Exception as e:
        print(f"网络错误: {e}")
        sys.exit(1)

    try:
        data = raw.decode('gb2312')
    except UnicodeDecodeError:
        try:
            data = raw.decode('gbk')
        except UnicodeDecodeError:
            data = raw.decode('utf-8', errors='ignore')

    results = []
    for line in data.split(';'):
        line = line.strip()
        if not line.startswith('v_'):
            continue
        m = re.match(r'v_(\w+)="(.+)"', line)
        if not m:
            continue
        api_code, values = m.groups()
        parts = values.split('~')
        if len(parts) < 35:
            continue

        # === Step 1: Market detection via index [0] ===
        mk = parts[0]
        if mk in ('1', '51'):
            market = 'A'
        elif mk == '100':
            market = 'HK'
        elif mk == '200':
            market = 'US'
        else:
            market = '?'

        # === Step 2: Common fields [1]-[34] ===
        name = parts[1]
        code = parts[2]
        price = parts[3]
        prev_close = parts[4]
        open_price = parts[5]
        update_time = parts[30] if len(parts) > 30 else ''
        change = parts[31]
        pct = parts[32]
        high = parts[33]
        low = parts[34]

        try:
            pct_f = float(pct)
            emoji = "🟢" if pct_f >= 0 else "🔴"
        except (ValueError, TypeError):
            emoji = "⚪"
            pct_f = 0.0

        r = {
            'market': market, 'code': code, 'name': name,
            'price': price, 'prev_close': prev_close, 'open': open_price,
            'change': change, 'pct': pct, 'pct_f': pct_f, 'emoji': emoji,
            'high': high, 'low': low, 'update_time': update_time,
            'api_code': api_code,
        }

        # === Step 3: Volume with auto-unit detection ===
        # API returns shares for HK/US, but for A-shares the unit varies:
        # most A-shares return 手, some high-volume ones return 股.
        # Detect using turnover rate cross-validation when available.
        raw_vol = parts[6] if len(parts) > 6 else '0'

        if market == 'A':
            # Cross-validate with turnover rate
            tr_rate_str = parts[38] if len(parts) > 38 else ''
            circ_sh_str = parts[72] if len(parts) > 72 else ''
            total_sh_str = parts[73] if len(parts) > 73 else ''
            try:
                tr_rate = float(tr_rate_str) if tr_rate_str else 0
                csh = float(circ_sh_str) if circ_sh_str else 0
                tsh = float(total_sh_str) if total_sh_str else 0
                raw = float(raw_vol)
                ref = csh if csh > 0 else tsh
                est = ref * tr_rate / 100 if tr_rate > 0 and ref > 0 else 0
                if est > 0:
                    if abs(raw - est) <= abs(raw * 100 - est):
                        r['volume'] = raw_vol
                    else:
                        r['volume'] = str(int(raw * 100))
                else:
                    r['volume'] = str(int(raw * 100))
            except (ValueError, TypeError):
                r['volume'] = str(int(float(raw_vol) * 100))
            r['turnover'] = parts[37] if len(parts) > 37 else '0'
            r['currency'] = 'CNY'
        else:
            r['volume'] = raw_vol
            r['turnover'] = parts[37] if len(parts) > 37 else '0'
            r['currency'] = 'HKD' if market == 'HK' else (parts[35] if len(parts) > 35 else 'USD')

        # === Step 4: Differentiated fields [35+] ===
        if market == 'A':
            r['circ_mktcap'] = parts[44] if len(parts) > 44 else ''   # 亿 CNY
            r['total_mktcap'] = parts[45] if len(parts) > 45 else ''  # 亿 CNY
            r['pe'] = parts[39] if len(parts) > 39 else ''
            r['pb'] = parts[46] if len(parts) > 46 else ''
            r['turnover_rate'] = parts[38] if len(parts) > 38 else ''  # %
            r['amplitude'] = parts[43] if len(parts) > 43 else ''       # %
            r['high52'] = parts[47] if len(parts) > 47 else ''
            r['low52'] = parts[48] if len(parts) > 48 else ''
            r['total_shares'] = parts[73] if len(parts) > 73 else ''
            r['circ_shares'] = parts[72] if len(parts) > 72 else ''
        elif market == 'HK':
            r['circ_mktcap'] = parts[44] if len(parts) > 44 else ''   # 亿 HKD
            r['total_mktcap'] = parts[45] if len(parts) > 45 else ''  # 亿 HKD
            r['pe'] = parts[39] if len(parts) > 39 else ''             # TTM PE
            r['pb'] = parts[43] if len(parts) > 43 else ''
            r['high52'] = parts[48] if len(parts) > 48 else ''
            r['low52'] = parts[49] if len(parts) > 49 else ''
            r['total_shares'] = parts[69] if len(parts) > 69 else ''
            r['circ_shares'] = parts[70] if len(parts) > 70 else ''
            r['lot_size'] = parts[60] if len(parts) > 60 else ''
            r['adr_ratio'] = parts[42] if len(parts) > 42 else ''
        elif market == 'US':
            r['circ_mktcap'] = parts[44] if len(parts) > 44 else ''
            r['total_mktcap'] = parts[45] if len(parts) > 45 else ''
            r['pe'] = parts[38] if len(parts) > 38 else ''
            r['pb'] = parts[43] if len(parts) > 43 else ''
            r['high52'] = parts[48] if len(parts) > 48 else ''
            r['low52'] = parts[49] if len(parts) > 49 else ''
            r['total_shares'] = parts[62] if len(parts) > 62 else ''
            r['circ_shares'] = parts[63] if len(parts) > 63 else ''
            r['adr_ratio'] = parts[42] if len(parts) > 42 else ''
            r['eng_name'] = parts[46] if len(parts) > 46 else ''

        # Index detection for skip-mktcap
        r['is_index'] = (
            (market == 'A' and code.startswith('000')) or
            api_code in ('hkHSI', 'hkHSTECH', 'usINX', 'usDJI', 'usIXIC', 'usNDX')
        )

        results.append(r)
    return results


# ==========================================
# Formatting helpers
# ==========================================
def fmt_num(n, unit=''):
    """Format a numeric string for display."""
    if not n or n in ('0', '0.0', '0.00'):
        return '-'
    try:
        f = float(n)
        if unit == 'shares':
            if f >= 1e8: return f'{f/1e8:.2f}亿'
            if f >= 1e4: return f'{f/1e4:.2f}万'
            return f'{f:.0f}'
        if unit == 'volume_a':
            if f >= 1e8: return f'{f/1e8:.2f}亿'
            if f >= 1e4: return f'{f/1e4:.2f}万'
            return f'{f:.0f}'
        if unit == 'turnover_a':
            # A-share turnover in 万元
            if f >= 1e4: return f'{f/1e4:.2f}亿'
            return f'{f:.2f}万'
        if unit == 'turnover_hk':
            # HK turnover in HKD 元
            if f >= 1e8: return f'{f/1e8:.2f}亿'
            if f >= 1e4: return f'{f/1e4:.2f}万'
            return f'{f:.2f}'
        # Auto
        if f >= 1e12: return f'{f/1e12:.2f}T'
        if f >= 1e8: return f'{f/1e8:.2f}亿'
        if f >= 1e4: return f'{f/1e4:.2f}万'
        return f'{f:.2f}'
    except (ValueError, TypeError):
        return n


def fmt_mktcap(n, currency=''):
    """Format market cap (in 亿, local currency)."""
    if not n or n == '0':
        return '-'
    try:
        f = float(n)
        if f >= 10000:
            return f'{f/10000:.1f}T {currency}'.strip()
        if f >= 1:
            return f'{f:.0f}亿 {currency}'.strip()
        return f'{f:.2f}亿 {currency}'.strip()
    except (ValueError, TypeError):
        return str(n)


# ==========================================
# Output
# ==========================================
def print_compact(results):
    print(f"{'名称':<16} {'价格':>10} {'涨跌':>10} {'涨跌幅':>8} {'市值':>16}")
    print("-" * 66)
    for r in results:
        mkt = ''
        if not r.get('is_index'):
            mkt_cap = r.get('total_mktcap', '') or r.get('circ_mktcap', '')
            if mkt_cap:
                mkt = fmt_mktcap(mkt_cap, r.get('currency', ''))
        mkt_s = mkt if mkt else '-'
        try:
            px = float(r['price'])
            ps = f'{px:>10.2f}'
        except (ValueError, TypeError):
            ps = f'{r["price"]:>10}'
        print(f"{r['name']:<16} {ps} {r['change']:>10} {r['emoji']} {r['pct']:>6}% {mkt_s:>16}")


def print_detail(results):
    for r in results:
        print(f"\n{'='*60}")
        print(f"  {r['name']} ({r['code']})  {'A股' if r['market']=='A' else '港股' if r['market']=='HK' else '美股'}")
        print(f"{'='*60}")
        print(f"  价格: {r['price']} {r.get('currency', '')}")
        print(f"  涨跌: {r['emoji']} {r['change']}  ({r['pct']}%)")

        if not r.get('is_index'):
            mkt = fmt_mktcap(r.get('total_mktcap', ''), r.get('currency', ''))
            circ = fmt_mktcap(r.get('circ_mktcap', ''), r.get('currency', ''))
            print(f"  总市值: {mkt}  |  流通市值: {circ}")

        pe = r.get('pe', '')
        pb = r.get('pb', '')
        if pe or pb:
            pe_s = pe if pe and pe != '0' else '-'
            pb_s = pb if pb and pb != '0' else '-'
            print(f"  PE(TTM): {pe_s}  |  PB: {pb_s}")

        if r['market'] == 'A':
            print(f"  成交量: {fmt_num(r['volume'], 'volume_a')} 股  |  成交额: {fmt_num(r['turnover'], 'turnover_a')}")
            print(f"  换手率: {r.get('turnover_rate', '-')}%  |  振幅: {r.get('amplitude', '-')}%")
            print(f"  总股本: {fmt_num(r.get('total_shares', ''), 'shares')} 股  |  流通股本: {fmt_num(r.get('circ_shares', ''), 'shares')} 股")
            hs = r.get('high52', '')
            ls = r.get('low52', '')
            if hs or ls:
                print(f"  52周高: {hs}  |  52周低: {ls}")
        elif r['market'] == 'HK':
            print(f"  成交量: {fmt_num(r['volume'], 'volume_a')} 股  |  成交额: {fmt_num(r['turnover'], 'turnover_hk')}")
            print(f"  总股本: {fmt_num(r.get('total_shares', ''), 'shares')} 股  |  每手: {r.get('lot_size', '-')} 股")
            hs = r.get('high52', '')
            ls = r.get('low52', '')
            if hs or ls:
                print(f"  52周高: {hs}  |  52周低: {ls}")
        elif r['market'] == 'US':
            print(f"  成交量: {fmt_num(r['volume'], 'volume_a')} 股  |  成交额: {fmt_num(r['turnover'], 'turnover_hk')} {r.get('currency', '')}")
            tsh = r.get('total_shares', '')
            csh = r.get('circ_shares', '')
            if tsh or csh:
                print(f"  总股本: {fmt_num(tsh, 'shares')} 股  |  流通股本: {fmt_num(csh, 'shares')} 股")
            hs = r.get('high52', '')
            ls = r.get('low52', '')
            if hs or ls:
                print(f"  52周高: {hs}  |  52周低: {ls}")

        print(f"  今开: {r.get('open', '-')}  |  昨收: {r.get('prev_close', '-')}")
        print(f"  最高: {r['high']}  |  最低: {r['low']}")
    print()


def main():
    detail = False
    codes = []
    for a in sys.argv[1:]:
        if a in ('--detail', '-d'):
            detail = True
        elif a in ('--help', '-h'):
            print("Usage: uv run query_stock.py [--detail] <code1> [code2] ...")
            print()
            print("通用股票行情查询工具 (腾讯财经 qt.gtimg.cn)")
            print()
            print("标志:")
            print("  -d, --detail  详细模式 (PE/PB/成交量/总股本/52周高低)")
            print("  (默认)        紧凑模式 (价格/涨跌幅/市值)")
            print()
            print("代码格式:")
            print("  A股:  sh000001(上证指数)  sh688008(澜起科技)  sh600519(茅台)")
            print("        或直接6位: 688008  600519")
            print("  港股: hkHSI(恒生)  hk02026(小马智行)  hk00700(腾讯)")
            print("        或直接5位: 02026  00700")
            print("  美股: usINX(标普500)  usNVDA(英伟达)  usAAPL(苹果)")
            print()
            print("示例:")
            print("  uv run query_stock.py sh688008 hk02026 usWOLF")
            print("  uv run query_stock.py --detail 688008 02026")
            print("  uv run query_stock.py sh000001 hkHSI usINX")
            return
        else:
            codes.append(a)

    if not codes:
        print("Usage: uv run query_stock.py <code1> [code2] ...")
        print("Try --help for more info.")
        sys.exit(1)

    results = query_stocks(codes)
    if not results:
        print("未获取到数据，请检查代码是否正确")
        sys.exit(1)

    if detail:
        print_detail(results)
    else:
        print_compact(results)


if __name__ == "__main__":
    main()
