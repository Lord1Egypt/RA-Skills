#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
留学助理 — UCLA 数据集画像权重校准（初版，仅依赖 stdlib）

数据源：Kaggle「Graduate Admission 2」(mohansacharya/graduate-admissions)，License **CC0: Public Domain**。
由 GitHub 镜像下载（Sourena-Mohit/Predicting-UCLA-Admissions-A-Neural-Network-Approach, MIT）。
样本：500 条；字段 GRE(340)/TOEFL(120)/Univ Rating/SOP/LOR/CGPA(10)/Research(0/1)/Chance of Admit(0-1)。

方法：各画像维与 Chance of Admit 的 Pearson 相关系数 → 归一化为相对权重。
映射：academic←CGPA, language←TOEFL, gre_q←GRE总分, research←Research(0/1), reco←LOR, intern←(缺失)。

局限（必须随结果一起呈现，仅作初版）：
- 合成问卷数据，Chance of Admit 为问卷/model 预测值，非真实录取结果；
- 印度视角；字段是"录取概率"而非二分类结果；
- GRE 为总分 340 制（无分项）；research 为 0/1 二值；
- GRE/TOEFL/CGPA 高度共线（相关 0.8+），Pearson 高估共线变量权重。
结论须用含真实录取结果的内部数据复核后才可采纳。
"""
import csv
import math
import os
import statistics
from datetime import date

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "cases", "ucla_admission_predict.csv")

# 列索引（Admission_Predict.csv 固定结构）
COL = {"gre": 1, "toefl": 2, "rating": 3, "sop": 4, "lor": 5, "cgpa": 6,
       "research": 7, "chance": 8}


def pearson(xs, ys):
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return cov / (sx * sy)


def main():
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        for r in csv.reader(f):
            if not r or len(r) < 9:
                continue
            if r[1].strip().lower().startswith("gre"):
                continue  # header
            try:
                rows.append([float(r[i]) for i in range(1, 9)])
            except ValueError:
                continue

    if not rows:
        print('{"error": "no rows loaded"}')
        return

    n = len(rows)
    chance = [r[COL["chance"] - 1] for r in rows]
    dims = {
        "academic": ("CGPA (10分制)", COL["cgpa"] - 1),
        "language": ("TOEFL (120)", COL["toefl"] - 1),
        "gre_q": ("GRE 总分 (340)", COL["gre"] - 1),
        "research": ("Research (0/1)", COL["research"] - 1),
        "reco": ("LOR (1-5)", COL["lor"] - 1),
        "sop": ("SOP (1-5)", COL["sop"] - 1),  # 引擎画像无 SOP 维，仅作参考
    }
    corr = {}
    for k, (label, idx) in dims.items():
        vals = [r[idx] for r in rows]
        corr[k] = {"source_field": label, "corr": round(pearson(vals, chance), 3)}
    # intern 维：数据集无实习字段
    corr["intern"] = {"source_field": None, "corr": None,
                      "note": "数据集无实习字段，权重置 0，须由含实习字段的真实数据补齐"}

    usable = {k: c for k, c in corr.items() if c["corr"] is not None}
    total = sum(max(abs(c["corr"]), 0.01) for c in usable.values()) or 1
    weights = {k: round(max(abs(c["corr"]), 0.01) / total, 3) for k, c in usable.items()}
    weights["intern"] = 0.0

    out = {
        "generated_at": str(date.today()),
        "source": "Kaggle Graduate Admission 2 (mohansacharya), CC0: Public Domain; "
                  "GitHub 镜像下载",
        "n_samples": n,
        "method": "pearson_correlation_to_chance_of_admit",
        "dimension_correlation": corr,
        "relative_weight": weights,
        "engine_6dims": {
            "academic": weights.get("academic"),
            "language": weights.get("language"),
            "research": weights.get("research"),
            "intern": weights.get("intern"),
            "reco": weights.get("reco"),
            "gre_q": weights.get("gre_q"),
        },
        "caveat": (
            "合成问卷数据（印度视角）；Chance of Admit 为预测值非真实录取结果；"
            "GRE 为总分 340 制（无分项）；research 为 0/1 二值；"
            "GRE/TOEFL/CGPA 高度共线（0.8+），Pearson 高估共线维权重。"
            "仅作画像权重初版参考，必须用含真实录取结果+科研/实习细节的内部数据复核后才可采纳。"
        ),
    }
    print(__import__("json").dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
