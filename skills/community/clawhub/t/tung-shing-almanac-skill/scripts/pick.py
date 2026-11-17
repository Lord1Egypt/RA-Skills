#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pick — bilingual transparent auspicious-date picker
====================================================
Data layer:  12Zodiacs.com Almanac API (JPL DE440s ephemeris, minute-precision
             solar terms, 1739 Xie Ji Bian Fang Shu arbitration).
Output layer: transparent scoring with itemized reasons (inspired by the
             folk-picker genre), hard-veto fixed inauspicious days, and a
             deliverable bilingual date-selection document (择吉文书).

Modes:
  fast  — one /auspicious call (engine shortlist), then enrich + score. 2-3 req.
  deep  — iterate every day in the window via /day, hard-veto + full scoring.
          Handles activities the /auspicious engine does not cover (burial,
          ancestor worship, ...). ~1 req/day, cached.

Usage:
  python3 pick.py --event wedding --birth 1990-05-20 \
      --start 2026-09-01 --end 2026-10-15 --top 5
  python3 pick.py --event 安葬 --start 2026-09-01 --end 2026-09-30 --lang zh
  python3 pick.py --event wedding --birth 1990-05-20 --start 2026-09-01 \
      --end 2026-09-30 --json --weekend-only
  python3 pick.py --event wedding --birth 1990-05-20 --start 2026-09-01 \
      --end 2026-09-30 --document            # deliverable 择吉文书
