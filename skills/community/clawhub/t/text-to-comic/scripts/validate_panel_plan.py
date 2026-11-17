#!/usr/bin/env python3
"""Validate panel plan JSON with simple business checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

from character_anchors import (  # noqa: E402  (需要先修正 sys.path)
    build_registry,
    derive_anchors,
    enrich_character,
    load_card,
    load_card_dir,
    load_json,
    match_card,
    missing_anchors,
)


def load_character_cards(paths: List[Path], card_dir: Path | None = None) -> List[Dict[str, Any]]:
    cards: List[Dict[str, Any]] = []
    for path in paths:
        card = load_card(path)
        if card:
            cards.append(card)
    if card_dir:
        known = {c.get("card_path") for c in cards}
        for card in load_card_dir(card_dir):
            if card.get("card_path") not in known:
                cards.append(card)
    return cards


def check_character_anchors(plan: Dict[str, Any], cards: List[Dict[str, Any]]) -> List[str]:
    """逐角色检查锚点是否写全 —— 默认主角和自定义角色同一套规则。

    自定义角色不再被跳过：有卡片就按卡片锚点查，没卡片就按它自己的 appearance 查。
    compile_prompt.py 会兜底补齐，但校验阶段就该拦住，避免"补了但没人知道漂过"。
    """
    errors: List[str] = []
    # 信息图/纯图表不需要角色一致性，跳过整段角色检查
    if plan.get("visual_form") == "infographic":
        return errors
    bible = plan.get("character_bible") or []
    if not bible:
        errors.append(
            "missing character_bible: 分镜缺少角色设定，角色会在逐格渲染时漂移"
            "（compile_prompt.py 可自动注入默认卡，但建议在分镜阶段显式写出）"
        )
        return errors
    if not cards:
        return errors

    registry = build_registry(cards)
    for index, raw_character in enumerate(bible, start=1):
        card = match_card(raw_character, registry)
        character = enrich_character(raw_character, card) if card else raw_character
        anchors = derive_anchors(
            character,
            card.get("hard_anchors") if card else character.get("hard_anchors"),
        )
        name = character.get("name") or character.get("character_id") or f"第 {index} 个角色"
        if not anchors:
            errors.append(
                f"{name} 缺少可用于一致性的外观字段"
                "（hair / eyewear / build / face 至少填一项，或提供角色卡）"
            )
            continue
        missing = missing_anchors(character, anchors)
        if missing:
            if card:
                hint = f"（compile_prompt.py 会按卡片 {card.get('card_path') or card.get('source_doc')} 补齐）"
            else:
                hint = "（compile_prompt.py 会按其 appearance 补齐，建议分镜阶段就写全）"
            errors.append(f"{name} 的 must_keep 缺少锚点：{'、'.join(missing)}{hint}")
    return errors


def expected_panel_count(format_name: str) -> int | None:
    mapping = {
        "single": 1,
        "4-panel": 4,
        "6-panel": 6,
        "8-panel": 8,
        "10-panel": 10,
        "12-panel": 12,
    }
    return mapping.get(format_name)


def validate(plan: Dict[str, Any], character_cards: List[Dict[str, Any]] | None = None, check_character: bool = True) -> List[str]:
    errors: List[str] = []
    required_top = ["story_id", "visual_form", "format", "language", "style_id", "panels"]
    for key in required_top:
        if key not in plan:
            errors.append(f"missing top-level field: {key}")

    panels = plan.get("panels", [])
    if not isinstance(panels, list) or not panels:
        errors.append("panels must be a non-empty array")
        return errors

    exp_count = expected_panel_count(plan.get("format", ""))
    if exp_count is not None and len(panels) != exp_count:
        errors.append(f"format {plan.get('format')} expects {exp_count} panels, got {len(panels)}")

    panel_ids = set()
    for idx, panel in enumerate(panels, start=1):
        for field in ["panel_id", "narrative_role", "shot", "scene", "action", "emotion", "dialogue", "must_include", "avoid"]:
            if field not in panel:
                errors.append(f"panel {idx} missing field: {field}")
        panel_id = panel.get("panel_id")
        if isinstance(panel_id, int):
            if panel_id in panel_ids:
                errors.append(f"duplicate panel_id: {panel_id}")
            panel_ids.add(panel_id)
        text_budget = panel.get("text_budget")
        if text_budget is not None and not isinstance(text_budget, int):
            errors.append(f"panel {panel_id} text_budget must be integer")
        dialogue = panel.get("dialogue", [])
        if not isinstance(dialogue, list):
            errors.append(f"panel {panel_id} dialogue must be array")
        else:
            total_chars = 0
            for line in dialogue:
                if not isinstance(line, dict) or "text" not in line:
                    errors.append(f"panel {panel_id} has invalid dialogue item")
                    continue
                total_chars += len(str(line.get("text", "")))
            if isinstance(text_budget, int) and total_chars > text_budget * 3:
                errors.append(
                    f"panel {panel_id} dialogue looks too long for text_budget={text_budget} (chars={total_chars})"
                )
        must_include = panel.get("must_include", [])
        avoid = panel.get("avoid", [])
        if not isinstance(must_include, list) or not isinstance(avoid, list):
            errors.append(f"panel {panel_id} must_include/avoid must be arrays")

    if plan.get("visual_form") == "infographic" and plan.get("format") != "single":
        errors.append("visual_form=infographic should usually use format=single")

    if check_character:
        errors.extend(check_character_anchors(plan, character_cards or []))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate panel plan JSON.")
    parser.add_argument("panel_plan", help="Path to panel plan JSON")
    parser.add_argument(
        "--character-card",
        action="append",
        default=None,
        help="Path to a structured character card (repeatable). Defaults to presets/default_character.json",
    )
    parser.add_argument(
        "--character-card-dir",
        default="characters/cards",
        help="Directory of character cards, all *.json are loaded (default: characters/cards)",
    )
    parser.add_argument(
        "--skip-character-check",
        action="store_true",
        help="Skip character bible / hard anchor checks",
    )
    args = parser.parse_args()

    plan = load_json(Path(args.panel_plan))
    if args.skip_character_check:
        cards: List[Dict[str, Any]] = []
    else:
        card_paths = [Path(p) for p in (args.character_card or ["presets/default_character.json"])]
        card_dir = Path(args.character_card_dir) if args.character_card_dir else None
        cards = load_character_cards(card_paths, card_dir)
    errors = validate(plan, character_cards=cards, check_character=not args.skip_character_check)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True, "errors": []}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
