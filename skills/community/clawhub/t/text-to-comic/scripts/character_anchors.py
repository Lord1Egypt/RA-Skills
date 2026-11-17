#!/usr/bin/env python3
"""角色锚点的共享逻辑：归一化角色卡、推导硬锚点、补齐 must_keep。

默认主角和自定义角色走同一套规则——角色卡只是"锚点从哪来"的差别：
- 有卡片：用卡片的 hard_anchors（没写就从 appearance 推导）
- 没卡片：直接从这个角色自己的 appearance 推导
这样自定义角色不再是"跳过保护"，而是"用自己的结构化字段保护自己"。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

# 适合做跨格锚点的外观字段，按重要性排序。
# 刻意不含 outfit / accent_color：这两项随场景变化，锁死会让服装无法替换。
# 也不含 face：脸型描述（"round face"）对模型的约束力远弱于发型/眼镜/体型，
# 且默认主角卡本身不锚脸型，两套规则保持一致。
ANCHOR_KEYS: Tuple[str, ...] = ("hair", "eyewear", "build")

# 上述字段全为空时的兜底：至少锁住一个可描述特征，总比完全不锚好
FALLBACK_ANCHOR_KEYS: Tuple[str, ...] = ("face", "outfit", "accent_color")

# 锚点字段的中文名，用于校验报错和 guard 记录
FIELD_LABELS: Dict[str, str] = {
    "hair": "发型发色",
    "eyewear": "眼镜",
    "build": "体型",
    "face": "脸型",
    "outfit": "服装",
    "accent_color": "点缀色",
    "age_presentation": "年龄感",
    "vibe": "气质",
}

# 外观字段在 prompt 里的固定顺序（与 summarize_character_bible 保持一致）
APPEARANCE_ORDER: Tuple[str, ...] = (
    "age_presentation",
    "hair",
    "face",
    "eyewear",
    "outfit",
    "accent_color",
    "build",
    "vibe",
)

MAX_ANCHOR_LEN = 48


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def shorten(value: str) -> str:
    """外观描述常写成一句话，取第一个逗号前的部分做锚点，太长则截断。"""
    text = str(value or "").strip()
    if not text:
        return ""
    head = text.split(",")[0].strip() or text
    if len(head) > MAX_ANCHOR_LEN:
        head = head[:MAX_ANCHOR_LEN].rstrip(" ,;，；")
    return head


def normalize_card(doc: Dict[str, Any], path: Optional[Path] = None) -> Dict[str, Any]:
    """把角色卡归一化成统一结构。

    兼容两种写法：
    - 包裹式（默认卡）：{"character": {...}, "hard_anchors": [...]}
    - 扁平式（用户手写）：{"character_id": ..., "appearance": {...}, ...}
    """
    if not isinstance(doc, dict):
        return {}
    body = doc.get("character") if isinstance(doc.get("character"), dict) else doc
    character = {
        "character_id": body.get("character_id"),
        "name": body.get("name"),
        "appearance": body.get("appearance") or {},
        "must_keep": list(body.get("must_keep") or []),
    }
    return {
        "character": character,
        "hard_anchors": list(doc.get("hard_anchors") or body.get("hard_anchors") or []),
        "reference_image": doc.get("reference_image") or body.get("reference_image") or "",
        "source_doc": doc.get("source_doc") or "",
        "card_path": str(path) if path else "",
    }


def load_card(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        return normalize_card(load_json(path), path)
    except (json.JSONDecodeError, OSError):
        return None


def load_card_dir(directory: Path) -> List[Dict[str, Any]]:
    """加载目录下所有角色卡（非递归）。目录不存在时返回空列表。"""
    if not directory.is_dir():
        return []
    cards: List[Dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        card = load_card(path)
        if card and card.get("character", {}).get("character_id"):
            cards.append(card)
    return cards


def _default_anchor(key: str, value: str) -> Dict[str, Any]:
    short = shorten(value)
    terms: List[str] = []
    for term in (short, str(value).strip(), FIELD_LABELS.get(key, key), key):
        if term and term not in terms:
            terms.append(term)
    return {
        "key": key,
        "label_zh": FIELD_LABELS.get(key, key),
        "must_keep_value": short,
        "must_match": terms,
    }


def derive_anchors(
    character: Dict[str, Any], hard_anchors: Optional[Iterable[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """得出这个角色该被锁住的锚点。

    优先用显式 hard_anchors；没有就从 appearance 里挑适合跨格保持的字段。
    都没有则返回空列表——调用方据此判断"这个角色无法锚定"。
    """
    explicit = [a for a in (hard_anchors or []) if isinstance(a, dict)]
    if explicit:
        anchors: List[Dict[str, Any]] = []
        for item in explicit:
            key = item.get("key", "")
            value = item.get("must_keep_value") or item.get("value") or ""
            if not value:
                continue
            terms = [str(t) for t in (item.get("must_match") or [])]
            label = item.get("label_zh") or FIELD_LABELS.get(key, key)
            for term in (value, label, key):
                if term and term not in terms:
                    terms.append(str(term))
            anchors.append(
                {
                    "key": key,
                    "label_zh": label,
                    "must_keep_value": str(value),
                    "must_match": terms,
                }
            )
        return anchors

    appearance = character.get("appearance") or {}
    anchors = []
    for key in ANCHOR_KEYS:
        value = str(appearance.get(key) or "").strip()
        if value:
            anchors.append(_default_anchor(key, value))
    if anchors:
        return anchors
    # 主锚点字段都没填：退回一个可描述特征（脸型 / 服装 / 点缀色）
    for key in FALLBACK_ANCHOR_KEYS:
        value = str(appearance.get(key) or "").strip()
        if value:
            return [_default_anchor(key, value)]
    return []


def anchor_covered(must_keep: Iterable[Any], anchor: Dict[str, Any]) -> bool:
    joined = " ".join(str(item).lower() for item in must_keep)
    return any(str(term).lower() in joined for term in anchor.get("must_match", []) if str(term).strip())


def apply_anchors(
    character: Dict[str, Any], anchors: Iterable[Dict[str, Any]]
) -> Tuple[List[str], List[str]]:
    """把缺失的锚点补进 must_keep，返回 (补齐后的列表, 补了哪些中文名)。"""
    must_keep = [str(item) for item in (character.get("must_keep") or [])]
    patched: List[str] = []
    for anchor in anchors:
        if anchor_covered(must_keep, anchor):
            continue
        value = str(anchor.get("must_keep_value") or "").strip()
        if value and value not in must_keep:
            must_keep.append(value)
            patched.append(anchor.get("label_zh") or anchor.get("key", ""))
    return must_keep, patched


def missing_anchors(
    character: Dict[str, Any], anchors: Iterable[Dict[str, Any]]
) -> List[str]:
    must_keep = character.get("must_keep") or []
    return [
        anchor.get("label_zh") or anchor.get("key", "")
        for anchor in anchors
        if not anchor_covered(must_keep, anchor)
    ]


def build_registry(cards: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """按 character_id 和 name 建索引，两者都能命中同一张卡。"""
    registry: Dict[str, Dict[str, Any]] = {}
    for card in cards:
        character = card.get("character") or {}
        for key in ("character_id", "name"):
            value = (character.get(key) or "").strip()
            if value:
                registry.setdefault(f"{key}:{value}", card)
    return registry


def match_card(
    character: Dict[str, Any], registry: Dict[str, Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    for key in ("character_id", "name"):
        value = (character.get(key) or "").strip()
        if value and f"{key}:{value}" in registry:
            return registry[f"{key}:{value}"]
    return None


def enrich_character(character: Dict[str, Any], card: Dict[str, Any]) -> Dict[str, Any]:
    """卡片里的外观字段用于补全分镜里没写全的角色（bible 优先，不覆盖）。"""
    enriched = dict(character)
    appearance = dict(card.get("character", {}).get("appearance") or {})
    appearance.update(character.get("appearance") or {})
    enriched["appearance"] = appearance
    return enriched
