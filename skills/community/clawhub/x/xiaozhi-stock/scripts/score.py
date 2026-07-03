#!/usr/bin/env python3
"""
小智评分引擎 v2 — BigA综合评分 + 技术面择时分
v2改进：从东方财富直接拉PE/板块数据，不再"数据缺失给中性分"
"""
import sys, os, re, json, urllib.request
from datetime import datetime

if sys.stdout.encoding and 'UTF-8' not in sys.stdout.encoding.upper():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_stock import fetch_stock, get_market_prefix

HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.eastmoney.com"}


# ============ 补充数据获取 ============

def fetch_pe_from_eastmoney(code: str) -> dict:
    """从东方财富拉PE/市值/申万行业/换手率/量比等基本面数据"""
    _, clean = get_market_prefix(code)
    market = 1 if clean.startswith(("60", "68", "11", "51", "58")) else (
        0 if clean.startswith(("00", "30", "15", "12", "16", "13")) else 2)
    # 字段说明
    # f43=现价(×100) f48=成交额(元) f57=代码 f58=名称 f60=昨收
    # f116=总市值(元) f127=申万行业 f128=地域板块 f129=概念标签(逗号分隔)
    # f162=PE_TTM(×100) f167=振幅(×100) f168=换手率(×100)
    # f170=涨跌幅(×100) f292=量比(×100)
    url = (f"http://push2.eastmoney.com/api/qt/stock/get?"
           f"secid={market}.{clean}"
           f"&fields=f43,f48,f57,f58,f60,f116,f127,f128,f129,f162,f167,f168,f170,f292")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            d = json.loads(resp.read().decode("utf-8", errors="replace")).get("data", {}) or {}
            if not d.get("f43"):
                return {}
            return {
                "pe_ttm": round((d.get("f162", 0) or 0) / 100, 2) if d.get("f162") else None,
                "total_market_cap_yi": round((d.get("f116", 0) or 0) / 1e8, 2) if d.get("f116") else None,
                "sw_sector": (d.get("f127", "") or "").strip(),
                "region_sector": (d.get("f128", "") or "").strip(),
                "concept_tags": (d.get("f129", "") or "").strip(),
                "turnover_pct": round((d.get("f168", 0) or 0) / 100, 2) if d.get("f168") else None,
                "amplitude_pct": round((d.get("f167", 0) or 0) / 100, 2) if d.get("f167") else None,
                "amount_yi": round((d.get("f48", 0) or 0) / 1e8, 2) if d.get("f48") else None,
                "volume_ratio": round((d.get("f292", 0) or 0) / 100, 2) if d.get("f292") else None,
            }
    except Exception:
        return {}


def fetch_sector_rank() -> list:
    """获取板块涨幅排行榜（行业+概念双维度合并去重）"""
    seen = set()
    merged = []
    for plate_type in ["t:3", "t:2"]:  # 先行业后概念
        url = ("http://push2.eastmoney.com/api/qt/clist/get?"
               f"pn=1&pz=80&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281"
               "&fltt=2&invt=2&fid=f3"
               f"&fs=m:90+{plate_type}"
               "&fields=f2,f3,f4,f12,f14,f20,f128,f136")
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=5) as resp:
                items = json.loads(resp.read().decode()).get("data", {}).get("diff", [])
                for item in items:
                    name = item.get("f14", "")
                    if name and name not in seen:
                        seen.add(name)
                        item["_rank"] = len(merged) + 1
                        merged.append(item)
        except Exception:
            continue
    return merged


