#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UDI 格式校验器（零依赖 / 确定性 / JSON IR / 修复回执）
# 支持 GS1 应用标识符 01/10/11/17/21/240/30；校验位按 GS1 Mod10。
import argparse, json, re, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FIXED_AI = {"01": 14, "11": 6, "17": 6}
VAR_AI = {"10": 20, "21": 20, "240": 30, "30": 8}
ALL_AI = list(FIXED_AI) + list(VAR_AI)


def gs1_check(d13):
    w = 3
    s = 0
    for ch in reversed(d13):
        s += int(ch) * w
        w = 4 - w
    return str((10 - s % 10) % 10)


def valid_ymd(s):
    if not re.match(r"^\d{6}$", s):
        return False
    mm, dd = int(s[2:4]), int(s[4:6])
    return 1 <= mm <= 12 and 0 <= dd <= 31


def pretty_ymd(s):
    dd = int(s[4:6])
    note = "(00=当月最后一天)" if dd == 0 else ""
    return "%04d-%s-%02d%s" % (2000 + int(s[:2]), s[2:4], dd, note)


def parse_paren(text):
    comps, errors = {}, []
    tokens = re.findall(r"\((\d{2})\)([^\(\)]*)", text)
    prefix = text.split("(")[0]
    if prefix.strip():
        errors.append(("UDI_E_UNKNOWN_AI", "前缀", prefix.strip(), "串首存在非标识内容，请核对输入"))
    for ai, val in tokens:
        if ai in comps:
            errors.append(("UDI_E_UNKNOWN_AI", ai, val, "同一 AI 重复出现"))
        comps[ai] = val.strip()
    return comps, errors


def parse_plain(text):
    comps, errors = {}, []
    m = re.match(r"^01(\d{14})", text)
    if not m:
        errors.append(("UDI_E_AMBIGUOUS", "整体", "", "无括号形态仅支持以 (01)+14 位开头的串；请改用带括号输入"))
        return comps, errors
    comps["01"] = m.group(1)
    rest = text[16:]
    pos = 0
    while pos < len(rest):
        ai = rest[pos:pos + 2]
        if ai in FIXED_AI:
            ln = FIXED_AI[ai]
            val = rest[pos + 2:pos + 2 + ln]
            if len(val) < ln:
                errors.append(("UDI_E_LEN", ai, val, "固定长段不足 %d 位" % ln))
                break
            comps[ai] = val
            pos += 2 + ln
        elif ai in VAR_AI:
            errors.append(("UDI_E_AMBIGUOUS", ai, "", "变长段在无括号串中无法定界；请使用带括号形态"))
            break
        else:
            errors.append(("UDI_E_UNKNOWN_AI", ai, rest[pos:pos + 8], "仅支持 " + ",".join(ALL_AI)))
            break
    return comps, errors


def validate_di(di, errors):
    if not di:
        errors.append(("UDI_E_LEN", "01", "", "缺少 UDI-DI：请提供 (01) 段或 --di"))
        return
    if len(di) != 14 or not di.isdigit():
        errors.append(("UDI_E_LEN", "01", di, "DI 固定 14 位数字"))
        return
    calc = gs1_check(di[:13])
    if calc != di[13]:
        errors.append(("UDI_E_CHECKDIGIT", "01", "期望 %s 实得 %s" % (calc, di[13]), "按 13 位数据位重算校验位或核对录入"))


