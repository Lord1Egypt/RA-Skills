# -*- coding: utf-8 -*-
"""无人机运营合规分类判定器 — 零依赖单文件 CLI · JSON IR 输出。

规则源（条款号与阈值数值**均待人工核对**，见输出字段 clause_review_checklist）：
  《无人驾驶航空器飞行管理暂行条例》(国务院令761号, 2024-01-01 施行) 第6/12/16/31/32条 + CCAR-92
定位：决策支持工具，非权威结论，须人工复核；一律以官方最新文本为准。
"""
import argparse, json, sys

META = {
    "slug": "uas-ops-checker",
    "version": "1.0.0",
    "args": [
        {"name": "mtow", "help": "最大起飞重量(kg)", "required": False},
        {"name": "empty_weight", "help": "空机重量(kg)", "required": False},
    ],
}

# 等级严重度序（用于“从严推定”：在输入不足可能出现的等级中取义务最重者）
GRADE_SEVERITY = ["微型", "轻型", "小型", "中型", "大型"]

# 分类级联的阈值断点（数值待人工核对，见 CLAUSE_CHECKLIST；本包未凭记忆改动任何数值）
_BREAKPOINTS = [0.25, 4.0, 7.0, 15.0, 25.0, 150.0]

# 条款号待人工核对清单：哪一条款/数值用于什么判定（随输出一并给出，便于人工复核）
CLAUSE_CHECKLIST = [
    {"clause": "暂行条例 第6条", "used_for": "无人驾驶航空器分类（微型/轻型/小型/中型/大型）的规则来源",
     "status": "待人工核对"},
    {"clause": "暂行条例 第12条", "used_for": "微型/轻型的实名登记与适飞空域（真高≤120m）内免执照义务",
     "status": "待人工核对"},
    {"clause": "暂行条例 第16条", "used_for": "小型的执照/实名登记/责任保险义务（原实现引用，条号待核）",
     "status": "待人工核对"},
    {"clause": "暂行条例 第31条 / 第32条", "used_for": "中型/大型的运营合格证、适航与飞行活动申请义务",
     "status": "待人工核对"},
    {"clause": "CCAR-92", "used_for": "分类参数与运行要求（轻型/小型分支引用）",
     "status": "待人工核对"},
    {"clause": "GB 45438-2025", "used_for": "AIGC 标识字段 aigc_mark 的标注依据",
     "status": "待人工核对"},
    {"clause": "阈值 0.25 / 4 / 7 / 15 / 25 / 150 (kg)", "used_for": "分类级联判定的断点取值（空机重量与最大起飞重量）",
     "status": "待人工核对"},
]

# 各等级的义务集与规则出处（出处＝条款依据，非运营行为记录）
RULES = {
    "微型": {
        "obligations": ["微型无人机在适飞空域（真高≤120m）飞行无需操控员执照", "依法完成实名登记"],
        "evidence": ["暂行条例 第6条", "暂行条例 第12条"],
    },
    "轻型": {
        "obligations": ["实名登记", "在适飞空域（真高≤120m）飞行无需执照",
                        "不得突破性能限制（高度/速度/空域）"],
        "evidence": ["暂行条例 第6条", "暂行条例 第12条", "CCAR-92"],
    },
    "小型": {
        "obligations": ["操控员执照（视具体机型）", "实名登记", "强制责任保险", "在适飞空域外飞行需申请"],
        "evidence": ["暂行条例 第6条", "暂行条例 第16条", "CCAR-92"],
    },
    "中型": {
        "obligations": ["运营合格证", "适航许可", "操控员执照", "飞行活动申请", "强制保险"],
        "evidence": ["暂行条例 第6条", "暂行条例 第31/32条"],
    },
    "大型": {
        "obligations": ["运营合格证", "型号合格证/适航证", "操控员执照", "飞行活动申请", "强制保险"],
        "evidence": ["暂行条例 第6条", "暂行条例 第31/32条"],
    },
}

NOTES = [
    "分级阈值以「最大起飞重量与空机重量同时满足」为准；参数不足时按从严推定（取可能等级中义务最重者），"
    "不静默按宽松等级输出（阈值与条款号以官方最新文本为准）。",
    "涉及微型/轻型在管制空域或超出性能限制飞行须另行申请。",
    "涉外/商业运营需额外审查，本工具不含该项判定。",
    "本输出 evidence 字段为『规则出处（条款依据）』；条款号与阈值数值待人工核对（见 clause_review_checklist）。",
    "本输出为分类判定依据，不是行为日志，也不构成对实际运营行为的记录。",
]


class GateError(Exception):
    pass


def _probe_values():
    """覆盖全部分类断点的代表值（含断点两侧探针与两端极值），用于“从严推定”枚举。"""
    vals = [1e-9, 1e6]
    for b in _BREAKPOINTS:
        vals += [b - 1e-6, b, b + 1e-6]
    return [v for v in vals if v > 0]


def _grade_for(m, e):
    """完整参数下的级联判定（按微型→大型顺序级联，命中即返回该等级）。

    规则源：无人驾驶航空器飞行管理暂行条例(国务院令761号,2024-01-01施行) 第6条 + CCAR-92 分类参数。
    """
    if (m is not None and m <= 0.25) or (e is not None and e < 0.25):
        return "微型"
    if (m is not None and m <= 7) and (e is not None and e <= 4):
        return "轻型"
    if (m is not None and m <= 25) and (e is not None and e <= 15):
        return "小型"
    if m is not None and m <= 150:
        return "中型"
    return "大型"