def find_code_in_sectors(code: str, sectors: list, extra: dict = None) -> dict:
    """匹配股票所属板块 — 优先用申万行业(f127)+概念标签(f129)"""
    # 从申万行业名和概念标签提取关键词
    keywords = set()
    if extra:
        sw = extra.get("sw_sector", "")  # 如 "白酒Ⅱ"、"银行Ⅱ"、"工业金属"
        if sw:
            # 去除Ⅱ/Ⅲ/Ⅳ后缀
            clean = sw.replace("Ⅱ","").replace("Ⅲ","").replace("Ⅳ","").replace("Ⅰ","")
            keywords.add(clean)
        ct = extra.get("concept_tags", "")
        if ct:
            for tag in ct.split(","):
                tag = tag.strip()
                if tag and len(tag) <= 6:  # 只取短标签如 "白酒"、"有色"
                    keywords.add(tag)
    if not keywords:
        return {}
    best = None
    best_rank = 999
    for sec in sectors:
        name = sec.get("f14", "") or ""
        for kw in keywords:
            if kw in name or name in kw:
                rank = sec.get("_rank", 999)
                if rank < best_rank:
                    best_rank = rank
                    best = {
                        "sector_name": name,
                        "sector_pct": sec.get("f3", 0),
                        "sector_rank": rank,
                        "sector_count": len(sectors),
                    }
                break
    return best or {}


# ============ 评分 ============

