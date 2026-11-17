#!/usr/bin/env python3
"""自定义角色卡工具：生成、迁移、检查。

自定义角色和默认主角走同一套锚点规则，只是锚点来源不同：
- 有卡片 → 用卡片的 hard_anchors（留空则从 appearance 推导）
- 没卡片 → 用分镜里该角色自己的 appearance 推导

所以"把一个松散的角色描述变成结构化卡片"是这套机制的关键一步，
from-bible 就负责这件事：把已有分镜里的角色直接迁成卡片。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

from character_anchors import (  # noqa: E402
    ANCHOR_KEYS,
    FIELD_LABELS,
    derive_anchors,
    load_card,
    load_card_dir,
    load_json,
    missing_anchors,
)

DEFAULT_CARD_DIR = Path("characters/cards")


def slugify(name: str) -> str:
    ascii_part = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if ascii_part:
        return ascii_part
    return "char-" + str(abs(hash(name)) % 100000)


def build_card(
    name: str,
    character_id: str | None = None,
    appearance: Dict[str, str] | None = None,
    must_keep: List[str] | None = None,
    reference_image: str = "",
    source_doc: str = "",
    notes: str = "",
) -> Dict[str, Any]:
    appearance = {key: value for key, value in (appearance or {}).items() if str(value or "").strip()}
    character: Dict[str, Any] = {
        "character_id": character_id or f"char_{slugify(name).replace('-', '_')}",
        "name": name,
        "appearance": appearance,
        "must_keep": [str(item) for item in (must_keep or []) if str(item).strip()],
    }
    # 先推导锚点，再把缺的补进 must_keep —— 保证新卡一生成就是自洽的
    anchors = derive_anchors(character, None)
    for anchor in anchors:
        value = anchor["must_keep_value"]
        if value and value not in character["must_keep"]:
            if not any(term.lower() in " ".join(character["must_keep"]).lower() for term in anchor["must_match"]):
                character["must_keep"].append(value)
    return {
        "version": "1.0.0",
        "source_doc": source_doc,
        "reference_image": reference_image,
        "notes": notes
        or "把「绝不能变」的部分写进 hair / eyewear / build / face，outfit 与 accent_color 可按场景替换。",
        "character": character,
        "hard_anchors": [
            {
                "key": a["key"],
                "label_zh": a["label_zh"],
                "must_keep_value": a["must_keep_value"],
                "must_match": a["must_match"],
            }
            for a in anchors
        ],
    }


def cmd_init(args: argparse.Namespace) -> int:
    appearance = {
        "age_presentation": args.age,
        "hair": args.hair,
        "face": args.face,
        "eyewear": args.eyewear,
        "outfit": args.outfit,
        "accent_color": args.accent,
        "build": args.build,
        "vibe": args.vibe,
    }
    if not any(str(v or "").strip() for v in appearance.values()):
        print(
            "error: 至少需要一个外观字段（如 --hair）。"
            "可用：--age --hair --face --eyewear --outfit --accent --build --vibe",
            file=sys.stderr,
        )
        return 2
    card = build_card(
        name=args.name,
        character_id=args.id,
        appearance=appearance,
        must_keep=args.must_keep or [],
        reference_image=args.reference_image,
        source_doc=args.source_doc,
    )
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"written: {out_path}")
        print(f"anchors: {', '.join(a['label_zh'] for a in card['hard_anchors']) or '无'}")
    else:
        print(json.dumps(card, ensure_ascii=False, indent=2))
    return 0


def cmd_from_bible(args: argparse.Namespace) -> int:
    plan = load_json(Path(args.plan))
    bible = plan.get("character_bible") or []
    if not bible:
        print("error: 这个分镜里没有 character_bible", file=sys.stderr)
        return 2
    target = None
    if args.name:
        for character in bible:
            if (character.get("name") or "").strip() == args.name:
                target = character
                break
    else:
        if args.index < 0 or args.index >= len(bible):
            print(f"error: index 越界（共 {len(bible)} 个角色）", file=sys.stderr)
            return 2
        target = bible[args.index]
    if target is None:
        print(f"error: 找不到角色 {args.name}", file=sys.stderr)
        return 2

    card = build_card(
        name=target.get("name") or "character",
        character_id=target.get("character_id"),
        appearance=dict(target.get("appearance") or {}),
        must_keep=list(target.get("must_keep") or []),
        reference_image=target.get("reference_image") or args.reference_image,
        source_doc=args.source_doc or "",
        notes=f"由 {args.plan} 的 character_bible 迁移生成。",
    )
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"written: {out_path}")
        print(f"anchors: {', '.join(a['label_zh'] for a in card['hard_anchors']) or '无'}")
    else:
        print(json.dumps(card, ensure_ascii=False, indent=2))
    return 0


def check_card(card: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    character = card.get("character") or {}
    name = character.get("name") or "(未命名)"
    if not character.get("character_id"):
        errors.append(f"{name}: 缺少 character_id")
    if not character.get("name"):
        errors.append("缺少 name")
    appearance = character.get("appearance") or {}
    if not appearance:
        errors.append(f"{name}: appearance 为空，无法锁定任何锚点")
    anchors = derive_anchors(character, card.get("hard_anchors"))
    if not anchors:
        keys = " / ".join(ANCHOR_KEYS)
        errors.append(f"{name}: appearance 里没有任何可锚定字段（{keys} 至少填一项）")
    for anchor in card.get("hard_anchors") or []:
        if not anchor.get("must_keep_value"):
            errors.append(f"{name}: 锚点 {anchor.get('key', '?')} 缺少 must_keep_value")
        if not anchor.get("must_match"):
            errors.append(f"{name}: 锚点 {anchor.get('key', '?')} 缺少 must_match")
    missing = missing_anchors(character, anchors)
    if missing:
        errors.append(
            f"{name}: must_keep 未覆盖锚点 {'、'.join(missing)}（compile 阶段会自动补齐，建议卡片里就写全）"
        )
    return errors


def cmd_check(args: argparse.Namespace) -> int:
    paths: List[Path] = []
    if args.card:
        paths = [Path(p) for p in args.card]
    else:
        paths = sorted(Path(args.dir).glob("*.json"))
    if not paths:
        print(f"error: 没有找到角色卡（{args.dir}）", file=sys.stderr)
        return 2

    results = []
    failed = 0
    for path in paths:
        card = load_card(path)
        if not card:
            results.append({"card": str(path), "ok": False, "errors": ["无法解析为角色卡"]})
            failed += 1
            continue
        errors = check_card(card)
        results.append({"card": str(path), "ok": not errors, "errors": errors})
        failed += 1 if errors else 0

    payload = {"ok": failed == 0, "checked": len(paths), "failed": failed, "results": results}
    duplicates = _duplicate_ids(paths)
    if duplicates:
        payload["duplicates"] = duplicates
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in results:
            mark = "✅" if item["ok"] else "❌"
            print(f"{mark} {item['card']}")
            for error in item["errors"]:
                print(f"   - {error}")
        for character_id, card_paths in duplicates.items():
            print(f"⚠️  character_id 重复：{character_id} → {', '.join(card_paths)}（只有第一张会生效）")
        print(f"--- 共 {len(paths)} 张，失败 {failed} 张")
    return 0 if failed == 0 else 1


def _duplicate_ids(paths: List[Path]) -> Dict[str, List[str]]:
    seen: Dict[str, List[str]] = {}
    for path in paths:
        card = load_card(path)
        character_id = (card or {}).get("character", {}).get("character_id")
        if character_id:
            seen.setdefault(character_id, []).append(str(path))
    return {key: value for key, value in seen.items() if len(value) > 1}


def cmd_list(args: argparse.Namespace) -> int:
    cards = load_card_dir(Path(args.dir))
    if not cards:
        print(f"（{args.dir} 下没有角色卡）")
        return 0
    for card in cards:
        character = card.get("character") or {}
        anchors = derive_anchors(character, card.get("hard_anchors"))
        labels = "、".join(a["label_zh"] for a in anchors) or "无锚点"
        print(
            f"{character.get('character_id')} | {character.get('name')} | "
            f"锚点: {labels} | {card.get('card_path')}"
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage structured character cards.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a character card from appearance flags")
    init.add_argument("--name", required=True, help="Character name (e.g. 小陈)")
    init.add_argument("--id", help="character_id (default: derived from name)")
    init.add_argument("--age", help="age_presentation")
    init.add_argument("--hair", help="hair")
    init.add_argument("--face", help="face")
    init.add_argument("--eyewear", help="eyewear")
    init.add_argument("--outfit", help="outfit")
    init.add_argument("--accent", help="accent_color")
    init.add_argument("--build", help="build")
    init.add_argument("--vibe", help="vibe")
    init.add_argument("--must-keep", nargs="*", help="Extra must_keep phrases")
    init.add_argument("--reference-image", default="", help="Reference sheet path")
    init.add_argument("--source-doc", default="", help="Human-readable card path (md)")
    init.add_argument("--out", help="Write to this path instead of stdout")
    init.set_defaults(func=cmd_init)

    from_bible = sub.add_parser("from-bible", help="Convert a character in a panel plan into a card")
    from_bible.add_argument("plan", help="Path to panel plan JSON")
    from_bible.add_argument("--index", type=int, default=0, help="Character index in character_bible")
    from_bible.add_argument("--name", help="Pick by name instead of index")
    from_bible.add_argument("--reference-image", default="", help="Fallback reference sheet path")
    from_bible.add_argument("--source-doc", default="", help="Human-readable card path (md)")
    from_bible.add_argument("--out", help="Write to this path instead of stdout")
    from_bible.set_defaults(func=cmd_from_bible)

    check = sub.add_parser("check", help="Validate character cards")
    check.add_argument("card", nargs="*", help="Card paths (default: all in --dir)")
    check.add_argument("--dir", default=str(DEFAULT_CARD_DIR), help="Card directory")
    check.add_argument("--json", action="store_true", help="JSON output")
    check.set_defaults(func=cmd_check)

    list_cmd = sub.add_parser("list", help="List cards in a directory")
    list_cmd.add_argument("--dir", default=str(DEFAULT_CARD_DIR), help="Card directory")
    list_cmd.set_defaults(func=cmd_list)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
