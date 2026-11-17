"""
Workflow registry for managing workflow definitions.
"""

from typing import Dict, List, Optional
from .models import WorkflowConfig, PhaseConfig, TransitionRule


class WorkflowRegistry:
    """Workflow registry for managing workflow definitions."""

    def __init__(self):
        self._workflows: Dict[str, WorkflowConfig] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register default workflow templates."""
        # Standard change workflow (8 phases)
        standard = WorkflowConfig(
            name="standard",
            description="Standard workflow for features, refactors, and medium/high-risk changes.",
            phases=[
                PhaseConfig(id="requirement", gate="requirement-gate", agent="requirement_agent", required_artifacts=["proposal.md"]),
                PhaseConfig(id="design", gate="design-gate", agent="design_agent", required_artifacts=["design.md", "tasks.md"]),
                PhaseConfig(id="development", gate="development-gate", agent="implementation_agent"),
                PhaseConfig(id="code_review", gate="code-review-gate", agent="code_review_agent", required_artifacts=["review_findings"]),
                PhaseConfig(id="test_planning", gate="test-planning-gate", agent="test_planner_agent", required_artifacts=["test_plan"]),
                PhaseConfig(id="testing", gate="testing-gate", agent="verification_agent", required_artifacts=["verification-report.md"]),
                PhaseConfig(id="reflection", gate="reflection-gate", agent="reflection_agent", required_artifacts=["retrospective.md"]),
                PhaseConfig(id="archive", gate="archive-gate", agent="archiver_agent"),
            ],
            transitions=[
                TransitionRule("requirement", "design", "proposal.md exists AND requirement-gate passed"),
                TransitionRule("design", "development", "design.md AND tasks.md exist AND design-gate passed"),
                TransitionRule("development", "code_review", "tasks implemented AND development-gate passed"),
                TransitionRule("code_review", "test_planning", "blocking_issues == 0 AND review_decision == 'approve'"),
                TransitionRule("test_planning", "testing", "test_plan exists AND test-planning-gate passed"),
                TransitionRule("testing", "reflection", "verification-report.md exists AND testing-gate passed"),
                TransitionRule("reflection", "archive", "retrospective.md exists AND reflection-gate passed"),
            ]
        )

        # Lightweight tweak workflow (4 phases)
        lightweight = WorkflowConfig(
            name="lightweight",
            description="Lightweight workflow for docs, prompts, and small config changes.",
            phases=[
                PhaseConfig(id="clarify", gate="requirement-gate"),
                PhaseConfig(id="update", gate="development-gate"),
                PhaseConfig(id="verify", gate="testing-gate"),
                PhaseConfig(id="archive", gate="archive-gate"),
            ],
            transitions=[
                TransitionRule("clarify", "update", "scope confirmed"),
                TransitionRule("update", "verify", "changes implemented"),
                TransitionRule("verify", "archive", "verification passed"),
            ]
        )

        # Hotfix workflow (5 phases)
        hotfix = WorkflowConfig(
            name="hotfix",
            description="Hotfix workflow that starts with diagnosis and requires regression verification.",
            phases=[
                PhaseConfig(id="diagnose", gate="requirement-gate", agent="requirement_agent"),
                PhaseConfig(id="fix", gate="development-gate", agent="implementation_agent"),
                PhaseConfig(id="regression_test", gate="testing-gate", agent="verification_agent"),
                PhaseConfig(id="reflection", gate="reflection-gate", agent="reflection_agent", required_artifacts=["retrospective.md"]),
                PhaseConfig(id="archive", gate="archive-gate", agent="archiver_agent"),
            ],
            transitions=[
                TransitionRule("diagnose", "fix", "proposal.md exists AND requirement-gate passed"),
                TransitionRule("fix", "regression_test", "fix implemented AND development-gate passed"),
                TransitionRule("regression_test", "reflection", "verification-report.md exists AND testing-gate passed"),
                TransitionRule("reflection", "archive", "retrospective.md exists AND reflection-gate passed"),
            ]
        )

        self._workflows["standard"] = standard
        self._workflows["lightweight"] = lightweight
        self._workflows["hotfix"] = hotfix

    def register_workflow(self, workflow_config: WorkflowConfig) -> None:
        """Register a workflow."""
        self._workflows[workflow_config.name] = workflow_config

    def get_workflow(self, workflow_name: str) -> Optional[WorkflowConfig]:
        """Get a workflow by name."""
        return self._workflows.get(workflow_name)

    def list_workflows(self) -> List[str]:
        """List all workflow names."""
        return list(self._workflows.keys())

    def validate_workflow(self, workflow_name: str) -> bool:
        """Validate a workflow exists."""
        return workflow_name in self._workflows