"""Zopaf Negotiation Simulator — Entry Point."""

import argparse
import sys
from pathlib import Path

from case import load_case
from simulator import run_negotiation
from scorer import print_analysis


def main():
    parser = argparse.ArgumentParser(description="Zopaf Negotiation Simulator")
    parser.add_argument(
        "case_file",
        nargs="?",
        default="cases/kdh_walmart.yaml",
        help="Path to the negotiation case YAML file",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress round-by-round transcript output",
    )
    args = parser.parse_args()

    case_path = Path(args.case_file)
    if not case_path.exists():
        print(f"Error: Case file not found: {case_path}")
        sys.exit(1)

    case = load_case(case_path)

    print(f"\n{'#'*60}")
    print(f"  ZOPAF NEGOTIATION SIMULATOR")
    print(f"  Case: {case.title}")
    print(f"  {case.party_a_name} vs {case.party_b_name}")
    print(f"  Max rounds: {case.max_rounds}")
    print(f"{'#'*60}")

    result = run_negotiation(case, verbose=not args.quiet)

    print_analysis(case, result["deal"])

    if not result["deal"]:
        print("  No deal was reached. Both parties walk away with their BATNA.\n")
    else:
        print(f"  Deal reached in {result['rounds']} round(s).\n")


if __name__ == "__main__":
    main()
