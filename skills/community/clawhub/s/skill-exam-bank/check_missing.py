"""漏题自检：核验每卷抽取结果 题号 是否连续（按题型分组）。
用法: python check_missing.py <抽取.json> [ocr.md]
- 题号来源：记录里的 题号 字段；缺失则从 题目内容 解析 "数字." 或 "第N题"。
- 按 题型 分组，每组检查 min..max 连续（兼容"全局连续编号"与"分节重新编号"两种试卷）。
- 若提供 ocr.md：解析各题型期望题数（如"共25题"），与实际数量对比，捕获"整节漏抽"。
- 输出人类可读报告到 stdout，并写 <json>.check.json；
  有缺题退出码 1，无缺题退出码 0（便于脚本/agent 判断要不要补题）。
"""
import sys, os, re, json, argparse


def get_qnum(rec):
    """优先用 题号 字段，否则从 题目内容 解析。"""
    if rec.get("题号") not in (None, ""):
        try:
            return int(rec["题号"])
        except (TypeError, ValueError):
            pass
    t = rec.get("题目内容", "") or ""
    m = re.match(r"\s*(\d+)\s*[.、．]", t)
    if m:
        return int(m.group(1))
    m = re.search(r"第\s*(\d+)\s*题", t)
    if m:
        return int(m.group(1))
    return None


def parse_ocr_expect(md_path):
    """从 OCR markdown 解析各题型期望题数。返回 {题型: int}。"""
    if not md_path or not os.path.exists(md_path):
        return {}
    text = open(md_path, encoding="utf-8").read()
    sec_map = {
        "单项选择": "单选", "多选": "多选", "判断": "判断", "填空": "填空",
        "简答": "简答", "计算": "计算", "论述": "论述", "材料": "材料", "分析": "分析",
    }
    expect = {}
    for m in re.finditer(r"(?:一|二|三|四|五|六|七|八|九|十)[、.]\s*([一-龥]{2,8}?题)", text):
        sec = m.group(1)
        em = re.search(r"共\s*(\d+)\s*题", text[m.end():m.end() + 40])
        cnt = int(em.group(1)) if em else None
        ttype = None
        for k, v in sec_map.items():
            if k in sec:
                ttype = v
                break
        if ttype and cnt:
            expect[ttype] = cnt
    return expect


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("md_path", nargs="?", default=None)
    a = ap.parse_args()

    with open(a.json_path, encoding="utf-8") as f:
        recs = json.load(f)
    if isinstance(recs, dict):
        recs = recs.get("records", [])

    groups = {}
    for r in recs:
        g = r.get("题型", "未知")
        q = get_qnum(r)
        groups.setdefault(g, []).append(q)

    ocr_expect = parse_ocr_expect(a.md_path)
    report = {"total": len(recs), "groups": {}, "missing": [], "ocr_expect": ocr_expect}
    has_gap = False

    for g, nums in groups.items():
        nums = [n for n in nums if n is not None]
        if not nums:
            report["groups"][g] = {"count": len(groups[g]), "note": "无题号，无法核验"}
            continue
        lo, hi = min(nums), max(nums)
        missing = [n for n in range(lo, hi + 1) if n not in nums]
        report["groups"][g] = {"count": len(groups[g]), "range": [lo, hi], "missing": missing}
        if missing:
            has_gap = True
            for n in missing:
                report["missing"].append({"题型": g, "题号": n})

    for t, exp in ocr_expect.items():
        got = len(groups.get(t, []))
        if got != exp:
            has_gap = True
            report["missing"].append({"题型": t, "期望": exp, "实抽": got, "类型": "整节数量不符"})

    out = a.json_path + ".check.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"总题数: {len(recs)}")
    for g, info in report["groups"].items():
        if "missing" not in info:
            print(f"  [{g}] 数量={info['count']} {info.get('note','')}")
        else:
            miss = info["missing"]
            flag = (" ❌缺 " + ",".join(map(str, miss))) if miss else " ✅连续"
            print(f"  [{g}] 数量={info['count']} 范围={info['range']}{flag}")
    if ocr_expect:
        for t, exp in ocr_expect.items():
            got = len(groups.get(t, []))
            print(f"  OCR校验[{t}] 期望={exp} 实抽={got} {'✅' if got == exp else '❌'}")
    if report["missing"]:
        print("\n❌ 发现缺题：")
        for m in report["missing"]:
            print("  ", m)
    else:
        print("\n✅ 题号连续，无缺题。")
    print(f"\n报告已写: {out}")
    sys.exit(1 if has_gap else 0)


if __name__ == "__main__":
    main()
