# -*- coding: utf-8 -*-
"""
build.example.py — 完全复刻（exact-replication）最小构建骨架 · 模板

管线（对齐 references/exact-replication-contract.md §2 六阶段）：
    S1 探查 → S2 逐页建模 → S3 原型分类 → S4 1:1 矢量底版
    → S5 槽位定义 + collision_report 碰撞预检
    → S6 ExactEditor.apply_pack 内容注入 + save + verify 零偏差验收 → 打印摘要

用法：
    1. 把本目录（slots.example.json / content_pack.example.json / 本脚本）复制到工作目录；
    2. 用 build_page_models 的实测 span 替换 slots.example.json 里的占位 bbox/text；
    3. 备好新图片素材（content_pack 里 image 槽位的文件名放到 ASSETS_DIR）；
    4. 替换下方 CONFIG 区的全部 "<...>" 占位常量；
    5. python3 build.example.py   → 打印验收摘要，PASS 才交付。

依赖：PyMuPDF(fitz)、numpy（exact_replication.py 依赖）。
脚本自动把技能包的 scripts/ 加入 sys.path 以 import exact_replication，无需安装包。

注意：所有 "<...>" 均为占位常量；未替换直接运行会因文件不存在而报错（预期行为）。
"""
from __future__ import annotations

import json
import os
import sys

# 让本模板无论放在技能包内还是复制到别处，都能找到引擎
HERE = os.path.dirname(os.path.abspath(__file__))            # .../templates/time-exact/
SKILL_ROOT = os.path.dirname(os.path.dirname(HERE))          # 技能包根（若复制出去请改成绝对路径）
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

import fitz  # noqa: E402
from exact_replication import (  # noqa: E402
    build_page_models, classify_archetype, replicate_1to1,
    collision_report, ExactEditor, verify, fallback_font,
)

# ---------------- CONFIG：全部为占位常量，替换后即可运行 ----------------
SRC = "<原刊.pdf 绝对路径>"                  # 只读，绝不修改原刊
OUT_DIR = "<产物输出目录 绝对路径>"
ASSETS_DIR = "<新图片素材目录 绝对路径>"       # content_pack 里 image 槽位的文件名在此查找
SLOTS_JSON = os.path.join(HERE, "slots.example.json")
PACK_JSON = os.path.join(HERE, "content_pack.example.json")
PACK_KEY = "A"                                 # 选用内容包 "A"（英文）/ "B"（中文）

BASE_PDF = os.path.join(OUT_DIR, "base_1to1.pdf")                       # S4 底版（归档/比对用）
OUT_PDF = os.path.join(OUT_DIR, "exact_replication_%s.pdf" % PACK_KEY)  # S6 复刻产物
REPORT = os.path.join(OUT_DIR, "zero_drift_%s.json" % PACK_KEY)         # 零偏差验收报告
# ------------------------------------------------------------------------


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- S1 探查 + S2 逐页建模 + S3 原型分类 ----
    doc = fitz.open(SRC)
    models = build_page_models(doc)                       # 不依赖任何外部 JSON，任意期刊 PDF 可直接跑
    area = models[0]["canvas"][0] * models[0]["canvas"][1]
    archetypes = [classify_archetype(m, area) for m in models]
    dist = {a: archetypes.count(a) for a in set(archetypes)}
    print("[S1-S3] 页数=%d 画布=%s 原型分布=%s" % (len(models), models[0]["canvas"], dist))
    doc.close()

    # ---- S4 1:1 矢量零偏差底版（整页 Form XObject，像素 100% 相同）----
    # 说明：ExactEditor 直接以 SRC 为副本开槽；底版用于阶段 A 归档与逐页比对，
    # verify() 的比对基准仍是 SRC（原刊），因此这里只产出底版文件。
    replicate_1to1(SRC, BASE_PDF)

    # ---- S5 槽位定义 + 碰撞预检（必须在注入前，不能靠扩大 mask 掩盖）----
    with open(SLOTS_JSON, encoding="utf-8") as f:
        slots = json.load(f)["slots"]
    conflicts = collision_report(models, slots)
    print("[S5] 槽位=%d 碰撞=%d" % (len(slots), len(conflicts)))
    if conflicts:
        for c in conflicts[:5]:
            print("   P%d victim=%r size=%s bbox=%s" %
                  (c["page"], c["victim_text"], c["victim_size"], c["victim_bbox"]))
        raise SystemExit("[abort] 槽位会误删非槽位文字，请收缩矩形/改选行/重建元素后重试"
                         "（见 references/exact-replication-contract.md §7 碰撞教训）")

    # ---- S6 内容注入 ----
    # image 槽位的值是文件名，这里拼成 ASSETS_DIR 下的真实路径
    with open(PACK_JSON, encoding="utf-8") as f:
        pack = json.load(f)[PACK_KEY]
    values = dict(pack["values"])
    for s in slots:
        if s["type"] == "image" and s["id"] in values:
            values[s["id"]] = os.path.join(ASSETS_DIR, values[s["id"]])

    ed = ExactEditor(SRC, models=models)       # models 复用，避免重复建模
    ed.apply_pack(slots, dict(values=values))  # 按 type 分派 text/image/chart/chart-redraw
    ed.save(OUT_PDF)

    # ---- 零偏差验收：matrix=2x、mask=删除区∪绘制区、pad_px=3 ----
    rep = verify(SRC, OUT_PDF, ed.masks, matrix=2.0, pad_px=3, out_json=REPORT)
    s = rep["summary"]
    print("\n=== 零偏差验收摘要 · 内容包 %s (%s) ===" % (PACK_KEY, pack["name"]))
    print("  画布/页数一致        : %s" % rep["canvas_all_equal"])
    print("  改动页               : %d" % s["edited_pages"])
    print("  槽位外像素零漂移     : %s" % s["all_edited_pages_zero_drift"])
    print("  最差槽位外变化率     : %s" % s["worst_outside_change_ratio"])
    print("  未改动页 100%% 相同  : %s (%d 页受检)" %
          (s["untouched_pages_identical"], s["untouched_pages_checked"]))
    for p in rep["pages"]:
        print("  P%02d 槽位外相同率=%.4f%% 槽位内变化率=%.4f zero_drift=%s" %
              (p["page"], p["outside_identical_pct"], p["inside_change_ratio"], p["zero_drift"]))
    tiers = sorted({t for r in ed.slot_log for t in r.get("tiers", [])})
    print("  字形资源档位         : %s" % (tiers or "无"))
    print("  verdict              : %s" % s["verdict"])
    print("  报告                 : %s" % REPORT)

    # 仅演示：需要手工排查字重映射时可调用 fallback_font（T2/T3 回退）
    _ = fallback_font("HaffnerTIMEDisplay-Black", cjk=False)
    return 0 if s["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
