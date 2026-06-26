import csv
import logging
import random
import tempfile
from pathlib import Path

from bot.ig_config import CSV_PATH

logger = logging.getLogger(__name__)

INDEX_TO_LETTER = {0: "A", 1: "B", 2: "C", 3: "D"}
MAX_QUESTION_LENGTH = 200


def _read_csv(path: Path = CSV_PATH) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_csv(rows: list[dict], path: Path = CSV_PATH) -> None:
    if not rows:
        return
    seen = set()
    fieldnames = []
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".csv", dir=path.parent)
    try:
        with open(tmp_fd, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        Path(tmp_path).replace(path)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def _normalize_row(row: dict) -> dict:
    if "option_a" in row:
        return row
    return {
        "question": row["question"],
        "option_a": row.get("option1", ""),
        "option_b": row.get("option2", ""),
        "option_c": row.get("option3", ""),
        "option_d": row.get("option4", ""),
        "answer": INDEX_TO_LETTER.get(int(row.get("correctIndex", 0)), "A"),
        "category": row.get("subject", row.get("category", "General")),
        "year": row.get("year", ""),
        "explanation": row.get("explanation", ""),
        "posted": row.get("posted", "no"),
    }


def _options_balanced(normalized: dict, tolerance: float = 0.20) -> bool:
    lengths = [
        len(normalized["option_a"]),
        len(normalized["option_b"]),
        len(normalized["option_c"]),
        len(normalized["option_d"]),
    ]
    avg = sum(lengths) / 4
    if avg == 0:
        return False
    return all(abs(l - avg) / avg <= tolerance for l in lengths)


def get_next_question(path: Path = CSV_PATH) -> tuple[int, dict] | None:
    rows = _read_csv(path)

    # Build list of unposted question indices
    unposted_indices = []
    for i, row in enumerate(rows):
        posted = row.get("posted", "no").strip().lower()
        if posted in ("no", ""):
            normalized = _normalize_row(row)
            if len(normalized["question"]) > MAX_QUESTION_LENGTH:
                logger.debug("Skipping question %d: too long (%d chars)", i, len(normalized["question"]))
                continue
            if not _options_balanced(normalized):
                logger.debug("Skipping question %d: options not balanced", i)
                continue
            unposted_indices.append(i)

    if not unposted_indices:
        logger.warning("No unposted questions remaining in %s", path)
        return None

    # Pick a random unposted question
    random_index = random.choice(unposted_indices)
    normalized = _normalize_row(rows[random_index])
    logger.info("Selected random question %d: %s", random_index, normalized["question"][:60])
    return random_index, normalized


def mark_as_posted(index: int, path: Path = CSV_PATH) -> None:
    rows = _read_csv(path)
    if 0 <= index < len(rows):
        rows[index]["posted"] = "yes"
        _write_csv(rows, path)
        logger.info("Marked question %d as posted", index)
    else:
        logger.error("Invalid question index: %d", index)


def get_unposted_count(path: Path = CSV_PATH) -> int:
    rows = _read_csv(path)
    return sum(
        1 for r in rows if r.get("posted", "no").strip().lower() in ("no", "")
    )
