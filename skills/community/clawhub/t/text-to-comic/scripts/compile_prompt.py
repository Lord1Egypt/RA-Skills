#!/usr/bin/env python3
"""Compile panel prompts from a panel plan and a style preset registry."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from character_anchors import (  # noqa: E402  (需要先修正 sys.path)
    build_registry,
    derive_anchors,
    enrich_character,
    load_card,
    load_card_dir,
    load_json,
    match_card,
    apply_anchors,
)


def load_character_cards(paths: List[Path], card_dir: Path | None = None) -> List[Dict[str, Any]]:
    """加载角色卡：显式指定的 + 卡片目录里的（后者方便用户随手丢卡）。"""
    cards: List[Dict[str, Any]] = []
    for path in paths:
        card = load_card(path)
        if card:
            cards.append(card)
        elif path.exists():
            print(f"warn: character card unreadable ({path})", file=sys.stderr)
        else:
            print(f"warn: character card not found ({path})", file=sys.stderr)
    if card_dir:
        known = {c.get("card_path") for c in cards}
        for card in load_card_dir(card_dir):
            if card.get("card_path") not in known:
                cards.append(card)
    return cards


def ensure_character_bible(
    panel_plan: Dict[str, Any], cards: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """保证每个角色的锚点都进 prompt —— 不管它是默认主角还是用户自定义的。

    规则对所有角色一致，区别只在锚点从哪来：
    - 该角色有结构化卡片 → 用卡片的 hard_anchors（没写就从卡片 appearance 推导）
    - 该角色没有卡片 → 从它自己的 appearance 推导（分镜里的字段本身就是结构化模板）
    - character_bible 缺失/为空 → 注入第一张卡（默认主角卡）的完整角色

    返回 (bible, guard)；guard 逐角色记录锚点来源与补齐项，便于定位漂移。
    """
    registry = build_registry(cards)
    primary = cards[0] if cards else None
    primary_path = (primary or {}).get("card_path") or ""

    guard: Dict[str, Any] = {
        "enabled": bool(cards),
        "injected": False,
        "patched_anchors": [],
        "source": (primary or {}).get("source_doc") or primary_path or None,
        "reference_image": (primary or {}).get("reference_image") or None,
        "characters": [],
    }
    bible = [dict(character) for character in (panel_plan.get("character_bible") or [])]
    if not cards:
        return bible, guard

    # 信息图/纯图表没有角色，注入主角反而是干扰
    if panel_plan.get("visual_form") == "infographic":
        guard["skipped_reason"] = "infographic — character consistency not applicable"
        return bible, guard

    if not bible and primary:
        bible = [copy.deepcopy(primary.get("character") or {})]
        guard["injected"] = True

    reference_images: List[str] = []
    for index, character in enumerate(bible):
        card = match_card(character, registry)
        if card:
            character = enrich_character(character, card)
            anchor_source = f"card:{card.get('card_path') or card.get('source_doc') or 'unknown'}"
            anchors = derive_anchors(character, card.get("hard_anchors"))
            reference = card.get("reference_image") or ""
        else:
            anchor_source = "plan:appearance"
            anchors = derive_anchors(character, character.get("hard_anchors"))
            reference = character.get("reference_image") or ""

        must_keep, patched = apply_anchors(character, anchors)
        character["must_keep"] = must_keep
        bible[index] = character

        if reference and reference not in reference_images:
            reference_images.append(reference)
        guard["patched_anchors"].extend(patched)
        guard["characters"].append(
            {
                "character_id": character.get("character_id"),
                "name": character.get("name"),
                "anchor_source": anchor_source,
                "anchors": [a.get("label_zh") or a.get("key") for a in anchors],
                "patched_anchors": patched,
                "reference_image": reference or None,
            }
        )

    if reference_images:
        guard["reference_images"] = reference_images
        # 兼容旧字段：首格参考图取第一个角色的卡片图
        guard["reference_image"] = reference_images[0]
    if not any(item["anchors"] for item in guard["characters"]):
        guard["skipped_reason"] = "no appearance fields on any character — nothing to anchor"
    elif not guard["patched_anchors"]:
        guard["patched_anchors"] = []
    return bible, guard


def summarize_character_bible(character_bible: List[Dict[str, Any]]) -> str:
    if not character_bible:
        return ""
    chunks: List[str] = []
    for character in character_bible:
        appearance = character.get("appearance", {})
        ordered = [
            appearance.get("age_presentation"),
            appearance.get("hair"),
            appearance.get("face"),
            appearance.get("eyewear"),
            appearance.get("outfit"),
            appearance.get("accent_color"),
            appearance.get("build"),
            appearance.get("vibe"),
        ]
        text = ", ".join([x for x in ordered if x])
        keep = ", ".join(character.get("must_keep", []))
        if keep:
            text = f"{character.get('name', 'character')}: {text}; must keep: {keep}"
        else:
            text = f"{character.get('name', 'character')}: {text}"
        chunks.append(text.strip())
    return " | ".join(chunks)


def build_style_index(styles_doc: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {style["style_id"]: style for style in styles_doc.get("styles", [])}


def build_tone_index(tones_doc: Dict[str, Any] | None) -> Dict[str, Dict[str, Any]]:
    if not tones_doc:
        return {}
    return {tone["tone_id"]: tone for tone in tones_doc.get("tones", [])}


def resolve_bundle(bundles_doc: Dict[str, Any] | None, bundle_id: str | None) -> Dict[str, Any] | None:
    """按 bundle_id 取预设包；bundle 只提供默认值，panel plan 显式字段优先。"""
    if not bundles_doc:
        return None
    bundles = {b["bundle_id"]: b for b in bundles_doc.get("bundles", [])}
    if bundle_id:
        if bundle_id not in bundles:
            raise KeyError(f"Unknown bundle_id: {bundle_id}")
        return bundles[bundle_id]
    default_id = bundles_doc.get("default_bundle_id")
    return bundles.get(default_id) if default_id else None



def compile_panel_prompt(
    panel_plan: Dict[str, Any],
    style: Dict[str, Any],
    panel: Dict[str, Any],
    clean_suffix: str,
    character_bible: List[Dict[str, Any]] | None = None,
    reference_images: List[str] | None = None,
    is_first_panel: bool = False,
    tone: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    bible = character_bible if character_bible is not None else panel_plan.get("character_bible", [])
    character_summary = summarize_character_bible(bible)
    must_include = ", ".join(panel.get("must_include", []))
    avoid = ", ".join(panel.get("avoid", []))
    dialogue_lines = []
    for item in panel.get("dialogue", []):
        speaker = item.get("speaker", "")
        text = item.get("text", "")
        if text:
            dialogue_lines.append(f"{speaker}: {text}".strip())
    dialogue_text = " | ".join(dialogue_lines)

    # 角色锚点紧跟画风模板：prompt 前段权重更高，锚点后置容易被场景描述稀释
    parts = [style.get("positive_prompt_template", "")]
    if tone and tone.get("prompt_fragment"):
        parts.append(f"tone: {tone['prompt_fragment']}")
    if character_summary:
        parts.append(f"character bible: {character_summary}")
    if is_first_panel and reference_images:
        refs = ", ".join(reference_images)
        parts.append(
            f"reference image: {refs} attached — match this character's face and build"
        )
    parts.extend([
        f"visual form: {panel_plan.get('visual_form', '')}",
        f"format: {panel_plan.get('format', '')}",
        f"shot: {panel.get('shot', '')}",
        f"scene: {panel.get('scene', '')}",
        f"scene tag: {panel.get('scene_tag', '')}",
        f"action: {panel.get('action', '')}",
        f"emotion: {panel.get('emotion', '')}",
    ])
    if must_include:
        parts.append(f"must include: {must_include}")
    if avoid:
        parts.append(f"avoid: {avoid}")
    if dialogue_text:
        parts.append(f"dialogue reference: {dialogue_text}")
    if clean_suffix:
        parts.append(clean_suffix)

    prompt = ", ".join([p for p in parts if p])
    negative_parts = [style.get("negative_prompt_template", "")]
    if tone:
        negative_parts.extend(tone.get("negative_additions") or [])
    negative = ", ".join([p for p in negative_parts if p])
    return {
        "panel_id": panel["panel_id"],
        "style_id": style["style_id"],
        "tone_id": (tone or {}).get("tone_id"),
        "prompt": prompt,
        "negative_prompt": negative,
        "fallback_style_id": style.get("fallback_style_id"),
        "stability_rank": style.get("stability_rank"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile prompts from panel plan JSON.")
    parser.add_argument("panel_plan", help="Path to panel plan JSON")
    parser.add_argument("--styles", default="presets/styles.json", help="Path to styles.json")
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
        "--no-character-guard",
        action="store_true",
        help="Disable automatic injection/patching of hard character anchors",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parser.add_argument("--tones", default="presets/tones.json", help="Path to tones.json")
    parser.add_argument(
        "--tone",
        default=None,
        help="Tone preset id (overrides panel plan tone_id / bundle tone_id). See presets/tones.json",
    )
    parser.add_argument("--bundles", default="presets/bundles.json", help="Path to bundles.json")
    parser.add_argument(
        "--bundle",
        default=None,
        help="Chinese scenario bundle id (diary-strip / knowledge-picturebook / family-quad / poetry-strip). Its style_id and tone_id are used as defaults only.",
    )
    args = parser.parse_args()

    panel_plan = load_json(Path(args.panel_plan))
    styles_doc = load_json(Path(args.styles))
    style_index = build_style_index(styles_doc)

    tones_path = Path(args.tones)
    tones_doc = load_json(tones_path) if tones_path.is_file() else None
    tone_index = build_tone_index(tones_doc)

    bundles_path = Path(args.bundles)
    bundles_doc = load_json(bundles_path) if bundles_path.is_file() else None
    try:
        bundle = resolve_bundle(bundles_doc, args.bundle)
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    style_id = panel_plan.get("style_id") or (bundle or {}).get("style_id")
    if style_id not in style_index:
        print(f"Unknown style_id: {style_id}", file=sys.stderr)
        return 2

    tone_id = args.tone or panel_plan.get("tone_id") or (bundle or {}).get("tone_id")
    if not tone_id and tones_doc:
        tone_id = tones_doc.get("default_tone_id")
    tone = tone_index.get(tone_id) if tone_id else None
    if tone_id and tone is None and tone_index:
        print(f"Unknown tone_id: {tone_id}", file=sys.stderr)
        return 2

    if args.no_character_guard:
        cards: List[Dict[str, Any]] = []
    else:
        card_paths = [Path(p) for p in (args.character_card or ["presets/default_character.json"])]
        card_dir = Path(args.character_card_dir) if args.character_card_dir else None
        cards = load_character_cards(card_paths, card_dir)
    character_bible, guard = ensure_character_bible(panel_plan, cards)

    style = style_index[style_id]
    clean_suffix = styles_doc.get("global_clean_image_suffix", "")
    effective_plan = dict(panel_plan)
    if bundle:
        for key in ("visual_form", "format"):
            if not effective_plan.get(key) and bundle.get(key):
                effective_plan[key] = bundle[key]
    compiled = [
        compile_panel_prompt(
            effective_plan,
            style,
            panel,
            clean_suffix,
            character_bible=character_bible,
            reference_images=guard.get("reference_images") or [],
            is_first_panel=(index == 0),
            tone=tone,
        )
        for index, panel in enumerate(panel_plan.get("panels", []))
    ]

    output = {
        "story_id": panel_plan.get("story_id"),
        "style_id": style_id,
        "tone_id": (tone or {}).get("tone_id"),
        "bundle_id": (bundle or {}).get("bundle_id") if args.bundle else None,
        "character_guard": guard,
        "compiled_panels": compiled,
    }
    if args.pretty:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