def _possible_grades(m, e):
    """输入不完整时，枚举物理可行补全（空机重量 ≤ 最大起飞重量）下所有可达等级，按严重度升序去重。"""
    grades = set()
    if e is None:
        for cand in _probe_values():
            if 0 < cand <= m:
                grades.add(_grade_for(m, cand))
    else:
        for cand in _probe_values():
            if cand >= e:
                grades.add(_grade_for(cand, e))
    return sorted(grades, key=lambda g: GRADE_SEVERITY.index(g))


def classify_uas(args):
    """无人机机型分类 + 运营合规路径判定（JSON IR 结果体）。"""
    mtow = args.get('mtow')          # 最大起飞重量 kg
    empty = args.get('empty_weight') # 空机重量 kg
    if mtow is None and empty is None:
        raise GateError("缺少必要参数：请提供 mtow(最大起飞重量) 或 empty_weight(空机重量)（kg）")
    try:
        m = float(mtow) if mtow is not None else None
        e = float(empty) if empty is not None else None
    except (TypeError, ValueError):
        raise GateError("mtow / empty_weight 必须为数字（kg）")
    if (m is not None and m <= 0) or (e is not None and e <= 0):
        raise GateError("mtow / empty_weight 必须为正数（kg）")
    if m is not None and e is not None and e > m:
        raise GateError("empty_weight 不应大于 mtow（空机重量 > 最大起飞重量），请核对输入")

    warnings = []
    missing = "empty_weight" if e is None else ("mtow" if m is None else None)

    if missing:
        # 输入不完整：从严推定，不静默错判
        warnings.append(
            "输入不完整：仅提供单一重量参数（缺 %s）；官方分类同时使用最大起飞重量与空机重量，"
            "建议补齐另一参数后复核。" % missing)
        grades = _possible_grades(m, e)
        strict = grades[-1]                      # 义务最重者
        lenient = grades[0]
        grade = strict
        basis = "从严推定（输入不完整）"
        if lenient != strict:
            warnings.append(
                "分类不确定（可能等级区间 %s～%s）：已按从严推定取『%s』（义务最重者），"
                "实际等级可能更宽松；请补齐参数后复核。" % (lenient, strict, strict))
    else:
        grade = _grade_for(m, e)
        basis = "完整参数直接判定"
        grades = [grade]

    if grade in ("小型", "中型", "大型"):
        warnings.append(
            "该等级不适用微型/轻型的『适飞空域内免执照』简化路径：实际合规义务还取决于空域属性、"
            "运营主体资质与保险安排；涉管制空域、商业运营或涉外运营的须另行申请与审查（本工具不含该项判定）。")

    return {
        "grade": grade,
        "grade_basis": basis,
        "possible_grades": grades,
        "obligations": RULES[grade]["obligations"],
        "evidence": RULES[grade]["evidence"],
        "notes": NOTES,
        "warnings": warnings,
    }


def _run(args):
    res = classify_uas(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc


def main():
    p = argparse.ArgumentParser(prog="uas-ops-checker", description="无人机运营合规分类判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    # AIGC 标识：本输出由工具生成（确定性规则计算 + AI 辅助撰写规则文本）⇒ is_generated=True；
    # 具体标注口径（是否属 GB 45438-2025 意义上的“生成合成内容”）待人工核对，见 label_note。
    AIGC = {"standard": "GB 45438-2025", "is_generated": True,
            "generator": META["slug"] + "@SynomosAI",
            "content_type": "decision_support_output",
            "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
            "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"mtow": "0.2"}, {"mtow": "5"}, {"mtow": "120"}]
        allok = True
        out_list = []
        for d in demos:
            try:
                res, rc = _run(dict(d))
                out_list.append({"tool": META["slug"], "input": d, "result": res, "rc": rc,
                                 "clause_review_checklist": CLAUSE_CHECKLIST, "aigc_mark": AIGC})
            except GateError as e:
                allok = False
                out_list.append({"tool": META["slug"], "input": d, "errors": [str(e)], "rc": 2,
                                 "clause_review_checklist": CLAUSE_CHECKLIST, "aigc_mark": AIGC})
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
        # 进程退出码遵循本技能库约定：0＝案例全部执行完毕 / 2＝存在输入错误。
        # 各案例的实际 rc 见 IR 的 rc 字段（可为 0/1/2），--demo 不代替单次调用的 rc 语义。
        sys.exit(0 if allok else 2)
    args = {k: getattr(ns, k) for k in argnames}
    try:
        res, rc = _run(args)
    except GateError as e:
        ir = {"tool": META["slug"], "version": META["version"], "input": args, "errors": [str(e)], "rc": 2,
              "clause_review_checklist": CLAUSE_CHECKLIST, "aigc_mark": AIGC}
        print(json.dumps(ir, ensure_ascii=False, indent=2))
        sys.exit(2)
    ir = {"tool": META["slug"], "version": META["version"], "input": args, "result": res, "rc": rc,
          "clause_review_checklist": CLAUSE_CHECKLIST, "aigc_mark": AIGC}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)


if __name__ == "__main__":
    main()
