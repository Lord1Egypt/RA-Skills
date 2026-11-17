# -*- coding: utf-8 -*-
"""sz-ink 体检脚本 check_numbers.py — S6 文中数字自洽检查
用法: python check_numbers.py <文本文件> | --self-test
输出: JSON。提取全文「数字+量词」声明（含表格），报告同一主体+量词下取值冲突
     （如正文写「AI 基线 5 篇」、表格写「AI 基线（4 篇）」）。
状态: 骨架——find_conflicts 未实现（TDD 先红）。
背景: 2026-10-28 博客稿外部盲评抓出 4篇/5篇 矛盾。锚点机制防"改丢"，不防"文中自相矛盾"。
"""
import json
import re
import sys
from pathlib import Path

# 量词白名单：文本声明里常见的计数单位
QUANTIFIERS = ("千字", "万字", "篇", "处", "张", "组", "条", "个", "项", "轮",
               "种", "名", "家", "款", "次", "遍", "句", "段", "页", "倍",
               "年", "月", "天", "小时", "分钟", "秒", "字", "%", "％")

# 主体键前的标点/空白：归一化时删掉
_NOISE = re.compile(r"[\s（）()：:，,。、；;—\-·「」『』""''\"']+")

_CN_DIGIT = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9}


def parse_num(s: str):
    """'5'/'五'/'十二'/'二十' -> int；解析不了返回 None。"""
    s = s.strip()
    if s.isdigit():
        return int(s)
    if not s:
        return None
    if all(c in _CN_DIGIT or c == "十" for c in s):
        if "十" in s:
            parts = s.split("十")
            tens = _CN_DIGIT.get(parts[0], 1) if parts[0] else 1
            ones = _CN_DIGIT.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
            return tens * 10 + ones
        return _CN_DIGIT.get(s)
    return None


_NUM_ALT = "0-9０-９零一二两三四五六七八九十"
_TOKEN = re.compile(
    r"([" + _NUM_ALT + r"]+)\s*(" + "|".join(QUANTIFIERS) + r")")


def extract_claims(text: str) -> list:
    """提取全部 数字+量词 声明：[{value, quant, subject, context}]。"""
    claims = []
    for m in _TOKEN.finditer(text):
        raw_num, quant = m.group(1), m.group(2)
        value = parse_num(raw_num)
        if value is None:
            continue
        head = text[max(0, m.start() - 10):m.start()]
        subject = _NOISE.sub("", head)[-4:]
        ctx = text[max(0, m.start() - 14):min(len(text), m.end() + 10)]
        claims.append({"value": value, "quant": quant,
                       "subject": subject, "context": ctx.replace("\n", " ")})
    return claims


def find_conflicts(claims: list) -> list:
    """同一 (主体键+量词) 出现不同取值 → 冲突。
    主体键 = 数字前 4 个归一化字符（去标点/空白/引号）。键长 <2 不参与
    （主体过短不可靠，宁漏勿误）。同值多现不报（口径一致反而是好事）。"""
    groups = {}
    for c in claims:
        if len(c["subject"]) < 2:
            continue
        key = (c["subject"], c["quant"])
        groups.setdefault(key, []).append(c)
    conflicts = []
    for (subject, quant), items in groups.items():
        values = sorted({c["value"] for c in items})
        if len(values) > 1:
            conflicts.append({
                "subject": subject, "quant": quant, "values": values,
                "occurrences": [{k: c[k] for k in ("value", "context")} for c in items],
            })
    return conflicts


def run(text: str) -> dict:
    claims = extract_claims(text)
    return {"claims_total": len(claims), "conflicts": find_conflicts(claims),
            "claims": claims, "version": "0.1.0"}


SELF_TEST = [
    # (文本, 期望冲突数, 说明)
    ("正文说 AI 基线 5 篇为当场生成。表格里写 AI 基线（4 篇）。",
     1, "同主体同量词不同值必须抓（4/5 矛盾原型）"),
    ("共 85 篇真人转写，另有 5 篇 CSDN 文章。九项指标做哨兵。",
     0, "不同主体不误报（85/5 各有所指）"),
]


def self_test() -> bool:
    ok = True
    for i, (text, expect, desc) in enumerate(SELF_TEST):
        n = len(find_conflicts(extract_claims(text)))
        passed = n == expect
        print(f"  [{'PASS' if passed else 'FAIL'}] 用例{i+1} {desc} (冲突={n} 期望={expect})")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--self-test" in args:
        print("check_numbers 自检（冲突必抓 / 各有所指必放）:")
        sys.exit(0 if self_test() else 1)
    if not args:
        print("usage: check_numbers.py <file> | --self-test")
        sys.exit(1)
    text = Path(args[0]).read_text(encoding="utf-8")
    print(json.dumps(run(text), ensure_ascii=False, indent=2))
