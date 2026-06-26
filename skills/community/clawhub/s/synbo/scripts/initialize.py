#!/usr/bin/env python3
"""
Initialize script for SynBO reaction optimization.

This script demonstrates how to initialize the ReactionOptimizer and perform
initial sampling without previous reaction data.

Usage:
    python initialize.py --project-dir examples
"""

import argparse
import json
from pathlib import Path

from synbo import ReactionOptimizer
from synbo.utils import load_desc_dict


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
        description="Initialize reaction optimization with initial sampling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Project directory",
    )
    parser.add_argument(
        "--name-suffix",
        nargs="+",
        default="_RDKit",
        help="Name suffixes for descriptor files (default: _RDKit)",
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
        help="Number of initial samples to generate (default: 5)",
    )
    parser.add_argument(
        "--desc-normalize",
        default="minmax",
        choices=["minmax", "zscore", "l2"],
        help="Descriptor normalization method (default: minmax)",
    )
    parser.add_argument(
        "--sampling-method",
        default="lhs",
        choices=["sobol", "random", "lhs", "kmeans"],
        help="Sampling strategy for initial points (default: kmeans)",
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
    """Main function to run initialization workflow."""
    args = parse_arguments()

    print("=" * 60)
    print("SynBO Initialization Script")
    print("=" * 60)
    print()

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
        opt_type="init",
        random_seed=args.random_seed,
        quiet=args.quiet,
        save_dir=Path(args.project_dir) / "results",
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

    print("Step 6: Running initialization with sampling...")
    print("-" * 60)

    # Initialize with sampling
    sbo.initialize(
        batch_size=args.batch_size,
        desc_normalize=args.desc_normalize,
        sampling_method=args.sampling_method,
    )
    print()

    print("Step 7: Saving results...")
    print("-" * 60)

    # Create output directory
    output_dir = Path(args.project_dir) / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save results
    sbo.save_results(filetype="csv")
    sbo.save_results(filetype="excel")
    print(f"✓ Results saved to {output_dir}")
    print()

    print("=" * 60)
    print("Initialization completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run the experiments with the recommended conditions")
    print("2. Collect the experimental results")
    print("3. Use optimize.py to continue optimization with the new data")
    print()

    return 0


if __name__ == "__main__":
    main()