def score_biga(data: dict, extra: dict = None, sector_info: dict = None) -> dict:
    """
    BigA综合评分 0-100 (v2 — 用真实数据替代"缺失给中性分")
    """
    pe = extra.get("pe_ttm") if extra else data.get("pe")
    chg_pct = data.get("change_pct", 0)
    amount_yi = extra.get("amount_yi") if extra else data.get("amount_yi", 0)
    market_cap = extra.get("total_market_cap_yi")
    vol_ratio = extra.get("volume_ratio")
    scores = {}

    # --- 基本面 (25) ---
    # PE合理性 (10)
    if pe is not None and pe > 0:
        if pe < 15:
            pe_score = 10; pe_note = f"PE={pe} 低估"
        elif pe < 30:
            pe_score = 8;  pe_note = f"PE={pe} 合理偏低"
        elif pe < 50:
            pe_score = 6;  pe_note = f"PE={pe} 合理偏高"
        elif pe < 100:
            pe_score = 3;  pe_note = f"PE={pe} 高估"
        else:
            pe_score = 1;  pe_note = f"PE={pe} 严重高估"
    else:
        pe_score = 5; pe_note = "PE数据缺失"

    # 市值判断 (10) — 用市值替代营收增速判断
    cap_score = 5
    cap_note = "市值数据缺失"
    if market_cap is not None:
        if market_cap < 50:
            cap_score = 8; cap_note = f"市值{market_cap}亿 小盘弹性"
        elif market_cap < 200:
            cap_score = 7; cap_note = f"市值{market_cap}亿 中盘成长"
        elif market_cap < 1000:
            cap_score = 6; cap_note = f"市值{market_cap}亿 中大盘"
        elif market_cap < 5000:
            cap_score = 5; cap_note = f"市值{market_cap}亿 大盘"
        else:
            cap_score = 4; cap_note = f"市值{market_cap}亿 超大盘"

    # 量比作为活跃度 (5)
    if vol_ratio is not None:
        if vol_ratio > 2:
            vol_score = 5; vol_note = f"量比{vol_ratio} 异常放量"
        elif vol_ratio > 1.2:
            vol_score = 4; vol_note = f"量比{vol_ratio} 活跃"
        elif vol_ratio > 0.5:
            vol_score = 3; vol_note = f"量比{vol_ratio} 正常"
        else:
            vol_score = 2; vol_note = f"量比{vol_ratio} 清淡"
    else:
        vol_score = 3; vol_note = "量比数据缺失"

    fundamental = pe_score + cap_score + vol_score
    scores["基本面"] = {"score": fundamental, "max": 25, "detail": [pe_note, cap_note, vol_note]}

    # --- 催化剂 (25) ---
    cat_score = 12  # base
    cat_notes = []
    if sector_info and sector_info.get("sector_rank", 999) <= 3:
        cat_score += 8; cat_notes.append(f"板块排名第{sector_info['sector_rank']} 强催化")
    elif sector_info and sector_info.get("sector_rank", 999) <= 10:
        cat_score += 5; cat_notes.append(f"板块排名第{sector_info['sector_rank']} 温和催化")
    else:
        cat_notes.append("板块未见明显催化")

    if chg_pct >= 9.5:
        cat_score += 5; cat_notes.append("涨停=强市场信号")
    elif chg_pct >= 5:
        cat_score += 3; cat_notes.append("大涨=市场关注度提升")

    scores["催化剂"] = {"score": min(cat_score, 25), "max": 25, "detail": cat_notes}

    # --- 技术面 (20) ---
    # 趋势 (10)
    if chg_pct > 5:
        trend = 9; trend_note = f"涨幅{chg_pct}% 强势"
    elif chg_pct > 2:
        trend = 7; trend_note = f"涨幅{chg_pct}% 偏强"
    elif chg_pct > 0:
        trend = 6; trend_note = f"涨幅{chg_pct}% 微涨"
    elif chg_pct > -3:
        trend = 4; trend_note = f"跌幅{chg_pct}% 弱势调整"
    else:
        trend = 2; trend_note = f"跌幅{chg_pct}% 走坏"

    # 量价 (5+量比修正)
    if amount_yi > 50:
        vol_px_score = 5 if chg_pct > 0 else 3
        vol_px_note = f"成交{amount_yi}亿 {'放量上涨' if chg_pct>0 else '放量异常'}"
    elif amount_yi > 10:
        vol_px_score = 4 if chg_pct > 0 else 3
        vol_px_note = f"成交{amount_yi}亿 正常"
    else:
        vol_px_score = 2; vol_px_note = f"成交{amount_yi}亿 清淡"

    # 相对强弱 (5) — 对比板块涨幅
    strength = 3; strength_note = "无板块对比"
    if sector_info:
        sector_pct = sector_info.get("sector_pct", 0)
        diff = chg_pct - sector_pct
        if diff > 3:
            strength = 5; strength_note = f"远超板块({sector_pct}%) +{diff:.1f}%"
        elif diff > 0:
            strength = 4; strength_note = f"跑赢板块({sector_pct}%)"
        elif diff > -3:
            strength = 2; strength_note = f"跑输板块({sector_pct}%)"
        else:
            strength = 1; strength_note = f"远弱于板块({sector_pct}%)"

    technical = trend + vol_px_score + strength
    scores["技术面"] = {"score": technical, "max": 20, "detail": [trend_note, vol_px_note, strength_note]}

    # --- 热度 (30) ---
    # 板块热度 (12)
    if sector_info:
        rank = sector_info.get("sector_rank", 999)
        total = sector_info.get("sector_count", 60)
        pct = sector_info.get("sector_pct", 0)
        if rank <= 3:
            sector_heat = 12; heat_note = f"板块TOP{rank}/{total} +{pct}%"
        elif rank <= 10:
            sector_heat = 9;  heat_note = f"板块TOP{rank}/{total}"
        elif rank <= 20:
            sector_heat = 6;  heat_note = f"板块第{rank}/{total} 中游"
        else:
            sector_heat = 3;  heat_note = f"板块第{rank}/{total} 靠后"
    else:
        sector_heat = 6; heat_note = "板块归属不确定"

    # 资金热度 (10) — 量比+涨幅判断
    if chg_pct > 0 and (vol_ratio or 1) > 1.5:
        flow = 9; flow_note = "量价齐升 资金追捧"
    elif chg_pct > 0:
        flow = 6; flow_note = "温和流入"
    elif chg_pct < 0 and (vol_ratio or 1) > 1.5:
        flow = 3; flow_note = "放量下跌 资金出逃"
    else:
        flow = 5; flow_note = "资金中性"

    # 情绪 (8) — 振幅反映情绪激烈程度
    amp = extra.get("amplitude_pct") if extra else None
    if amp is not None:
        if amp < 2:
            emotion = 5; emo_note = f"振幅{amp}% 平静"
        elif amp < 5:
            emotion = 6; emo_note = f"振幅{amp}% 正常"
        else:
            emotion = 7; emo_note = f"振幅{amp}% 激烈"
    else:
        emotion = 4; emo_note = "振幅数据缺失"

    heat = sector_heat + flow + emotion
    scores["热度"] = {"score": heat, "max": 30, "detail": [heat_note, flow_note, emo_note]}

    total = fundamental + min(cat_score, 25) + technical + heat
    scores["total"] = total

    # 扣分
    deductions = []
    if pe is not None and pe > 80: deductions.append(f"PE过高({pe})")
    if chg_pct < -5: deductions.append(f"跌幅过大({chg_pct}%)")
    if amount_yi is not None and amount_yi < 1: deductions.append(f"成交清淡({amount_yi}亿)")
    if chg_pct > 20: deductions.append(f"短期涨幅过大({chg_pct}%) 追高风险")
    scores["deductions"] = deductions
    return scores


