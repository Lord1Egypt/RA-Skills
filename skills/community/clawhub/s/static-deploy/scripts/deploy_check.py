#!/usr/bin/env python3
"""静态站产物校验：确认目录可作为静态站发布，输出入口/体积/可疑文件。"""
import argparse, json, os, sys


SUSPICIOUS = (".env", "credentials", "id_rsa", "secret", ".pem", "key.json")


def check(dist_dir):
    dist_dir = os.path.abspath(dist_dir)
    if not os.path.isdir(dist_dir):
        raise SystemExit(f"❌ 不是目录：{dist_dir}")
    files = []
    total = 0
    for root, _, fs in os.walk(dist_dir):
        for f in fs:
            fp = os.path.join(root, f)
            try:
                sz = os.path.getsize(fp)
            except OSError:
                sz = 0
            total += sz
            rel = os.path.relpath(fp, dist_dir)
            files.append({"path": rel, "size": sz})
    has_index = any(f["path"] == "index.html" or f["path"].endswith("/index.html") for f in files)
    suspects = [f["path"] for f in files if any(s in f["path"].lower() for s in SUSPICIOUS)]
    # 入口候选
    entries = [f["path"] for f in files if os.path.basename(f["path"]) in ("index.html", "index.htm")]
    top = sorted(files, key=lambda x: x["size"], reverse=True)[:8]
    return {
        "dir": dist_dir,
        "file_count": len(files),
        "total_bytes": total,
        "has_index_html": has_index,
        "entries": entries,
        "suspicious_files": suspects,
        "top_files": top,
        "ok": has_index and not suspects,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dist_dir")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    r = check(args.dist_dir)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"目录：{r['dir']}")
        print(f"文件数：{r['file_count']} ｜ 总体积：{r['total_bytes']:,} bytes")
        print(f"含 index.html：{r['has_index_html']}")
        print(f"入口：{r['entries']}")
        if r["suspicious_files"]:
            print(f"⚠️ 可疑敏感文件（勿部署）：{r['suspicious_files']}")
        print(f"是否可发布：{r['ok']}")
        if not r["ok"]:
            print("  建议：缺 index.html 或含密钥文件，请先修复")
    sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()
