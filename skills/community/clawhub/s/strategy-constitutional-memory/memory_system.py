"""
Constitutional Memory — Strategy Lesson & Ban Management System
===============================================================
Maintains a living knowledge base of hard-earned lessons and banned
code patterns from past strategy iterations.

Core capabilities:
  1. Load lessons (load) — Read historical lessons
  2. Add lessons (add_lesson) — Extract from diagnosis reports
  3. Scan code (scan_code) — Detect constitutional violations
  4. Export context (get_context) — Generate LLM system prompt fragment
"""
import os
import json
import re
from datetime import datetime
from typing import List, Dict, Optional


# Severity ranking used for sorting (lower = more severe)
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

# Severity display labels for context output
SEVERITY_LABELS = {
    "critical": "[CRITICAL]",
    "high": "[HIGH]",
    "medium": "[MEDIUM]",
    "low": "[LOW]",
}


class ConstitutionalMemory:
    """Strategy generational memory repository."""

    # Default banned patterns — empty by default; users populate their own.
    BANNED_PATTERNS: List[str] = []

    def __init__(self, memory_dir: str):
        """
        Initialize the constitutional memory system.

        Args:
            memory_dir: Path to the directory where lessons.json and bans.json
                        will be stored.  Created automatically if it does not
                        exist.
        """
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)

        self.lessons_file = os.path.join(self.memory_dir, "lessons.json")
        self.bans_file = os.path.join(self.memory_dir, "bans.json")

        self.lessons: List[Dict] = []
        self.bans: List[str] = list(self.BANNED_PATTERNS)

        self._load()

    # ================================================================
    # Load / Save
    # ================================================================
    def _load(self):
        """Load lessons and bans from disk (if files exist)."""
        if os.path.exists(self.lessons_file):
            with open(self.lessons_file, encoding="utf-8") as f:
                self.lessons = json.load(f)

        if os.path.exists(self.bans_file):
            with open(self.bans_file, encoding="utf-8") as f:
                extra_bans = json.load(f)
                self.bans = list(set(self.bans + extra_bans))

    def _save(self):
        """Persist lessons and bans to disk."""
        with open(self.lessons_file, "w", encoding="utf-8") as f:
            json.dump(self.lessons, f, indent=2, ensure_ascii=False)
        with open(self.bans_file, "w", encoding="utf-8") as f:
            json.dump(self.bans, f, indent=2)

    # ================================================================
    # Add Lesson
    # ================================================================
    def add_lesson(
        self,
        strategy_name: str,
        category: str,
        description: str,
        evidence: str = "",
        severity: str = "high",
        new_ban: Optional[str] = None,
    ):
        """
        Record a single lesson learned from a strategy iteration.

        Args:
            strategy_name: Strategy identifier (e.g. "v3", "alpha_test").
            category:      Classification — e.g. drawdown, selection,
                           position_sizing, timing, survival_structure,
                           ml_failure, success.
            description:   Concise root-cause description.
            evidence:      Supporting data (e.g. "Max drawdown: 72%").
            severity:      One of critical / high / medium / low.
            new_ban:       Optional code pattern to add to the ban list.
        """
        lesson = {
            "id": len(self.lessons) + 1,
            "timestamp": datetime.now().isoformat(),
            "strategy": strategy_name,
            "category": category,
            "description": description,
            "evidence": evidence,
            "severity": severity,
        }
        self.lessons.append(lesson)

        if new_ban and new_ban not in self.bans:
            self.bans.append(new_ban)

        self._save()

    def add_ban(self, pattern: str):
        """
        Add a banned code pattern directly (without an associated lesson).

        Args:
            pattern: The code pattern string to prohibit.
        """
        if pattern and pattern not in self.bans:
            self.bans.append(pattern)
            self._save()

    def add_lesson_from_diagnosis(self, strategy_name: str, diagnosis_report: str):
        """
        Auto-extract lessons from a plain-text diagnosis report using keyword
        and regex matching.

        Detected conditions:
          - High drawdown (> 50%)
          - High zero/expiry rate (> 60%)
          - Negative overall ROI

        Patterns are matched in English first with Chinese fallbacks so the
        method works with both bilingual and English-only reports.

        Args:
            strategy_name:    Strategy identifier.
            diagnosis_report: Full text of the diagnosis / post-mortem report.
        """
        report_lower = diagnosis_report.lower()

        # -- Drawdown detection -----------------------------------------------
        if "drawdown" in report_lower or "\u56de\u64a4" in report_lower:
            dd_match = re.search(
                r"(?:max\s*)?drawdown[:\s]*(\d+\.?\d*)%",
                report_lower,
                re.IGNORECASE,
            )
            if not dd_match:
                # Chinese fallback: "最大回撤: XX%"
                dd_match = re.search(
                    r"\u6700\u5927?\u56de\u64a4[:\s]*(\d+\.?\d*)%", diagnosis_report
                )
            if dd_match:
                dd_val = float(dd_match.group(1))
                if dd_val > 50:
                    self.add_lesson(
                        strategy_name,
                        "drawdown",
                        (
                            f"Maximum drawdown reached {dd_val}% — "
                            f"severe capital management deficiency"
                        ),
                        evidence=f"Drawdown: {dd_val}%",
                        severity="critical",
                    )

        # -- Zero / expiry rate detection -------------------------------------
        if "zero" in report_lower or "expir" in report_lower or "\u5f52\u96f6" in report_lower:
            zero_match = re.search(
                r"(?:zero|expir\w*)\s*rate[:\s]*(\d+\.?\d*)%",
                report_lower,
                re.IGNORECASE,
            )
            if not zero_match:
                # Chinese fallback: "归零率: XX%"
                zero_match = re.search(
                    r"\u5f52\u96f6\u7387[:\s]*(\d+\.?\d*)%", diagnosis_report
                )
            if zero_match:
                zero_rate = float(zero_match.group(1))
                if zero_rate > 60:
                    self.add_lesson(
                        strategy_name,
                        "selection",
                        (
                            f"Zero/expiry rate {zero_rate}% exceeds 60% — "
                            f"selection quality is critically poor"
                        ),
                        evidence=f"Zero rate: {zero_rate}%",
                        severity="high",
                    )

        # -- Negative ROI detection -------------------------------------------
        roi_match = re.search(
            r"(?:overall\s*)?ROI[:\s]*-\d+\.?\d*%",
            diagnosis_report,
            re.IGNORECASE,
        )
        if not roi_match:
            # Chinese fallback: "整体 ROI: -XX%"
            roi_match = re.search(
                r"(?:\u6574\u4f53\s*)?ROI[:\s]*-\d+\.?\d*%",
                diagnosis_report,
                re.IGNORECASE,
            )
        if roi_match:
            self.add_lesson(
                strategy_name,
                "selection",
                (
                    f"Overall ROI is negative — strategy cannot cover "
                    f"decay costs ({roi_match.group(0).strip()})"
                ),
                evidence=roi_match.group(0).strip(),
                severity="critical",
            )

    # ================================================================
    # Code Scanning
    # ================================================================
    def scan_code(self, code: str) -> List[Dict]:
        """
        Scan source code for banned pattern violations.

        The scanner is case-insensitive, tracks multi-line strings (triple
        quotes), skips comment lines, and strips inline strings/comments
        before matching.

        Args:
            code: The full source code as a single string.

        Returns:
            A list of violation dicts, each containing:
              - pattern: the banned pattern that matched
              - line:    1-based line number
              - content: the stripped source line
        """
        violations: List[Dict] = []
        in_multiline_string = False

        for i, line in enumerate(code.split("\n"), 1):
            stripped = line.strip()

            # Track multi-line strings (triple quotes)
            triple_count = stripped.count('"""') + stripped.count("'''")
            if triple_count % 2 == 1:
                in_multiline_string = not in_multiline_string
            if in_multiline_string:
                continue

            # Skip comment lines
            if stripped.startswith("#"):
                continue

            # Strip inline strings and comments before matching
            code_part = self._strip_strings_and_comments(line)

            for ban in self.bans:
                if ban.lower() in code_part.lower():
                    violations.append(
                        {
                            "pattern": ban,
                            "line": i,
                            "content": stripped,
                        }
                    )
        return violations

    @staticmethod
    def _strip_strings_and_comments(line: str) -> str:
        """
        Remove inline string literals and trailing comments from a line,
        leaving only executable code for pattern matching.
        """
        # Remove string literals (single and double quoted, non-greedy)
        result = re.sub(r'"(?:[^"\\]|\\.)*"', '""', line)
        result = re.sub(r"'(?:[^'\\]|\\.)*'", "''", result)
        # Remove inline comment
        hash_idx = result.find("#")
        if hash_idx >= 0:
            result = result[:hash_idx]
        return result

    # ================================================================
    # Export LLM Context
    # ================================================================
    def get_context(self, max_lessons: int = 30) -> str:
        """
        Generate a formatted text block suitable for inclusion in an LLM
        system prompt.  Contains all lessons (sorted by severity) and
        banned patterns.

        Args:
            max_lessons: Maximum number of recent lessons to include.

        Returns:
            A multi-line string ready to be injected into a prompt.
        """
        lines: List[str] = []
        lines.append("=== CONSTITUTIONAL MEMORY ===")
        lines.append(
            f"Based on {len(self.lessons)} lessons from past iterations.\n"
        )

        # Sort by severity (most severe first)
        sorted_lessons = sorted(
            self.lessons[-max_lessons:],
            key=lambda x: SEVERITY_ORDER.get(x.get("severity", "medium"), 2),
        )

        for lesson in sorted_lessons:
            label = SEVERITY_LABELS.get(lesson["severity"], "[INFO]")
            lines.append(
                f"{label} [{lesson['strategy']}] {lesson['category']}: "
                f"{lesson['description']}"
            )
            if lesson.get("evidence"):
                lines.append(f"  Evidence: {lesson['evidence']}")

        lines.append(f"\n=== Banned Code Patterns ({len(self.bans)} total) ===")
        for ban in self.bans:
            lines.append(f"  X Prohibited: `{ban}`")

        return "\n".join(lines)

    # ================================================================
    # Seed Example Lessons (for documentation / onboarding only)
    # ================================================================
    def seed_from_examples(self):
        """
        Populate the memory with a handful of *generic* example lessons to
        illustrate the data format.  This is intended for onboarding and
        documentation purposes only — it will NOT overwrite existing data.

        The examples are deliberately generic and do not reference any
        specific project, ticker, or model.

        Call this once on a fresh memory directory to see how lessons
        and bans look in practice, then replace with your own data.
        """
        if len(self.lessons) > 0:
            return  # Already populated — do not overwrite.

        examples = [
            (
                "example_v1",
                "drawdown",
                "Periodic rebalancing during drawdowns created a sell-low-buy-high "
                "death spiral that compounded losses across three consecutive months.",
                "Max drawdown: 78%, triggered at 20% backtest progress",
                "critical",
                "periodic_rebalance",
            ),
            (
                "example_v2",
                "ml_failure",
                "ML-based signal filter compressed the trade count from 40 to 8, "
                "accidentally filtering out all winning trades while keeping losers.",
                "Sharpe dropped from 3.4 to 0.9; net profit -94 pp",
                "high",
                None,
            ),
            (
                "example_v3",
                "success",
                "Allocating a fixed safety cushion (buy-and-hold index) alongside "
                "the speculative book allowed the strategy to survive drawdown "
                "periods and eventually compound during a recovery rally.",
                "Full-period return: +328%, max drawdown: 40%",
                "medium",
                None,
            ),
        ]

        for strategy, category, desc, evidence, severity, ban in examples:
            self.add_lesson(strategy, category, desc, evidence, severity, ban)
