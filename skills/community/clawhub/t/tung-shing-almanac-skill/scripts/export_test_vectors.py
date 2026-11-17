#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export deterministic test vectors from pick.py logic for TS cross-validation.
Pure functions only — no network. Output: test-vectors.json"""
import sys, os, json, datetime
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from pick import (gz_index, si_li_si_jue, YANGONGJI_LUNAR, SANNIANG_LUNAR_DAY,
                  SHIEDABAI_GZ, OFFICER_SCORE, BELT_SCORE, SANHE_LIUHE_SCORE,
                  ZH_REL, resolve_event, PROFILES)

vectors = {"gz_index": [], "si_li_si_jue": [], "fixed_days": [],
           "relations": [], "resolve_event": []}

# 1. gz_index: all 60 valid combos + a few invalid ones
GAN = "甲乙丙丁戊己庚辛壬癸"; ZHI = "子丑寅卯辰巳午未申酉戌亥"
for a in range(10):
    for b in range(12):
        stem, branch = GAN[a], ZHI[b]
        vectors["gz_index"].append({"in": [stem, branch], "out": gz_index(stem, branch)})

# 2. si_li_si_jue: days around each term boundary.
#    Year-keyed: real API lookups are per-year, and term keys collide across
#    years (qiufen exists in both 2026 and 2027) — never merge into one map.
TERMS_BY_YEAR = {
    2026: {"lichun": "2026-02-04", "chunfen": "2026-03-20", "lixia": "2026-05-05",
           "xiazhi": "2026-06-21", "liqiu": "2026-08-07", "qiufen": "2026-09-23",
           "lidong": "2026-11-07", "dongzhi": "2026-12-21"},
    2027: {"lichun": "2027-02-04", "chunfen": "2027-03-21", "xiazhi": "2027-06-21",
           "qiufen": "2027-09-23", "dongzhi": "2027-12-22", "lidong": "2027-11-08",
           "liqiu": "2027-08-08", "lixia": "2027-05-06"},
}
for _year, _tmap in TERMS_BY_YEAR.items():
    _t = {k: {"date": v} for k, v in _tmap.items()}
    for k, v in _tmap.items():
        d = datetime.date.fromisoformat(v)
        for off in (-1, 0, 1):
            dd = (d + datetime.timedelta(days=off)).isoformat()
            vectors["si_li_si_jue"].append(
                {"in": [dd, _t], "out": si_li_si_jue(dd, _t)})
# random non-boundary dates
for ds in ["2026-09-01", "2026-10-15", "2026-12-25", "2027-01-01", "2026-06-30"]:
    _t = {k: {"date": v} for k, v in TERMS_BY_YEAR[int(ds[:4])].items()}
    vectors["si_li_si_jue"].append({"in": [ds, _t], "out": si_li_si_jue(ds, _t)})

# 3. fixed-day flags: given lunar month/day + ganzhi index + profile flags,
#    which vetoes fire? (pure table logic replicated exactly as in score paths)
for lm, ld in sorted(YANGONGJI_LUNAR):
    vectors["fixed_days"].append({"kind": "yangongji", "in": [lm, ld], "out": True})
vectors["fixed_days"].append({"kind": "yangongji", "in": [7, 2], "out": False})
for ld in sorted(SANNIANG_LUNAR_DAY):
    vectors["fixed_days"].append({"kind": "sanniang", "in": [ld], "out": True})
vectors["fixed_days"].append({"kind": "sanniang", "in": [15], "out": False})
for gz in sorted(SHIEDABAI_GZ):
    vectors["fixed_days"].append({"kind": "shiedabai", "in": [gz], "out": True})
for gz in [0, 1, 2, 39, 41, 58]:
    if gz not in SHIEDABAI_GZ:
        vectors["fixed_days"].append({"kind": "shiedabai", "in": [gz], "out": False})

# 4. zodiac relation scoring matrix (chong/hai veto, sanhe/liuhe +15, self note)
REL_SCORES = {"chong": "veto", "hai": "veto", "sanhe": 15, "liuhe": 15,
              "self": "fuyin", "plain": 0}
vectors["relations"] = [{"rel": k, "out": v} for k, v in REL_SCORES.items()]

# 5. event alias resolution
cases = [("wedding", "wedding"), ("婚嫁", "wedding"), ("marriage", "wedding"),
         ("搬家", "moving-house"), ("moving", "moving-house"),
         ("开业", "grand-opening"), ("签约", "signing-contracts"),
         ("buy-a-car", "signing-contracts"), ("安葬", "burial"),
         ("祭祀", "ancestor-worship"), ("剖腹产", "c-section"),
         ("赴任", "starting-a-new-job"), ("旅游", "travel"),
         ("装修", "renovation"), ("nonexistent", None), ("租房", None)]
for raw, expect in cases:
    vectors["resolve_event"].append({"in": raw, "out": resolve_event(raw)})

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-vectors.json")
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(vectors, fh, ensure_ascii=False, indent=1)
print(f"exported: gz_index={len(vectors['gz_index'])}, "
      f"si_li={len(vectors['si_li_si_jue'])}, fixed={len(vectors['fixed_days'])}, "
      f"relations={len(vectors['relations'])}, resolve={len(vectors['resolve_event'])}")
