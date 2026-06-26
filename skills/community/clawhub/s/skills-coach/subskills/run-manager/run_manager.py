"""
Run Manager for Skills-Coach v2.3.1

Manages versioned run directories with metadata tracking and comparison capabilities.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class RunMetadata:
    """Metadata for a single optimization run."""
    run_id: str
    target_skill: str
    target_skill_version: str
    skills_coach_version: str
    config: Dict
    start_time: str
    end_time: Optional[str]
    duration_seconds: Optional[float]
    result: Optional[Dict]
    iterations: int
    tasks_generated: int
    variants_tested: int


class RunManager:
    """Manages versioned optimization runs."""

    def __init__(self, base_dir: str = "skills-coach-runs"):
        self.base_dir = Path(base_dir)
        self.current_run_dir: Optional[Path] = None
        self.current_metadata: Optional[RunMetadata] = None

    def create_run(
        self,
        target_skill_path: str,
        config: Dict
    ) -> Path:
        """
        Create a new timestamped run directory.

        Args:
            target_skill_path: Path to target skill
            config: Configuration dictionary

        Returns:
            Path to the new run directory
        """
        # Generate run ID with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        skill_name = Path(target_skill_path).name
        run_id = f"run_{timestamp}"

        # Create run directory structure
        run_dir = self.base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (run_dir / "tasks" / "train").mkdir(parents=True, exist_ok=True)
        (run_dir / "tasks" / "test").mkdir(parents=True, exist_ok=True)
        (run_dir / "optimization").mkdir(parents=True, exist_ok=True)
        (run_dir / "exec_results" / "original").mkdir(parents=True, exist_ok=True)
        (run_dir / "exec_results" / "optimized").mkdir(parents=True, exist_ok=True)

        # Initialize metadata
        self.current_metadata = RunMetadata(
            run_id=run_id,
            target_skill=skill_name,
            target_skill_version="unknown",
            skills_coach_version="1.2.0",
            config=config,
            start_time=datetime.now().isoformat(),
            end_time=None,
            duration_seconds=None,
            result=None,
            iterations=0,
            tasks_generated=0,
            variants_tested=0
        )

        # Save initial metadata
        self._save_metadata(run_dir)

        # Copy config to run directory
        with open(run_dir / "config.yaml", 'w') as f:
            import yaml
            yaml.dump(config, f, default_flow_style=False)

        # Update latest symlink
        latest_link = self.base_dir / "latest"
        if latest_link.exists() or latest_link.is_symlink():
            latest_link.unlink()
        latest_link.symlink_to(run_id)

        self.current_run_dir = run_dir
        print(f"✓ Created run directory: {run_dir}")

        return run_dir

    def update_metadata(self, **kwargs):
        """Update metadata fields."""
        if not self.current_metadata:
            raise RuntimeError("No active run")

        for key, value in kwargs.items():
            if hasattr(self.current_metadata, key):
                setattr(self.current_metadata, key, value)

        self._save_metadata(self.current_run_dir)

    def finalize_run(
        self,
        decision: str,
        baseline_score: float,
        final_score: float,
        improvement: float
    ):
        """
        Finalize the run with results.

        Args:
            decision: "RETAINED" or "DELETED"
            baseline_score: Original skill score
            final_score: Optimized skill score
            improvement: Score improvement
        """
        if not self.current_metadata:
            raise RuntimeError("No active run")

        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.current_metadata.start_time)
        duration = (end_time - start_time).total_seconds()

        self.current_metadata.end_time = end_time.isoformat()
        self.current_metadata.duration_seconds = duration
        self.current_metadata.result = {
            "decision": decision,
            "improvement": improvement,
            "baseline_score": baseline_score,
            "final_score": final_score
        }

        self._save_metadata(self.current_run_dir)

        print(f"✓ Finalized run: {self.current_metadata.run_id}")
        print(f"  Duration: {duration:.1f}s")
        print(f"  Decision: {decision}")
        print(f"  Improvement: {improvement:+.1%}")

    def _save_metadata(self, run_dir: Path):
        """Save metadata to JSON file."""
        metadata_path = run_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(asdict(self.current_metadata), f, indent=2)

    def get_run_dir(self, subpath: str = "") -> Path:
        """Get path within current run directory."""
        if not self.current_run_dir:
            raise RuntimeError("No active run")

        if subpath:
            return self.current_run_dir / subpath
        return self.current_run_dir

    def list_runs(self) -> List[Dict]:
        """List all runs with metadata."""
        if not self.base_dir.exists():
            return []

        runs = []
        for run_dir in sorted(self.base_dir.glob("run_*")):
            metadata_path = run_dir / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path) as f:
                    runs.append(json.load(f))

        return runs

    def compare_runs(self, run_ids: List[str]) -> Dict:
        """
        Compare multiple runs.

        Args:
            run_ids: List of run IDs to compare

        Returns:
            Comparison data dictionary
        """
        comparison = {
            "runs": [],
            "summary": {}
        }

        for run_id in run_ids:
            run_dir = self.base_dir / run_id
            metadata_path = run_dir / "metadata.json"

            if metadata_path.exists():
                with open(metadata_path) as f:
                    metadata = json.load(f)
                    comparison["runs"].append(metadata)

        # Calculate summary statistics
        if comparison["runs"]:
            improvements = [r["result"]["improvement"] for r in comparison["runs"] if r.get("result")]
            comparison["summary"] = {
                "total_runs": len(comparison["runs"]),
                "avg_improvement": sum(improvements) / len(improvements) if improvements else 0,
                "retained_count": sum(1 for r in comparison["runs"] if r.get("result", {}).get("decision") == "RETAINED"),
                "deleted_count": sum(1 for r in comparison["runs"] if r.get("result", {}).get("decision") == "DELETED")
            }

        return comparison

    def cleanup_old_runs(self, keep_latest: int = 10):
        """
        Remove old runs, keeping only the latest N.

        Args:
            keep_latest: Number of runs to keep
        """
        runs = sorted(self.base_dir.glob("run_*"), key=lambda p: p.name, reverse=True)

        for run_dir in runs[keep_latest:]:
            print(f"Removing old run: {run_dir.name}")
            shutil.rmtree(run_dir)

        print(f"✓ Kept {min(len(runs), keep_latest)} most recent runs")


def main():
    """Test the run manager."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python run_manager.py <command> [args]")
        print("Commands:")
        print("  list - List all runs")
        print("  compare <run_id1> <run_id2> ... - Compare runs")
        print("  cleanup [N] - Keep only N latest runs (default: 10)")
        return

    manager = RunManager()
    command = sys.argv[1]

    if command == "list":
        runs = manager.list_runs()
        print(f"\nFound {len(runs)} runs:\n")
        for run in runs:
            print(f"  {run['run_id']}")
            print(f"    Skill: {run['target_skill']}")
            print(f"    Duration: {run.get('duration_seconds', 0):.1f}s")
            if run.get('result'):
                print(f"    Decision: {run['result']['decision']}")
                print(f"    Improvement: {run['result']['improvement']:+.1%}")
            print()

    elif command == "compare":
        if len(sys.argv) < 3:
            print("Error: Specify run IDs to compare")
            return

        run_ids = sys.argv[2:]
        comparison = manager.compare_runs(run_ids)

        print(f"\nComparing {len(run_ids)} runs:\n")
        print(f"Summary:")
        print(f"  Total runs: {comparison['summary']['total_runs']}")
        print(f"  Avg improvement: {comparison['summary']['avg_improvement']:+.1%}")
        print(f"  Retained: {comparison['summary']['retained_count']}")
        print(f"  Deleted: {comparison['summary']['deleted_count']}")

    elif command == "cleanup":
        keep = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        manager.cleanup_old_runs(keep)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
