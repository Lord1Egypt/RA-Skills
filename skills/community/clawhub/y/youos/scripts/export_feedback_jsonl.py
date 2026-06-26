"""Export feedback pairs to JSONL for MLX chat fine-tuning."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import yaml

from app.core.settings import get_settings
from app.db.bootstrap import resolve_sqlite_path

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT_DIR / "data" / "feedback"
CONFIGS_DIR = ROOT_DIR / "configs"

# Above this many qualified pairs, skip the O(n^2) near-duplicate dedup — it
# would otherwise stall fine-tuning for many minutes on a large organic corpus.
DEDUP_MAX_PAIRS = 2000


def parse_args() -> argparse.Namespace:
    # Same shape as scripts/finetune_lora.py: defaults resolved at call time
    # so YOUOS_DATA_DIR set on the calling shell (e.g. the nightly under
    # launchd) lands the export's DB read on the active instance.
    default_db = resolve_sqlite_path(get_settings().database_url)
    p = argparse.ArgumentParser(description="Export feedback pairs to JSONL")
    p.add_argument("--all", action="store_true", help="Export all pairs, not just unused")
    p.add_argument("--since", type=str, default=None, help="Only pairs created after this date (YYYY-MM-DD)")
    p.add_argument("--output", type=str, default=None, help="Output file path (default: data/feedback/train.jsonl)")
    p.add_argument("--min-rating", type=int, default=3, help="Minimum rating to include (default: 3)")
    p.add_argument("--min-edit-pct", type=float, default=0.05, help="Minimum edit distance pct (default: 0.05)")
    p.add_argument("--db", type=str, default=str(default_db), help="Database path")
    p.add_argument("--no-persona", action="store_true", help="Use bare format without persona/system prompt")
    p.add_argument("--configs-dir", type=str, default=str(CONFIGS_DIR), help="Configs directory")
    p.add_argument("--dpo", action="store_true", help="Export DPO preference pairs (chosen/rejected)")
    p.add_argument("--curriculum", action=argparse.BooleanOptionalAction, default=True, help="Sort first 20%% by quality (curriculum learning)")
    p.add_argument("--no-dedup", action="store_true", help="Disable near-duplicate deduplication")
    p.add_argument(
        "--persona",
        type=str,
        default=None,
        help=(
            "Filter to one sender_type cohort for per-persona fine-tuning "
            "(e.g. --persona internal). Omit to export all cohorts mixed "
            "together for the global adapter. Used by Phase 2 of the "
            "per-persona adapters work."
        ),
    )
    return p.parse_args()


def _load_persona(configs_dir: Path) -> dict:
    path = configs_dir / "persona.yaml"
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_prompts(configs_dir: Path) -> dict:
    path = configs_dir / "prompts.yaml"
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _build_system_message(persona: dict, prompts: dict) -> str:
    """Build a system message combining system_prompt and persona preamble."""
    system_prompt = prompts.get("system_prompt", "You are YouOS, a local-first personal email copilot.").strip()

    style = persona.get("style", {})
    voice = style.get("voice")
    avg_words = style.get("avg_reply_words")
    greeting_patterns = persona.get("greeting_patterns", {})
    closing_patterns = persona.get("closing_patterns", {})

    preamble_parts: list[str] = []
    if voice:
        preamble_parts.append(f"Voice style: {voice}.")
    if avg_words:
        preamble_parts.append(f"Target reply length: ~{avg_words} words.")
    if greeting_patterns:
        greetings = ", ".join(f"{k}: {v}" for k, v in greeting_patterns.items() if k != "default")
        if greetings:
            preamble_parts.append(f"Greeting patterns: {greetings}.")
    if closing_patterns:
        closings = ", ".join(f"{k}: {v}" for k, v in closing_patterns.items() if k != "default")
        if closings:
            preamble_parts.append(f"Closing patterns: {closings}.")

    if preamble_parts:
        return system_prompt + "\n\n" + "\n".join(preamble_parts)
    return system_prompt


def build_record(
    inbound: str,
    edited_reply: str,
    *,
    system_message: str | None = None,
) -> dict:
    """Build a JSONL record with optional system message."""
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": inbound})
    messages.append({"role": "assistant", "content": edited_reply})
    return {"messages": messages}


def export_dpo(args: argparse.Namespace) -> None:
    """Export DPO preference pairs: chosen (rating >= 4) vs rejected (rating <= 2)."""
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        chosen_rows = conn.execute("SELECT inbound_text, edited_reply, rating FROM feedback_pairs WHERE rating >= 4 AND LENGTH(edited_reply) >= 15").fetchall()
        rejected_rows = conn.execute(
            "SELECT inbound_text, edited_reply, rating FROM feedback_pairs WHERE rating <= 2 AND LENGTH(edited_reply) >= 15"
        ).fetchall()
    finally:
        conn.close()

    if not chosen_rows or not rejected_rows:
        print(f"Not enough DPO pairs: {len(chosen_rows)} chosen, {len(rejected_rows)} rejected")
        return

    pairs: list[dict] = []
    used_rejected: set[int] = set()

    for chosen in chosen_rows:
        c_len = len(chosen["inbound_text"] or "")
        if c_len == 0:
            continue
        for j, rejected in enumerate(rejected_rows):
            if j in used_rejected:
                continue
            r_len = len(rejected["inbound_text"] or "")
            if r_len == 0:
                continue
            # Match by similar inbound length (within 50%)
            ratio = min(c_len, r_len) / max(c_len, r_len)
            if ratio >= 0.5:
                pairs.append(
                    {
                        "prompt": chosen["inbound_text"],
                        "chosen": chosen["edited_reply"],
                        "rejected": rejected["edited_reply"],
                    }
                )
                used_rejected.add(j)
                break

    if not pairs:
        print("No DPO pairs could be matched.")
        return

    output_path = ROOT_DIR / "data" / "dpo_train.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"Exported {len(pairs)} DPO pairs to {output_path}")


def deduplicate_pairs(
    qualified: list[tuple[str, str, str, float]],
    threshold: float = 0.95,
) -> tuple[list[tuple[str, str, str, float]], int]:
    """Deduplicate pairs by inbound text similarity.

    If two pairs have hybrid_similarity >= threshold on their inbound text,
    keep only the one with higher quality score (or more recent if tied).
    Returns (deduped list, number removed).
    """
    from app.core.diff import hybrid_similarity

    if len(qualified) <= 1:
        return qualified, 0

    # O(n^2) hybrid_similarity over every pair — fine for a review-queue-sized
    # set, pathological for a large organic corpus (tens of thousands of pairs),
    # where it runs for many minutes and stalls the wizard's / nightly's
    # fine-tune. Above the cap the marginal cleanup isn't worth the cost.
    if len(qualified) > DEDUP_MAX_PAIRS:
        return qualified, 0

    keep = list(qualified)
    removed = 0
    i = 0
    while i < len(keep):
        j = i + 1
        while j < len(keep):
            sim = hybrid_similarity(keep[i][1], keep[j][1])  # compare inbound texts
            if sim >= threshold:
                # Keep the one with higher quality; if tied, keep more recent (later in list)
                q_i, q_j = keep[i][3], keep[j][3]
                if q_j > q_i:
                    keep.pop(i)
                else:
                    keep.pop(j)
                removed += 1
                continue  # don't increment j since we removed an element
            j += 1
        i += 1
    return keep, removed


def _is_low_signal_pair(inbound: str, edited_reply: str) -> bool:
    """Return True when pair carries little learning signal for fine-tuning.

    Keep this conservative: only filter obvious acknowledgement / phatic exchanges.
    """
    import re

    low_signal_reply = re.compile(
        r"^\s*(ok|okay|k|sure|thanks|thank you|thx|ty|noted|got it|sounds good|perfect|great|hello|hi)\s*[.!]?\s*$",
        re.IGNORECASE,
    )

    inbound_text = (inbound or "").strip()
    reply_text = (edited_reply or "").strip()

    inbound_words = inbound_text.split()
    reply_words = reply_text.split()

    # Empty/tiny responses are generally poor supervision targets.
    if not reply_words:
        return True
    if low_signal_reply.match(reply_text):
        return True

    # Very short back-and-forths usually add little style signal.
    if len(inbound_words) <= 2 and len(reply_words) <= 2:
        return True

    return False


def export(args: argparse.Namespace) -> None:
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return

    configs_dir = Path(args.configs_dir)

    # Build system message from persona + prompts (unless --no-persona)
    system_message = None
    if not args.no_persona:
        persona = _load_persona(configs_dir)
        prompts = _load_prompts(configs_dir)
        system_message = _build_system_message(persona, prompts)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        # `organic` pairs are real sent replies with no YouOS draft (see
        # extract_auto_feedback.py). Detect the column so older DBs that predate
        # it still export; absent → treated as non-organic (0).
        cols = {r[1] for r in conn.execute("PRAGMA table_info(feedback_pairs)")}
        organic_select = "COALESCE(organic, 0) as organic" if "organic" in cols else "0 as organic"
        query = (
            "SELECT inbound_text, edited_reply, rating, edit_distance_pct, created_at, "
            f"{organic_select}, COALESCE(rating, 3) as quality_score "
            "FROM feedback_pairs WHERE 1=1"
        )
        params: list = []

        # `used_in_finetune` is a global flag — it gates the incremental
        # global-adapter loop ("don't retrain on data the global already saw").
        # Per-persona training should use the *entire* cohort every time
        # (each persona's adapter is smallish and retrains from scratch), so
        # `--persona` implicitly bypasses this filter. Otherwise the first
        # persona to train would steal pairs from the global / other personas.
        # ``getattr`` since some legacy callers (tests, direct invocations)
        # build a Namespace without the new attribute.
        persona_filter = getattr(args, "persona", None)
        if not args.all and not persona_filter:
            query += " AND used_in_finetune = 0"

        if args.since:
            query += " AND created_at >= ?"
            params.append(args.since)

        if persona_filter:
            # Filter to one sender_type cohort. We explicitly do NOT include
            # NULL-sender_type rows here — those are pre-Phase-1 historical
            # rows that haven't been backfilled, and we'd rather have a smaller
            # honest cohort than dilute it with un-classifiable data.
            query += " AND sender_type = ?"
            params.append(persona_filter.strip().lower())

        rows = conn.execute(query, params).fetchall()
    finally:
        conn.close()

    if not rows:
        print("No matching feedback pairs found. Exported 0 pairs.")
        return

    # Quality filters
    min_rating = args.min_rating
    min_edit_pct = args.min_edit_pct
    qualified: list[tuple[str, str, str]] = []
    filtered_count = 0
    null_rating_count = 0

    for row in rows:
        rating = row["rating"]
        edit_pct = row["edit_distance_pct"]
        edited_reply = row["edited_reply"] or ""
        organic = row["organic"]

        # Exclude pairs with short edited replies
        if len(edited_reply) < 15:
            filtered_count += 1
            continue

        # E20: quality gate — drop low-signal acknowledgement-only pairs
        if _is_low_signal_pair(row["inbound_text"] or "", edited_reply):
            filtered_count += 1
            continue

        # Handle null rating: include with warning
        if rating is None:
            null_rating_count += 1
        elif rating < min_rating:
            filtered_count += 1
            continue

        # Exclude pairs with low edit + not 5-star (no signal). The edit-distance
        # floor only makes sense for review-queue pairs, where a YouOS draft
        # existed to diff against. Organic pairs (real sent replies, no draft)
        # have edit_distance_pct=0 by construction — applying the floor would
        # discard the entire historical corpus, so a fresh user's first
        # fine-tune would see "No qualifying pairs". Exempt them.
        if not organic and edit_pct is not None and edit_pct < min_edit_pct and (rating is None or rating < 5):
            filtered_count += 1
            continue

        quality = row["quality_score"] if "quality_score" in row.keys() else (rating or 3)
        qualified.append((row["created_at"] or "", row["inbound_text"], edited_reply, quality))

    if null_rating_count > 0:
        print(f"Warning: {null_rating_count} pairs have null rating (included)")

    if not qualified:
        print(f"No qualifying pairs after filtering. Filtered out {filtered_count} low-quality pairs.")
        return

    # E15: oversample 5-star recent pairs (last 90 days) 2-3x for stronger training signal
    from datetime import datetime, timedelta
    from datetime import timezone as _tz
    cutoff_90d = (datetime.now(_tz.utc) - timedelta(days=90)).isoformat()[:10]
    oversampled: list[tuple[str, str, str, float]] = []
    for item in qualified:
        created_at, inbound, reply, quality = item
        is_recent = (created_at or "")[:10] >= cutoff_90d
        rating_approx = int(round(quality))
        if rating_approx >= 5 and is_recent:
            oversampled.extend([item, item, item])  # 3x
        elif rating_approx >= 4 and is_recent:
            oversampled.extend([item, item])  # 2x
        else:
            oversampled.append(item)
    if len(oversampled) > len(qualified):
        print(f"E15 oversampling: {len(qualified)} -> {len(oversampled)} pairs (5-star/recent boosted)")
    qualified = oversampled

    print(f"Exported {len(qualified)} pairs (filtered out {filtered_count} low-quality pairs)")

    # Deduplication by inbound similarity (before temporal split)
    if not getattr(args, "no_dedup", False):
        if len(qualified) > DEDUP_MAX_PAIRS:
            print(f"Skipping near-duplicate dedup ({len(qualified)} pairs > {DEDUP_MAX_PAIRS} cap — O(n^2) too slow)")
        else:
            qualified, dedup_count = deduplicate_pairs(qualified)
            if dedup_count:
                print(f"Deduped {dedup_count} near-duplicate training pairs")

    # Temporal split: sort by created_at ASC, most recent 15% as validation
    qualified.sort(key=lambda x: x[0])

    # Curriculum learning: sort first 20% by quality_score ASC (warmup on easier examples)
    curriculum_applied = False
    warmup_count = 0
    if getattr(args, "curriculum", True):
        warmup_count = max(1, int(len(qualified) * 0.2))
        warmup = sorted(qualified[:warmup_count], key=lambda x: x[3])  # sort by quality ASC
        remainder = qualified[warmup_count:]
        qualified = warmup + remainder
        curriculum_applied = True
        print(f"Curriculum learning: warmup on first {warmup_count} easiest examples")

    records = [build_record(inbound, reply, system_message=system_message) for _, inbound, reply, _q in qualified]

    # Prepend curriculum metadata line if applicable
    if curriculum_applied:
        meta_line = {"_curriculum": True, "warmup_count": warmup_count, "total": len(records)}
        records.insert(0, meta_line)

    val_count = max(1, min(20, int(len(records) * 0.15)))
    if len(records) <= 1:
        train = records
        valid = []
    else:
        train = records[:-val_count]
        valid = records[-val_count:]

    print(f"Train: {len(train)} pairs | Val: {len(valid)} pairs (temporal split, val = most recent 15%)")

    # Determine output paths
    if args.output:
        train_path = Path(args.output)
        valid_path = train_path.parent / "valid.jsonl"
    else:
        output_dir = DEFAULT_OUTPUT_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        train_path = output_dir / "train.jsonl"
        valid_path = output_dir / "valid.jsonl"

    train_path.parent.mkdir(parents=True, exist_ok=True)

    with open(train_path, "w", encoding="utf-8") as f:
        for rec in train:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    with open(valid_path, "w", encoding="utf-8") as f:
        for rec in valid:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Exported {len(records)} pairs to {train_path}")
    print(f"  Train: {len(train)} pairs -> {train_path}")
    print(f"  Valid: {len(valid)} pairs -> {valid_path}")


def main() -> None:
    args = parse_args()
    if args.dpo:
        export_dpo(args)
    else:
        export(args)


if __name__ == "__main__":
    main()
