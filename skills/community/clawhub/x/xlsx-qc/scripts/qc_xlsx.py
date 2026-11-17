#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qc_xlsx.py — XLSX 交付前确定性质检。

只做机器可验证的检查。零第三方依赖（直接读 OOXML）。
用法: python qc_xlsx.py book.xlsx [--json]
退出码: 0=无阻断  1=有阻断
"""
import json
import re
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
ERR_VALUES = ("#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NULL!", "#NUM!")
EXT_REF = re.compile(r"\[\d+\][^!]*!")


def _shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall(f"{{{MAIN}}}si"):
        out.append("".join(t.text or "" for t in si.iter(f"{{{MAIN}}}t")))
    return out


def _workbook_sheets(z):
    """返回 [(sheet_name, sheet_path, hidden_bool)]；缺少 workbook.xml 时返回空表。"""
    if "xl/workbook.xml" not in z.namelist():
        return []
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {}
    if "xl/_rels/workbook.xml.rels" in z.namelist():
        rr = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        for r in rr:
            rels[r.get("Id")] = r.get("Target").lstrip("/")
    sheets = []
    for sh in wb.iter(f"{{{MAIN}}}sheet"):
        rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = rels.get(rid, "")
        if target and not target.startswith("xl/"):
            target = "xl/" + target
        sheets.append((sh.get("name"), target, sh.get("state") in ("hidden", "veryHidden")))
    return sheets


def _is_number(s):
    return bool(re.fullmatch(r"\s*-?\d+(\.\d+)?([eE][+-]?\d+)?\s*%?\s*", s or ""))


def check(path: Path):
    res = {"file": path.name, "sheets": 0, "issues": [], "stats": {}}
    sheet_issues = []

    def issue(sev, sheet, ref, code, msg):
        sheet_issues.append({"severity": sev, "sheet": sheet, "cell": ref, "code": code, "msg": msg})

    if not zipfile.is_zipfile(path):
        issue("BLOCK", None, None, "NOT_ZIP", "不是有效的 XLSX（不是 zip 容器），文件可能已损坏")
        res["issues"] = sheet_issues
        res["summary"] = {"block": 1, "warn": 0}
        return res
    try:
        return _scan(path, res, sheet_issues, issue)
    except Exception as e:  # 残缺/非标文件不允许让质检器崩掉
        issue("BLOCK", None, None, "PARSE_ERROR",
              f"文件结构异常，解析中断：{type(e).__name__}: {e}。"
              "常见原因是文件被第三方工具改写或传输中损坏，建议用 Excel/WPS 重新另存后重试")
        res["issues"] = sheet_issues
        res["summary"] = {"block": sum(1 for i in sheet_issues if i["severity"] == "BLOCK"),
                          "warn": sum(1 for i in sheet_issues if i["severity"] == "WARN")}
        return res


def _scan(path, res, sheet_issues, issue):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        shared = _shared_strings(z)
        sheets = _workbook_sheets(z)
        if not sheets:
            sheets = [(f"Sheet{i+1}", n, False) for i, n in
                      enumerate(sorted(x for x in names if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", x)))]
        res["sheets"] = len(sheets)

        n_formula = n_error = n_ext = n_textnum = n_merged = 0
        for sname, spath, hidden in sheets:
            if hidden:
                issue("WARN", sname, None, "HIDDEN_SHEET",
                      "该工作表被隐藏：收件人可能忽略其中数据，或数据在无人察觉的情况下被带走")
            if spath not in names:
                continue
            root = ET.fromstring(z.read(spath))

            # 隐藏行列
            for col in root.iter(f"{{{MAIN}}}col"):
                if col.get("hidden") in ("1", "true"):
                    rng = f"{col.get('min')}:{col.get('max')}"
                    issue("WARN", sname, f"列{rng}", "HIDDEN_COL",
                          f"第 {rng} 列被隐藏：排序/筛选/复制时会漏掉，统计口径易被误读")

            for row in root.iter(f"{{{MAIN}}}row"):
                if row.get("hidden") in ("1", "true"):
                    issue("WARN", sname, f"行{row.get('r')}", "HIDDEN_ROW",
                          f"第 {row.get('r')} 行被隐藏：同上")

            for c in root.iter(f"{{{MAIN}}}c"):
                ref = c.get("r")
                t = c.get("t")
                f = c.find(f"{{{MAIN}}}f")
                v = c.find(f"{{{MAIN}}}v")

                # 公式错误
                if t == "e":
                    n_error += 1
                    issue("BLOCK", sname, ref, "FORMULA_ERROR",
                          f"单元格含错误值 {v.text if v is not None else '?'}，交付后对方第一眼就看到报错")
                    continue
                if v is not None and v.text and v.text.strip() in ERR_VALUES:
                    n_error += 1
                    issue("BLOCK", sname, ref, "FORMULA_ERROR", f"缓存值为 {v.text}")

                if f is not None and f.text:
                    n_formula += 1
                    if EXT_REF.search(f.text):
                        n_ext += 1
                        issue("BLOCK", sname, ref, "EXTERNAL_REF",
                              f"公式引用了外部工作簿（{f.text[:40]}）：对方打开时必然取不到值")
                    if ref and "!" in f.text and not EXT_REF.search(f.text):
                        # 同表内引用，标记为 INFO 级别的事实
                        pass

                # 文本型数字
                if t == "s" and v is not None and v.text:
                    try:
                        sval = shared[int(v.text)]
                    except (ValueError, IndexError):
                        sval = ""
                    if _is_number(sval):
                        n_textnum += 1
                        issue("WARN", sname, ref, "TEXT_NUMBER",
                              f"数字以文本存储（{sval}）：SUM/排序/透视表会静默漏算")
                if t == "inlineStr":
                    is_el = c.find(f"{{{MAIN}}}is")
                    sval = "".join(x.text or "" for x in is_el.iter(f"{{{MAIN}}}t")) if is_el is not None else ""
                    if _is_number(sval):
                        n_textnum += 1
                        issue("WARN", sname, ref, "TEXT_NUMBER",
                              f"数字以文本存储（{sval}）：SUM/排序/透视表会静默漏算")

            for mc in root.iter(f"{{{MAIN}}}mergeCell"):
                n_merged += 1
            if n_merged:
                issue("WARN", sname, None, "MERGED_CELLS",
                      f"{n_merged} 处合并单元格：排序、筛选、填充会异常，下游处理常见事故来源")

        res["stats"] = {"sheets": res["sheets"], "formulas": n_formula,
                        "formula_errors": n_error, "external_refs": n_ext,
                        "text_numbers": n_textnum, "merged": n_merged}

    res["issues"] = sheet_issues
    res["summary"] = {
        "block": sum(1 for i in sheet_issues if i["severity"] == "BLOCK"),
        "warn": sum(1 for i in sheet_issues if i["severity"] == "WARN"),
    }
    return res


def render(res):
    o = [f"文件: {res['file']}",
         f"工作表: {res['sheets']} | 公式: {res['stats'].get('formulas', 0)} | "
         f"阻断 {res['summary']['block']} / 提醒 {res['summary']['warn']}", ""]
    for i in res["issues"]:
        loc = f"{i['sheet']}!{i['cell']}" if i["cell"] else (i["sheet"] or "--")
        o.append(f"[{i['severity']}] {loc} {i['code']}: {i['msg']}")
    if not res["issues"]:
        o.append("未发现机器可检出问题。")
    o.append("")
    o.append("提示：口径是否一致、口径与业务是否匹配属主观项，需人工判断。")
    return "\n".join(o)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    p = Path(args[0])
    if not p.is_file():
        print(f"文件不存在: {p}")
        sys.exit(2)
    res = check(p)
    print(json.dumps(res, ensure_ascii=False, indent=2) if "--json" in sys.argv else render(res))
    sys.exit(1 if res["summary"]["block"] else 0)


if __name__ == "__main__":
    main()
