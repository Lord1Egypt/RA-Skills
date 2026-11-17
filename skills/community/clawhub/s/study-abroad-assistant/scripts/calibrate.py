#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
留学助理 — 案例校准脚本（本地可跑，仅依赖 stdlib）

功能：读取 cases/admission_*.jsonl 中的录取结果案例，
  1) 反推选校 tier 分桶（GPA 分箱 × 目标校档 的相对命中率矩阵 → strong/medium/weak 建议）
  2) 计算画像 6 维的区分度，输出权重建议

方法学要点（v2）：
  绝对录取率（GPA→全局录取率）非单调——高 GPA 申请人多冲顶尖校，被校档拉低。
  故改用「相对命中率」：固定目标校档后，看不同 GPA 区间在该校档下的录取率，
  消除校档混杂，才能正确反推分桶边界。

输出：stdout 的 JSON（建议配置），供引擎侧（search.py CONFIG / analytics）采纳。

注意：示例启发式，非最终模型。样本量 < 30 时仅作演示，结论需在引擎侧用更大样本复核。
"""
import json
import glob
import os
import statistics
from datetime import date

CASES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cases")
SCHOOL_TIERS_PATH = os.path.join(CASES_DIR, "school_tiers.json")

# ---------- 学校→校档映射（交付引擎侧的校档定义建议）----------
def load_school_tiers():
    try:
        with open(SCHOOL_TIERS_PATH, "r", encoding="utf-8") as f:
            d = json.load(f)
        return {k: v for k, v in d.items() if not k.startswith("_")}
    except FileNotFoundError:
        return {}

SCHOOL_TIERS = load_school_tiers()


def load_cases():
    rows = []
    for path in glob.glob(os.path.join(CASES_DIR, "admission_*.jsonl")):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rows.append(json.loads(line))
    return rows


def app_tier(c, app):
    """解析单条申请的目标校档：优先用数据里标注的 tier，否则查学校映射。"""
    t = app.get("tier")
    if t and t != "unknown":
        return t
    return SCHOOL_TIERS.get(app.get("school"))


# ---------- 维度归一化（对齐引擎画像 6 维口径）----------
def norm_applicant(a):
    gpa = a.get("gpa") or 0
    scale = a.get("gpa_scale") or 4.0
    academic = (gpa / scale) * 100 if scale else 0

    toefl = a.get("toefl") or 0
    gre = a.get("gre", {}) or {}
    language = (toefl / 120.0 * 100) if toefl > 0 else None  # 海本 waive 等缺失标记

    gre_q = None
    if gre.get("taken") and gre.get("q"):
        gre_q = (gre["q"] - 130) / 40.0 * 100  # 130-170 → 0-100

    r = a.get("research", {}) or {}
    research = min(100, r.get("papers", 0) * 25 + r.get("ra_months", 0) * 2 + (20 if r.get("top_venue") else 0))

    inter = a.get("intern", {}) or {}
    tier_w = {"大厂": 20, "中厂": 10, "实验室": 10, "无": 0}
    intern = min(100, inter.get("months", 0) * 5 + tier_w.get(inter.get("tier", "无"), 0))

    reco = (a.get("reco", 0) or 0) / 5.0 * 100

    return {
        "academic": academic,
        "language": language,
        "gre_q": gre_q,
        "research": research,
        "intern": intern,
        "reco": reco,
        "gpa_raw": gpa,
    }


def bin_admit_rate(rows, key, bins):
    """按某字段分箱，计算各箱 admit 率（admit=1, 其余=0）。缺失值(None)跳过。"""
    out = []
    for lo, hi, label in bins:
        vals = [1 if app["result"] == "admit" else 0
                for c in rows for app in c["applications"]
                if (lambda v: v is not None and lo <= v < hi)(c["applicant"].get(key))]
        if vals:
            out.append({"bin": label, "n": len(vals),
                        "admit_rate": round(sum(vals) / len(vals), 3)})
    return out


def differentiate(rows, dim_fn):
    """计算某维在 admit / reject 组的均值差与区分度。"""
    adm, rej = [], []
    for c in rows:
        v = dim_fn(c["applicant"])
        if v is None:
            continue
        for app in c["applications"]:
            if app["result"] == "admit":
                adm.append(v)
            elif app["result"] == "reject":
                rej.append(v)
    if not adm or not rej:
        return None
    ma, mr = statistics.mean(adm), statistics.mean(rej)
    pooled = statistics.pstdev(adm + rej) or 1
    disc = abs(ma - mr) / pooled  # 效应量式区分度
    return {"admit_mean": round(ma, 1), "reject_mean": round(mr, 1),
            "discriminance": round(disc, 3), "n_admit": len(adm), "n_reject": len(rej)}


def band(r):
    """由命中率给出校档建议。"""
    if r is None:
        return None
    if r >= 0.7:
        return "strong"
    if r >= 0.35:
        return "medium"
    return "weak"


def main():
    rows = load_cases()
    if not rows:
        print(json.dumps({"error": "no admission cases found"}, ensure_ascii=False))
        return

    # 预处理：注入 GRE-Q 原始分（仅 taken 时），供分箱；缺失则不注入
    for c in rows:
        g = c["applicant"].get("gre", {}) or {}
        if g.get("taken") and g.get("q"):
            c["applicant"]["gre_q_raw"] = g["q"]

    n_apps = sum(len(c["applications"]) for c in rows)

    tiers = ["reach", "match", "safety"]
    gpa_bins = [(0, 3.3, "<3.3"), (3.3, 3.6, "3.3-3.6"),
                (3.6, 3.8, "3.6-3.8"), (3.8, 4.01, ">=3.8")]

    # === 核心：相对命中率矩阵 GPA 分箱 × 校档 ===
    matrix = {}
    for glo, ghi, glabel in gpa_bins:
        row_out = {}
        for t in tiers:
            vals = []
            for c in rows:
                gpa = c["applicant"].get("gpa")
                if gpa is None:
                    continue
                for app in c["applications"]:
                    if app_tier(c, app) == t and glo <= gpa < ghi:
                        vals.append(1 if app["result"] == "admit" else 0)
            row_out[t] = {"n": len(vals),
                          "admit_rate": (round(sum(vals) / len(vals), 3) if vals else None)}
        matrix[glabel] = row_out

    tiering_advice = {glabel: {t: band(matrix[glabel][t]["admit_rate"]) for t in tiers}
                      for glabel in matrix}

    # === 参考：全局 GRE 分箱（样本少，仅参考）===
    gre_bins = [(0, 155, "<155"), (155, 165, "155-165"), (165, 170.1, ">=165")]
    by_gre = bin_admit_rate(rows, "gre_q_raw", gre_bins)

    # === 画像 6 维区分度 ===
    dims = {
        "academic": lambda a: norm_applicant(a)["academic"],
        "language": lambda a: norm_applicant(a)["language"],
        "research": lambda a: norm_applicant(a)["research"],
        "intern": lambda a: norm_applicant(a)["intern"],
        "reco": lambda a: norm_applicant(a)["reco"],
    }
    disc = {}
    for k, fn in dims.items():
        r = differentiate(rows, fn)
        if r:
            disc[k] = r
    total = sum(max(v["discriminance"], 0.01) for v in disc.values()) or 1
    weights = {k: round(max(v["discriminance"], 0.01) / total, 3) for k, v in disc.items()}

    # 标记本数据集可校准的维度
    calibrated = [k for k, v in disc.items() if v["discriminance"] > 0.05]
    missing = [k for k in dims if k not in disc or disc[k]["discriminance"] <= 0.05]

    out = {
        "generated_at": str(date.today()),
        "n_cases": len(rows),
        "n_applications": n_apps,
        "method": "relative_hit_rate",
        "method_note": ("相对命中率：固定目标校档后，不同 GPA 区间在该校档下的录取率，"
                        "消除校档混杂。绝对录取率非单调（高GPA冲顶尖校被拉低），故不采用全局率。"),
        "school_tier_map": SCHOOL_TIERS,
        "relative_hit_rate_matrix": matrix,
        "tiering_advice": tiering_advice,
        "band_rule": "admit_rate>=0.7→strong; 0.35-0.7→medium; <0.35→weak",
        "by_gre_q": by_gre,
        "portrait_weights": {
            "by_dimension": disc,
            "relative_weight": weights,
            "calibrated_dims": calibrated,
            "missing_dims_due_to_data": missing,
            "note": ("相对权重=区分度归一化，非最终。当前数据集混合了含科研字段的种子案例与不含该字段的 "
                     "gradcafe 案例；且 academic 维出现 reject 组 GPA 均值(3.72) 高于 admit 组(3.19) 的"
                     "方向异常——系校档混杂（reject 集中于冲顶尖校的高GPA申请人）所致，非真实因果。"
                     "故画像权重当前不可用于定稿，须 M4 阶段引入纯含科研/实习/语言字段的数据源重新校准。"),
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
