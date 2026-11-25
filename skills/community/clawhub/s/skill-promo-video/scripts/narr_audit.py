#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""narr_audit.py — 旁白数字口径哨兵（10-22 立规，用户令：机制上杜绝「一成六」类缺陷）。

规则（全部硬 fail，发车链必过）：
  R1 成数词族禁令：text/tts 出现「数字+成」（一成六/六成二/八成）→ fail。
     成数是模糊修辞，教学片的数值必须与图表同值同精度。
  R2 口语百分点禁令：「X个点」→ fail（「个百分点」合法——串里无"个点"连续子串）。
  R3 tts 读法展开：text 中的每个百分数 NUM% 必须在 tts 有「百分之…」展开；
     tts 字段禁出现 % / 阿拉伯数字带百分号（TTS 逐字直读会念成"百分号"）。
  R4 text 数字清单：列出每段的全部数值供与屏上图表人工对值（自动对图表属后续）。

用法：python3 narr_audit.py tts.json [更多tts.json …]
退出码：0=全过，1=有 fail（挂 assemble 断言层/发车链）。
"""
import json
import re
import sys

CN_NUM = "零一二三四五六七八九十两"


def num_to_cn_reading(s: str) -> str:
    """数字读法展开（旁白口径）：61.7% -> 百分之六十一点七；3.1 -> 三点一。"""
    def int_cn(n: int) -> str:
        digits = "零一二三四五六七八九"
        if n == 10:
            return "十"
        if n < 10:
            return digits[n]
        if n < 20:
            return "十" + digits[n % 10] if n % 10 else "十"
        if n < 100:
            return digits[n // 10] + "十" + (digits[n % 10] if n % 10 else "")
        # 大数逐字读（1384 -> 一千三百八十四，旁白场景够用）
        units = ["", "十", "百", "千"]
        out, zero = "", False
        for i, ch in enumerate(str(n)):
            d = int(ch)
            if d == 0:
                zero = bool(out)
                continue
            out += ("零" if zero else "") + digits[d] + units[len(str(n)) - 1 - i]
            zero = False
        return out

    s = s.strip().rstrip("%")
    if "." in s:
        a, b = s.split(".")
        return f"百分之{int_cn(int(a))}点" + "".join(CN_NUM[int(c)] for c in b)
    return f"百分之{int_cn(int(s))}"


def audit(path: str) -> int:
    data = json.load(open(path, encoding="utf-8"))
    rows = data if isinstance(data, list) else [
        {"id": k, **v} if isinstance(v, dict) else {"id": k, "text": v}
        for k, v in data.items()]
    fails = 0
    print(f"== {path} ({len(rows)} 段) ==")
    for it in rows:
        sid = it.get("id", "?")
        text = it.get("text", "")
        tts = it.get("tts", text)
        issues = []

        for field, val in (("text", text), ("tts", tts)):
            for m in re.finditer(rf"[0-9{CN_NUM}]+成[0-9{CN_NUM}]?", val):
                issues.append(f"R1 {field} 成数表述「{m.group(0)}」")
            for m in re.finditer(rf"[0-9{CN_NUM}]+个点", val):
                issues.append(f"R2 {field} 口语百分点「{m.group(0)}」（应作『个百分点』并给真值）")

        for m in re.finditer(r"(\d+(?:\.\d+)?)\s*%", text):
            want = num_to_cn_reading(m.group(1))
            if want not in tts:
                issues.append(f"R3 text「{m.group(1)}%」tts 缺展开「{want}…」")
        if re.search(r"\d+(?:\.\d+)?\s*%", tts):
            issues.append("R3 tts 字段含 %/阿拉伯百分数（TTS 会逐字直读）")

        nums = re.findall(r"\d+(?:\.\d+)?%?", text)
        tag = "FAIL" if issues else "pass"
        print(f"[{tag}] {sid}" + (f"  数值清单={nums}" if nums else ""))
        for x in issues:
            print(f"    ✗ {x}")
        fails += bool(issues)
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    rc = 0
    for p in sys.argv[1:]:
        rc |= audit(p)
    sys.exit(rc)
