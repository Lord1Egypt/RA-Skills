#!/usr/bin/env python3

import argparse
from hashlib import sha1
import importlib.util
import json
from pathlib import Path
import random
from typing import Any, Dict, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent

TEMPLATE_MODULES = {
    "template_bilingual_keyword": "template_bilingual_keyword.py",
    "template_dual_track_motion": "template_dual_track_motion.py",
    "template_karaoke_highlight": "template_karaoke_highlight.py",
    "template_preset_transition": "template_preset_transition.py",
    "template_roll_focus": "template_roll_focus.py",
    "template_slide_in_out": "template_slide_in_out.py",
    "template_word_pop": "template_word_pop.py",
}


def _detect_effect_mode(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""

    meta = payload.get("meta")
    if isinstance(meta, dict):
        mode = str(meta.get("effect_mode") or meta.get("asr_effect_mode") or "").strip()
        if mode:
            return mode.lower()

    raw = payload.get("raw_result")
    if isinstance(raw, dict):
        mode = str(raw.get("effect_mode") or "").strip()
        if mode:
            return mode.lower()

    return ""


def _to_ms(value: Any, source_key: str) -> int:
    try:
        num = float(value)
    except Exception:
        return -1

    if source_key in {"start_ms", "end_ms", "start_time", "end_time"}:
        return int(num)
    # start/end are often seconds in manual payloads.
    if source_key in {"start", "end"} and num <= 600:
        return int(num * 1000)
    return int(num)


def _pick_time_keys(item: Dict[str, Any], start_candidates: List[str], end_candidates: List[str]) -> Tuple[int, int]:
    start_ms = -1
    end_ms = -1
    for key in start_candidates:
        if key in item:
            start_ms = _to_ms(item.get(key), key)
            if start_ms >= 0:
                break
    for key in end_candidates:
        if key in item:
            end_ms = _to_ms(item.get(key), key)
            if end_ms >= 0:
                break
    return start_ms, end_ms


def _normalize_segments(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        raw_segments = payload
    elif isinstance(payload, dict):
        raw_segments = payload.get("segments")
        if not isinstance(raw_segments, list):
            raw_segments = payload.get("editable_subtitles")
        if not isinstance(raw_segments, list):
            raw_result = payload.get("raw_result")
            if isinstance(raw_result, dict):
                raw_segments = raw_result.get("segments")
        if not isinstance(raw_segments, list):
            raw_segments = []
    else:
        raw_segments = []

    normalized: List[Dict[str, Any]] = []
    for item in raw_segments:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text") or item.get("sentence") or "").strip()
        start_ms, end_ms = _pick_time_keys(
            item,
            ["start_ms", "start_time", "start"],
            ["end_ms", "end_time", "end"],
        )
        if not text or start_ms < 0 or end_ms <= start_ms:
            continue

        seg: Dict[str, Any] = {
            "start": start_ms,
            "end": end_ms,
            "text": text,
        }
        if isinstance(item.get("words"), list):
            seg["words"] = item["words"]
        if isinstance(item.get("phrase"), list):
            seg["phrase"] = item["phrase"]
        if item.get("en"):
            seg["en"] = item.get("en")
        normalized.append(seg)
    return normalized


def _segment_signature(segments: List[Dict[str, Any]]) -> str:
    text_blob = "|".join(s.get("text", "") for s in segments)
    return sha1(text_blob.encode("utf-8")).hexdigest()


def _pick_from_pool(
    pool: List[str], segments: List[Dict[str, Any]], selection_mode: str
) -> str:
    if not pool:
        raise RuntimeError("Template pool is empty.")
    if selection_mode == "stable":
        sig = _segment_signature(segments)
        pick = int(sig[:8], 16) % len(pool)
        return pool[pick]
    return random.choice(pool)


def _select_template(
    segments: List[Dict[str, Any]],
    forced_template: str = "",
    selection_mode: str = "random",
) -> str:
    if forced_template:
        if forced_template not in TEMPLATE_MODULES:
            raise RuntimeError(
                f"Unknown template: {forced_template}. "
                f"Available: {', '.join(sorted(TEMPLATE_MODULES.keys()))}"
            )
        return forced_template

    if not segments:
        raise RuntimeError("No valid segments found for template selection.")

    has_en = any(bool(str(s.get("en") or "").strip()) for s in segments)
    if has_en:
        return "template_bilingual_keyword"

    word_timed_count = 0
    word_count_total = 0
    for seg in segments:
        words = seg.get("words")
        if not isinstance(words, list) or not words:
            continue
        valid_words = [
            w
            for w in words
            if isinstance(w, dict)
            and ("start_time" in w and "end_time" in w)
        ]
        if valid_words:
            word_timed_count += 1
            word_count_total += len(valid_words)
    if word_timed_count >= max(2, len(segments) // 2):
        avg_words = word_count_total / max(1, word_timed_count)
        if avg_words >= 4:
            return "template_karaoke_highlight"
        return "template_word_pop"

    avg_duration_ms = sum(s["end"] - s["start"] for s in segments) / max(1, len(segments))
    if len(segments) >= 18:
        return "template_roll_focus"
    if len(segments) >= 10 and avg_duration_ms <= 1400:
        motion_pool = [
            "template_dual_track_motion",
            "template_slide_in_out",
            "template_preset_transition",
        ]
        return _pick_from_pool(
            motion_pool, segments, selection_mode=selection_mode
        )

    # Sentence-level subtitles: random by default, stable when explicitly requested.
    basic_pool = [
        "template_slide_in_out",
        "template_roll_focus",
        "template_dual_track_motion",
        "template_preset_transition",
    ]
    return _pick_from_pool(
        basic_pool, segments, selection_mode=selection_mode
    )


def _load_template_module(template_name: str):
    script_name = TEMPLATE_MODULES[template_name]
    module_path = SCRIPT_DIR / script_name
    spec = importlib.util.spec_from_file_location(template_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load template module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_workflow(
    payload: Any,
    draft_id: str = "",
    forced_template: str = "",
    selection_mode: str = "random",
) -> Dict[str, Any]:
    detected_effect_mode = _detect_effect_mode(payload)
    if detected_effect_mode == "basic":
        raise RuntimeError(
            "Detected ASR effect_mode=basic in subtitle payload. "
            "basic results are analysis-only and cannot be used for subtitle on-screen. "
            "Please rerun llm-asr with --effect-mode nlp."
        )
    segments = _normalize_segments(payload)
    if selection_mode not in {"random", "stable"}:
        raise RuntimeError("selection_mode must be one of: random|stable")
    template_name = _select_template(
        segments,
        forced_template,
        selection_mode=selection_mode,
    )
    module = _load_template_module(template_name)
    workflow = module.apply_template(segments, draft_id)
    if not isinstance(workflow, dict):
        raise RuntimeError(f"Template {template_name} returned non-dict workflow.")
    workflow["_selected_template"] = template_name
    workflow["_segment_count"] = len(segments)
    return workflow


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to subtitle payload JSON")
    parser.add_argument("--draft-id", default="", help="Existing draft id")
    parser.add_argument(
        "--template",
        default="",
        help=f"Optional template override: {', '.join(sorted(TEMPLATE_MODULES.keys()))}",
    )
    parser.add_argument(
        "--selection-mode",
        default="random",
        choices=["random", "stable"],
        help="Template selection mode when template is not forced. Default: random.",
    )
    parser.add_argument(
        "--output",
        default="subtitle_template_workflow.json",
        help="Path to output workflow JSON",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    workflow = build_workflow(
        payload=payload,
        draft_id=args.draft_id,
        forced_template=args.template,
        selection_mode=args.selection_mode,
    )

    selected_template = workflow.pop("_selected_template", "")
    segment_count = workflow.pop("_segment_count", 0)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(workflow, f, ensure_ascii=False, indent=2)

    print(
        json.dumps(
            {
                "success": True,
                "selected_template": selected_template,
                "segment_count": segment_count,
                "output": args.output,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