def main():
    ap = argparse.ArgumentParser(prog="udi_format_validator", description="UDI 格式校验器（GS1 AI 01/10/11/17/21/240/30）")
    ap.add_argument("udi", nargs="?", help="UDI 串，推荐带括号形态 (01)...(17)...(10)...")
    ap.add_argument("--di", help="仅校验 14 位 UDI-DI")
    ap.add_argument("--type", choices=["udi", "basic"], default="udi", help="udi=带生产标识的 UDI；basic=Basic UDI-DI")
    ap.add_argument("--json", action="store_true", help="输出 JSON 中间表示")
    a = ap.parse_args()
    if not a.udi and not a.di:
        ap.error("需要提供 UDI 串或 --di")
    errors, notes = [], []
    comps = {}
    if a.type == "basic":
        code = (a.di or a.udi or "").strip()
        if re.search(r"\(\d{2}\)", code):
            errors.append(("UDI_E_UNKNOWN_AI", "basic", code, "Basic UDI-DI 不含 AI 括号段；请去掉 (01) 等包装标识"))
        if not re.match(r"^[A-Za-z0-9\-]{6,}$", code):
            errors.append(("UDI_E_LEN", "basic", code, "Basic UDI-DI 应为发码机构签发的字母数字串"))
        notes.append("Basic UDI-DI 结构与归属由发码机构（GS1 AIDC/HIBCC/ICCBBA）定义，格式通过仍需向发码机构核验。")
        comps = {"basic": code}
    else:
        if a.di:
            comps["01"] = a.di.strip()
            src = a.di.strip()
        else:
            src = a.udi.strip()
            if re.search(r"\(\d{2}\)", src):
                comps, errs2 = parse_paren(src)
                errors.extend(errs2)
            else:
                comps, errs2 = parse_plain(src)
                errors.extend(errs2)
        if a.di and re.search(r"\(\d{2}\)", src):
            errors.append(("UDI_E_LEN", "01", src, "--di 只接受 14 位纯数字，不要带括号段"))
            comps["01"] = ""
        validate_di(comps.get("01", ""), errors)
        for ai, label in (("17", "失效日期"), ("11", "生产日期")):
            if ai in comps and comps[ai] and not valid_ymd(comps[ai]):
                errors.append(("UDI_E_DATE", ai, comps[ai], "%s 应为 YYMMDD，日位 00 表示当月最后一天" % label))
        for ai in comps:
            if ai not in ALL_AI:
                errors.append(("UDI_E_UNKNOWN_AI", ai, comps[ai], "仅支持 " + ",".join(ALL_AI)))
        pi = [ai for ai in ("10", "21", "11", "17", "240", "30") if comps.get(ai)]
        if not errors and not pi and a.type == "udi" and not a.di:
            notes.append("未发现生产标识（PI）段：仅有 DI 的串请用 --di 或确认是否漏扫。")
        notes.append("NMPA：三类械 UDI 已全面实施（2022-06-01 起），二类自 2024-06-01 起实施；以官方最新通告为准。")
        notes.append("EU MDR：上市还需 Basic UDI-DI 并录入 EUDAMED；与 UDI-DI 是两个层级。")
        if comps.get("17") and valid_ymd(comps["17"]):
            comps["17_pretty"] = pretty_ymd(comps["17"])
        if comps.get("11") and valid_ymd(comps["11"]):
            comps["11_pretty"] = pretty_ymd(comps["11"])

    valid = not errors
    if a.json:
        out = {"valid": valid, "type": a.type, "parsed": comps, "notes": notes}
        if errors:
            out["errors"] = [{"code": c, "subject": s, "evidence": e, "fixes": [f]} for c, s, e, f in errors]
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        if a.type == "basic":
            print("Basic UDI-DI 校验：%s" % ("通过" if valid else "未通过"))
            if comps.get("basic"):
                print("  code: %s" % comps["basic"])
        else:
            print("UDI 校验：%s" % ("通过" if valid else "未通过"))
            di = comps.get("01", "")
            if di:
                ok = "✓" if not any(c == "UDI_E_CHECKDIGIT" or c == "UDI_E_LEN" for _, s, _, _ in errors if s == "01") else "✗"
                print("  DI        %-16s 校验位 %s（GS1 Mod10）" % (di, ok))
            if comps.get("17"):
                print("  失效日期  %-16s %s" % (comps["17"], comps.get("17_pretty", "")))
            if comps.get("11"):
                print("  生产日期  %-16s %s" % (comps["11"], comps.get("11_pretty", "")))
            for ai, label in (("10", "批号"), ("21", "序列号"), ("240", "附加标识"), ("30", "数量")):
                if comps.get(ai):
                    print("  %-10s %s" % (label, comps[ai]))
        for c, s, e, f in errors:
            print("  [%s] %s: %s -> %s" % (c, s, e or "-", f))
        for n in notes:
            print("提示：%s" % n)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
