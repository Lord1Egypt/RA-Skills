#!/usr/bin/env python3
from common import (
    classify_comparison,
    clean_text,
    extract_title,
    get_final_price,
    infer_decision_mode,
    infer_source_from_url,
    make_candidate_id,
    merge_notes,
    read_stdin_json,
    write_error,
    write_json,
)


def main() -> None:
    try:
        payload = read_stdin_json()
        items = payload.get("items") or []
        if not isinstance(items, list):
            raise ValueError("items must be an array when provided")

        notes_text = merge_notes(payload.get("notes"), payload.get("query"))
        explicit_decision_mode = payload.get("decision_mode")
        inferred_mode = infer_decision_mode(items, notes_text)
        decision_mode = explicit_decision_mode or inferred_mode

        candidates = []
        warnings = []
        missing_fields = []
        candidate_missing_price = False

        if explicit_decision_mode and explicit_decision_mode != inferred_mode:
            warnings.append("Explicit decision_mode conflicts with item count or user wording; keeping explicit value.")

        title_texts = []
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                continue

            title, weak_title = extract_title(item, index)
            title_texts.append(merge_notes(title, item.get("raw_text")) or title)
            explicit_source = clean_text(item.get("source")) or None
            inferred_source = infer_source_from_url(clean_text(item.get("url")) or None)
            source = explicit_source or inferred_source or "manual"
            if explicit_source and inferred_source and explicit_source != inferred_source:
                warnings.append(f"Candidate {index + 1}: source conflicts with URL; keeping explicit source '{explicit_source}'.")
            if weak_title:
                warnings.append(f"Candidate {index + 1}: title was weak and had to be generated from limited input.")
            if item.get("screenshot_path") and not item.get("raw_text"):
                warnings.append(f"Candidate {index + 1}: screenshot path provided without readable extracted text.")

            price = get_final_price(item)
            if price is None:
                candidate_missing_price = True
                warnings.append(f"Candidate {index + 1}: missing price information.")

            evidence = []
            if clean_text(item.get("title")):
                evidence.append({"type": "user_input", "value": clean_text(item.get("title"))})
            if clean_text(item.get("raw_text")):
                evidence.append({"type": "manual_note", "value": clean_text(item.get("raw_text"))[:200]})
            if clean_text(item.get("url")):
                evidence.append({"type": "other", "value": clean_text(item.get("url"))})
            if clean_text(item.get("screenshot_path")):
                evidence.append({"type": "other", "value": clean_text(item.get("screenshot_path"))})
            if notes_text:
                evidence.append({"type": "manual_note", "value": notes_text[:200]})

            candidate = {
                "id": make_candidate_id(index),
                "title": title,
                "source": source,
                "url": clean_text(item.get("url")) or None,
                "price": price,
                "evidence": evidence or [{"type": "user_input", "value": title}],
            }
            candidates.append({k: v for k, v in candidate.items() if v is not None})

        if candidates:
            base_text = title_texts[0]
            candidates[0]["comparison"] = {"relation": "same_item", "reason_tags": []}
            for index in range(1, len(candidates)):
                candidates[index]["comparison"] = classify_comparison(base_text, title_texts[index])

        if not clean_text(payload.get("category")):
            missing_fields.append("category")
        if not clean_text(payload.get("scenario")):
            missing_fields.append("scenario")
        priorities = payload.get("priorities")
        if not priorities:
            missing_fields.append("priorities")
        if not payload.get("budget"):
            missing_fields.append("budget")
        if not candidates:
            missing_fields.append("candidates")
            warnings.append("No candidate items provided; decision will stay in guidance mode.")
        elif all((candidate.get("price") or {}).get("final_price") is None for candidate in candidates):
            missing_fields.append("price")
        elif candidate_missing_price:
            warnings.append("Some candidates are missing price information, so later comparisons may be weaker.")

        context = {
            "query": {
                "category": clean_text(payload.get("category")) or None,
                "budget": payload.get("budget"),
                "scenario": clean_text(payload.get("scenario")) or None,
                "priorities": priorities,
                "decision_mode": decision_mode,
                "notes": notes_text,
            },
            "candidates": candidates,
            "meta": {
                "data_source_mode": "user_only",
                "missing_fields": missing_fields,
                "warnings": warnings,
            },
        }
        write_json(context)
    except Exception as exc:
        write_error(str(exc))


if __name__ == "__main__":
    main()
