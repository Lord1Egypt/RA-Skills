"""
Main retrospective analyzer.
"""

import json
import os
import threading
import uuid
from typing import Dict, List

from .models import (
    AnalysisResult,
    GateFriction,
    ImprovementCandidate,
    ProjectInfo,
    Retrospective,
    RetrospectiveReport,
    RetroStatus,
)


class RetrospectiveAnalyzer:
    """Analyzer that drives the retrospective lifecycle.

    Tracks retrospectives in memory, analyzes friction and failures,
    generates improvement candidates, and supports JSON persistence.
    """

    def __init__(self) -> None:
        self._retros: Dict[str, Retrospective] = {}
        self._analyses: Dict[str, AnalysisResult] = {}
        self._reports: Dict[str, RetrospectiveReport] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Retrospective lifecycle
    # ------------------------------------------------------------------ #
    def start_retrospective(self, project_info: ProjectInfo) -> Retrospective:
        """Start a new retrospective and return it."""
        retro_id = str(uuid.uuid4())
        retro = Retrospective(id=retro_id, project_info=project_info)
        with self._lock:
            self._retros[retro_id] = retro
        return retro

    def get_retrospective(self, retro_id: str) -> Retrospective:
        """Return the retrospective for the given id."""
        with self._lock:
            retro = self._retros.get(retro_id)
        if retro is None:
            raise KeyError(f"Retrospective '{retro_id}' not found")
        return retro

    def list_retrospectives(self) -> List[str]:
        """Return all retrospective ids."""
        with self._lock:
            return list(self._retros.keys())

    def archive(self, retro_id: str) -> None:
        """Archive a retrospective."""
        retro = self.get_retrospective(retro_id)
        retro.status = RetroStatus.ARCHIVED

    # ------------------------------------------------------------------ #
    # Adding entries
    # ------------------------------------------------------------------ #
    def _get_retro(self, retro_id: str) -> Retrospective:
        with self._lock:
            retro = self._retros.get(retro_id)
        if retro is None:
            raise KeyError(f"Retrospective '{retro_id}' not found")
        return retro

    @staticmethod
    def _validate_item(item: str) -> None:
        if item is None or not isinstance(item, str) or not item.strip():
            raise ValueError("item cannot be empty")

    def add_what_went_well(self, retro_id: str, item: str) -> None:
        """Record something that went well."""
        self._validate_item(item)
        retro = self._get_retro(retro_id)
        with self._lock:
            retro.what_went_well.append(item)

    def add_what_was_slow(self, retro_id: str, item: str) -> None:
        """Record something that was slow or redundant."""
        self._validate_item(item)
        retro = self._get_retro(retro_id)
        with self._lock:
            retro.what_was_slow.append(item)

    def add_what_failed(self, retro_id: str, item: str) -> None:
        """Record something that failed or caused rework."""
        self._validate_item(item)
        retro = self._get_retro(retro_id)
        with self._lock:
            retro.what_failed.append(item)

    def add_gate_friction(self, retro_id: str, friction: GateFriction) -> None:
        """Record gate friction."""
        if not isinstance(friction, GateFriction):
            raise TypeError("friction must be a GateFriction")
        retro = self._get_retro(retro_id)
        with self._lock:
            retro.gate_frictions.append(friction)

    # ------------------------------------------------------------------ #
    # Analysis
    # ------------------------------------------------------------------ #
    def _generate_candidates(self, retro: Retrospective) -> List[ImprovementCandidate]:
        candidates: List[ImprovementCandidate] = []
        for friction in retro.gate_frictions:
            impact_lower = friction.impact.lower()
            if "block" in impact_lower or "critical" in impact_lower:
                priority = "high"
            elif "minor" in impact_lower or "low" in impact_lower:
                priority = "low"
            else:
                priority = "medium"
            candidates.append(
                ImprovementCandidate(
                    target=friction.gate,
                    recommendation=friction.suggested_change,
                    reason=friction.impact,
                    priority=priority,
                )
            )
        for fail in retro.what_failed:
            candidates.append(
                ImprovementCandidate(
                    target="process",
                    recommendation=f"Address failure: {fail}",
                    reason="Recorded failure during retrospective",
                    priority="high",
                )
            )
        for slow in retro.what_was_slow:
            candidates.append(
                ImprovementCandidate(
                    target="process",
                    recommendation=f"Optimize slow step: {slow}",
                    reason="Recorded slowness during retrospective",
                    priority="medium",
                )
            )
        return candidates

    @staticmethod
    def _severity_for(total_issues: int) -> str:
        if total_issues == 0:
            return "low"
        if total_issues < 5:
            return "medium"
        if total_issues < 10:
            return "high"
        return "critical"

    def analyze(self, retro_id: str) -> AnalysisResult:
        """Analyze a retrospective and return the analysis result."""
        retro = self.get_retrospective(retro_id)
        total_issues = (
            len(retro.what_was_slow) + len(retro.what_failed) + len(retro.gate_frictions)
        )
        friction_points = len(retro.gate_frictions)
        candidates = self._generate_candidates(retro)
        severity = self._severity_for(total_issues)
        summary = (
            f"Found {total_issues} issues with {friction_points} gate frictions. "
            f"Severity: {severity}."
        )
        result = AnalysisResult(
            total_issues=total_issues,
            friction_points=friction_points,
            improvement_candidates=candidates,
            summary=summary,
            severity=severity,
        )
        with self._lock:
            self._analyses[retro_id] = result
            retro.status = RetroStatus.ANALYZED
        return result

    def get_improvement_candidates(self, retro_id: str) -> List[ImprovementCandidate]:
        """Return improvement candidates, analyzing if needed."""
        with self._lock:
            cached = self._analyses.get(retro_id)
        if cached is not None:
            return list(cached.improvement_candidates)
        analysis = self.analyze(retro_id)
        return list(analysis.improvement_candidates)

    def generate_report(self, retro_id: str) -> RetrospectiveReport:
        """Generate a retrospective report."""
        retro = self.get_retrospective(retro_id)
        with self._lock:
            analysis = self._analyses.get(retro_id)
        if analysis is None:
            analysis = self.analyze(retro_id)
        recommendations = [c.recommendation for c in analysis.improvement_candidates]
        action_items = [
            f"[{c.priority}] {c.target}: {c.recommendation}"
            for c in analysis.improvement_candidates
        ]
        report = RetrospectiveReport(
            retro_id=retro_id,
            project_info=retro.project_info,
            analysis=analysis,
            recommendations=recommendations,
            action_items=action_items,
        )
        with self._lock:
            self._reports[retro_id] = report
            retro.status = RetroStatus.REPORTED
        return report

    def get_report(self, retro_id: str) -> RetrospectiveReport:
        """Return a previously generated report."""
        with self._lock:
            report = self._reports.get(retro_id)
        if report is None:
            raise KeyError(f"Report for '{retro_id}' not found")
        return report

    # ------------------------------------------------------------------ #
    # Persistence
    # ------------------------------------------------------------------ #
    def save_to_file(self, retro_id: str, path: str) -> None:
        """Persist a retrospective to a JSON file."""
        retro = self.get_retrospective(retro_id)
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(retro.to_dict(), f, ensure_ascii=False, indent=2)

    def load_from_file(self, path: str) -> Retrospective:
        """Load a retrospective from a JSON file and register it."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        retro = Retrospective.from_dict(data)
        with self._lock:
            self._retros[retro.id] = retro
        return retro

    def export_report(self, retro_id: str, path: str) -> None:
        """Export a generated report to a JSON file."""
        report = self.get_report(retro_id)
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
