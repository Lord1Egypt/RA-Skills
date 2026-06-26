"""
SkillGuard — Pipeline Engine + Detector Registry
"""

from typing import Dict, List
from skillguard.detectors.base import BaseDetector, Finding, SkillContext, PipelineContext


class DetectorRegistry:
    """Registry of all available detectors."""

    _detectors: Dict[str, BaseDetector] = {}

    @classmethod
    def register(cls, detector: BaseDetector):
        cls._detectors[detector.name] = detector

    @classmethod
    def get(cls, name: str) -> BaseDetector:
        return cls._detectors.get(name)

    @classmethod
    def all(cls) -> List[BaseDetector]:
        return list(cls._detectors.values())

    @classmethod
    def names(cls) -> List[str]:
        return list(cls._detectors.keys())


class PipelineRunner:
    """Orchestrates the detection pipeline."""

    def __init__(self, detectors: List[BaseDetector] = None):
        self.detectors = detectors or list(DetectorRegistry.all())
        self._sort_by_priority()

    def _sort_by_priority(self):
        """Group detectors: infrastructure first, then AST-heavy, then cross-analysis."""
        priority = {
            "secret_exposure": 1, "dependency_audit": 1,
            "prompt_injection": 2, "sensitive_file_access": 2, "network_whitelist": 2,
            "code_execution": 3, "permission_analysis": 3,
            "memory_pollution": 4,
        }
        self.detectors.sort(key=lambda d: priority.get(d.name, 5))

    def run(self, skill_ctx: SkillContext) -> tuple[List[Finding], PipelineContext]:
        """Run all detectors. Individual failures don't stop the pipeline."""
        ctx = PipelineContext()
        ctx.skill_context = skill_ctx
        all_findings: List[Finding] = []

        for detector in self.detectors:
            try:
                findings = detector.analyze(skill_ctx, ctx)
                all_findings.extend(findings)
            except Exception as e:
                # Log failure but continue
                all_findings.append(Finding(
                    id=f"INTERNAL-{detector.name}",
                    detector="pipeline",
                    severity="LOW",
                    confidence=1.0,
                    title=f"Detector '{detector.name}' failed",
                    description=str(e),
                ))

        return all_findings, ctx

    def run_named(self, names: List[str], skill_ctx: SkillContext) -> tuple[List[Finding], PipelineContext]:
        """Run only named detectors."""
        selected = [d for d in self.detectors if d.name in names]
        runner = PipelineRunner(selected)
        return runner.run(skill_ctx)
