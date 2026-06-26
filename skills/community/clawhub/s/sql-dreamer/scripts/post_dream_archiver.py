"""
scripts/post_dream_archiver.py — Post-dream output archiver

Runs AFTER the OpenClaw dream cycle (e.g., 4:00 AM when dream runs at 3:30 AM).

What it does:
1. Reads memory/dreaming/light/YYYY-MM-DD.md — parses light sleep candidates
2. Reads memory/dreaming/rem/YYYY-MM-DD.md — parses REM themes + lasting truths
3. Reads memory/dreaming/deep/YYYY-MM-DD.md — parses deep sleep promotions
4. Inserts structured rows into dreams.DreamLight, DreamREM, DreamDeep
5. Deletes dream output .md files older than archive_after_days

Usage:
    python scripts/post_dream_archiver.py
    python scripts/post_dream_archiver.py --date 2026-04-25  # Archive specific date
    python scripts/post_dream_archiver.py --config /path/to/config.yml
    python scripts/post_dream_archiver.py --dry-run
"""

import sys
import os
import re
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
from src.sql_connector import SQLDreamerConnector


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def parse_light_file(content: str) -> list[dict]:
    """
    Parse memory/dreaming/light/YYYY-MM-DD.md into structured entries.

    Format:
        - Candidate: <snippet>
          - confidence: 0.62
          - evidence: memory/2026-04-25.md:3-3
          - recalls: 0
          - status: staged
    """
    entries = []
    current = None
    for line in content.splitlines():
        if line.startswith("- Candidate:"):
            if current:
                entries.append(current)
            snippet = line[len("- Candidate:"):].strip()
            current = {"snippet": snippet, "confidence": None, "evidence": "", "recalls": 0, "status": "staged"}
        elif current and "- confidence:" in line:
            try:
                current["confidence"] = float(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif current and "- evidence:" in line:
            current["evidence"] = line.split(":", 1)[1].strip()
        elif current and "- recalls:" in line:
            try:
                current["recalls"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif current and "- status:" in line:
            current["status"] = line.split(":", 1)[1].strip()

    if current:
        entries.append(current)

    # Generate stable keys from evidence path
    for e in entries:
        e["key"] = e.get("evidence", "") or e["snippet"][:80]

    return entries


def parse_rem_file(content: str) -> tuple[list[dict], list[str]]:
    """
    Parse memory/dreaming/rem/YYYY-MM-DD.md.
    Returns (themes, lasting_truths).
    """
    themes = []
    lasting_truths = []
    in_truths = False

    for line in content.splitlines():
        if "### Possible Lasting Truths" in line:
            in_truths = True
            continue
        if "### Reflections" in line:
            in_truths = False
            continue

        if not in_truths and line.startswith("- Theme:"):
            theme_text = re.sub(r"^- Theme:\s*`([^`]+)`.*$", r"\1", line).strip()
            freq_match = re.search(r"across (\d+) memories", line)
            conf_match = re.search(r"confidence: ([0-9.]+)", "\n".join([line]))
            themes.append({
                "theme": theme_text,
                "frequency": int(freq_match.group(1)) if freq_match else 0,
                "confidence": float(conf_match.group(1)) if conf_match else None,
                "evidence": "",
            })
        elif in_truths and line.startswith("- ") and len(line) > 3:
            lasting_truths.append(line[2:].strip())

    return themes, lasting_truths


def parse_deep_file(content: str) -> list[dict]:
    """
    Parse memory/dreaming/deep/YYYY-MM-DD.md into promotion records.
    """
    promotions = []
    ranked = re.findall(r"Ranked (\d+) candidate", content)
    promoted = re.findall(r"Promoted (\d+) candidate", content)

    # Basic record of the deep sleep run
    promotions.append({
        "key": "deep_sleep_summary",
        "snippet": content.strip()[:500],
        "score": None,
        "recallCount": int(ranked[0]) if ranked else 0,
        "uniqueQueries": 0,
        "promoted": int(promoted[0]) > 0 if promoted else False,
    })
    return promotions


def archive_date(conn: SQLDreamerConnector, date_str: str, workspace_dir: Path, dry_run: bool) -> None:
    """Archive dream outputs for a specific date."""
    dreaming_dir = workspace_dir / "memory" / "dreaming"

    for phase in ("light", "rem", "deep"):
        path = dreaming_dir / phase / f"{date_str}.md"
        if not path.exists():
            print(f"  ⚠️  {phase}/{date_str}.md not found — skipping")
            continue

        content = path.read_text(encoding="utf-8")
        print(f"  📄 Parsing {phase}/{date_str}.md ({len(content)} chars)")

        if dry_run:
            print(f"     [dry-run] would insert to dreams.Dream{phase.capitalize()}")
            continue

        if phase == "light":
            entries = parse_light_file(content)
            if entries:
                conn.write_dream_light(date_str, entries)
                print(f"  ✅ Inserted {len(entries)} light entries")
        elif phase == "rem":
            themes, truths = parse_rem_file(content)
            if themes or truths:
                conn.write_dream_rem(date_str, themes, truths)
                print(f"  ✅ Inserted {len(themes)} themes, {len(truths)} lasting truths")
        elif phase == "deep":
            promotions = parse_deep_file(content)
            if promotions:
                conn.write_dream_deep(date_str, promotions)
                print(f"  ✅ Inserted {len(promotions)} deep records")


def cleanup_old_files(workspace_dir: Path, archive_after_days: int, dry_run: bool) -> None:
    """Delete dream output files older than archive_after_days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=archive_after_days)
    dreaming_dir = workspace_dir / "memory" / "dreaming"
    deleted = 0

    for phase_dir in dreaming_dir.iterdir():
        if not phase_dir.is_dir():
            continue
        for f in phase_dir.glob("*.md"):
            match = re.match(r"^(\d{4}-\d{2}-\d{2})\.md$", f.name)
            if not match:
                continue
            file_date = datetime.fromisoformat(match.group(1)).replace(tzinfo=timezone.utc)
            if file_date < cutoff:
                if dry_run:
                    print(f"  [dry-run] would delete: {f}")
                else:
                    f.unlink()
                    print(f"  🗑️  Deleted: {f}")
                deleted += 1

    if deleted == 0:
        print(f"  ✅ No files older than {archive_after_days} days to clean up")
    else:
        print(f"  ✅ Cleaned up {deleted} old dream files")


def run(config_path: str, target_date: str = None, dry_run: bool = False) -> None:
    cfg = load_config(config_path)
    workspace_dir = Path(cfg["dreaming"]["workspace_dir"])
    archive_after_days = cfg["dreaming"].get("archive_after_days", 7)

    date_str = target_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"post_dream_archiver: {date_str}")
    print(f"  Workspace: {workspace_dir}")
    print(f"  Archive after: {archive_after_days} days")
    if dry_run:
        print("  MODE: dry-run")

    with SQLDreamerConnector.from_config(config_path) as conn:
        print("\n--- Archiving dream outputs ---")
        archive_date(conn, date_str, workspace_dir, dry_run)

        print("\n--- Cleaning up old files ---")
        cleanup_old_files(workspace_dir, archive_after_days, dry_run)

    print("\n✅ post_dream_archiver complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post-dream output archiver")
    parser.add_argument("--config", default="config/config.yml")
    parser.add_argument("--date", default=None, help="Date to archive (YYYY-MM-DD), defaults to today")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run(args.config, target_date=args.date, dry_run=args.dry_run)
