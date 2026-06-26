#!/usr/bin/env python3
"""Trim an oversized JSONL transcript: keep session header + synthetic compaction + recent exchanges.

Usage: trim.py <jsonl_file> <session_id> <gateway_name> <state_file> [keep_pairs [keep_full_pairs [min_archive_pairs [trim_full_threshold_pct [trim_max_kb]]]]]

- Writes a trimmed transcript in-place with:
  - Original session header
  - A synthetic compaction entry summarizing what was archived
  - The last `keep_pairs` user/assistant exchange pairs (default 10)
  - Full toolResult bodies preserved for the most recent `keep_full_pairs` assistant turns (default 2)
- If the retained pairs still exceed `trim_full_threshold_pct`% of `trim_max_kb`, all pairs are
  further stripped (tool args removed, thinking dropped) to minimize size.
- Archives the original as .pre-trim.<timestamp>

Exits 0 on success, 1 if nothing to do.
"""
import json, sys, os, shutil, hashlib
from datetime import datetime

def random_id():
    return hashlib.md5(os.urandom(8)).hexdigest()[:8]

def main():
    jsonl_file = sys.argv[1]
    session_id = sys.argv[2]
    gateway = sys.argv[3]
    state_file = sys.argv[4]
    keep_pairs = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    keep_full_pairs = int(sys.argv[6]) if len(sys.argv) > 6 else 2
    min_archive_pairs = int(sys.argv[7]) if len(sys.argv) > 7 else 5  # kept for backward compat; no longer blocks trim
    trim_full_threshold_pct = float(sys.argv[8]) if len(sys.argv) > 8 else 50.0
    trim_max_kb = int(sys.argv[9]) if len(sys.argv) > 9 else 250

    entries = []
    with open(jsonl_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try: entries.append(json.loads(line))
            except: continue

    if not entries: sys.exit(1)

    header = None
    content_entries = []
    for e in entries:
        if e.get("type") == "session":
            header = e
        else:
            content_entries.append(e)

    if not header:
        print(f"No session header in {jsonl_file}", file=sys.stderr)
        sys.exit(1)

    message_entries = []
    tool_result_entries = []
    other_entries = []
    for e in content_entries:
        if e.get("type") == "message":
            role = e.get("message", {}).get("role", "")
            if role in ("user", "assistant"):
                message_entries.append(e)
            elif role == "toolResult":
                tool_result_entries.append(e)
            else:
                other_entries.append(e)
        else:
            other_entries.append(e)

    # Build a map from toolCallId → entry index in tool_result_entries for fast lookup
    tool_result_map = {}
    for e in tool_result_entries:
        tcid = e.get("message", {}).get("toolCallId")
        if tcid:
            tool_result_map[tcid] = e

    total_user = sum(1 for e in message_entries if e.get("message", {}).get("role") == "user")
    if total_user < keep_pairs:
        print(f"Only {total_user} user messages (need {keep_pairs}) — proceeding with shallow trim (keep all)")

    user_count = 0
    cut_index = 0  # default: keep everything (shallow trim)
    if total_user >= keep_pairs:
        cut_index = len(message_entries)
        for i in range(len(message_entries) - 1, -1, -1):
            if message_entries[i].get("message", {}).get("role") == "user":
                user_count += 1
                if user_count >= keep_pairs:
                    cut_index = i
                    break

    kept_messages = message_entries[cut_index:]
    archived_messages = message_entries[:cut_index]

    # Identify toolCallIds referenced in kept vs archived messages
    def get_tool_call_ids(msgs):
        ids = set()
        for e in msgs:
            content = e.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue
            for b in content:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use" and b.get("id"):
                    ids.add(b["id"])
                elif b.get("type") == "toolCall" and b.get("id"):
                    ids.add(b["id"])
        return ids

    # Find the most recent N assistant turns (for full tool result preservation)
    recent_tool_ids = set()
    asst_count = 0
    for e in reversed(kept_messages):
        if e.get("message", {}).get("role") == "assistant":
            asst_count += 1
            if asst_count <= keep_full_pairs:
                recent_tool_ids.update(get_tool_call_ids([e]))

    kept_tool_ids = get_tool_call_ids(kept_messages)
    archived_tool_ids = get_tool_call_ids(archived_messages)

    if len(kept_messages) == 0:
        print(f"Would keep 0 messages — aborting trim")
        sys.exit(1)

    # Note: min_archive_pairs no longer blocks trim — session always gets trimmed if oversized.
    # (The check is kept as an informational log only.)
    if len(archived_messages) < min_archive_pairs:
        print(f"Only {len(archived_messages)} messages to archive — proceeding with shallow trim")

    # Build topic summary for compaction entry
    user_topics = []
    for e in archived_messages:
        if e.get("message", {}).get("role") != "user": continue
        content = e.get("message", {}).get("content", "")
        if isinstance(content, list):
            content = " ".join(c.get("text", "") for c in content if c.get("type") == "text")
        content = content.strip()
        if content and len(content) > 5:
            if len(content) > 200: content = content[:200] + "..."
            user_topics.append(content)

    # Build trimmed transcript
    trimmed = [header]

    summary_lines = [
        "## Archived Context", "",
        f"{len(archived_messages)} older messages were archived to memory files by transcript maintenance.",
        f"Key topics: {'; '.join(t[:80] for t in user_topics[:5])}{'...' if len(user_topics) > 5 else ''}",
        "", "Recent conversation continues below.",
    ]

    first_kept_id = kept_messages[0].get("id") if kept_messages else None
    last_parent = header.get("id", random_id())

    compaction_entry = {
        "type": "compaction",
        "id": random_id(),
        "parentId": last_parent,
        "timestamp": datetime.now(tz=__import__('datetime').timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "summary": "\n".join(summary_lines),
        "firstKeptEntryId": first_kept_id,
        "tokensBefore": 0,
    }
    trimmed.append(compaction_entry)

    def strip_assistant_entry(e):
        """For non-recent assistant turns: strip thinking blocks entirely,
        strip arguments from toolCall blocks (keep id + name only)."""
        import copy
        e = copy.deepcopy(e)
        msg = e["message"]
        content = msg.get("content", [])
        if not isinstance(content, list):
            return e  # String content — nothing to strip
        new_content = []
        for b in content:
            if not isinstance(b, dict):
                new_content.append(b)
                continue
            t = b.get("type", "")
            if t == "thinking":
                continue  # Drop entirely
            elif t == "toolCall":
                new_content.append({"type": "toolCall", "id": b["id"], "name": b["name"]})
            else:
                new_content.append(b)
        msg["content"] = new_content
        return e

    prev_id = compaction_entry["id"]
    for e in kept_messages:
        e["parentId"] = prev_id
        if "id" not in e: e["id"] = random_id()
        prev_id = e["id"]
        # Strip thinking + toolCall args from older assistant turns
        if (e.get("message", {}).get("role") == "assistant" and
                not get_tool_call_ids([e]).intersection(recent_tool_ids)):
            e = strip_assistant_entry(e)
        trimmed.append(e)

    def make_turn_summary_entry(asst_entry, results_for_turn, parent_id):
        """Collapse all toolResults for one assistant turn into a single synthetic entry.
        Format: 'exec ✓(0): first line | Read ✓(0) | exec ✗(1): error text'
        """
        parts = []
        for r in results_for_turn:
            msg = r.get("message", {})
            tool_name = msg.get("toolName", "tool")
            is_error = msg.get("isError", False)
            details = msg.get("details", {})
            exit_code = details.get("exitCode", "?")
            mark = "\u2713" if not is_error and exit_code in (0, "0", None, "?") else "\u2717"
            # Get first line of output
            text = ""
            raw_content = msg.get("content", [])
            if isinstance(raw_content, str):
                text = raw_content.strip()
            else:
                for b in raw_content:
                    if isinstance(b, dict) and b.get("type") == "text":
                        text = b["text"].strip()
                        break
            first_line = text.splitlines()[0][:100] if text else ""
            if first_line:
                parts.append(f"{tool_name} {mark}({exit_code}): {first_line}")
            else:
                parts.append(f"{tool_name} {mark}({exit_code})")

        summary_text = " | ".join(parts)
        asst_id = asst_entry.get("id", random_id())
        ts = asst_entry.get("timestamp",
            datetime.now(tz=__import__('datetime').timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"))
        return {
            "type": "message",
            "id": random_id(),
            "parentId": parent_id,
            "timestamp": ts,
            "message": {
                "role": "toolResult",
                "toolCallId": f"summary-{asst_id[:8]}",
                "toolName": "[tool summary]",
                "content": [{"type": "text", "text": summary_text}],
                "details": {"summarized": True, "count": len(results_for_turn)},
            }
        }

    # Build mapping: toolCallId → toolResult entry
    tcid_to_result = {}
    for e in tool_result_entries:
        tcid = e.get("message", {}).get("toolCallId")
        if tcid:
            tcid_to_result[tcid] = e

    # For kept messages, emit toolResults per assistant turn:
    # - Recent 2 turns: individual entries (full output)
    # - Older turns: single collapsed summary entry per turn
    # - Archived turns: dropped
    for asst_entry in kept_messages:
        if asst_entry.get("message", {}).get("role") != "assistant":
            continue
        turn_ids = get_tool_call_ids([asst_entry])
        if not turn_ids:
            continue
        turn_results = [tcid_to_result[tid] for tid in turn_ids if tid in tcid_to_result]
        if not turn_results:
            continue
        asst_id = asst_entry.get("id", "")
        if any(tid in recent_tool_ids for tid in turn_ids):
            # Recent turn: keep full individual entries
            trimmed.extend(turn_results)
        else:
            # Older turn: collapse to single summary entry
            summary_entry = make_turn_summary_entry(asst_entry, turn_results, asst_entry.get("id", random_id()))
            trimmed.append(summary_entry)

    kept_ids = {e.get("id") for e in kept_messages}
    for e in other_entries:
        if e.get("parentId") and e["parentId"] in kept_ids:
            trimmed.append(e)

    # Post-trim size check: if still over threshold, first strip all assistant turns,
    # then if STILL over threshold, drop all toolResult entries entirely.
    trimmed_size_kb = sum(len(json.dumps(e)) for e in trimmed) / 1024
    threshold_kb = trim_max_kb * (trim_full_threshold_pct / 100.0)
    if trimmed_size_kb > threshold_kb:
        print(f"Post-trim size {trimmed_size_kb:.0f}KB exceeds {trim_full_threshold_pct:.0f}% of limit "
              f"({threshold_kb:.0f}KB) — stripping all assistant pairs")
        stripped_trimmed = []
        for e in trimmed:
            if e.get("type") == "message" and e.get("message", {}).get("role") == "assistant":
                stripped_trimmed.append(strip_assistant_entry(e))
            else:
                stripped_trimmed.append(e)
        trimmed = stripped_trimmed
        new_size_kb = sum(len(json.dumps(e)) for e in trimmed) / 1024
        print(f"After assistant strip: {new_size_kb:.0f}KB")

        # Still over threshold — drop ALL toolResult entries
        if new_size_kb > threshold_kb:
            print(f"Still {new_size_kb:.0f}KB over threshold — dropping all toolResult entries")
            trimmed = [
                e for e in trimmed
                if not (e.get("type") == "message" and
                        e.get("message", {}).get("role") == "toolResult")
            ]
            new_size_kb = sum(len(json.dumps(e)) for e in trimmed) / 1024
            print(f"After toolResult drop: {new_size_kb:.0f}KB")

    # Archive original, write trimmed
    archive_path = f"{jsonl_file}.pre-trim.{datetime.now(tz=__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')}"
    shutil.move(jsonl_file, archive_path)

    with open(jsonl_file, "w") as f:
        for entry in trimmed:
            f.write(json.dumps(entry) + "\n")

    orig_kb = os.path.getsize(archive_path) // 1024
    new_kb = os.path.getsize(jsonl_file) // 1024
    print(f"Trimmed {session_id[:12]}: {orig_kb}KB → {new_kb}KB "
          f"({len(archived_messages)} archived, {len(kept_messages)} kept)")

if __name__ == "__main__":
    main()
