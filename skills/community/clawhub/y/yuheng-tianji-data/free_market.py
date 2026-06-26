"""
七政系统·天枢免费市场数据模块 v6
使用urllib.request（已验证可用），简化请求头
"""
import urllib.request
import re
import datetime

# ─── 网络请求 ─────────────────────────────────────────

def _fetch(url: str, enc: str = 'gbk') -> str | None:
    """发送HTTP请求，返回响应体文本"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://finance.sina.com.cn/',
        })
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode(enc, errors='replace').strip()
    except Exception:
        return None


# ─── 解析器 ───────────────────────────────────────────

def _hf(raw: str) -> dict | None:
    """
    解析新浪hf_格式：黄金/白银/铜/原油
    实测字段索引（2026-04-06 黄金数据）：
      raw: var hq_str_hf_GC="4668.595,,4664.300,4665.000,4699.300,4668.595,10:17:54,4679.700,4675.000,0,1,1,2026-04-06,纽约黄金,0"
      split('=')[1].split(',') 后：
      p[0]=4668.595(当前价格)  p[2]=4664.300(开)  p[3]=4665.000(昨收)
      p[4]=4699.300(今高)  p[5]=4668.595(当前价格重复)  p[6]=10:17:54(时间)
      p[7]=4679.700(买)  p[8]=4675.000(卖)
      p[11]=2026-04-06  p[12]=纽约黄金
    结论：hf_格式每个字段向右偏移1位！p[0]=价格, p[2]=开, p[3]=昨, p[4]=高, p[6]=时间, p[7]=买, p[8]=卖
    """
    try:
        parts_raw = raw.split('=')
        if len(parts_raw) < 2:
            return None
        inner = parts_raw[1].strip('"; ')
        p = inner.split(',')
        if len(p) < 9:
            return None

        price = float(p[0]) if p[0] else None
        open_ = float(p[2]) if len(p) > 2 and p[2] else None
        prev_close = float(p[3]) if len(p) > 3 and p[3] else None
        high = float(p[4]) if len(p) > 4 and p[4] else None
        t = p[6] if len(p) > 6 else None
        bid = float(p[7]) if len(p) > 7 and p[7] else None
        ask = float(p[8]) if len(p) > 8 and p[8] else None
        date_s = p[11] if len(p) > 11 else None
        name_s = p[12] if len(p) > 12 else None
        low = min(open_ or price or 0, price or 0) if (open_ and price) else None

        chg = (price - prev_close) if (price is not None and prev_close is not None) else None
        chg_pct = (chg / prev_close * 100) if (prev_close and chg is not None) else None

        return {
            'price': price, 'open': open_, 'prev_close': prev_close,
            'high': high, 'low': low, 'bid': bid, 'ask': ask,
            'time': t, 'date': date_s, 'name': name_s,
            'change': chg, 'change_pct': chg_pct,
        }
    except Exception as e:
        return None


def _nf(raw: str) -> dict | None:
    """解析国内商品期货（新浪nf_）"""
    try:
        if '"' not in raw:
            return None
        start = raw.index('"')
        end = raw.rindex('"')
        inner = raw[start+1:end]
        p = inner.split(',')
        if len(p) < 4:
            return None
        return {
            'name': p[0],
            'price': float(p[1]) if p[1] else None,
            'change': float(p[2]) if p[2] else None,
            'change_pct': float(p[3]) if p[3] else None,
            'bid': float(p[4]) if len(p) > 4 and p[4] else None,
        }
    except Exception:
        return None


def _hk(raw: str) -> dict | None:
    """解析港股指数（腾讯）"""
    try:
        parts = raw.split('~')
        if len(parts) < 7 or not parts[3]:
            return None
        price = float(parts[3])
        meta = parts[6].split(',') if len(parts) > 6 and parts[6] else []
        change = float(meta[1]) if len(meta) > 1 and meta[1] else None
        pct = meta[2].replace('%', '') if len(meta) > 2 and meta[2] else None
        change_pct = float(pct) if pct else None
        return {'price': price, 'change': change, 'change_pct': change_pct}
    except Exception:
        return None


def _etf(raw: str) -> dict | None:
    """解析QDII ETF（腾讯）"""
    try:
        parts = raw.split('~')
        if len(parts) < 33:
            return None
        return {
            'price': float(parts[3]) if parts[3] else None,
            'change': float(parts[31]) if parts[31] else None,
            'change_pct': float(parts[32]) if parts[32] else None,
        }
    except Exception:
        return None


# ─── 数据获取函数 ─────────────────────────────────────

def get_commodities() -> dict:
    """黄金/白银/铜/原油"""
    mapping = [
        ('gold',      '黄金',  'https://hq.sinajs.cn/list=hf_GC'),
        ('silver',    '白银',  'https://hq.sinajs.cn/list=hf_SI'),
        ('copper',    '铜',    'https://hq.sinajs.cn/list=hf_HG'),
        ('crude_oil', '原油',  'https://hq.sinajs.cn/list=hf_CL'),
    ]
    result = {}
    for key, name, url in mapping:
        raw = _fetch(url)
        if not raw:
            continue
        d = _hf(raw)
        if d:
            d['name_cn'] = name
            d['unit'] = ('美元/盎司' if key in ('gold', 'silver')
                         else '美分/磅' if key == 'copper' else '美元/桶')
            d['source'] = 'sina_hf'
            result[key] = d
    return result


def get_cn_futures() -> dict:
    """螺纹钢/铁矿石/焦煤/焦炭/豆粕"""
    mapping = [
        ('rebar',        '螺纹钢', 'https://hq.sinajs.cn/list=nf_SHFE.RB00Y'),
        ('iron_ore',     '铁矿石', 'https://hq.sinajs.cn/list=nf_DCE.I2409'),
        ('coking_coal',  '焦煤',   'https://hq.sinajs.cn/list=nf_DCE.JM2409'),
        ('coke',         '焦炭',   'https://hq.sinajs.cn/list=nf_DCE.J2409'),
        ('soybean_meal', '豆粕',   'https://hq.sinajs.cn/list=nf_DCE.M2409'),
    ]
    result = {}
    for key, name, url in mapping:
        raw = _fetch(url)
        if not raw:
            continue
        d = _nf(raw)
        if d:
            d['name_cn'] = name
            d['unit'] = '元/吨'
            d['source'] = 'sina_nf'
            result[key] = d
    return result


def get_hk_indices() -> dict:
    """恒生指数/恒生科技"""
    mapping = [
        ('hsi',    '恒生指数', 'https://qt.gtimg.cn/q=hkHSI'),
        ('hstech', '恒生科技', 'https://qt.gtimg.cn/q=hkHSTECH'),
    ]
    result = {}
    for key, name, url in mapping:
        raw = _fetch(url)
        if not raw:
            continue
        d = _hk(raw)
        if d:
            d['name_cn'] = name
            d['source'] = 'tencent_hk'
            result[key] = d
    return result


def get_us_etf_cn() -> dict:
    """纳指ETF/标普500ETF"""
    mapping = [
        ('nasdaq_etf',  '纳指ETF(513100)',    'https://qt.gtimg.cn/q=sh513100'),
        ('sp500_etf',   '标普500ETF(513500)', 'https://qt.gtimg.cn/q=sh513500'),
        ('hk_tech_etf', '恒生科技ETF(513180)','https://qt.gtimg.cn/q=sh513180'),
    ]
    result = {}
    for key, name, url in mapping:
        raw = _fetch(url)
        if not raw:
            continue
        d = _etf(raw)
        if d:
            d['name_cn'] = name
            d['note'] = 'QDII估算，非精确美股期货'
            d['source'] = 'tencent_etf'
            result[key] = d
    return result


# ─── 全量快照 ─────────────────────────────────────────

def get_full_market_snapshot() -> dict:
    """天枢全市场快照"""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comm = get_commodities()
    cn = get_cn_futures()
    hk = get_hk_indices()
    etf = get_us_etf_cn()
    return {
        'timestamp': now,
        'status': {
            'intl_commodities': 'ok' if comm else 'fail',
            'cn_futures': 'ok' if cn else 'fail',
            'hk_indices': 'ok' if hk else 'fail',
            'us_est': 'ok' if etf else 'fail',
        },
        'commodities_intl': comm,
        'commodities_cn': cn,
        'hk_indices': hk,
        'us_etf_est': etf,
    }


# ─── 格式化输出 ───────────────────────────────────────

def format_snapshot(snap: dict) -> str:
    now_str = datetime.datetime.now().strftime('%m/%d %H:%M')
    lines = [
        "═" * 52,
        f"  天枢·全市场快照  {now_str}",
        "═" * 52,
    ]

    comm = snap.get('commodities_intl', {})
    if comm:
        lines.append("\n🛢️ 国际商品（新浪hf_）")
        for v in comm.values():
            p = f"{v['price']:.2f}" if v.get('price') else '—'
            c = f"{v['change_pct']:+.2f}%" if v.get('change_pct') else ''
            t = v.get('time', '')
            lines.append(f"  {v['name_cn']}：{p}{v.get('unit','')}  {c}  [{t}]")
    else:
        lines.append("\n🛢️ 国际商品：暂无数据")

    cn = snap.get('commodities_cn', {})
    if cn:
        lines.append("\n🏭 国内期货（新浪nf_）")
        for v in cn.values():
            p = f"{v['price']:.0f}" if v.get('price') else '—'
            c = f"{v['change_pct']:+.2f}%" if v.get('change_pct') else ''
            lines.append(f"  {v['name_cn']}：{p}元/吨  {c}")

    hk = snap.get('hk_indices', {})
    if hk:
        lines.append("\n🇭🇰 港股指数")
        for v in hk.values():
            p = f"{v['price']:.0f}" if v.get('price') else '—'
            c = f"{v['change_pct']:+.2f}%" if v.get('change_pct') else ''
            lines.append(f"  {v['name_cn']}：{p}  {c}")

    etf = snap.get('us_etf_est', {})
    if etf:
        lines.append("\n🌐 QDII ETF")
        for v in etf.values():
            p = f"{v['price']:.3f}" if v.get('price') else '—'
            c = f"{v['change_pct']:+.2f}%" if v.get('change_pct') else ''
            lines.append(f"  {v['name_cn']}：{p}  {c}")

    st = snap.get('status', {})
    ok = sum(1 for v in st.values() if v == 'ok')
    lines += ["─" * 52, f"  数据源：{ok}/{len(st)} 可用"]
    lines.append("═" * 52)
    return '\n'.join(lines)


if __name__ == '__main__':
    snap = get_full_market_snapshot()
    print(format_snapshot(snap))
