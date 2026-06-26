#!/usr/bin/env python3
"""
Failure Analyzer for Skills-Coach v2.3.1

Analyzes failed task executions to identify root causes and suggest fixes.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ErrorPattern:
    """Pattern for matching and categorizing errors."""
    category: str
    pattern: str
    description: str
    fix_suggestion: str
    confidence: float


@dataclass
class FailureAnalysis:
    """Analysis result for a failed task."""
    task_id: str
    error_category: str
    error_message: str
    root_cause: str
    fix_suggestion: str
    fix_difficulty: str  # easy, medium, hard
    affected_files: List[str]
    confidence: float


class FailureAnalyzer:
    """Analyzes task failures and suggests fixes."""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.error_patterns = self._init_error_patterns()

    def _init_error_patterns(self) -> List[ErrorPattern]:
        """Initialize error detection patterns."""
        return [
            ErrorPattern(
                category="missing_parameter",
                pattern=r"error: unrecognized arguments?: (.+)",
                description="Script does not support the specified parameter",
                fix_suggestion="Add parameter support to the script's argument parser",
                confidence=0.95
            ),
            ErrorPattern(
                category="missing_parameter",
                pattern=r"invalid choice: '(.+)'",
                description="Parameter value not in allowed choices",
                fix_suggestion="Add the value to the parameter's choices list",
                confidence=0.90
            ),
            ErrorPattern(
                category="missing_dependency",
                pattern=r"ModuleNotFoundError: No module named '(.+)'",
                description="Required Python module is not installed",
                fix_suggestion="Add module to requirements or install with pip",
                confidence=0.95
            ),
            ErrorPattern(
                category="missing_dependency",
                pattern=r"command not found: (.+)",
                description="Required command-line tool is not installed",
                fix_suggestion="Install the required tool or add to dependencies",
                confidence=0.95
            ),
            ErrorPattern(
                category="file_not_found",
                pattern=r"No such file or directory: '(.+)'",
                description="Required file does not exist",
                fix_suggestion="Check file path or create the required file",
                confidence=0.90
            ),
            ErrorPattern(
                category="file_not_found",
                pattern=r"FileNotFoundError: \[Errno 2\] (.+)",
                description="File path is incorrect or file is missing",
                fix_suggestion="Verify file paths in the skill configuration",
                confidence=0.90
            ),
            ErrorPattern(
                category="invalid_input",
                pattern=r"ValueError: (.+)",
                description="Input value is invalid or out of range",
                fix_suggestion="Add input validation and error handling",
                confidence=0.75
            ),
            ErrorPattern(
                category="timeout",
                pattern=r"TimeoutExpired|timed out",
                description="Command execution exceeded time limit",
                fix_suggestion="Optimize performance or increase timeout",
                confidence=0.85
            ),
            ErrorPattern(
                category="logic_error",
                pattern=r"AssertionError|RuntimeError",
                description="Logic error in code execution",
                fix_suggestion="Review and fix the code logic",
                confidence=0.70
            ),
        ]

    def analyze_failure(self, task_dir: Path) -> Optional[FailureAnalysis]:
        """Analyze a failed task and return detailed analysis."""
        run_log = task_dir / "run_log.md"

        if not run_log.exists():
            return None

        # Read the run log
        with open(run_log, 'r', encoding='utf-8') as f:
            log_content = f.read()

        # Extract error information
        error_message = self._extract_error_message(log_content)
        if not error_message:
            return None

        # Match against error patterns
        for pattern in self.error_patterns:
            match = re.search(pattern.pattern, error_message, re.IGNORECASE)
            if match:
                return self._create_analysis(
                    task_dir.name,
                    pattern,
                    error_message,
                    match
                )

        # Unknown error
        return FailureAnalysis(
            task_id=task_dir.name,
            error_category="unknown",
            error_message=error_message,
            root_cause="Unable to categorize error",
            fix_suggestion="Manual investigation required",
            fix_difficulty="hard",
            affected_files=[],
            confidence=0.5
        )

    def _extract_error_message(self, log_content: str) -> Optional[str]:
        """Extract error message from run log."""
        # Look for stderr section
        stderr_match = re.search(
            r'## Standard Error\s*```\s*(.+?)\s*```',
            log_content,
            re.DOTALL
        )

        if stderr_match:
            return stderr_match.group(1).strip()

        # Look for error status
        if "Status**: ERROR" in log_content:
            # Try to find any error-like text
            error_lines = [
                line for line in log_content.split('\n')
                if 'error' in line.lower() or 'failed' in line.lower()
            ]
            if error_lines:
                return '\n'.join(error_lines[:3])

        return None

    def _create_analysis(
        self,
        task_id: str,
        pattern: ErrorPattern,
        error_message: str,
        match: re.Match
    ) -> FailureAnalysis:
        """Create detailed failure analysis."""

        # Extract specific details from the match
        details = match.group(1) if match.lastindex else ""

        # Determine affected files based on error category
        affected_files = self._identify_affected_files(
            pattern.category,
            details
        )

        # Estimate fix difficulty
        difficulty = self._estimate_difficulty(pattern.category)

        # Generate specific fix suggestion
        fix_suggestion = self._generate_specific_fix(
            pattern,
            details
        )

        return FailureAnalysis(
            task_id=task_id,
            error_category=pattern.category,
            error_message=error_message[:200],  # Truncate long messages
            root_cause=f"{pattern.description}: {details}",
            fix_suggestion=fix_suggestion,
            fix_difficulty=difficulty,
            affected_files=affected_files,
            confidence=pattern.confidence
        )

    def _identify_affected_files(
        self,
        category: str,
        details: str
    ) -> List[str]:
        """Identify which files need to be modified."""
        if category == "missing_parameter":
            # Likely need to modify the script's argument parser
            return ["scripts/*.py"]
        elif category == "missing_dependency":
            return ["requirements.txt", "SKILL.md"]
        elif category == "file_not_found":
            return [details] if details else []
        else:
            return []

    def _estimate_difficulty(self, category: str) -> str:
        """Estimate fix difficulty."""
        difficulty_map = {
            "missing_parameter": "easy",
            "missing_dependency": "easy",
            "file_not_found": "medium",
            "invalid_input": "medium",
            "timeout": "hard",
            "logic_error": "hard",
        }
        return difficulty_map.get(category, "medium")

    def _generate_specific_fix(
        self,
        pattern: ErrorPattern,
        details: str
    ) -> str:
        """Generate specific fix suggestion based on error details."""
        if pattern.category == "missing_parameter":
            param_name = details.split()[0] if details else "PARAM"
            return (
                f"{pattern.fix_suggestion}\n\n"
                f"Example code:\n"
                f"```python\n"
                f"parser.add_argument(\n"
                f"    '{param_name}',\n"
                f"    help='Description of {param_name}'\n"
                f")\n"
                f"```"
            )
        elif pattern.category == "missing_dependency":
            module_name = details
            return (
                f"{pattern.fix_suggestion}\n\n"
                f"Run: pip3 install {module_name}\n"
                f"Or add to requirements.txt: {module_name}"
            )
        else:
            return pattern.fix_suggestion

    def analyze_all_failures(
        self,
        exec_results_dir: Path
    ) -> List[FailureAnalysis]:
        """Analyze all failed tasks in the execution results."""
        analyses = []

        for task_dir in sorted(exec_results_dir.glob("task_*")):
            analysis = self.analyze_failure(task_dir)
            if analysis:
                analyses.append(analysis)

        return analyses

    def generate_report(
        self,
        analyses: List[FailureAnalysis]
    ) -> str:
        """Generate a detailed failure analysis report."""
        if not analyses:
            return "No failures to analyze."

        report = ["# Failure Analysis Report\n"]

        # Group by category
        by_category = {}
        for analysis in analyses:
            category = analysis.error_category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(analysis)

        # Report by category
        for category, items in sorted(by_category.items()):
            report.append(f"\n## {category.replace('_', ' ').title()}\n")
            report.append(f"**Count:** {len(items)} task(s)\n")

            for analysis in items:
                report.append(f"\n### {analysis.task_id}\n")
                report.append(f"**Root Cause:** {analysis.root_cause}\n\n")
                report.append(f"**Fix Suggestion ({analysis.fix_difficulty}):**\n")
                report.append(f"{analysis.fix_suggestion}\n")

                if analysis.affected_files:
                    report.append(f"\n**Affected Files:** {', '.join(analysis.affected_files)}\n")

                report.append(f"\n**Confidence:** {analysis.confidence:.0%}\n")

        return '\n'.join(report)


def main():
    """CLI entry point."""
    import sys
    import yaml

    if len(sys.argv) < 2:
        print("Usage: python failure_analyzer.py <exec_results_dir> [work_dir]")
        sys.exit(1)

    exec_results_dir = Path(sys.argv[1])
    work_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()

    # Load config
    config_path = work_dir / "config.yaml"
    config = {}
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f).get('failure_analysis', {})

    # Analyze failures
    analyzer = FailureAnalyzer(config)
    analyses = analyzer.analyze_all_failures(exec_results_dir)

    # Generate report
    report = analyzer.generate_report(analyses)

    # Save report
    report_path = work_dir / "failure_analysis.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Failure analysis saved to {report_path}")
    print(f"  Analyzed {len(analyses)} failed task(s)")

    # Also save JSON for programmatic use
    json_path = work_dir / "failure_analysis.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump([asdict(a) for a in analyses], f, indent=2)


if __name__ == "__main__":
    main()
