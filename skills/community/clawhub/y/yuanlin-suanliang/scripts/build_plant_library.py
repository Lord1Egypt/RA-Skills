#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把分区苗木选型库拆成 rules/plant_library/<大区>/<城市>.json 两级结构。

数据来源：rules/plant_library_分区苗木选型.json（01–08 区苗木品种表，仅“名称+章节→大类”）。
拆分依据：源库条目按 01→08 区顺序写入，每个区的章节序列固定为
乔木→灌木→其他(竹/藤本)→地被；脚本按这一可验证的序列切出 8 个气候区，
不逐条猜单株分布。每个大区取该气候区在本大区的首个城市作为文件锚点，
完整城市清单写入 cities 字段；条目 confidence 统一为 medium（区级候选池，非单城实测分布）。

只用标准库；可重复运行。原文件拆分后改写为索引（保留 zones/cities 与计数）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RULES = Path(__file__).resolve().parent.parent / "rules"
SOURCE = RULES / "plant_library_分区苗木选型.json"
OUT_ROOT = RULES / "plant_library"

ZONES = [
    {"zone": "01-区", "climate": "II温带针阔叶混交林区", "cities": ["哈尔滨", "长春", "抚顺", "铁岭"]},
    {"zone": "02-区", "climate": "III北部暖温带落叶阔叶林区", "cities": ["沈阳", "大连", "北京", "天津", "天水"]},
    {"zone": "03-区", "climate": "IV南部暖温带落叶阔叶林区", "cities": ["青岛", "烟台", "郑州", "连云港"]},
    {"zone": "04-区", "climate": "IX温带草原区", "cities": ["兰州", "满洲里", "齐齐哈尔", "银川", "呼和浩特", "张家口"]},
    {"zone": "05-区", "climate": "V北亚热带落叶、常绿阔叶混交林区", "cities": ["南京", "苏州", "合肥"]},
    {"zone": "06-区", "climate": "VI中亚热带常绿、落叶阔叶林区", "cities": ["上海", "长沙", "桂林", "杭州", "重庆", "贵阳", "昆明"]},
    {"zone": "07-区", "climate": "VII南亚热带常绿阔叶林区", "cities": ["厦门", "广州", "台北", "柳州"]},
    {"zone": "08-区", "climate": "VIII热带季风气候区", "cities": ["海口", "三亚", "深圳", "南宁"]},
]

REGION_OF_CITY = {
    "哈尔滨": "东北", "长春": "东北", "抚顺": "东北", "铁岭": "东北",
    "沈阳": "东北", "大连": "东北", "北京": "华北", "天津": "华北", "天水": "西北",
    "青岛": "华东", "烟台": "华东", "连云港": "华东", "郑州": "华中",
    "兰州": "西北", "满洲里": "东北", "齐齐哈尔": "东北", "银川": "西北",
    "呼和浩特": "华北", "张家口": "华北",
    "南京": "华东", "苏州": "华东", "合肥": "华东",
    "上海": "华东", "杭州": "华东", "长沙": "华中", "桂林": "华南",
    "重庆": "西南", "贵阳": "西南", "昆明": "西南",
    "厦门": "华南", "广州": "华南", "台北": "华南", "柳州": "华南",
    "海口": "华南", "三亚": "华南", "深圳": "华南", "南宁": "华南",
}

REGION_ORDER = ["华北", "东北", "华东", "华中", "华南", "西南", "西北"]


def clean(text: str) -> str:
    return re.sub(r"\s+", "", str(text or ""))


def split_alias(raw: str) -> tuple[str, list[str]]:
    """'东北红豆杉(紫杉）' -> ('东北红豆杉(紫杉）', ['紫杉'])；name 保留原词，避免图例全名失配。"""
    s = clean(raw)
    m = re.search(r"[（(]([^（）()]*)[）)]", s)
    aliases: list[str] = []
    if m:
        body = m.group(1).strip("、，,；; /")
        aliases = [a for a in re.split(r"[、，,；;/]", body) if a]
        base = (s[: m.start()] + s[m.end():]).strip()
        aliases = [a for a in aliases if a and a != base]
    return s, aliases


