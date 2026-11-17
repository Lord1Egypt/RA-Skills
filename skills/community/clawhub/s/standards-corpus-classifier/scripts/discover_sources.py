# -*- coding: utf-8 -*-
"""
Phase2 来源发现 · 写回工具（skill: standards-corpus-classifier）

负责把"联网搜索得到的某标准代号 → 官方平台链接"安全写回 references/sources.json。
联网搜索(WebSearch/WebFetch)由 agent 完成，本脚本只做结构化的 JSON 更新，并先备份。

用法:
    python discover_sources.py --code DB44 --name 广东 --portal https://amr.gd.gov.cn/standard/
    python discover_sources.py --code QX   --name 气象 --portal https://qx.example.gov.cn --level 行业
    python discover_sources.py --code DB4403 --name 深圳 --portal https://amr.sz.gov.cn/.../szsdfbz/ --level 地方

级别推断: 以 DB 开头→地方; 纯字母 2~3 位→行业; GB→国家; 也可用 --level 显式指定。
"""
import os, re, json, shutil, argparse, sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = SKILL_ROOT / "references" / "sources.json"
AGG = "https://dbba.sacinfo.org.cn"  # 地方标准信息服务平台(兜底)


def infer_level(code):
    if code.startswith("DB"):
        return "地方"
    if re.fullmatch(r"[A-Z]{2,3}", code):
        return "行业"
    if code == "GB":
        return "国家"
    return None


def main():
    ap = argparse.ArgumentParser(description="将发现的标准来源写回 sources.json")
    ap.add_argument("--code", required=True, help="标准代号前缀, 如 DB44 / QX / GB")
    ap.add_argument("--name", required=True, help="归属名称, 如 广东 / 气象")
    ap.add_argument("--portal", required=True, help="官方平台网址")
    ap.add_argument("--aggregator", default=AGG, help="兜底聚合平台(默认地方标准信息服务平台)")
    ap.add_argument("--level", default=None, help="级别: 国家/行业/地方(默认按代号推断)")
    ap.add_argument("--sources", default=str(DEFAULT_SOURCES))
    args = ap.parse_args()

    code = args.code.strip().upper()
    level = args.level or infer_level(code)
    if not level:
        sys.exit(f"无法推断级别, 请用 --level 指定(代号={code})")

    bucket = {"国家": "national", "行业": "industry", "地方": "local"}.get(level)
    if not bucket:
        sys.exit(f"级别必须是 国家/行业/地方, 收到: {level}")

    path = Path(args.sources)
    if not path.exists():
        sys.exit(f"sources.json 不存在: {path}")
    data = json.load(open(path, encoding="utf-8"))

    # 备份
    bak = path.with_suffix(".json.bak")
    shutil.copy2(path, bak)

    entry = data.setdefault(bucket, {}).get(code)
    if entry:
        # 已存在: 仅补充缺失字段, 不覆盖已有 portal
        entry["name"] = args.name
        entry.setdefault("level", level)
        entry.setdefault("portal", args.portal)
        entry["aggregator"] = args.aggregator
        verb = "更新"
    else:
        entry = {"name": args.name, "level": level, "portal": args.portal, "aggregator": args.aggregator}
        data[bucket][code] = entry
        verb = "新增"

    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[{verb}] {bucket}.{code} -> {args.name} | {args.portal}")
    print(f"备份: {bak}")


if __name__ == "__main__":
    main()