def score_timing(data: dict, extra: dict = None, sector_info: dict = None) -> dict:
    """技术面择时分 v2 — 加入板块对比和量比"""
    chg_pct = data.get("change_pct", 0)
    amount_yi = extra.get("amount_yi") if extra else data.get("amount_yi", 0)
    vol_ratio = extra.get("volume_ratio") if extra else None

    # 趋势方向 (-4~+4)
    if chg_pct > 5:  trend_score = 3; trend_note = "强势上涨"
    elif chg_pct > 2: trend_score = 2; trend_note = "温和上涨"
    elif chg_pct > 0: trend_score = 1; trend_note = "微涨"
    elif chg_pct > -2: trend_score = -1; trend_note = "微跌"
    elif chg_pct > -5: trend_score = -2; trend_note = "下跌"
    else: trend_score = -3; trend_note = "大跌"

    # 量价(-3~+3) — 量比修正
    if chg_pct > 0 and (vol_ratio or 1) > 1.5:
        volume_score = 3; vol_note = f"量比{vol_ratio} 放量上攻"
    elif chg_pct > 0:
        volume_score = 1; vol_note = "缩量上涨"
    elif chg_pct < 0 and (vol_ratio or 1) > 1.5:
        volume_score = -3; vol_note = f"量比{vol_ratio} 放量下跌"
    elif chg_pct < 0:
        volume_score = -1; vol_note = "缩量下跌"
    else:
        volume_score = 0; vol_note = "量价中性"

    # 技术指标(-2~+2) — 用振幅趋势近似
    amp = extra.get("amplitude_pct") if extra else None
    if amp is not None and amp > 5 and chg_pct > 0:
        indicator_score = 1; ind_note = "振幅大+上涨=资金活跃"
    elif amp is not None and amp > 5 and chg_pct < 0:
        indicator_score = -1; ind_note = "振幅大+下跌=分歧大"
    else:
        indicator_score = 0; ind_note = "需多日K线计算MACD/RSI"

    # 支撑压力(-1~+1) — 板块强弱辅助判断
    if sector_info:
        diff = chg_pct - sector_info.get("sector_pct", 0)
        if diff > 3:
            support_score = 1; supp_note = f"远超板块{diff:.1f}% 强势"
        elif diff < -3:
            support_score = -1; supp_note = f"远弱于板块{diff:.1f}%"
        else:
            support_score = 0; supp_note = "与板块同步"
    else:
        support_score = 0; supp_note = "需历史数据"

    total = trend_score + volume_score + indicator_score + support_score
    total = max(-10, min(10, total))

    return {
        "timing_score": total,
        "max": 10, "min": -10,
        "details": {
            "趋势方向": {"score": trend_score, "note": trend_note},
            "量价关系": {"score": volume_score, "note": vol_note},
            "技术指标": {"score": indicator_score, "note": ind_note},
            "支撑压力": {"score": support_score, "note": supp_note},
        },
        "signal": ("🔥买入" if total >= 6 else "✅可买" if total >= 3 else
                   "👀持有" if total >= -2 else "⚠️减仓" if total >= -5 else "🛑离场")
    }


