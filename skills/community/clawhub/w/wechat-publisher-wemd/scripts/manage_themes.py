#!/usr/bin/env python3
"""主题管理：添加 / 列出 / 删除"""
import argparse, json, sys
from pathlib import Path

THEMES_DIR = Path(__file__).resolve().parent.parent / "vendor" / "wemd" / "themes"
CUSTOM_JSON = THEMES_DIR.parent / "custom_themes.json"

BUILTIN = {"默认":"Default","学术论文":"Academic-Paper","极光玻璃":"Aurora-Glass","包豪斯":"Bauhaus","赛博朋克":"Cyberpunk-Neon","知识库":"Knowledge-Base","黑金奢华":"Luxury-Gold","莫兰迪森林":"Morandi-Forest","新粗野主义":"Neo-Brutalism","购物小票":"Receipt","落日胶片":"Sunset-Film","主题模板":"Template"}

def _load(): return json.loads(CUSTOM_JSON.read_text(encoding="utf-8")) if CUSTOM_JSON.is_file() else {}
def _save(d): CUSTOM_JSON.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("--cn", required=True); a.add_argument("--en", required=True); a.add_argument("--css", default=None); a.add_argument("--css-file", default=None)
    d = sub.add_parser("delete"); d.add_argument("--name", required=True)
    sub.add_parser("list")
    args = parser.parse_args()

    if args.cmd == "list":
        all_t = {**BUILTIN, **_load()}
        custom = _load()
        r = {"themes": [{"cn": c, "en": e, "builtin": c not in custom} for c, e in all_t.items()], "total": len(all_t), "custom_count": len(custom)}
    elif args.cmd == "add":
        css = ""
        if args.css_file:
            p = Path(args.css_file).expanduser().resolve()
            if not p.is_file():
                r = {"ok": False, "message": f"CSS file not found: {args.css_file}"}; json.dump(r, sys.stdout, ensure_ascii=False, indent=2); sys.stdout.write("\n"); return 1
            css = p.read_text(encoding="utf-8")
        elif args.css:
            css = args.css
        else:
            css = sys.stdin.read()
        if not css.strip():
            r = {"ok": False, "message": "Empty CSS"}; json.dump(r, sys.stdout, ensure_ascii=False, indent=2); sys.stdout.write("\n"); return 1
        all_t = {**BUILTIN, **_load()}
        if args.cn in all_t:
            r = {"ok": False, "message": f"Name exists: {args.cn}"}
        elif args.en in set(all_t.values()):
            r = {"ok": False, "message": f"ID exists: {args.en}"}
        else:
            (THEMES_DIR / f"{args.en}.css").write_text(css, encoding="utf-8")
            custom = _load(); custom[args.cn] = args.en; _save(custom)
            r = {"ok": True, "cn": args.cn, "en": args.en, "css_length": len(css)}
    elif args.cmd == "delete":
        custom = _load(); cn = en = None
        if args.name in custom: cn, en = args.name, custom[args.name]
        else:
            for c, e in custom.items():
                if e == args.name: cn, en = c, e; break
        if not cn:
            r = {"ok": False, "message": f"Not a custom theme: {args.name}"}
        else:
            f = THEMES_DIR / f"{en}.css"
            if f.is_file(): f.unlink()
            del custom[cn]; _save(custom)
            r = {"ok": True, "deleted_cn": cn, "deleted_en": en}
    else:
        r = {"ok": False, "message": "Unknown command"}

    json.dump(r, sys.stdout, ensure_ascii=False, indent=2); sys.stdout.write("\n")
    return 0 if r.get("ok", True) else 1

if __name__ == "__main__":
    raise SystemExit(main())
