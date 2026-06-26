from __future__ import annotations

from pathlib import Path

from .config import Config
from .detectors import DetectorContext, build_detector_registry
from .filesystem import read_text_candidate
from .models import Finding, MatchCandidate, ScanReport


class ScanEngine:
    def __init__(self, repo_root: Path, config: Config) -> None:
        self.repo_root = repo_root
        self.config = config
        self.detectors = build_detector_registry(
            DetectorContext(repo_root=repo_root, home_dir=Path.home())
        )

    def scan_paths(self, paths: list[Path], scope: str) -> ScanReport:
        findings: list[Finding] = []
        files_scanned = 0
        files_skipped = 0

        for path in paths:
            relative_path = str(path.relative_to(self.repo_root))
            if self.config.is_path_excluded(relative_path):
                continue

            text = read_text_candidate(path)
            if text is None:
                files_skipped += 1
                continue

            files_scanned += 1
            findings.extend(self.scan_text(relative_path, text))

        findings.sort(key=lambda finding: (finding.path, finding.line, finding.column, finding.detector_id))
        return ScanReport(
            root=self.repo_root,
            scope=scope,
            files_scanned=files_scanned,
            files_skipped=files_skipped,
            findings=findings,
        )

    def scan_text(self, relative_path: str, text: str) -> list[Finding]:
        candidates: list[MatchCandidate] = []
        for detector in self.detectors:
            if self.config.is_detector_ignored(detector.detector_id):
                continue
            severity = self.config.severity_for(detector.detector_id, detector.severity)
            candidates.extend(detector.find_matches(text, self.config.placeholders, severity))

        selected = self._select_non_overlapping(
            [
                candidate
                for candidate in candidates
                if not self.config.is_allowed(relative_path, candidate.matched_text)
            ]
        )
        return [self._candidate_to_finding(relative_path, text, candidate) for candidate in selected]

    def _select_non_overlapping(self, candidates: list[MatchCandidate]) -> list[MatchCandidate]:
        accepted: list[MatchCandidate] = []
        for candidate in sorted(
            candidates,
            key=lambda item: (-item.priority, item.start_offset, -(item.end_offset - item.start_offset)),
        ):
            if any(_overlaps(candidate, existing) for existing in accepted):
                continue
            accepted.append(candidate)
        return sorted(accepted, key=lambda item: (item.start_offset, item.end_offset))

    def _candidate_to_finding(self, relative_path: str, text: str, candidate: MatchCandidate) -> Finding:
        line = text.count("\n", 0, candidate.start_offset) + 1
        last_newline = text.rfind("\n", 0, candidate.start_offset)
        column = candidate.start_offset + 1 if last_newline == -1 else candidate.start_offset - last_newline
        return Finding(
            path=relative_path,
            line=line,
            column=column,
            detector_id=candidate.detector_id,
            title=candidate.title,
            category=candidate.category,
            severity=candidate.severity,
            message=candidate.message,
            preview=candidate.preview,
            replacement_text=candidate.replacement_text,
            editable_in_place=candidate.editable_in_place,
            review_required=candidate.review_required,
            start_offset=candidate.start_offset,
            end_offset=candidate.end_offset,
        )


def _overlaps(left: MatchCandidate, right: MatchCandidate) -> bool:
    return left.start_offset < right.end_offset and right.start_offset < left.end_offset
