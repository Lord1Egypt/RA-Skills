"""TSV-based experiment logging.

Inspired by autoresearch results.tsv — a flat-file experiment log
that is human-readable, git-diffable, and easy to parse.
"""

import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


COLUMNS = [
    "iteration",
    "commit",
    "metric_value",
    "memory_mb",
    "status",
    "hypothesis",
    "duration_s",
    "reputation",
]


@dataclass
class ResultEntry:
    """A single experiment result row."""

    iteration: int
    commit: str
    metric_value: float
    memory_mb: int
    status: str  # "keep" | "discard" | "crash" | "error"
    hypothesis: str
    duration_s: float
    reputation: float


class ResultsLog:
    """TSV experiment log — append-only, human-readable.

    File format:
        iteration\\tcommit\\tmetric_value\\tmemory_mb\\tstatus\\thypothesis\\tduration_s\\treputation
        0\\ta1b2c3d\\t0.9979\\t44000\\tkeep\\tbaseline\\t305\\t0.500
        1\\tb2c3d4e\\t0.9932\\t44200\\tkeep\\tincrease LR\\t310\\t0.650
    """

    def __init__(self, path: str | Path = "results.tsv") -> None:
        self.path = Path(path)
        self._ensure_header()

    def _ensure_header(self) -> None:
        """Create file with header if it doesn't exist."""
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w", newline="") as f:
                writer = csv.writer(f, delimiter="\t")
                writer.writerow(COLUMNS)

    def log(
        self,
        iteration: int,
        commit: str = "",
        metric_value: float = 0.0,
        memory_mb: int = 0,
        status: str = "keep",
        hypothesis: str = "",
        duration_s: float = 0.0,
        reputation: float = 0.0,
        error: Optional[str] = None,
    ) -> None:
        """Append a result row to the TSV.

        Args:
            iteration: Iteration number (0 = baseline).
            commit: Short git SHA.
            metric_value: Parsed metric from experiment.
            memory_mb: Peak memory usage (0 if unknown).
            status: One of "keep", "discard", "crash", "error".
            hypothesis: What was tried this iteration.
            duration_s: Wall-clock seconds.
            reputation: Current reputation score after update.
            error: Optional error message (appended to hypothesis).
        """
        if error:
            hypothesis = f"{hypothesis} [ERROR: {error}]" if hypothesis else error

        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow([
                iteration,
                commit,
                f"{metric_value:.6f}",
                memory_mb,
                status,
                hypothesis.replace("\t", " ").replace("\n", " "),
                f"{duration_s:.1f}",
                f"{reputation:.3f}",
            ])

    @property
    def history(self) -> list[dict]:
        """Read all entries as list of dicts for brainstorm consumption."""
        if not self.path.exists():
            return []

        entries: list[dict] = []
        with open(self.path, "r") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                try:
                    entries.append({
                        "iteration": int(row["iteration"]),
                        "commit": row.get("commit", ""),
                        "metric_value": float(row.get("metric_value", 0)),
                        "memory_mb": int(row.get("memory_mb", 0)),
                        "status": row.get("status", ""),
                        "hypothesis": row.get("hypothesis", ""),
                        "duration_s": float(row.get("duration_s", 0)),
                        "reputation": float(row.get("reputation", 0)),
                    })
                except (ValueError, KeyError):
                    continue

        return entries

    def best(self, minimize: bool = True) -> Optional[dict]:
        """Return the entry with the best metric value.

        Args:
            minimize: If True, lowest value wins. If False, highest wins.

        Returns:
            Best entry dict, or None if no entries with status "keep".
        """
        kept = [e for e in self.history if e["status"] == "keep"]
        if not kept:
            return None
        return min(kept, key=lambda e: e["metric_value"]) if minimize else max(
            kept, key=lambda e: e["metric_value"]
        )

    @property
    def count(self) -> int:
        """Number of logged entries."""
        return len(self.history)
