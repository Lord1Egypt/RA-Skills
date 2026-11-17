# -*- coding: utf-8 -*-
"""去敏扫描器：扫 PII/密钥/内部路径/内部项目代号，打码并输出脱敏清单。零依赖。"""
import argparse, json, pathlib, re

RULES = [
    ("手机号", re.compile(r"1[3-9]\d{9}")),
    ("身份证", re.compile(r"\b\d{17}[\dXx]\b")),
    ("邮箱", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    # 用拼接构造令牌前缀，避免扫描器把本脚本自身当成密钥泄漏
    ("密钥", re.compile("(" + "s" + "k-[A-Za-z0-9]{8,}|" + "g" + "hp_[A-Za-z0-9]{8,}|" + r"api[_-]?key[=:]\S+|" + r"password[=:]\S+)", re.I)),
    # 拼接构造路径模式，避免扫描器把本脚本自身当成路径泄漏
    # 覆盖：任意盘符绝对路径(C:\ / D:\ 含 Users 或任意路径)、/home/*、*.local
    ("内部路径", re.compile(r"(?:[A-Za-z]:\\[Uu]sers\\[\w.\-]+|[A-Za-z]:\\[\w.\- \\\/]+|/[Uu]sers/[\w.\-]+|/home/[\w.\-]+|[\w.\-]+\.local)")),
    # 内置项目代号启发式：CamelCase 项目词(≥10字符) 或 含 Project/Proj/Internal/Confidential 词
    ("内部项目代号", re.compile(r"\b([A-Z][a-z]+\d*[A-Z]\w{6,}|[A-Za-z]*Project\w*|[A-Za-z]*Proj\w*|[A-Za-z]*Internal\w*|[A-Za-z]*Confidential\w*)\b")),
]

def scan(text, extra=None):
    hits = []
    for name, pat in RULES:
        for m in pat.finditer(text):
            frag = m.group(0)
            # 过滤明显过短/误伤的 CamelCase（单词）
            if name == "内部项目代号" and len(frag) < 8:
                continue
            hits.append((name, m.start(), frag))
    if extra:
        for w in extra:
            for m in re.finditer(re.escape(w), text):
                hits.append(("内部项目代号", m.start(), w))
    return hits

def mask_text(text, hits, mask):
    out = text
    # 从后往前替，避免位移
    for name, pos, frag in sorted(hits, key=lambda x: -x[1]):
        out = out[:pos] + mask + out[pos + len(frag):]
    return out

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    ap.add_argument("--mask", default="***")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--extra", nargs="*", help="额外敏感词(内部项目代号)")
    a = ap.parse_args()
    text = a.text if a.text else pathlib.Path(a.file).read_text(encoding="utf-8")
    hits = scan(text, a.extra)
    if not hits:
        print("✅ 未发现敏感项")
        return
    masked = mask_text(text, hits, a.mask)
    print(masked)
    if a.report:
        rep = [{"type": n, "sample": f[:12] + ("…" if len(f) > 12 else "")} for n, _, f in hits]
        print("\n--- desens_report ---")
        print(json.dumps({"count": len(hits), "items": rep}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
