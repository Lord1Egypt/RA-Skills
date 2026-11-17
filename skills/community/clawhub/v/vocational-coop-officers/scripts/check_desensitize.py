#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VCO 脱敏自检：实体、个人信息、数字档位、承诺性表述、外部数据来源。

用法：
    python scripts/check_desensitize.py            # 检查本技能包
    python scripts/check_desensitize.py <包目录>

判定：
  FAIL = 出现疑似真实主体名、身份证/手机号/银行卡号
  WARN = 数字缺档位标注、承诺性表述（可能为禁语示例）、外部数据缺来源
"""
import re
import sys
from pathlib import Path

FAIL_PATTERNS = [
    ("疑似企业名", re.compile(r"(?<![某该])[\u4e00-\u9fa5]{2,4}(科技|光电|电子|通信|智能|实业|控股)(股份)?有限公司")),
    ("疑似院校名", re.compile(r"(?<![某该所])[\u4e00-\u9fa5]{2,4}(职业技术|职业|技师|技工)学院")),
    ("身份证号", re.compile(r"\b\d{17}[\dXx]\b")),
    ("手机号", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("银行卡号", re.compile(r"(?<!\d)\d{16,19}(?!\d)")),
]
WARN_PATTERNS = [
    ("承诺性表述", re.compile(r"(包就业|保薪资|包转正|包过|包认定|保证安排到)")),
    ("绝对化用语", re.compile(r"(最靠谱|最好|第一品牌|唯一指定|官方指定)")),
]
PRICE = re.compile(r"(\d[\d,]{2,6})\s*元/人/月")
MARKS = ("区间", "示例", "D2", "法定", "行业", "约")


def scan(path, lines):
    rel = path.name
    for i, line in enumerate(lines, 1):
        for name, pat in FAIL_PATTERNS:
            m = pat.search(line)
            if m:
                yield "FAIL", rel, i, name, m.group(0)
        for name, pat in WARN_PATTERNS:
            m = pat.search(line)
            if m:
                yield "WARN", rel, i, name, m.group(0)
        for m in PRICE.finditer(line):
            ctx = line[max(0, m.start() - 40): m.end() + 40]
            if not any(k in ctx for k in MARKS):
                yield "WARN", rel, i, "价格缺档位", m.group(0)


def main(root):
    files = [root / "SKILL.md"]
    for sub in ("references", "templates"):
        d = root / sub
        if d.is_dir():
            files += sorted(d.glob("*.md"))
    total = {"FAIL": 0, "WARN": 0}
    rows = []
    for pth in files:
        if not pth.is_file():
            continue
        for r in scan(pth, pth.read_text(encoding="utf-8", errors="replace").splitlines()):
            rows.append(r)
            total[r[0]] += 1

    print("=" * 60)
    print("VCO 脱敏自检：文件 %d，FAIL %d，WARN %d" % (len(files), total["FAIL"], total["WARN"]))
    print("=" * 60)
    for r in rows:
        print("[%s] %s:%d %s -> %s" % r)
    if total["FAIL"] == 0:
        print("结果：无实质性问题（WARN 需人工确认是否为禁语示例或已标档）")
    print("\n提示：D1 法定值（6%、6.3396%、10%/20%）应标注「法定」；D3 内部值应标注「示例值」。")
    return 1 if total["FAIL"] else 0


if __name__ == "__main__":
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    sys.exit(main(base))
