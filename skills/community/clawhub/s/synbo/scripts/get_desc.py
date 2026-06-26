#!/usr/bin/env python3
"""
Generate molecular descriptors from SMILES strings.

This script calculates SPOC (Structure-Property Oriented Classification) descriptors
for a list of SMILES strings and saves them to a CSV file.

Supports handling of entries without valid SMILES (e.g., "no_alkali") by filling
their descriptor columns with 0.0 placeholders.
"""

import argparse
from pathlib import Path
import pandas as pd
from typing import List, Tuple

try:
    from synbo.descriptor import spoc_desc
    from rdkit import Chem
except ImportError:
    print("Error: synbo/rdkit package is not installed. Please install it first.")
    raise Exception()


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate SPOC molecular descriptors from SMILES strings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate descriptors from a file containing SMILES (one per line)
  python get_desc.py --input reagent.csv --name "reagent" --output ./desc
        """,
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--input", type=Path, help="Path to CSV file with SMILES and name columns")
    parser.add_argument("--smiles-col", default="SMILES", required=True, help="Name of the column containing SMILES strings")
    parser.add_argument("--name-col", default="name", help="Name of the column containing names")
    parser.add_argument(
        "--output", type=Path, default=Path("./descriptors"), help="Output directory for the descriptor CSV file (default: ./descriptors)"
    )
    parser.add_argument("--index-name", default="Name", help="Name for the index column in the output CSV (default: Name)")
    parser.add_argument("--fp-type", default="RDKit", help="Fingerprint/descriptor type (default: RDKit)")

    return parser.parse_args()


def is_valid_smiles(smiles: str) -> bool:
    """Check if a SMILES string can be parsed by RDKit."""
    if not isinstance(smiles, str) or not smiles.strip():
        return False
    mol = Chem.MolFromSmiles(smiles.strip())
    return mol is not None


def read_smiles_from_file(smiles_col: str, file_path: Path) -> Tuple[pd.DataFrame, List[int]]:
    """Read SMILES and name from CSV. Returns (df, list of invalid SMILES row indices)."""
    assert file_path.exists(), f"Error: File {file_path} does not exist."
    df = pd.read_csv(file_path)
    assert smiles_col in df.columns, f"Error: File {file_path} does not contain a '{smiles_col}' column."

    invalid_indices = []
    for idx, row in df.iterrows():
        if not is_valid_smiles(row[smiles_col]):
            invalid_indices.append(idx)

    return df, invalid_indices


def generate_descriptors(valid_df: pd.DataFrame, args: argparse.Namespace, output_dir: Path, fill_zero_row: str = None) -> None:
    """
    Generate SPOC descriptors and return the result DataFrame.
    The actual saved file will be named {base_name}_{fp_type}.csv
    """
    save_path = output_dir / f"{args.input.stem}.csv"
    smiles_list = valid_df[args.smiles_col].tolist()
    name_list = valid_df[args.name_col].tolist() if args.name_col in valid_df.columns else None
    try:
        print(f"Generating {args.fp_type} descriptors for {len(smiles_list)} SMILES strings...")
        spoc_desc.calc_spoc_desc(
            smiles_list=smiles_list,
            name_list=name_list,
            save_path=save_path,
            fp_type=args.fp_type,
            index_name="name",
            rtype=args.input.stem,
            fill_zero_row=fill_zero_row,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to generate descriptors: {e}") from e


def main() -> int:
    args = parse_arguments()
    df, invalid_indices = read_smiles_from_file(args.smiles_col, args.input)
    if len(invalid_indices) > 1:
        raise Exception(f"More than one invalid SMILES found in the input file: {invalid_indices}. Please fix the input data.")
    elif len(invalid_indices) == 1:
        invalid_names = df.loc[invalid_indices, args.name_col].tolist()
        print(f"the `{invalid_names[0]}` is invalid SMILES. using 0.0 as placeholder for its descriptors.")

    df = df.drop(index=invalid_indices) if invalid_indices else df
    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate descriptors for valid SMILES
    generate_descriptors(df, args, output_dir, fill_zero_row=invalid_names[0] if invalid_indices else None)

    return 0


if __name__ == "__main__":
    main()
