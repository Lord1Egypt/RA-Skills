# -*- coding: utf-8 -*-
"""医疗器械检测项目与实验室匹配器 — 零依赖单文件 CLI · JSON IR 输出。规则源：GB/T 16886 系列 / GB 9706.1 / YY 0505 / ISO 11135·11137·17665 / ISO 11607 / IEC 62304"""
import argparse
import json
import sys

META = {"slug": "test-lab-match-check", "version": "1.0.0", "args": [{"name": "device_type", "help": "器械类型: active/passive/implant/ivd（必填）"}, {"name": "material", "help": "主体材料: metal/polymer/ceramic/natural/biologic"}, {"name": "contact", "help": "接触性质: surface/insert/implant/blood/mucosa"}, {"name": "sterile", "help": "是否无菌提供: yes/no"}, {"name": "steril_method", "help": "灭菌方式: eo/radiation/steam"}, {"name": "has_software", "help": "是否含软件: yes/no"}, {"name": "dest", "help": "申报目的国: cn/eu/us（默认 cn）"}]}


class GateError(Exception):
    code = "E_RUNTIME"
    def __init__(self, msg, code=None):
        super().__init__(msg)
        if code:
            self.code = code


def match_test_lab(args):
    """检测项目推导与实验室资质匹配。规则源：GB/T 16886 系列 / GB 9706 / YY 0505 / ISO 11135·11137·17665 / ISO 11607 / GB 18279·18280。"""
    dtype = (args.get("device_type") or "").lower()
    if dtype not in ("active", "passive", "implant", "ivd"):
        raise GateError("--device_type 必填，且必须为 active / passive / implant / ivd 之一", "E_ENUM_INVALID")
    material = (args.get("material") or "").lower()
    contact = (args.get("contact") or "").lower()
    sterile = (args.get("sterile") or "").lower()
    method = (args.get("steril_method") or "").lower()
    software = (args.get("has_software") or "").lower()
    dest = (args.get("dest") or "cn").lower()
    if contact and contact not in ("surface", "insert", "implant", "blood", "mucosa"):
        raise GateError("contact 必须为 surface / insert / implant / blood / mucosa 之一", "E_ENUM_INVALID")
    if dest not in ("cn", "eu", "us"):
        raise GateError("dest 必须为 cn / eu / us 之一", "E_ENUM_INVALID")

    items = []
    if dtype == "implant" or contact == "implant":
        items.append("生物学评价·全套终点（GB/T 16886.1 表 A.1 植入类终点，含全身毒性/遗传毒性/致癌性/血液相容性等）")
    elif contact in ("blood", "mucosa"):
        items.append("生物学评价·血液/黏膜接触终点（含溶血、血液相容性）")
    else:
        items.append("生物学评价·基础终点（细胞毒性/致敏/刺激，按接触性质与时长选做）")
    if material:
        items.append("材料表征与化学表征（如适用，支持等同性与浸提液制备）")
    if dtype in ("active", "implant"):
        items.append("电气安全（GB 9706.1 通用 + 适用专用并列标准）")
        items.append("电磁兼容 EMC（YY 0505 / YY 9706.102）")
    if dtype == "ivd":
        items.append("分析性能（准确度/精密度/检出限/线性/干扰）与稳定性（实时 + 加速）")
    if sterile in ("yes", "true"):
        if method == "eo":
            items.append("环氧乙烷灭菌验证（ISO 11135 / GB 18279）+ EO 残留量")
        elif method == "radiation":
            items.append("辐射灭菌验证（ISO 11137 / GB 18280）+ 剂量设定")
        elif method == "steam":
            items.append("湿热灭菌验证（ISO 17665 / GB 18278）")
        else:
            items.append("灭菌验证（须先确定灭菌方式：eo / radiation / steam）")
        items.append("无菌屏障系统与包装验证（ISO 11607 / GB/T 19633）")
    if software in ("yes", "true"):
        items.append("软件验证与确认（含网络安全，按 IEC 62304 对应等级）")

    lab_qual = ["CMA（检验检测机构资质认定）", "CNAS（实验室认可）"]
    if dest in ("eu", "us"):
        lab_qual.append("境外注册场景须确认实验室报告可被公告机构/FDA 接受（认可范围与报告语言）")
    cycle = "%d–%d 周（视项目数量与实验室排期，属量级参考）" % (max(2, len(items)), max(6, len(items) * 3))

    warns = []
    if not material:
        warns.append("未提供 --material：材料类别直接影响生物相容性终点与化学表征，缺失将降低清单精度")
    if sterile in ("yes", "true") and method not in ("eo", "radiation", "steam"):
        warns.append("已声明无菌但未指定灭菌方式，无法给出确定的验证标准")
    oblig = [
        "实验室资质与其「认可范围」须逐一核对，超范围出具的报告不被接受",
        "检测样品须为设计定型后、与申报资料一致的产品",
        "检测项目应由产品标准/技术要求与风险管理输出共同推导，本清单为起点",
    ]
    notes = [
        "项目清单为「推导结果」，最终以产品技术要求、适用标准清单与注册检验要求为准",
        "周期为量级参考，不构成承诺",
        "出口注册（ce/fda）通常需要补充境外认可实验室报告，且标准版本可能不同",
    ]
    return {
        "device_type": dtype, "required_tests": items, "lab_qualification": lab_qual,
        "ref_cycle": cycle, "destination": dest,
        "obligations": oblig, "notes": notes,
        "evidence": ["GB/T 16886 系列", "GB 9706.1", "YY 0505", "ISO 11135/11137/17665", "ISO 11607", "IEC 62304"],
        "warnings": warns,
    }


