"""Persistent learning log.

Inspired by self-improving-agent's .learnings/ directory with
structured LRN/ERR entries and recurring pattern detection.
"""

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class LearningsLog:
    """Structured learning log persisted as markdown.

    File structure:
        .state/learnings/
        ├── learnings.md    # Successful experiment insights
        └── errors.md       # Failed experiment patterns

    Each entry uses the self-improving-agent format for cross-tool compatibility.
    """

    def __init__(self, state_dir: str | Path = ".state/learnings") -> None:
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.learnings_path = self.state_dir / "learnings.md"
        self.errors_path = self.state_dir / "errors.md"

        # Ensure files exist with headers
        if not self.learnings_path.exists():
            self.learnings_path.write_text("# Experiment Learnings\n\n")
        if not self.errors_path.exists():
            self.errors_path.write_text("# Experiment Errors\n\n")

    def _next_id(self, prefix: str, path: Path) -> str:
        """Generate next sequential ID (e.g. LRN-20250319-001)."""
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        content = path.read_text() if path.exists() else ""
        pattern = rf"{prefix}-{date_str}-(\d{{3}})"
        matches = re.findall(pattern, content)
        next_num = max((int(m) for m in matches), default=0) + 1
        return f"{prefix}-{date_str}-{next_num:03d}"

    def log_learning(
        self,
        iteration: int,
        hypothesis: str,
        metric_before: float,
        metric_after: float,
        status: str,
        area: str = "model",
        details: str = "",
    ) -> str:
        """Log a successful experiment insight.

        Args:
            iteration: Iteration number.
            hypothesis: What was tried.
            metric_before: Metric value before this iteration.
            metric_after: Metric value after this iteration.
            status: "keep" or "discard".
            area: Category (model, optimizer, data, hyperparams).
            details: Additional context.

        Returns:
            Entry ID (e.g. "LRN-20250319-001").
        """
        entry_id = self._next_id("LRN", self.learnings_path)
        timestamp = datetime.now(timezone.utc).isoformat()
        delta = metric_after - metric_before
        direction = "↓" if delta < 0 else "↑" if delta > 0 else "→"

        entry = f"""## [{entry_id}] {area}

**Logged**: {timestamp}
**Iteration**: {iteration}
**Status**: {status}
**Metric**: {metric_before:.6f} {direction} {metric_after:.6f} (Δ {delta:+.6f})

### Hypothesis
{hypothesis}

### Result
{"✅ Improvement — changes kept." if status == "keep" else "❌ No improvement — changes discarded."}

{f"### Details{chr(10)}{details}" if details else ""}

---

"""
        self.learnings_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.learnings_path.exists():
            self.learnings_path.write_text("# Experiment Learnings\n\n")
        with open(self.learnings_path, "a") as f:
            f.write(entry)

        return entry_id

    def log_error(
        self,
        iteration: int,
        error_msg: str,
        hypothesis: str = "",
        area: str = "runtime",
    ) -> str:
        """Log an experiment error/crash.

        Returns:
            Entry ID (e.g. "ERR-20250319-001").
        """
        entry_id = self._next_id("ERR", self.errors_path)
        timestamp = datetime.now(timezone.utc).isoformat()

        entry = f"""## [{entry_id}] {area}

**Logged**: {timestamp}
**Iteration**: {iteration}
**Priority**: high
**Status**: pending

### Summary
Experiment crashed during iteration {iteration}.

### Error
```
{error_msg}
```

### Context
Hypothesis: {hypothesis or "N/A"}

---

"""
        self.errors_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.errors_path.exists():
            self.errors_path.write_text("# Experiment Errors\n\n")
        with open(self.errors_path, "a") as f:
            f.write(entry)

        return entry_id

    def get_patterns(self) -> dict:
        """Analyze learnings for recurring patterns.

        Returns a dict with:
            - successful_areas: Areas where "keep" entries concentrate.
            - failed_areas: Areas where "discard" entries concentrate.
            - error_count: Total error entries.
            - recurring_errors: Error messages that appear > 1 time.
            - successful_hypotheses: Hypotheses that led to "keep".
            - failed_hypotheses: Hypotheses that led to "discard".

        This is the 🟡 Pattern-Algorithm (Dr. Neuron finding), made concrete:
        We parse the structured markdown entries and aggregate by area and status.
        """
        patterns: dict = {
            "successful_areas": {},
            "failed_areas": {},
            "error_count": 0,
            "recurring_errors": [],
            "successful_hypotheses": [],
            "failed_hypotheses": [],
        }

        # Parse learnings
        if not self.learnings_path.exists():
            return patterns
        content = self.learnings_path.read_text()
        entries = content.split("\n## [")[1:]  # Skip header

        for entry in entries:
            status_match = re.search(r"\*\*Status\*\*:\s*(\w+)", entry)
            area_match = re.search(r"^\w+-\d+-\d+\]\s*(\w+)", entry)
            hypothesis_match = re.search(
                r"### Hypothesis\n(.+?)(?:\n###|\n---)", entry, re.DOTALL
            )

            status = status_match.group(1) if status_match else ""
            area = area_match.group(1) if area_match else "unknown"
            hypothesis = (
                hypothesis_match.group(1).strip() if hypothesis_match else ""
            )

            if status == "keep":
                patterns["successful_areas"][area] = (
                    patterns["successful_areas"].get(area, 0) + 1
                )
                if hypothesis:
                    patterns["successful_hypotheses"].append(hypothesis)
            elif status == "discard":
                patterns["failed_areas"][area] = (
                    patterns["failed_areas"].get(area, 0) + 1
                )
                if hypothesis:
                    patterns["failed_hypotheses"].append(hypothesis)

        # Parse errors
        if not self.errors_path.exists():
            return patterns
        error_content = self.errors_path.read_text()
        error_entries = error_content.split("\n## [")[1:]
        patterns["error_count"] = len(error_entries)

        # Find recurring error messages
        error_msgs: list[str] = []
        for entry in error_entries:
            msg_match = re.search(r"```\n(.+?)\n```", entry, re.DOTALL)
            if msg_match:
                error_msgs.append(msg_match.group(1).strip()[:100])  # First 100 chars

        # Count occurrences
        from collections import Counter

        msg_counts = Counter(error_msgs)
        patterns["recurring_errors"] = [
            {"error": msg, "count": count}
            for msg, count in msg_counts.items()
            if count > 1
        ]

        return patterns

    def get_summary(self) -> str:
        """One-line summary of learning state."""
        patterns = self.get_patterns()
        keeps = sum(patterns["successful_areas"].values())
        discards = sum(patterns["failed_areas"].values())
        errors = patterns["error_count"]
        return f"Learnings: {keeps} keeps, {discards} discards, {errors} errors"
