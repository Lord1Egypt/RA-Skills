#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
留学助理 — 引擎侧采纳包导出（Gate 1）

将本地已收敛/已核实的产物合并为一份部署配置 JSON，供引擎侧采纳：
  1. 校档映射（school_tiers.json，19 校 reach/match/safety）
  2. 选校分桶 v1（calibrate.py 相对命中率矩阵 + tiering_advice）
  3. 画像权重 v1（calibrate_ucla.py UCLA 初版）
  4. 录取画像（school_profiles.jsonl，9 校，B 类起步）

产出：deliverables/engine_adoption_gate1.json
注意：本地只产出"建议配置"，最终由引擎侧审核采纳；verified=false 部分必须带"待核实"提示。
"""
import json
import os
import subprocess
import sys
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # skill 根目录
CASES = os.path.join(BASE, "cases")
SCRIPTS = os.path.join(BASE, "scripts")
OUT_DIR = os.path.join(BASE, "deliverables")


def run_calibrate(script):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)],
                       capture_output=True, text=True, cwd=BASE)
    if r.returncode != 0:
        raise RuntimeError(f"{script} 运行失败: {r.stderr[:500]}")
    return json.loads(r.stdout)


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main():
    cal = run_calibrate("calibrate.py")          # 选校分桶 v1
    ucla = run_calibrate("calibrate_ucla.py")    # 画像权重 v1
    with open(os.path.join(CASES, "school_tiers.json"), "r", encoding="utf-8") as f:
        tiers = json.load(f)
    profiles = load_jsonl(os.path.join(CASES, "school_profiles.jsonl"))

    pkg = {
        "package": "engine-adoption-gate1",
        "version": "1.0",
        "generated_at": str(date.today()),
        "role": "本地建议配置，引擎侧审核采纳后写入 search.py CONFIG / analytics / 知识库",
        "sections": {
            "school_tier_map": {
                "comment": "校档定义建议（人工判定，可调）。用于选校分层与分桶矩阵的轴。",
                "map": {k: v for k, v in tiers.items() if not k.startswith("_")},
            },
            "tier_bucketing": {
                "method": cal["method"],
                "method_note": cal["method_note"],
                "band_rule": cal["band_rule"],
                "relative_hit_rate_matrix": cal["relative_hit_rate_matrix"],
                "tiering_advice": cal["tiering_advice"],
                "by_gre_q": cal["by_gre_q"],
                "data": {"n_cases": cal["n_cases"],
                         "n_applications": cal["n_applications"],
                         "sources": ["gradcafe", "1point3acres"],
                         "verified": False},
            },
            "portrait_weights": {
                "version": "v1-draft",
                "source": ucla["source"],
                "n_samples": ucla["n_samples"],
                "method": ucla["method"],
                "relative_weight": ucla["engine_6dims"],
                "caveat": ucla["caveat"],
                "verified": False,
            },
            "school_profiles": {
                "note": "一亩三分地录取画像（B 类起步）。仅录取样本，作录取标准参考线，非录取率。",
                "schools": profiles,
                "verified": False,
            },
        },
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "engine_adoption_gate1.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pkg, f, ensure_ascii=False, indent=2)

    print(f"已生成: {out_path}")
    print(f"  sections: {list(pkg['sections'].keys())}")
    print("  tiering_advice 3.6-3.8:", pkg["sections"]["tier_bucketing"]["tiering_advice"]["3.6-3.8"])
    print("  portrait_weights:", pkg["sections"]["portrait_weights"]["relative_weight"])
    print("  school_profiles:", len(pkg["sections"]["school_profiles"]["schools"]), "校")


if __name__ == "__main__":
    main()
