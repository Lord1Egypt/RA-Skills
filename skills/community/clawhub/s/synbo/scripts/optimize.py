#!/usr/bin/env python3
"""
Optimize script for SynBO reaction optimization.

This script demonstrates how to run Bayesian optimization with previous
reaction data to recommend new experimental conditions.

Usage:
    python optimize.py --project-dir examples
"""

import argparse
import json
from pathlib import Path

from synbo import ReactionOptimizer
from synbo.utils import load_desc_dict, get_prev_rxn


def load_optimization_settings(project_dir: Path):
    """Load optimization settings from config.json and optimization_settings.json."""
    # Read config.json to get project_wd

    # Read optimization_settings.json
    opt_settings_path = Path(project_dir) / "optimization_settings.json"
    if not opt_settings_path.exists():
        raise FileNotFoundError(
            f"optimization_settings.json not found at {opt_settings_path}. " "Please define optimization metrics first."
        )

    with open(opt_settings_path, "r") as f:
        settings = json.load(f)

    reagent_types = settings.get("reagent_types")
    opt_metrics = settings.get("opt_metrics")
    opt_direct_info = settings.get("opt_direct_info")

    assert reagent_types is not None, "reagent_types must be defined in optimization_settings.json"
    assert opt_metrics is not None, "opt_metrics must be defined in optimization_settings.json"
    assert opt_direct_info is not None, "opt_direct_info must be defined in optimization_settings.json"

    if not opt_metrics:
        raise ValueError("No optimization metrics found in optimization_settings.json")

    return reagent_types, opt_metrics, opt_direct_info


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run Bayesian optimization with previous reaction data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        required=True,
        help="Project directory containing configuration files",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default="results",
        help="Directory containing previous reaction data. Relative to --project-dir (default: results)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default="results",
        help="Output directory for results. Relative to --project-dir (default: results)",
    )
    parser.add_argument(
        "--name-suffix",
        nargs="+",
        default="_RDKit",
        help="Name suffixes for descriptor files",
    )
    parser.add_argument(
        "--index-col",
        default="name",
        help="Index column for descriptor files (default: 'name')",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of new conditions to recommend",
    )
    parser.add_argument(
        "--desc-normalize",
        default="zscore",
        choices=["minmax", "zscore", "l2"],
        help="Descriptor normalization method (default: zscore)",
    )
    parser.add_argument(
        "--optimize-method",
        default="default_BO",
        help="Optimization algorithm to use (default: default_BO)",
    )
    parser.add_argument(
        "--accuracy",
        default="medium",
        choices=["tiny", "low", "medium", "high", "ultra"],
        help="Optimization accuracy level. Lower values are faster and use less memory (default: medium)",
    )
    parser.add_argument(
        "--acq-func",
        default="EHVI",
        choices=["EHVI", "UCB", "ParEGO", "NEI"],
        help="Acquisition function to use for Bayesian optimization (default: EHVI)",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output",
    )

    return parser.parse_args()


def main() -> int:
    """Main function to run optimization workflow."""
    args = parse_arguments()

    name_suffix = [s if s != "None" else None for s in args.name_suffix]

    # Load optimization settings from configuration files
    print("Step 1: Loading optimization settings...")
    print("-" * 60)
    try:
        reagent_types, opt_metrics, opt_direct_info = load_optimization_settings(args.project_dir)
        name_suffix = [args.name_suffix] * len(reagent_types) if isinstance(args.name_suffix, str) else args.name_suffix
        print(f"✓ Loaded reagent types: {reagent_types}")
        print(f"✓ Loaded optimization metrics: {opt_metrics}")
        print(f"  Metrics configuration: {len(opt_direct_info)} metric(s)")
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERROR] {e}")
        return 1
    print()

    print("Step 2: Loading descriptors...")
    print("-" * 60)

    # Load descriptors
    desc_dict, condition_dict = load_desc_dict(
        reagent_types=reagent_types,
        desc_dir=Path(args.project_dir) / "descriptors",
        name_suffix=name_suffix,
        return_condition_dict=True,
        index_col=args.index_col,
    )
    print(f"✓ Loaded {len(desc_dict)} descriptor files")
    print()

    print("Step 3: Creating ReactionOptimizer instance...")
    print("-" * 60)

    # Create optimizer
    sbo = ReactionOptimizer(
        opt_metrics=opt_metrics,
        opt_metric_settings=opt_direct_info,
        opt_type="auto",
        random_seed=args.random_seed,
        quiet=args.quiet,
        save_dir=Path(args.project_dir) / args.output_dir,
    )
    print("✓ ReactionOptimizer instance created")
    print()

    print("Step 4: Loading reaction space...")
    print("-" * 60)

    # Load reaction space
    sbo.load_rxn_space(condition_dict=condition_dict)
    print("✓ Reaction space loaded")
    print()

    print("Step 5: Loading descriptors...")
    print("-" * 60)

    # Load descriptors
    sbo.load_desc(desc_dict=desc_dict)
    print("✓ Descriptors loaded")
    print()

    print("Step 6: Loading previous reaction data...")
    print("-" * 60)

    # Load previous reaction data
    if not Path(args.project_dir / args.input_dir).exists():
        print(f"[ERROR] Input file not found: {Path(args.project_dir / args.input_dir)}")
        print()
        print("Please provide previous reaction data to run optimization.")
        print("If you want to start with initial sampling, use initialize.py instead.")
        return 1

    prev_rxn_data = get_prev_rxn(Path(args.project_dir / args.input_dir), "batch-*.csv")
    sbo.load_prev_rxn(prev_rxn_data)
    print(f"✓ Loaded previous reactions from {args.input_dir}")
    print(f"  Total reactions: {len(prev_rxn_data)}")
    if "batch" in prev_rxn_data.columns:
        print(f"  Batch range: {prev_rxn_data['batch'].min()} to {prev_rxn_data['batch'].max()}")
    print()

    print("Step 7: Running optimization...")
    print("-" * 60)

    # Run optimization
    sbo.optimize(
        batch_size=args.batch_size,
        desc_normalize=args.desc_normalize,
        optimize_method=args.optimize_method,
        accuracy=args.accuracy,
        acq_func=args.acq_func,
    )
    print()

    print("Step 8: Saving results...")
    print("-" * 60)

    # Save results
    sbo.save_results(filetype="csv")
    sbo.save_results(filetype="excel")
    print(f"✓ Results saved to {Path(args.project_dir) / args.output_dir}")
    print()

    # Display optimization summary
    print("=" * 60)
    print("Optimization completed successfully!")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  - Recommended {len(sbo.selected_conditions)} new conditions")
    print(f"  - Exploit: {sum(1 for t in sbo.recommend_type if t == 'exploit')}")
    print(f"  - Explore: {sum(1 for t in sbo.recommend_type if t == 'explore')}")
    print()
    print("Next steps:")
    print("1. Run the experiments with the recommended conditions")
    print("2. Collect the experimental results")
    print("3. Update your reaction data file")
    print("4. Run optimize.py again to continue optimization")
    print()

    return 0


if __name__ == "__main__":
    main()
