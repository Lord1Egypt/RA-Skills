#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地方关键词族生成器（时间分层版，wenbo-research Step 1）

设计原则：时间线索清晰——政区地名/人物/民俗物产/地貌生态按朝代分层，
历史复原时用「当时」的称谓，不把现代资料混进古代叙述。

用法:
    python3 keywords.py 榆林                # 全部（按时间分层展示）
    python3 keywords.py 榆林 --era 明       # 明代历史复原关键词集
    python3 keywords.py 榆林 --era 秦汉     # 秦汉复原关键词集
    python3 keywords.py 榆林 --json         # JSON 输出
    python3 keywords.py --list              # 列出已内置种子的地方

结构约定（data/keywords_seed.json）:
    - 某类别值为 list → 跨朝代通用（如军政边防、地理参照）
    - 某类别值为 dict → 按时间分层，key 为朝代/古今，value 为词列表
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEED_PATH = os.path.join(HERE, "..", "data", "keywords_seed.json")

CATEGORIES = ["政区地名", "军政边防", "人物", "民俗物产", "地理参照", "地貌生态"]

# 归入「古代物产/古名地貌」的朝代（历史复原时用古称，不用现代术语）
ANCIENT_ERAS = {"秦汉", "十六国", "隋唐", "隋唐宋", "唐宋", "宋", "明", "清", "明清"}

GENERIC_SKELETON = {
    "政区地名": {"秦汉": ["<郡县名>"], "明清": ["<府州县>"], "今": ["<现行政区>"]},
    "军政边防": ["<边墙/营堡/马政/屯田/市口，若为边地>"],
    "人物": {"<朝代>": ["<名宦/乡贤/武人>"]},
    "民俗物产": {"古代": ["<屯田/盐/马/饮食>"], "近现代": ["<民歌/饮食/物产/节俗>"]},
    "地理参照": ["<遗址/摩崖/碑刻/山川/关隘>"],
    "地貌生态": {"今名": ["<现代地貌名>"], "古名": ["<古籍地貌词>"], "古今对照": ["<古名(朝代)=今名>"]},
}


def load_seed():
    if os.path.exists(SEED_PATH):
        with open(SEED_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def is_dict(v):
    return isinstance(v, dict)


def resolve_era_key(value, era):
    """在时间分层 dict 里，把用户输入的朝代模糊匹配到真实 key。"""
    if era in value:
        return era
    for k in value.keys():
        if era and (era in k or k in era):
            return k
    return None


def filter_by_era(value, era, cat):
    """按朝代从时间分层 dict 抽取为词列表（历史复原用）。"""
    if not is_dict(value):
        return value  # list 跨朝代，直接返回
    if cat == "政区地名":
        # 沿革追溯：取该朝代及之前所有层
        keys = list(value.keys())
        target = resolve_era_key(value, era)
        if target and target in keys:
            idx = keys.index(target)
            result = []
            for k in keys[: idx + 1]:
                result.extend(value[k])
            return result
        return [w for sub in value.values() for w in sub]
    if cat == "人物":
        target = resolve_era_key(value, era)
        return value.get(target, [])
    if cat == "民俗物产":
        return value.get("古代", []) if (era and era in ANCIENT_ERAS) else value.get("近现代", [])
    if cat == "地貌生态":
        if era and era in ANCIENT_ERAS:
            return value.get("古名", []) + value.get("古今对照", [])
        return value.get("今名", [])
    return []


def render_value(value):
    """把某类别值渲染成行（dict 分层 / list 平铺）。"""
    if is_dict(value):
        lines = []
        for k, v in value.items():
            items = v if isinstance(v, list) else [v]
            lines.append(f"  [{k}] " + " / ".join(items))
        return lines
    return ["  " + " / ".join(value)]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    list_only = "--list" in sys.argv
    era = None
    if "--era" in sys.argv:
        i = sys.argv.index("--era")
        if i + 1 < len(sys.argv):
            era = sys.argv[i + 1]

    seed = load_seed()

    if list_only:
        print("已内置种子的地方：", "、".join(seed.keys()))
        return
    if not args:
        print(__doc__)
        return

    place = args[0]
    if place not in seed:
        seed[place] = GENERIC_SKELETON

    data = seed[place]

    if era:
        print(f"「{place}」{era} 历史复原关键词集：\n")
        for cat in CATEGORIES:
            val = data.get(cat, [])
            words = filter_by_era(val, era, cat)
            if not words:
                continue
            print(f"■ {cat}")
            print("  " + " / ".join(words) + "\n")
        return

    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print(f"「{place}」关键词族（按时间分层）：\n")
    for cat in CATEGORIES:
        val = data.get(cat, [])
        print(f"■ {cat}")
        for line in render_value(val):
            print(line)
        print()

    if place not in seed:
        print("⚠️ 该地未内置种子，以上为通用骨架。请按实际沿革/人物/民俗补全到 data/keywords_seed.json。")


if __name__ == "__main__":
    main()