def _call(args):
    fn_name = "match_test_lab"
    res = globals()[fn_name](args)
    return res


def main():
    p = argparse.ArgumentParser(prog="test-lab-match-check", description="医疗器械检测项目与实验室匹配器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, default=None, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR")
    ns = p.parse_args()
    names = [a["name"] for a in META["args"]]

    if ns.demo:
        ok = True
        for d in [{"device_type": "implant", "material": "metal", "contact": "implant", "sterile": "yes", "steril_method": "eo", "dest": "cn"}, {"device_type": "active", "material": "polymer", "contact": "surface", "sterile": "no", "has_software": "yes", "dest": "eu"}, {"device_type": "ivd", "contact": "blood", "dest": "cn"}]:
            try:
                res = _call(dict(d))
                rc = 1 if (res.get("warnings") or []) else 0
                print(json.dumps({"tool": META["slug"], "input": d, "result": res,
                                  "rc": rc, "error_code": None}, ensure_ascii=False))
            except GateError as e:
                ok = False
                print(json.dumps({"tool": META["slug"], "input": d, "errors": [str(e)],
                                  "rc": 2, "error_code": e.code}, ensure_ascii=False))
        sys.exit(0 if ok else 2)

    args = {k: getattr(ns, k) for k in names}
    if not any(v not in (None, "") for v in args.values()):
        p.print_help()
        sys.exit(0)
    try:
        res = _call(args)
    except GateError as e:
        print(json.dumps({"tool": META["slug"], "version": META["version"], "input": args,
                          "errors": [str(e)], "rc": 2, "error_code": e.code},
                         ensure_ascii=False, indent=2))
        sys.exit(2)
    rc = 1 if (res.get("warnings") or []) else 0
    ir = {"tool": META["slug"], "version": META["version"], "input": args,
          "result": res, "rc": rc, "error_code": None,
          "aigc_mark": {"standard": "GB 45438-2025", "is_generated": True,
                        "generator": META["slug"] + "@SynomosAI",
                        "content_type": "decision_support_output",
                        "disclaimer": "决策支持非权威结论，须人工复核；以官方最新文件为准"}}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)


if __name__ == "__main__":
    main()
