import argparse, glob, json, os, re, shutil, sys

def main():
    ap = argparse.ArgumentParser(description="text-replace · 跨文件批量查找替换（默认统计，--apply 才写入）")
    ap.add_argument("--glob", required=True, help='文件通配，如 "src/**/*.py" 或 "docs/*.md"')
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--regex", action="store_true", help="按正则解释 old")
    ap.add_argument("--apply", action="store_true", help="写入（缺省只统计；写入前每文件生成 .bak）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    files = [f for f in glob.glob(a.glob, recursive=True) if os.path.isfile(f)]
    pat = re.compile(a.old) if a.regex else None
    results, total = [], 0
    for f in files:
        try:
            txt = open(f, encoding="utf-8-sig").read()
        except (UnicodeDecodeError, OSError):
            continue
        n = len(pat.findall(txt)) if pat else txt.count(a.old)
        if n:
            total += n
            results.append((f, n))
            if a.apply:
                shutil.copy2(f, f + ".bak")
                open(f, "w", encoding="utf-8-sig").write(pat.sub(a.new, txt) if pat else txt.replace(a.old, a.new))
    if a.json:
        print(json.dumps({"mode": "apply" if a.apply else "dry-run", "files": len(results),
                          "total_hits": total, "detail": [{"file": f, "hits": n} for f, n in results]},
                         ensure_ascii=False, indent=2))
    else:
        print("模式: %s ｜ 命中 %d 个文件 / %d 处" % ("APPLY 已替换(.bak已备份)" if a.apply else "DRY-RUN 仅统计", len(results), total))
        for f, n in results:
            print("  %4d  %s" % (n, f))
    sys.exit(0)

if __name__ == "__main__":
    main()
