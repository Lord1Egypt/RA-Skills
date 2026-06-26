#!/usr/bin/env python3
"""
Training-Free GRPO Optimizer CLI

Command-line interface for running Training-Free GRPO optimization.
"""

import sys
import yaml
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from training_free_grpo_optimizer import TrainingFreeGRPOOptimizer


def load_training_tasks(tasks_dir: Path):
    """Load training tasks from directory."""
    tasks = []
    train_dir = tasks_dir / "train"

    if not train_dir.exists():
        print(f"ERROR: Training tasks directory not found: {train_dir}")
        return tasks

    for task_dir in sorted(train_dir.glob("task_*")):
        task_md = task_dir / "task.md"
        speccheck_md = task_dir / "speccheck.md"

        if task_md.exists() and speccheck_md.exists():
            with open(task_md, 'r', encoding='utf-8') as f:
                task_content = f.read()
            with open(speccheck_md, 'r', encoding='utf-8') as f:
                speccheck_content = f.read()

            tasks.append({
                "task_id": task_dir.name,
                "task_dir": task_dir,
                "task_content": task_content,
                "speccheck_content": speccheck_content
            })

    return tasks


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python training_free_grpo_optimizer.py <target-skill-path> <work-dir>")
        sys.exit(1)

    target_skill_path = Path(sys.argv[1]).resolve()
    work_dir = Path(sys.argv[2]).resolve()

    # Load config
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    config = {}
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

    # Get Training-Free GRPO config
    tf_grpo_config = config.get('training_free_grpo', {})

    # Initialize optimizer
    optimizer = TrainingFreeGRPOOptimizer(
        target_skill_path=str(target_skill_path),
        training_tasks_dir=str(work_dir / "tasks"),
        output_dir=str(target_skill_path),  # Save optimized version in place
        group_size=tf_grpo_config.get('group_size', 5),
        num_epochs=tf_grpo_config.get('num_epochs', 3),
        config=config
    )

    # Load original skill
    if not optimizer.load_original_skill():
        sys.exit(1)

    # Load training tasks
    training_tasks = load_training_tasks(work_dir / "tasks")

    if not training_tasks:
        print("ERROR: No training tasks found")
        sys.exit(1)

    print(f"✓ Loaded {len(training_tasks)} training tasks")

    # Run optimization
    try:
        results = optimizer.optimize(training_tasks)

        print("\n" + "="*60)
        print("Training-Free GRPO Complete")
        print("="*60)
        print(f"Baseline: {results['baseline_score']}")
        print(f"Final: {results['final_score']}")
        print(f"Improvement: +{results['improvement']}")

        sys.exit(0)

    except Exception as e:
        print(f"\nERROR: Optimization failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
