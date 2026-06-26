#!/usr/bin/env python3

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Tuple

KEEP = "keep"
DROP = "drop"


def _safe_int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except Exception:
        return default


def _normalize_input(payload: Any) -> Tuple[Any, str]:
    """Normalize llm-asr output into asr-vad compatible structure."""
    if not isinstance(payload, dict):
        return payload, "raw"

    # Keep existing labeled payloads as-is.
    for key in ("data", "vad_decisions", "segments"):
        items = payload.get(key)
        if isinstance(items, list) and items:
            return payload, "provided"

    editable = payload.get("editable_subtitles")
    if not isinstance(editable, list) or not editable:
        return payload, "raw"

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(editable, start=1):
        if not isinstance(item, dict):
            continue
        sentence = str(item.get("text") or item.get("sentence") or "").strip()
        st = _safe_int(item.get("start_ms"), -1)
        if st < 0:
            st = _safe_int(item.get("start_time"), -1)
        if st < 0:
            st = _safe_int(item.get("start"), -1)
        et = _safe_int(item.get("end_ms"), -1)
        if et < 0:
            et = _safe_int(item.get("end_time"), -1)
        if et < 0:
            et = _safe_int(item.get("end"), -1)
        if not sentence or st < 0 or et <= st:
            continue
        normalized.append(
            {
                "id": idx,
                "sentence": sentence,
                "start_time": st,
                "end_time": et,
                "action": KEEP,
                "drop_reason": "",
            }
        )

    merged = dict(payload)
    merged["data"] = normalized
    return merged, "auto_default"


def _extract_decisions(payload: Any) -> List[Dict[str, Any]]:
    # 输入支持：
    # 1) {"data":[...]}（第一步标注结果）
    # 2) {"vad_decisions":[...]}（封装结果）
    # 3) 直接 list
    if isinstance(payload, dict):
        items = payload.get("data")
        if not isinstance(items, list):
            items = payload.get("vad_decisions")
        if not isinstance(items, list):
            items = payload.get("segments")
    elif isinstance(payload, list):
        items = payload
    else:
        items = []

    out: List[Dict[str, Any]] = []
    idx = 1
    for it in items or []:
        if not isinstance(it, dict):
            continue
        sentence = str(it.get("sentence") or it.get("text") or "").strip()
        st = _safe_int(it.get("start_time"), -1)
        if st < 0:
            st = _safe_int(it.get("start"), -1)
        et = _safe_int(it.get("end_time"), -1)
        if et < 0:
            et = _safe_int(it.get("end"), -1)
        action = str(it.get("action") or KEEP).strip().lower()
        if action not in {KEEP, DROP}:
            action = KEEP
        reason = str(it.get("drop_reason") or "").strip().lower()
        if not sentence or st < 0 or et <= st:
            continue
        out.append(
            {
                "id": idx,
                "sentence": sentence,
                "start_time": st,
                "end_time": et,
                "action": action,
                "drop_reason": reason if action == DROP else "",
            }
        )
        idx += 1
    return out


def _extract_source_video_url(payload: Any, video_url_override: str) -> str:
    if video_url_override:
        return video_url_override
    if not isinstance(payload, dict):
        return ""
    meta = payload.get("meta")
    if isinstance(meta, dict):
        source = str(meta.get("source_video_url") or meta.get("source_url") or "").strip()
        if source:
            return source
    return str(payload.get("video_url") or "").strip()


def run_asr_vad(payload: Any, video_url_override: str = "") -> Dict[str, Any]:
    payload, label_source = _normalize_input(payload)
    decisions = _extract_decisions(payload)
    if not decisions:
        raise RuntimeError(
            "No valid VAD decisions extracted. Please provide labeled data or "
            "editable_subtitles with start_ms/end_ms/text."
        )
    source_video_url = _extract_source_video_url(payload, video_url_override)

    keep_items = [d for d in decisions if d.get("action") == KEEP]
    editable_subtitles: List[Dict[str, Any]] = []
    clip_plan: List[Dict[str, Any]] = []
    timeline_ms = 0

    for i, item in enumerate(keep_items, start=1):
        src_st = _safe_int(item.get("start_time"), 0)
        src_et = _safe_int(item.get("end_time"), src_st)
        duration_ms = max(1, src_et - src_st)
        dst_st = timeline_ms
        dst_et = dst_st + duration_ms
        timeline_ms = dst_et

        editable_subtitles.append(
            {
                "id": i,
                "start_ms": dst_st,
                "end_ms": dst_et,
                "text": str(item.get("sentence") or ""),
                "source_start_ms": src_st,
                "source_end_ms": src_et,
            }
        )

        clip_plan.append(
            {
                "id": i,
                "video_url": source_video_url,
                "start": round(src_st / 1000.0, 3),
                "end": round(src_et / 1000.0, 3),
                "target_start": round(dst_st / 1000.0, 3),
                "track_name": "video_main",
            }
        )

    workflow_json = {
        "inputs": {"clips": clip_plan},
        "script": [
            {
                "type": "for",
                "id": "add_vad_clips",
                "index": 0,
                "in": "${clips}",
                "loop": [
                    {
                        "type": "action",
                        "id": "add_video_clip",
                        "index": 0,
                        "action_type": "add_video",
                        "params": {
                            "video_url": "${item.video_url}",
                            "start": "${item.start}",
                            "end": "${item.end}",
                            "target_start": "${item.target_start}",
                            "track_name": "${item.track_name}",
                        },
                    }
                ],
            }
        ],
    }

    reason_counter = Counter(
        d.get("drop_reason", "")
        for d in decisions
        if d.get("action") == DROP and d.get("drop_reason")
    )
    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_video_url": source_video_url,
            "label_source": label_source,
            "stats": {
                "total": len(decisions),
                "keep": len(keep_items),
                "drop": len(decisions) - len(keep_items),
                "drop_reasons": dict(reason_counter),
            },
        },
        "vad_decisions": decisions,
        "editable_subtitles": editable_subtitles,
        "workflow_json": workflow_json,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to labeled VAD JSON")
    parser.add_argument(
        "--output",
        default="subtitle_vad_editable.json",
        help="Path to rebuilt contiguous subtitle JSON output",
    )
    parser.add_argument(
        "--workflow-output",
        default="asr_vad_clip_workflow.json",
        help="Path to extracted clip workflow JSON",
    )
    parser.add_argument(
        "--video-url",
        default="",
        help="Optional source video url override",
    )
    parser.add_argument(
        "--draft-id",
        default="",
        help="Optional existing draft id to continue editing",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    result = run_asr_vad(payload, video_url_override=args.video_url)
    if args.draft_id:
        result["workflow_json"]["draft_id"] = args.draft_id

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    with open(args.workflow_output, "w", encoding="utf-8") as f:
        json.dump(result["workflow_json"], f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
