import argparse, json, re, sys

def main():
    ap = argparse.ArgumentParser(description="regex-sandbox · 正则即写即测（零依赖）")
    ap.add_argument("--pattern", required=True)
    ap.add_argument("--text", help="待测文本（缺省读 stdin）")
    ap.add_argument("--file", help="从文件读文本")
    ap.add_argument("--replace", help="替换模板（如 <b>\\1</b>）")
    ap.add_argument("--flags", default="", help="标志位组合 i(忽略大小写) m(多行) s(点匹配换行)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    f = 0
    for c in a.flags:
        f |= {"i": re.I, "m": re.M, "s": re.S}.get(c, 0)
    try:
        pat = re.compile(a.pattern, f)
    except re.error as e:
        print("正则编译失败: %s" % e); sys.exit(2)
    text = open(a.file, encoding="utf-8-sig").read() if a.file else (a.text if a.text is not None else sys.stdin.read())
    ms = list(pat.finditer(text))
    if a.json:
        print(json.dumps({"matches": len(ms),
                          "groups": [{"span": list(m.span()), "match": m.group(0),
                                      "groups": list(m.groups())} for m in ms],
                          "replaced": pat.sub(a.replace, text) if a.replace is not None else None},
                         ensure_ascii=False, indent=2))
    else:
        print("匹配 %d 处" % len(ms))
        for m in ms[:50]:
            extra = "  组:" + str(list(m.groups())) if m.groups() else ""
            print("  [%d:%d] %r%s" % (m.start(), m.end(), m.group(0), extra))
        if a.replace is not None:
            print("---替换结果---")
            print(pat.sub(a.replace, text))
    sys.exit(0 if ms else 1)

if __name__ == "__main__":
    main()
