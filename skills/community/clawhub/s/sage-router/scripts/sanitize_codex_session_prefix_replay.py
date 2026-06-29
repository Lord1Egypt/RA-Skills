#!/usr/bin/env python3
"""Remove replayed Sage Router model-prefix storms from Codex JSONL sessions."""

import argparse
import json
import re
import shutil
import time
from pathlib import Path


TOOL_CALLS_OMITTED_RE = r"\[\s*tool\s+calls\s*omitted\s*\]"
MODEL_PREFIX_LABEL_RE = r"\[[A-Za-z0-9_.-]+/[^\]\s]+\]"
PARTIAL_MODEL_PREFIX_LABEL_RE = r"\[[A-Za-z0-9_.-]*(?:/[^\]\s]*)?$"


def looks_like_model_prefix_label(label):
    label = str(label or "").strip()
    if label.lower().startswith("sage-router "):
        label = label.split(None, 1)[1].strip()
    if len(label) > 140 or " " in label or "/" not in label:
        return False
    return bool(re.match(r"^[A-Za-z0-9_.-]+/[^\]\s]+$", label))


def strip_model_prefix_tool_placeholder_noise(text):
    remaining = str(text or "")
    if not remaining:
        return ""
    prefix_run_re = rf"(?:{MODEL_PREFIX_LABEL_RE}\s*)+"
    placeholder_run_re = rf"(?:{MODEL_PREFIX_LABEL_RE}\s*)*{TOOL_CALLS_OMITTED_RE}"
    cleaned_lines = []
    changed = False
    for line in remaining.splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append(line)
            continue
        labels = re.findall(MODEL_PREFIX_LABEL_RE, stripped)
        without_noise = re.sub(MODEL_PREFIX_LABEL_RE, "", stripped).strip()
        without_noise = re.sub(TOOL_CALLS_OMITTED_RE, "", without_noise, flags=re.IGNORECASE).strip()
        if labels:
            without_noise = re.sub(PARTIAL_MODEL_PREFIX_LABEL_RE, "", without_noise).strip()
        if not labels and "/" in stripped and stripped.rsplit("/", 1)[1] and re.fullmatch(PARTIAL_MODEL_PREFIX_LABEL_RE, stripped):
            changed = True
            continue
        if labels and not without_noise:
            changed = True
            continue
        if not labels and not without_noise and re.search(TOOL_CALLS_OMITTED_RE, stripped, flags=re.IGNORECASE):
            changed = True
            continue
        cleaned_lines.append(line)
    cleaned = "\n".join(cleaned_lines).strip() if changed else remaining
    if not cleaned.rstrip().endswith("]"):
        return cleaned
    suffix_noise_re = rf"(?:\s+(?:{placeholder_run_re}|{prefix_run_re}))+\s*$"
    suffix_cleaned = re.sub(suffix_noise_re, "", cleaned, flags=re.IGNORECASE).rstrip()
    if suffix_cleaned != cleaned:
        cleaned = suffix_cleaned
        changed = True
    if changed:
        return re.sub(PARTIAL_MODEL_PREFIX_LABEL_RE, "", cleaned.strip()).rstrip()
    return cleaned


def strip_leading_generic_model_prefix_labels(text):
    remaining = str(text or "")
    changed = False
    while True:
        stripped = remaining.lstrip()
        leading_ws = remaining[: len(remaining) - len(stripped)]
        match = re.match(r"^\[([^\]\n]{1,140})\](?=\s|$)\s*", stripped)
        if not match or not looks_like_model_prefix_label(match.group(1)):
            break
        remaining = leading_ws + stripped[match.end() :].lstrip()
        changed = True
    return remaining.strip() if changed else remaining


def sanitize_visible_output(text):
    cleaned = strip_model_prefix_tool_placeholder_noise(text)
    cleaned = strip_leading_generic_model_prefix_labels(cleaned)
    cleaned = re.sub(rf"(^|[\s]){TOOL_CALLS_OMITTED_RE}(?=\s|$)", r"\1", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def sanitize_event(obj):
    changed = 0
    if obj.get("type") == "response_item":
        payload = obj.get("payload")
        if isinstance(payload, dict):
            for part in payload.get("content") or []:
                if isinstance(part, dict) and isinstance(part.get("text"), str):
                    cleaned = sanitize_visible_output(part["text"])
                    if cleaned != part["text"]:
                        part["text"] = cleaned
                        changed += 1
    if obj.get("type") == "event_msg":
        payload = obj.get("payload")
        if isinstance(payload, dict):
            for key in ("message", "last_agent_message"):
                if isinstance(payload.get(key), str):
                    cleaned = sanitize_visible_output(payload[key])
                    if cleaned != payload[key]:
                        payload[key] = cleaned
                        changed += 1
    return changed


def sanitize_file(path, in_place=False):
    path = Path(path)
    changed_fields = 0
    changed_lines = 0
    output_lines = []
    for raw_line in path.read_text(errors="replace").splitlines():
        try:
            obj = json.loads(raw_line)
        except json.JSONDecodeError:
            output_lines.append(raw_line)
            continue
        changed = sanitize_event(obj)
        if changed:
            changed_fields += changed
            changed_lines += 1
            output_lines.append(json.dumps(obj, separators=(",", ":"), ensure_ascii=False))
        else:
            output_lines.append(raw_line)
    backup = None
    if in_place and changed_fields:
        backup = path.with_suffix(path.suffix + f".bak-prefix-sanitize-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}")
        shutil.copy2(path, backup)
        path.write_text("\n".join(output_lines) + "\n")
    return {"path": str(path), "changedFields": changed_fields, "changedLines": changed_lines, "backup": str(backup) if backup else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_jsonl", help="Codex session JSONL file")
    parser.add_argument("--in-place", action="store_true", help="rewrite the file after creating a timestamped backup")
    args = parser.parse_args()
    print(json.dumps(sanitize_file(args.session_jsonl, in_place=args.in_place), indent=2))


if __name__ == "__main__":
    main()
