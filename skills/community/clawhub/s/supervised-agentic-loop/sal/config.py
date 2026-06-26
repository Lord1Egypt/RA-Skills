"""Configuration schema for supervised-agentic-loop."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from sal.metric_extractor import get_parser


@dataclass
class EvolveConfig:
    """All settings for a single evolution run.

    Attributes:
        target_file: The single file the agent modifies (like train.py).
        metric_command: Shell command to run (e.g. "pytest -q", "python train.py").
        metric_parser: Named strategy OR regex for extracting a float from output.
        minimize: True → lower is better (loss, BPB). False → higher is better (accuracy).
        time_budget: Max seconds per experiment iteration.
        max_iterations: Total iteration budget.
        plateau_patience: Stop after N iterations without improvement.
        run_tag: Git branch tag (auto-generated if empty).
        readonly_files: Files the agent must NOT modify.
        council_size: Number of LLM reviewers for optional council review.
        work_dir: Working directory (defaults to cwd).
    """

    target_file: str
    metric_command: str
    metric_parser: str
    minimize: bool = True
    time_budget: int = 300
    max_iterations: int = 100
    plateau_patience: int = 5
    run_tag: str = ""
    readonly_files: list[str] = field(default_factory=list)
    council_size: int = 3
    work_dir: str = "."

    def __post_init__(self) -> None:
        """Validate configuration after creation."""
        # Auto-generate run_tag from timestamp
        if not self.run_tag:
            self.run_tag = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Validate target_file exists
        target = Path(self.work_dir) / self.target_file
        if not target.exists():
            raise FileNotFoundError(
                f"target_file '{self.target_file}' not found in '{self.work_dir}'"
            )

        # Validate metric_parser resolves
        get_parser(self.metric_parser)

        # Validate numeric bounds
        if self.time_budget <= 0:
            raise ValueError(f"time_budget must be > 0, got {self.time_budget}")
        if self.max_iterations <= 0:
            raise ValueError(f"max_iterations must be > 0, got {self.max_iterations}")
        if self.plateau_patience <= 0:
            raise ValueError(
                f"plateau_patience must be > 0, got {self.plateau_patience}"
            )

        # Ensure target_file is not in readonly_files
        if self.target_file in self.readonly_files:
            raise ValueError(
                f"target_file '{self.target_file}' cannot be in readonly_files"
            )