"""

import os
import sys
import json
import argparse
import datetime
import urllib.request
import urllib.parse

# ---------------------------------------------------------------------------
# Bootstrap: use the bundled API client (almanac.sh) config; API base fixed.
# ---------------------------------------------------------------------------

API = "https://12zodiacs.com/wp-json/12z/v1/almanac"
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
CACHE_TTL = 6 * 3600  # seconds

def api_get(endpoint, params, key=None):
    """GET with disk cache. Returns parsed JSON. Never raises on 4xx/5xx —
    returns {'_error': code, '_body': text}."""
    if key is None:
        key = os.environ.get("TZS_API_KEY")
    if key:
        params = dict(params, key=key)
    qs = urllib.parse.urlencode(params)
    url = f"{API}/{endpoint}?{qs}"
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(
        CACHE_DIR, f"{endpoint}_{hashlib_sha(url)}.json")
    now = datetime.datetime.now().timestamp()
    if os.path.exists(cache_file) and now - os.path.getmtime(cache_file) < CACHE_TTL:
        with open(cache_file, "r", encoding="utf-8") as fh:
            try:
                return json.load(fh)
            except json.JSONDecodeError:
                pass
    req = urllib.request.Request(url, headers={"User-Agent": "tung-shing-almanac-skill/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode("utf-8", "replace")[:200]}
    except Exception as e:  # network down
        return {"_error": -1, "_body": str(e)[:200]}
    with open(cache_file, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    return data


def hashlib_sha(s):
    import hashlib
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Fixed inauspicious days (hard veto) — computed from API data, not tables
# ---------------------------------------------------------------------------

YANGONGJI_LUNAR = {  # 杨公十三忌 (lunar month, day)
    (1, 13), (2, 11), (3, 9), (4, 7), (5, 5), (6, 3),
    (7, 1), (7, 29), (8, 27), (9, 25), (10, 23), (11, 21), (12, 19),
}
SANNIANG_LUNAR_DAY = {3, 7, 13, 18, 22, 27}  # 三娘煞 (lunar day)
SHIEDABAI_GZ = {  # 十恶大败 (day GanZhi index, 0-based JiaZi, 甲子=0)
    # 甲辰40 乙巳41 丙申32 丁亥23 戊戌34 己丑25 庚辰16 辛巳17 壬申8 癸亥59
    40, 41, 32, 23, 34, 25, 16, 17, 8, 59,
}


def gz_index(stem_cn, branch_cn):
    """0-based JiaZi index (甲子=0) via CRT — n%10==stem, n%12==branch."""
    GAN = "甲乙丙丁戊己庚辛壬癸"
    ZHI = "子丑寅卯辰巳午未申酉戌亥"
    if stem_cn not in GAN or branch_cn not in ZHI:
        return None
    a, b = GAN.index(stem_cn), ZHI.index(branch_cn)
    for n in range(60):
        if n % 10 == a and n % 12 == b:
            return n
    return None  # odd parity mismatch — impossible Ganzhi combo


def get_solar_terms(year):
    """Fetch minute-precision solar terms from /term (cached per year)."""
    d = api_get("term", {"year": year})
    if "_error" in d:
        return {}
    return d.get("terms", {})


def si_li_si_jue(date_str, terms):
    """四离 (day before equinox/solstice) & 四绝 (day before 立春/立夏/立秋/立冬).
    Uses API minute-precision term dates."""
    if not terms:
        return None
    d = datetime.date.fromisoformat(date_str) + datetime.timedelta(days=1)
    nxt = d.isoformat()
    lijie = {"chunfen": "四离", "xiazhi": "四离", "qiufen": "四离", "dongzhi": "四离",
             "lichun": "四绝", "lixia": "四绝", "liqiu": "四绝", "lidong": "四绝"}
    for term_key, kind in lijie.items():
        if term_key in terms and terms[term_key].get("date") == nxt:
            return kind
    return None


# ---------------------------------------------------------------------------
# Event profiles — scoring weights per activity
# ---------------------------------------------------------------------------

PROFILES = {
    "wedding": {
        "zh": "婚嫁", "aliases": ["marriage", "结婚", "嫁娶", "领证", "婚"],
        "auspicious_api": "wedding", "deep_yi_keywords": ["wed", "marri", "嫁娶", "结婚"],
        "good_officers": ["Open", "Complete", "Stable", "Initiate"],
        "avoid_officers": ["Break", "Close"],
        "prefer_gods": ["不将", "天喜", "三合", "月德", "天德", "六仪", "玉宇"],
        "prefer_gods_en": ["Bu Jiang", "Tian Xi", "San He", "Yue De", "Tian De"],
        "veto_sanniang": True, "major": True,
        "note_zh": "婚嫁首重不将/天喜/三合六合；避三娘煞、杨公忌、四离四绝、本命冲日。",
        "note_en": "Wedding favors Bu Jiang / Tian Xi / San He-Liu He; avoid Sanniang Sha, Yang Gong Ji, Si Li Si Jue, and days clashing the couple.",
    },
    "moving-house": {
        "zh": "入宅", "aliases": ["moving", "搬家", "乔迁", "入宅", "移徙"],
        "auspicious_api": "moving-house", "deep_yi_keywords": ["move", "入宅", "移徙"],
        "good_officers": ["Open", "Complete", "Stable", "Initiate"],
        "avoid_officers": ["Break", "Close"],
        "prefer_gods": ["天德", "月德", "三合", "六合", "驿马", "民日"],
        "prefer_gods_en": ["Tian De", "Yue De", "San He", "Liu He", "Yi Ma"],
        "veto_sanniang": False, "major": True,
        "note_zh": "入宅重驿马/民日；避四离四绝、杨公忌、月破、本命冲日。",
        "note_en": "Moving favors Yi Ma (Traveling Horse); avoid Si Li Si Jue, Yang Gong Ji, Month Breaker, and personal clash days.",
    },
    "grand-opening": {
        "zh": "开业", "aliases": ["opening", "launch", "开业", "开市", "剪彩"],
        "auspicious_api": "grand-opening", "deep_yi_keywords": ["open", "开市", "开业"],
        "good_officers": ["Open", "Full", "Complete", "Initiate"],
        "avoid_officers": ["Break", "Close"],
        "prefer_gods": ["天德", "月德", "三合", "六合", "民日", "金堂"],
        "prefer_gods_en": ["Tian De", "Yue De", "San He", "Min Ri"],
        "veto_sanniang": False, "major": True,
        "note_zh": "开市重民日/金堂；避月破、大耗、四离四绝、本命冲日。",
        "note_en": "Opening favors Min Ri / Jin Tang; avoid Month Breaker, Da Hao, Si Li Si Jue, and personal clash days.",
    },
    "renovation": {
        "zh": "装修动土", "aliases": ["renovation", "装修", "动土", "修造"],
        "auspicious_api": "renovation", "deep_yi_keywords": ["renovat", "动土", "修造", "装修"],
        "good_officers": ["Initiate", "Stable", "Complete", "Open"],
        "avoid_officers": ["Break", "Close"],
        "prefer_gods": ["天德", "月德", "三合", "六合", "天恩"],
        "prefer_gods_en": ["Tian De", "Yue De", "San He"],
        "veto_sanniang": False, "major": True,
        "note_zh": "动土重天德/月德合；避土府、土煞、四离四绝、本命冲日。",
        "note_en": "Renovation favors Tian De / Yue De; avoid Earth taboos, Si Li Si Jue, and personal clash days.",
    },
    "signing-contracts": {
        "zh": "签约交易", "aliases": ["signing", "contract", "签约", "交易", "买车", "买房"],
        "auspicious_api": "signing-contracts", "deep_yi_keywords": ["contract", "sign", "交易", "立券", "纳财"],
        "good_officers": ["Full", "Stable", "Complete", "Open", "Initiate"],
        "avoid_officers": ["Break", "Close"],
        "prefer_gods": ["天德", "月德", "三合", "六合", "五富", "天愿"],
        "prefer_gods_en": ["Tian De", "Yue De", "San He", "Wu Fu"],
        "veto_sanniang": False, "major": False,
        "note_zh": "签约重五富/天愿；避月破、大耗、四离四绝、本命冲日。",
        "note_en": "Signing favors Wu Fu / Tian Yuan; avoid Month Breaker, Da Hao, and personal clash days.",
    },
    "travel": {
        "zh": "出行", "aliases": ["trip", "travel", "出行", "旅游", "出差"],
        "auspicious_api": "travel", "deep_yi_keywords": ["travel", "出行"],
        "good_officers": ["Initiate", "Open", "Full", "Remove"],
        "avoid_officers": ["Break", "Close"],
        "prefer_gods": ["天德", "月德", "驿马", "天马", "三合"],
        "prefer_gods_en": ["Yi Ma", "Tian Ma", "Tian De"],
        "veto_sanniang": False, "major": False,
        "note_zh": "出行重驿马/天马；避月破、往亡、四离四绝、本命冲日。",
        "note_en": "Travel favors Yi Ma / Tian Ma; avoid Wang Wang, Month Breaker, and personal clash days.",
    },
    "starting-a-new-job": {
        "zh": "入职赴任", "aliases": ["new-job", "job", "入职", "赴任", "上任"],
        "auspicious_api": "starting-a-new-job", "deep_yi_keywords": ["job", "赴任", "入职", "上官"],
        "good_officers": ["Open", "Stable", "Initiate", "Full"],
        "avoid_officers": ["Break", "Close"],
        "prefer_gods": ["天德", "月德", "天恩", "三合", "六合"],
        "prefer_gods_en": ["Tian En", "Tian De", "San He"],
        "veto_sanniang": False, "major": False,
        "note_zh": "赴任重天恩；避月破、四离四绝、本命冲日。",
        "note_en": "New job favors Tian En; avoid Month Breaker, Si Li Si Jue, and personal clash days.",
    },
    "c-section": {
        "zh": "剖腹产", "aliases": ["cesarean", "childbirth", "剖腹产", "生子"],
        "auspicious_api": "c-section", "deep_yi_keywords": [],
        "good_officers": ["Open", "Full", "Stable", "Complete"],
        "avoid_officers": ["Break", "Close"],
        "prefer_gods": ["天德", "月德", "三合", "六合", "天喜"],
        "prefer_gods_en": ["Tian De", "Yue De", "San He", "Tian Xi"],
        "veto_sanniang": False, "major": True,
        "note_zh": "择日产重日课四柱平和，避月破、四离四绝；务必遵医嘱优先。",
        "note_en": "C-section favors a balanced day chart; medical advice always comes first.",
    },
    # Extended: /auspicious has no engine for these — deep mode only
    "burial": {
        "zh": "安葬", "aliases": ["funeral", "下葬", "安葬", "落葬"],
        "auspicious_api": None, "deep_yi_keywords": ["burial", "funeral", "安葬", "启钻"],
        "good_officers": ["Close", "Remove", "Stable", "Collect"],
        "avoid_officers": ["Break"],
        "prefer_gods": ["鸣吠", "鸣吠对", "天德", "月德", "三合"],
        "prefer_gods_en": ["Ming Fei", "Tian De", "Yue De"],
        "veto_sanniang": False, "major": True,
        "note_zh": "安葬重鸣吠日；避重丧、复日、四离四绝、本命冲日。民俗参考，务必结合师承。",
        "note_en": "Burial favors Ming Fei days; avoid Chong Sang, Fu Ri, Si Li Si Jue. Folk reference only.",
    },
    "ancestor-worship": {
        "zh": "祭祀", "aliases": ["worship", "祭祀", "祭拜", "上坟"],
        "auspicious_api": None, "deep_yi_keywords": ["worship", "prayer", "ancestor", "祭祀"],
        "good_officers": ["Stable", "Close", "Remove", "Full"],
        "avoid_officers": ["Break"],
        "prefer_gods": ["天德", "月德", "天愿", "民日", "福德"],
        "prefer_gods_en": ["Tian De", "Yue De", "Tian Yuan", "Min Ri"],
        "veto_sanniang": False, "major": False,
        "note_zh": "祭祀重天愿/民日；避四离四绝、杨公忌。",
        "note_en": "Worship favors Tian Yuan / Min Ri; avoid Si Li Si Jue and Yang Gong Ji.",
    },
}

OFFICER_SCORE = {"Open": 15, "Complete": 15, "Stable": 10, "Initiate": 10,
                 "Full": 8, "Remove": 6, "Collect": 4, "Close": 2,
                 "Establish": 2, "Balance": 4, "Danger": 0, "Break": -40}
BELT_SCORE = {"yellow": 20, "black": -5}
SANHE_LIUHE_SCORE = 15
GOD_PREFER_SCORE = 6          # per preferred auspicious god present (cap below)
GOD_PREFER_CAP = 18
XIU_WEIGHT = 0               # reserved

ZH_REL = {"chong": "冲", "sanhe": "三合", "liuhe": "六合", "hai": "害", "self": "本位", "plain": "平"}
OFFICER_CN = {"Open": "开", "Complete": "成", "Stable": "定", "Initiate": "执",
              "Full": "满", "Remove": "除", "Collect": "收", "Close": "闭",
              "Establish": "建", "Balance": "平", "Danger": "危", "Break": "破"}


def resolve_event(raw):
    r = raw.strip().lower()
    for key, p in PROFILES.items():
        if r == key or r == p["zh"] or r in p["aliases"]:
            return key
    return None


def zodiac_of_birth(birth_str):
    """Return Chinese zodiac (立春 boundary) for a birth date.
    Tries the API first; falls back to a pure stem-branch cycle computation
    (year GanZhi from JDN offset — exact for years 1900-2100) when the date
    is outside the free ±90d window."""
    d = api_get("day", {"date": birth_str})
    if "_error" not in d and d.get("lunar"):
        ygz = d.get("lunar", {}).get("year_gz_cn", "")  # 丙午 — CN chars
        branch_cn = ygz[1] if len(ygz) >= 2 else ""
    else:
        # Offline fallback: year GanZhi cycles independently of the free-tier
        # window. 1984 = 甲子 (index 0); approximate 立春 boundary Feb 4.
        try:
            y = datetime.date.fromisoformat(birth_str)
        except ValueError:
            return None
        gz_year = y.year - (1 if (y.month, y.day) < (2, 4) else 0)
        idx = (gz_year - 1984) % 60
        ZHI = "子丑寅卯辰巳午未申酉戌亥"
        branch_cn = ZHI[idx % 12]
    ZHI = "子丑寅卯辰巳午未申酉戌亥"
    ANIMALS = ["rat", "ox", "tiger", "rabbit", "dragon", "snake",
               "horse", "goat", "monkey", "rooster", "dog", "pig"]
    ANIMALS_CN = "鼠牛虎兔龙蛇马羊猴鸡狗猪"
    if branch_cn in ZHI:
        i = ZHI.index(branch_cn)
        return {"slug": ANIMALS[i], "cn": ANIMALS_CN[i]}
    return None


def score_day_fast(day, eng, profile, birth_zodiac):
    """Fast mode: the /auspicious engine score IS the primary score (four-tier
    arbitration already excludes Month/Year Breakers, Four Departures/Absolutes,
    and non-premier officers). Local work is limited to what the engine cannot
    know: fixed inauspicious days (Yang Gong Ji / Sanniang Sha / Shi E Da Bai),
    patron-zodiac veto (chong/hai) and sanhe/liuhe bonus. No re-scoring of
    officer/belt/gods — those stay descriptive fields.
    Returns (score, base, adjust, reasons_zh, reasons_en, veto)."""
    base = int(eng.get("score", 0))
    score = base
    adjust = 0
    verdict = f"{eng.get('officer', '')} officer, {eng.get('belt', '')} belt"
    rz = [f"引擎四层仲裁评分：{base}/5 · {verdict}"]
    re_ = [f"Engine arbitration score: {base}/5 ({verdict})"] + \
        [f"{w}" for w in eng.get("why", [])]
    veto = []

    lunar = day.get("lunar", {})
    lm, ld = lunar.get("month", 0), lunar.get("day", 0)
    gz_i = gz_index(day.get("day_pillar", {}).get("stem_cn", ""),
                    day.get("day_pillar", {}).get("branch_cn", ""))
    terms = get_solar_terms(int(day["date"][:4]))
    slsj = si_li_si_jue(day["date"], terms)

    if (lm, ld) in YANGONGJI_LUNAR:
        veto.append(("杨公忌", "Yang Gong Ji"))
    if profile.get("veto_sanniang") and ld in SANNIANG_LUNAR_DAY:
        veto.append(("三娘煞", "Sanniang Sha"))
    if gz_i in SHIEDABAI_GZ:
        veto.append(("十恶大败", "Shi E Da Bai"))
    if slsj:  # engine should have excluded these; belt-and-suspenders check
        veto.append((slsj, "Si Li / Si Jue"))

    if birth_zodiac:
        rel_map = {m["slug"]: m["rel"] for m in day.get("relations", {}).get("map", [])}
        rel = rel_map.get(birth_zodiac["slug"], "plain")
        if rel in ("chong", "hai"):
            veto.append((f"本命{ZH_REL[rel]}({birth_zodiac['cn']})",
                         f"Clashes patron ({ZH_REL[rel]})"))
        elif rel in ("sanhe", "liuhe"):
            adjust = SANHE_LIUHE_SCORE
            score += adjust
            rz.append(f"日支与福主{ZH_REL[rel]}(+{adjust})")
            re_.append(f"{'San He' if rel == 'sanhe' else 'Liu He'} with patron (+{adjust})")
        elif rel == "self":
            # 伏吟 (day branch == patron branch): folk-taboo for weddings,
            # neutral-weak otherwise — keep as candidate, no bonus
            rz.append(f"日支与福主本位（伏吟，婚嫁慎用）")
            re_.append("Day branch = patron branch (Fu Yin, cautious for weddings)")

    return score, base, adjust, rz, re_, veto


def score_day(day, profile, birth_zodiac):
    """Transparent scoring for one /day record. Returns (score, reasons_zh, reasons_en, veto_list)."""
    score = 0
    rz, re_ = [], []
    veto = []

    officer_en = day.get("day_officer_zhi_shen", {}).get("en", "")
    officer_cn = day.get("day_officer_zhi_shen", {}).get("cn", "")
    officer_quality = day.get("day_officer_zhi_shen", {}).get("quality", "")
    belt = day.get("belt", {}).get("type", "")

    # 1. fixed inauspicious days — hard veto
    lunar = day.get("lunar", {})
    lm, ld = lunar.get("month", 0), lunar.get("day", 0)
    gz_i = gz_index(day.get("day_pillar", {}).get("stem_cn", ""),
                    day.get("day_pillar", {}).get("branch_cn", ""))
    terms = get_solar_terms(int(day["date"][:4]))
    slsj = si_li_si_jue(day["date"], terms)

    if (lm, ld) in YANGONGJI_LUNAR:
        veto.append(("杨公忌", "Yang Gong Ji"))
    if profile.get("veto_sanniang") and ld in SANNIANG_LUNAR_DAY:
        veto.append(("三娘煞", "Sanniang Sha"))
    if gz_i in SHIEDABAI_GZ:
        veto.append(("十恶大败", "Shi E Da Bai"))
    if slsj:
        veto.append((slsj, "Si Li / Si Jue"))

    # 2. officer
    if officer_en in profile["good_officers"]:
        s = OFFICER_SCORE.get(officer_en, 8)
        score += s
        rz.append(f"建除【{officer_cn}】日(+{s})")
        re_.append(f"{officer_en} ({officer_cn}) Day Officer (+{s})")
    elif officer_en in profile["avoid_officers"]:
        rz.append(f"建除【{officer_cn}】日(忌)")
        re_.append(f"{officer_en} ({officer_cn}) Day Officer — avoided")
        veto.append((f"建除{officer_cn}", f"Day Officer {officer_en}"))

    # 3. yellow/black belt
    s = BELT_SCORE.get(belt, 0)
    if s:
        belt_cn = day.get("belt", {}).get("name_cn", "")
        score += s
        rz.append(f"值神【{belt_cn}】{'黄道' if belt=='yellow' else '黑道'}({s:+d})")
        re_.append(f"{day.get('belt', {}).get('name', '')} {'Yellow' if belt=='yellow' else 'Black'} Belt ({s:+d})")

    # 4. relation with the principal (birth zodiac)
    if birth_zodiac:
        rel_map = {m["slug"]: m["rel"] for m in day.get("relations", {}).get("map", [])}
        rel = rel_map.get(birth_zodiac["slug"], "plain")
        if rel in ("chong", "hai"):
            veto.append((f"本命{ZH_REL[rel]}({birth_zodiac['cn']})", f"Clashes patron ({ZH_REL[rel]})"))
        elif rel in ("sanhe", "liuhe"):
            score += SANHE_LIUHE_SCORE
            rz.append(f"日支与福主{ZH_REL[rel]}(+{SANHE_LIUHE_SCORE})")
            re_.append(f"{ 'San He' if rel=='sanhe' else 'Liu He'} with patron ({s:+d})".replace("{s:+d}", f"(+{SANHE_LIUHE_SCORE})"))

    # 5. auspicious / caution gods
    jx = day.get("jishen_xiongsha", {})
    gods_a = jx.get("auspicious", [])
    gods_c = jx.get("caution", [])
    hits = [g for g in gods_a if g in profile["prefer_gods"]]
    if hits:
        s = min(GOD_PREFER_SCORE * len(hits), GOD_PREFER_CAP)
        score += s
        rz.append(f"吉神加持：{', '.join(hits)}(+{s})")
        re_.append(f"Auspicious gods: {', '.join(hits)} (+{s})")
    elif gods_a:
        score += 2
        rz.append(f"吉神：{', '.join(gods_a[:3])}(+2)")
        re_.append(f"Auspicious gods present (+2)")

    # 6. yi list contains the activity (API English folk list)
    yi_text = " ".join(clean_yi(day)).lower()
    if any(k.lower() in yi_text for k in profile["deep_yi_keywords"]):
        score += 12
        rz.append(f"当日宜含本事项(+12)")
        re_.append(f"Yi list covers this activity (+12)")
    if officer_quality == "auspicious" and belt == "yellow":
        score += 3

    return score, rz, re_, veto


def enrich_hours(date_str, birth_zodiac):
    """Fetch /hours; return top 3 yellow-belt hours (not clashing patron)."""
    d = api_get("hours", {"date": date_str})
    if "_error" in d:
        return []
    out = []
    for h in d.get("hours", []):
        if h.get("huanghei", {}).get("type") != "yellow":
            continue
        if birth_zodiac and h.get("clash_zodiac", "").lower() == birth_zodiac["slug"]:
            continue
        out.append(h)
    return out[:3]


def fmt_hours(hours, lang):
    if not hours:
        return "—" if lang == "zh" else "—"
    parts = []
    for h in hours:
        parts.append(f"{h['branch_cn']}时({h['time']},{h['huanghei']['name_cn']} {h['huanghei'].get('name','')})")
    return "、".join(parts)


def parse_date(s):
    try:
        return datetime.date.fromisoformat(s.strip())
    except ValueError:
        print(json.dumps({"error": f"invalid date: {s}",
                          "expected": "YYYY-MM-DD"}, ensure_ascii=False))
        sys.exit(2)


def daterange(start_s, end_s):
    d0 = parse_date(start_s)
    d1 = parse_date(end_s)
    if d1 < d0:
        print(json.dumps({"error": "window end before start"}, ensure_ascii=False))
        sys.exit(2)
    d = d0
    while d <= d1:
        yield d.isoformat()
        d += datetime.timedelta(days=1)


def yi_list_raw(day):
    return day.get("auspicious_for_yi", [])


def clean_yi(day):
    """Strip zero-width chars the API embeds in Yi/Ji strings."""
    ZW = "\u200b\u200c\u200d\ufeff"
    return [s.strip().translate({ord(c): None for c in ZW}) for s in yi_list_raw(day)]


def _candidate(ds, day, score, base, adjust, rz, re_, birth_zodiac, with_hours=True):
    return {
        "date": ds,
        "score": score,
        "engine_score": base,
        "local_adjustment": adjust,
        "weekday": datetime.date.fromisoformat(ds).strftime("%A"),
        "date_cn": f"{day['lunar']['month']}月{day['lunar']['day']}日",
        "year_gz_cn": day["lunar"].get("year_gz_cn", ""),
        "day_pillar_cn": day["day_pillar"]["stem_cn"] + day["day_pillar"]["branch_cn"],
        "month_pillar_cn": day.get("folk", {}).get("month_pillar_cn", ""),
        "officer_en": day["day_officer_zhi_shen"]["en"],
        "officer_cn": day["day_officer_zhi_shen"]["cn"],
        "belt_type": day["belt"]["type"],
        "belt_cn": day["belt"]["name_cn"],
        "clash_animal": day["clash"]["animal"],
        "clash_animal_cn": ZH_ANIMAL_CN.get(day["clash"]["animal"], day["clash"]["animal"]),
        "sha_direction": day.get("sha_direction", ""),
        "relations": day.get("relations", {}).get("map", []),
        "yi": clean_yi(day),
        "ji": [s.strip().translate({ord(c): None for c in "\u200b\u200c\u200d\ufeff"})
               for s in day.get("avoid_ji", [])],
        "gods_auspicious": day.get("jishen_xiongsha", {}).get("auspicious", []),
        "gods_caution": day.get("jishen_xiongsha", {}).get("caution", []),
        "pengzu": day.get("pengzu", {}),
        "nayin": day.get("folk", {}).get("nayin", []),
        "reasons_zh": rz,
        "reasons_en": re_,
        # hours enriched later for top-N only (saves /hours calls)
        "hours": enrich_hours(ds, birth_zodiac) if with_hours else [],
    }


def run(args):
    ev = resolve_event(args.event)
    if not ev:
        print(json.dumps({"error": "unknown event",
                          "valid": sorted(PROFILES.keys()),
                          "tip": "use --event wedding|moving-house|grand-opening|renovation|signing-contracts|travel|starting-a-new-job|c-section|burial|ancestor-worship"}, ensure_ascii=False))
        return 2
    profile = PROFILES[ev]
    birth_zodiac = None
    if args.birth:
        birth_zodiac = zodiac_of_birth(args.birth)

    # ---------------- fast mode via /auspicious shortlist ----------------
    engine_meta = {}
    candidates = []
    used_fast = profile["auspicious_api"] and args.mode == "fast"
    if used_fast:
        params = {"activity": profile["auspicious_api"],
                  "days": days_between(args.start, args.end)}
        if args.weekend_only:
            params["weekend_only"] = 1
        d = api_get("auspicious", params)
        recs = d.get("recommended_dates", []) if "_error" not in d else []
        # NOTE: the engine counts `days` from TODAY, not from --start. Clip
        # the shortlist to the requested window and surface out-of-window
        # dates as reference only.
        start_d = parse_date(args.start)
        end_d = parse_date(args.end)
        in_window = [x for x in recs if start_d.isoformat() <= x["date"] <= end_d.isoformat()]
        out_of_window = [x for x in recs if x not in in_window]
        shortlist = [x["date"] for x in in_window]
        engine_meta = {x["date"]: x for x in in_window}
        if not shortlist:
            # engine found nothing inside the window → fall back to deep scan
            used_fast = False
            args.mode = "deep"
    if not used_fast:
        shortlist = list(daterange(args.start, args.end))

    def collect(shortlist, fast_mode):
        out = []
        for ds in shortlist:
            day = api_get("day", {"date": ds})
            if "_error" in day:
                continue
            if fast_mode and ds in engine_meta:
                score, base, adjust, rz, re_, veto = score_day_fast(
                    day, engine_meta[ds], profile, birth_zodiac)
            else:
                score, rz, re_, veto = score_day(day, profile, birth_zodiac)
                base, adjust = None, 0
            if veto:
                continue  # hard-vetoed
            # with_hours=False: enrich only after top-N cut (saves calls)
            out.append(_candidate(ds, day, score, base, adjust, rz, re_,
                                  birth_zodiac, with_hours=False))
        return out

    candidates = collect(shortlist, used_fast)

    # fast shortlist exhausted (e.g. all vetoed) → deep fallback
    if used_fast and len(candidates) < args.top:
        extra = collect([d for d in daterange(args.start, args.end)
                         if d not in set(shortlist)], fast_mode=False)
        candidates.extend(extra)
        args.mode = "fast+deep"

    candidates.sort(key=lambda x: -x["score"])
    candidates = candidates[: args.top]
    # enrich lucky hours only for the finalists
    for c in candidates:
        c["hours"] = enrich_hours(c["date"], birth_zodiac)

    # surface engine dates that fell outside the requested window
    try:
        oow = [{"date": x["date"], "score": x["score"], "officer": x["officer"],
                "belt": x["belt"], "why": x["why"]} for x in out_of_window]
    except NameError:
        oow = []

    result = {
        "event": profile["zh"] if args.lang.startswith("zh") else ev,
        "event_zh": profile["zh"], "event_en": ev,
        "patron_zodiac": birth_zodiac,
        "window": {"start": args.start, "end": args.end},
        "mode": args.mode,
        "note_zh": profile["note_zh"], "note_en": profile["note_en"],
        "recommended": candidates,
        "engine_dates_outside_window": oow,
        "attribution": "Almanac data computed by 12Zodiacs.com API",
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(render_text(result, args.lang, args.document))
    return 0


ZH_ANIMAL_CN = {"Rat": "鼠", "Ox": "牛", "Tiger": "虎", "Rabbit": "兔", "Dragon": "龙",
                "Snake": "蛇", "Horse": "马", "Goat": "羊", "Monkey": "猴",
                "Rooster": "鸡", "Dog": "狗", "Pig": "猪"}


def days_between(start_s, end_s):
    d0 = parse_date(start_s)
    d1 = parse_date(end_s)
    return max(7, min(60, (d1 - d0).days))


def render_text(result, lang, as_document):
    zh = lang.startswith("zh")
    lines = []
    sep = "=" * 60
    lines.append(sep)
    if as_document:
        title = f"【择吉文书 · Date Selection Certificate】{result['event_zh']} / {result['event_en']}"
    else:
        title = f"【{result['event_zh']} 吉日 · {result['event_en']} Dates】"
    lines.append(title)
    patron = result["patron_zodiac"]
    if patron:
        lines.append(f"福主生肖 Patron: {patron['cn']} ({patron['slug'].title()})")
    w = result["window"]
    lines.append(f"区间 Window: {w['start']} ~ {w['end']}   模式 Mode: {result['mode']}")
    lines.append(sep)

    for i, c in enumerate(result["recommended"], 1):
        lines.append("")
        belt_zh = "黄道" if c["belt_type"] == "yellow" else "黑道"
        if c.get("engine_score") is not None:
            adj = c.get("local_adjustment", 0)
            score_line = f"◆ 候选 {i} Candidate 〔引擎 Engine {c['engine_score']}/5"
            score_line += f" + 生肖调整 zodiac +{adj} = {c['score']}〕" if adj else f"〕"
        else:
            score_line = f"◆ 候选 {i} Candidate 〔{c['score']} 分〕"
        lines.append(score_line)
        lines.append(f"  公历 {c['date']} ({c['weekday']})  农历 {c['date_cn']}")
        lines.append(f"  四柱 Pillars: 年 {c['year_gz_cn']}  月 {c['month_pillar_cn']}  日 {c['day_pillar_cn']}")
        lines.append(f"  建除 Officer: {c['officer_cn']} ({c['officer_en']})   值神 {c['belt_cn']} ({belt_zh})")
        lines.append(f"  冲煞 Clash: 冲{c['clash_animal_cn']}({c['clash_animal']}) 煞{c['sha_direction']}")
        if c["nayin"]:
            lines.append(f"  纳音 Nayin: {c['nayin'][0]} / {c['nayin'][1] if len(c['nayin'])>1 else ''}")
        lines.append(f"  吉神 Gods: {', '.join(c['gods_auspicious']) or '—'}")
        if c["gods_caution"]:
            lines.append(f"  凶神 Caution: {', '.join(c['gods_caution'])}")
        lines.append(f"  宜 Yi: {'; '.join(c['yi']) or '—'}")
        lines.append(f"  忌 Ji: {'; '.join(c['ji']) or '—'}")
        lines.append(f"  吉时 Hours: {fmt_hours(c['hours'], 'zh' if zh else 'en')}")
        lines.append("  入选理由 Why:")
        fast = c.get("engine_score") is not None
        if zh:
            for r in c["reasons_zh"]:
                lines.append(f"    · {r}")
            # fast mode: engine whys are bilingual already; only print the
            # extra local adjustment lines from the en list (avoid duplicates)
            for r in c["reasons_en"]:
                if fast and not any(r2.endswith(r) or r2 == r for r2 in c["reasons_zh"]):
                    lines.append(f"    · {r}")
        else:
            for r in c["reasons_en"]:
                lines.append(f"    · {r}")
            if not fast:
                for r in c["reasons_zh"]:
                    lines.append(f"    · {r}")
    lines.append("")
    lines.append("-" * 60)
    lines.append(f"民俗提示 Note: {result['note_zh']}")
    lines.append(f"Folk note: {result['note_en']}")
    lines.append("民俗文化参考，非宿命定论 | Folk-cultural reference, not fatalism.")
    lines.append("Almanac data computed by 12Zodiacs.com API")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="bilingual transparent auspicious-date picker")
    ap.add_argument("--event", required=True, help="wedding/moving-house/... or 婚嫁/搬家/...")
    ap.add_argument("--birth", help="patron birthdate YYYY-MM-DD (zodiac match)")
    ap.add_argument("--start", required=True, help="window start YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="window end YYYY-MM-DD")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--mode", choices=["fast", "deep"], default="fast",
                    help="fast=engine shortlist (2-3 calls); deep=every day (burial/worship etc.)")
    ap.add_argument("--weekend-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--document", action="store_true", help="render deliverable 择吉文书")
    ap.add_argument("--lang", default="zh", choices=["zh", "en"])
    ap.add_argument("--key", help="12Zodiacs API key (±365d)")
    args = ap.parse_args()
    if args.key:
        global API
        # key appended by api_get callers; simplest: stash in env for api_get
        os.environ["TZS_API_KEY"] = args.key
    sys.exit(run(args) or 0)


if __name__ == "__main__":
    main()