def category_groups(names: list[tuple[str, str]]) -> list[int]:
    """按 乔木→灌木→其他→地被 的章节序列切区，返回每区起始下标。"""
    runs: list[tuple[str, int]] = []
    for _, cat in names:
        if runs and runs[-1][0] == cat:
            runs[-1] = (cat, runs[-1][1] + 1)
        else:
            runs.append((cat, 1))
    starts, i = [], 0
    pattern = ["乔木", "灌木", "其他", "地被"]
    while i < len(runs):
        group = runs[i:i + len(pattern)]
        cats = [c for c, _ in group]
        if cats != pattern[: len(cats)]:
            raise SystemExit(f"章节序列异常：runs[{i}:{i+len(pattern)}]={cats}")
        starts.append(sum(n for _, n in runs[:i]))
        i += len(group)
    if len(starts) != len(ZONES):
        raise SystemExit(f"切出 {len(starts)} 个区，预期 {len(ZONES)} 个；请先核对源库顺序")
    return starts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=str(SOURCE))
    ap.add_argument("--check", action="store_true", help="只校验拆分结果，不写文件")
    args = ap.parse_args()
    src = Path(args.source)
    data = json.loads(src.read_text(encoding="utf-8"))
    if str(data.get("schema", "")).endswith("plant-library-index/v2"):
        print(f"SKIP index already split: {src}")
        return 0
    names = list((data.get("names") or {}).items())
    if not names:
        raise SystemExit(f"源库没有 names：{src}")

    starts = category_groups(names)
    bounds = starts + [len(names)]
    pools = [names[bounds[i]:bounds[i + 1]] for i in range(len(ZONES))]

    union = {clean(n) for n, _ in names}
    got: set[str] = set()
    written = []
    for zone, pool in zip(ZONES, pools):
        # 一个气候区可能跨多个大区：每个大区取该区首个城市作锚点，避免同区数据重复多份。
        anchors = {}
        for city in zone["cities"]:
            anchors.setdefault(REGION_OF_CITY[city], city)
        for region, city in anchors.items():
            plants = []
            for raw, cat in pool:
                nm, aliases = split_alias(raw)
                got.add(nm)
                plants.append({
                    "name": nm,
                    "aliases": aliases,
                    "region": region,
                    "city": city,
                    "category": cat,
                    "source": f"plant_library_分区苗木选型.json#{zone['zone']}",
                    "confidence": "medium",
                })
            doc = {
                "schema": "yuanlin-suanliang/plant-library/v2",
                "region": region,
                "city": city,
                "zone": zone["zone"],
                "zone_climate": zone["climate"],
                "cities": zone["cities"],
                "scope": "climate-zone-pool",
                "source": f"plant_library_分区苗木选型.json#{zone['zone']}（按源库 01–08 区章节序列切分；区级候选池，非单城实测分布）",
                "confidence": "medium",
                "plants": plants,
            }
            out = OUT_ROOT / region / f"{city}.json"
            written.append((out, len(plants)))
            if not args.check:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    if got != union:
        raise SystemExit(f"拆分后名称集合不一致：缺少 {sorted(union - got)[:5]} 多出 {sorted(got - union)[:5]}")

    index = {
        "name": "分区苗木选型植物名库（索引）",
        "schema": "yuanlin-suanliang/plant-library-index/v2",
        "source": data.get("source", ""),
        "boundary": data.get("boundary", ""),
        "count": len(union),
        "library_root": "plant_library/",
        "split_rule": "按源库 01–08 区章节序列切分（乔木→灌木→其他→地被），每个气候区写入所在大区的城市文件；zone pool，非单株分布。",
        "zones": {z["zone"]: {"climate": z["climate"], "cities": z["cities"]} for z in ZONES},
        "regions": REGION_ORDER,
    }
    print(f"plants={len(union)} zones={len(ZONES)} files={len(written)} entries={sum(n for _, n in written)}")
    for out, n in written:
        print(f"  {out.relative_to(RULES)}: {n}")
    if args.check:
        return 0
    SOURCE.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"index: {SOURCE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
