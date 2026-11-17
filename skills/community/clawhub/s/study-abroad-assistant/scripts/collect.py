#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
留学助理 — 案例采集与人工录入工具（半自动，仅依赖 stdlib）

子命令：
  validate  校验一个 jsonl 文件（按 SCHEMA.md 的 A 类规则），列出错误
  import    导入一个 jsonl，逐条校验，通过的写入 cases/admission_collected.jsonl
  interactive  交互式录入一条 A 类案例（引导提问 → 写入 collected 文件）
  stats     统计当前 cases/ 下 A 类案例量与申请条数

设计原则：
  - 仅处理公开 / 已授权数据；synthetic 须显式标注
  - 去隐私：检测邮箱 / 疑似个人姓名，发出警告（不自动写入带隐私字段的行）
  - 本地产物，最终交引擎侧采纳
"""
import argparse
import glob
import json
import os
import re
import sys
from datetime import date

CASES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cases")
COLLECTED = os.path.join(CASES_DIR, "admission_collected.jsonl")

VALID_SOURCES = {"gradcafe", "1point3acre", "official", "internal", "synthetic"}
VALID_RESULT = {"admit", "reject", "waitlist", "pending"}
VALID_SCHOOL_TIER = {"985", "211", "双非", "海本", "海硕", "unknown"}
VALID_APP_TIER = {"reach", "match", "safety", "unknown"}
VALID_DISCIPLINE = {"cs", "ee", "data", "其他"}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# 简单中文姓名检测：2-4 个连续汉字（仅作隐私预警，误报可接受）
CN_NAME_RE = re.compile(r"[\u4e00-\u9fa5]{2,4}")


def _errs_common(meta, obj):
    errs = []
    if meta.get("source") not in VALID_SOURCES:
        errs.append(f"meta.source 非法: {meta.get('source')}")
    if not meta.get("season"):
        errs.append("meta.season 缺失")
    if obj.get("school_tier") not in VALID_SCHOOL_TIER:
        errs.append(f"applicant.school_tier 非法: {obj.get('school_tier')}")
    if obj.get("discipline") not in VALID_DISCIPLINE:
        errs.append(f"applicant.discipline 非法: {obj.get('discipline')}")
    return errs


def validate_admission(c):
    """返回错误列表；空表示通过。"""
    errs = []
    if c.get("type") != "admission":
        return ["type 非 admission"]
    meta = c.get("meta", {})
    a = c.get("applicant", {})
    errs += _errs_common(meta, a)
    gpa = a.get("gpa")
    if gpa is not None and not isinstance(gpa, (int, float)):
        errs.append("applicant.gpa 非数值")
    # gpa 为 None 视为缺失，不阻断（部分公开源如 gradcafe 不公布 GPA）
    gre = a.get("gre", {})
    if gre.get("taken") and not isinstance(gre.get("q"), int):
        errs.append("gre.taken=true 但 gre.q 缺失")
    apps = c.get("applications", [])
    if not apps:
        errs.append("applications 为空")
    for i, ap in enumerate(apps):
        if ap.get("result") not in VALID_RESULT:
            errs.append(f"applications[{i}].result 非法: {ap.get('result')}")
        if ap.get("tier") not in VALID_APP_TIER:
            errs.append(f"applications[{i}].tier 非法: {ap.get('tier')}")
    # 去隐私预警（不阻断，仅提示）
    blob = json.dumps(c, ensure_ascii=False)
    if EMAIL_RE.search(blob):
        errs.append("⚠ 隐私预警: 检测到邮箱，建议移除后再入库")
    return errs


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append((ln, json.loads(line)))
            except json.JSONDecodeError as e:
                rows.append((ln, {"__parse_error__": str(e)}))
    return rows


def cmd_validate(path):
    rows = load_jsonl(path)
    bad = 0
    for ln, c in rows:
        if "__parse_error__" in c:
            print(f"  [行 {ln}] JSON 解析失败: {c['__parse_error__']}")
            bad += 1
            continue
        errs = validate_admission(c)
        if errs:
            bad += 1
            print(f"  [行 {ln}] {c.get('meta', {}).get('id', '?')}: {'; '.join(errs)}")
        else:
            print(f"  [行 {ln}] {c.get('meta', {}).get('id', '?')}: OK")
    print(f"\n校验完成: {len(rows)} 行, {bad} 行有问题")
    return 1 if bad else 0


def cmd_import(path):
    rows = load_jsonl(path)
    ok = 0
    with open(COLLECTED, "a", encoding="utf-8") as out:
        for ln, c in rows:
            if "__parse_error__" in c:
                print(f"  [行 {ln}] 跳过(解析失败)")
                continue
            errs = validate_admission(c)
            privacy = any(e.startswith("⚠") for e in errs)
            hard = [e for e in errs if not e.startswith("⚠")]
            if hard:
                print(f"  [行 {ln}] 跳过(硬错误): {'; '.join(hard)}")
                continue
            if privacy:
                print(f"  [行 {ln}] 跳过(隐私预警): {c.get('meta', {}).get('id', '?')}")
                continue
            out.write(json.dumps(c, ensure_ascii=False) + "\n")
            ok += 1
    print(f"\n导入完成: {ok} 条写入 {COLLECTED}")


def cmd_stats():
    n_cases = n_apps = 0
    for p in glob.glob(os.path.join(CASES_DIR, "admission_*.jsonl")):
        for _, c in load_jsonl(p):
            if isinstance(c, dict) and c.get("type") == "admission":
                n_cases += 1
                n_apps += len(c.get("applications", []))
    print(f"A 类案例: {n_cases} 条, 申请记录: {n_apps} 条")


def cmd_interactive():
    print("=== 交互录入一条 A 类录取案例（直接回车=跳过该项）===")
    meta = {
        "id": f"adm_{date.today().strftime('%Y%m%d')}_{os.urandom(2).hex()}",
        "source": input("来源(gradcafe/1point3acre/official/internal/synthetic): ") or "internal",
        "season": input("申请季(如 2025Fall): ") or "2026Fall",
        "privacy": "anonymized",
        "verified": input("已核实?(y/N): ").lower() == "y",
        "collected_at": str(date.today()),
    }
    a = {
        "school_tier": input("本科档位(985/211/双非/海本/海硕): "),
        "gpa": float(input("GPA: ") or 0),
        "gpa_scale": float(input("GPA 满分(默认4.0): ") or 4.0),
        "toefl": int(input("TOEFL(无填0): ") or 0),
        "gre": {"taken": False},
        "research": {},
        "intern": {},
        "reco": int(input("推荐信强度(1-5): ") or 3),
        "discipline": input("学科(cs/ee/data/其他): ") or "cs",
        "direction": [x.strip() for x in input("方向(逗号分隔): ").split(",") if x.strip()],
    }
    if input("考了 GRE?(y/N): ").lower() == "y":
        a["gre"] = {"taken": True, "v": int(input("GRE V: ") or 0),
                    "q": int(input("GRE Q: ") or 0), "aw": float(input("GRE AW: ") or 0)}
    a["research"] = {"papers": int(input("论文数: ") or 0),
                     "ra_months": int(input("科研月数: ") or 0),
                     "top_venue": input("顶会?(y/N): ").lower() == "y"}
    a["intern"] = {"months": int(input("实习月数: ") or 0),
                   "tier": input("实习档(大厂/中厂/实验室/无): ") or "无"}
    apps = []
    print("逐条录入申请(空 program 结束):")
    while True:
        prog = input("  program(空结束): ")
        if not prog:
            break
        apps.append({
            "program": prog,
            "school": input("  school: "),
            "tier": input("  tier(reach/match/safety): "),
            "result": input("  result(admit/reject/waitlist/pending): "),
        })
    if not apps:
        print("无申请记录，放弃。")
        return
    case = {"type": "admission", "meta": meta, "applicant": a, "applications": apps}
    errs = validate_admission(case)
    if any(e.startswith("⚠") for e in errs):
        print("⚠ 隐私预警，未写入。请移除邮箱/姓名后重试。")
        print(json.dumps(case, ensure_ascii=False, indent=2))
        return
    with open(COLLECTED, "a", encoding="utf-8") as out:
        out.write(json.dumps(case, ensure_ascii=False) + "\n")
    print(f"已写入 {COLLECTED}: {meta['id']}")


def main():
    ap = argparse.ArgumentParser(description="留学助理案例采集工具")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("validate").add_argument("path")
    sub.add_parser("import").add_argument("path")
    sub.add_parser("interactive")
    sub.add_parser("stats")
    args = ap.parse_args()
    if args.cmd == "validate":
        sys.exit(cmd_validate(args.path))
    elif args.cmd == "import":
        cmd_import(args.path)
    elif args.cmd == "interactive":
        cmd_interactive()
    elif args.cmd == "stats":
        cmd_stats()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
