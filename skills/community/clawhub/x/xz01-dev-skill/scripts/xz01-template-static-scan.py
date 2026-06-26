#!/usr/bin/env python3
"""Static xz01 theme scan: backend boundary, template completeness, resource conventions, URL/link anti-patterns."""
from __future__ import annotations
from pathlib import Path
import argparse, re, sys, json

CORE_PAIRS = [
    ("cms/index.html", "mobile/index.html"),
    ("cms/list_soft.html", "mobile/list_soft.html"),
    ("cms/list_game.html", "mobile/list_game.html"),
    ("cms/list_news.html", "mobile/list_news.html"),
    ("cms/list_collection.html", "mobile/list_collection.html"),
    ("cms/show_soft_detail.html", "mobile/show_soft_detail.html"),
    ("cms/show_game_detail.html", "mobile/show_game_detail.html"),
    ("cms/show_news.html", "mobile/show_news.html"),
    ("cms/show_collection.html", "mobile/show_collection.html"),
]
BAD_PATTERNS = {
    "common_jquery_path": re.compile(r"common_cms/common/jquery\.min\.js", re.I),
    "duplicate_host_literal": re.compile(r"https://(?:www|m)\.900az\.com\s*https:?//", re.I),
    "cms_page_index": re.compile(r"cms/page/index/id|cms/Page/index|mobile/Page/index", re.I),
    "filler_svg": re.compile(r"/themes/default/common_cms/.+?/assets/images/(?:app-\d+|banner-\d+|topic-\d+)\.svg", re.I),
    "mobile_blank": re.compile(r"target\s*=\s*['\"]_blank['\"]", re.I),
}
PAGE_VAR_RX = re.compile(r"\$page_code|get(?:Pc|Mobile)PageData|pagination|class=\"pagination\"", re.I)
JQ_OK_RX = re.compile(r"common_cms/(?:pc|mobile)/assets/js/jquery\.min\.js", re.I)
UIKIT_RX = re.compile(r"uikit(?:\.min)?\.(?:css|js)", re.I)
SWIPER_RX = re.compile(r"swiper-bundle\.min\.(?:css|js)", re.I)

def rel(p: Path, root: Path) -> str:
    try: return str(p.relative_to(root))
    except Exception: return str(p)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("theme", nargs="?", default="/www/wwwroot/www.900az.com/public/themes/default")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.theme)
    issues=[]; facts=[]
    if not root.exists():
        print(f"FAIL theme_not_found {root}", file=sys.stderr); return 2
    for a,b in CORE_PAIRS:
        if not (root/a).exists(): issues.append({"type":"missing_pc_template","file":a})
        if not (root/b).exists(): issues.append({"type":"missing_mobile_template","file":b})
    for p in sorted(root.rglob("*.html")):
        text=p.read_text(errors="ignore")
        r=rel(p,root)
        for name,rx in BAD_PATTERNS.items():
            if name=="mobile_blank" and not r.startswith("mobile/") and "/mobile/" not in r:
                continue
            for m in rx.finditer(text):
                issues.append({"type":name,"file":r,"match":m.group(0)[:160]})
        if (r.startswith("cms/list_") or r.startswith("mobile/list_")) and not PAGE_VAR_RX.search(text):
            issues.append({"type":"list_template_missing_pagination_pattern","file":r})
        if "jquery" in text.lower() and not JQ_OK_RX.search(text) and "assets/js/jquery.min.js" not in text:
            issues.append({"type":"jquery_unrecognized_path","file":r})
        if UIKIT_RX.search(text): facts.append({"type":"uikit_used","file":r})
        if SWIPER_RX.search(text): facts.append({"type":"swiper_used","file":r})
    result={"theme":str(root),"issue_count":len(issues),"issues":issues,"facts":facts[:100]}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if issues:
            print(f"FAIL static_scan issues={len(issues)}")
            for it in issues[:200]: print(json.dumps(it, ensure_ascii=False))
        else:
            print("PASS static_scan")
    return 1 if issues else 0
if __name__ == "__main__":
    raise SystemExit(main())