def full_score(code: str) -> dict:
    """完整评分：获取行情+补充数据+板块排名→评分"""
    data = fetch_stock(code)
    if "error" in data:
        return {"error": data["error"]}

    extra = fetch_pe_from_eastmoney(code)
    sectors = fetch_sector_rank()
    sector_info = find_code_in_sectors(code, sectors, extra) if sectors else None

    # 合并数据（东财补充字段优先）
    if extra:
        data["pe"] = extra.get("pe_ttm") or data.get("pe")
        data["amount_yi"] = extra.get("amount_yi") or data.get("amount_yi", 0)
        data["turnover_pct"] = extra.get("turnover_pct")

    biga = score_biga(data, extra, sector_info)
    timing = score_timing(data, extra, sector_info)

    return {
        "code": code,
        "name": data.get("name", ""),
        "price": data.get("current", 0),
        "change_pct": data.get("change_pct", 0),
        "pe": extra.get("pe_ttm") if extra else data.get("pe"),
        "turnover": extra.get("turnover_pct") if extra else None,
        "vol_ratio": extra.get("volume_ratio") if extra else None,
        "sector": sector_info.get("sector_name") if sector_info else None,
        "sector_rank": sector_info.get("sector_rank") if sector_info else None,
        "biga_score": biga["total"],
        "biga_dimensions": {k: v for k, v in biga.items() if k not in ("total", "deductions")},
        "deductions": biga.get("deductions", []),
        "timing_score": timing["timing_score"],
        "timing_signal": timing["signal"],
        "timing_details": timing["details"],
        "dual_signal": {
            "long_ok": biga["total"] >= 50,
            "short_ok": timing["timing_score"] >= 0,
            "all_pass": biga["total"] >= 50 and timing["timing_score"] >= 0,
        }
    }


def fmt_score(r: dict) -> str:
    if "error" in r:
        return f"❌ {r['error']}"
    sign = "+" if r["change_pct"] >= 0 else ""
    lines = [
        "=" * 45,
        f"📊 {r['name']}({r['code']})  {sign}{r['change_pct']}%",
        "=" * 45,
        f"BigA评分: {r['biga_score']}/100  择时分: {r['timing_score']:+d} ({r['timing_signal']})",
    ]
    if r.get("pe"): lines.append(f"PE: {r['pe']}")
    if r.get("turnover"): lines.append(f"换手率: {r['turnover']}%")
    if r.get("vol_ratio"): lines.append(f"量比: {r['vol_ratio']}")
    if r.get("sector"): lines.append(f"板块: {r['sector']} (排名第{r.get('sector_rank','?')})")

    lines.append("")
    lines.append("--- BigA维度 ---")
    for dim, info in r["biga_dimensions"].items():
        lines.append(f"  {dim}: {info['score']}/{info['max']}")
        for d in info.get("detail", []):
            lines.append(f"    └ {d}")

    if r.get("deductions"):
        lines.append("--- 扣分 ---")
        for d in r["deductions"]:
            lines.append(f"  - {d}")

    lines.append("")
    lines.append("--- 择时 ---")
    for dim, info in r["timing_details"].items():
        lines.append(f"  {dim}: {info['score']:+d} ({info['note']})")

    lines.append("")
    d = r["dual_signal"]
    lines.append(f"双信号: 长线{'✅' if d['long_ok'] else '❌'} 短线{'✅' if d['short_ok'] else '❌'} 全通{'✅' if d['all_pass'] else '❌'}")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="小智评分引擎 v2")
    parser.add_argument("--code", nargs="+", help="股票代码")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    if not args.code:
        parser.print_help()
        return

    results = [full_score(c) for c in args.code]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(fmt_score(r))
            print()


if __name__ == "__main__":
    main()
