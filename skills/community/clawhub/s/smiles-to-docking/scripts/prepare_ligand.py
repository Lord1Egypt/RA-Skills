#!/usr/bin/env python3
"""
Step 2a: Batch ligand preparation from SDF to PDBQT.
Usage:
    python prepare_ligand.py --sdf_dir ./step1/ligands --output_dir ./step2/ligands
"""

import argparse
import subprocess
from pathlib import Path

from rdkit import Chem
from meeko import MoleculePreparation


def sdf_to_pdbqt(sdf_path: str, out_pdbqt: str) -> bool:
    """Convert SDF ligand to PDBQT using Meeko with Open Babel fallback."""
    try:
        mol = Chem.SDMolSupplier(str(sdf_path), removeHs=False)[0]
        if mol is None:
            print(f"  WARNING: Could not read SDF: {sdf_path}")
            return False

        preparator = MoleculePreparation()
        setup_list = preparator.prepare(mol)
        preparator.write_pdbqt_file(out_pdbqt, setup_list)
        return True
    except Exception as e:
        print(f"  WARNING Meeko failed for {Path(sdf_path).name}, fallback to Open Babel: {e}")
        cmd = f'obabel "{sdf_path}" -O "{out_pdbqt}" --partialcharge gasteiger -h'
        result = subprocess.run(cmd, shell=True, capture_output=True)
        return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(
        description="Batch ligand preparation: SDF to PDBQT"
    )
    parser.add_argument("--sdf_dir", required=True, help="Input SDF directory")
    parser.add_argument("--output_dir", required=True, help="Output PDBQT directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    sdf_dir = Path(args.sdf_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    sdf_files = sorted(sdf_dir.glob("*.sdf"))
    if not sdf_files:
        raise SystemExit(f"No SDF files found in {sdf_dir}")

    success_count = 0
    failed = []

    for i, sdf_path in enumerate(sdf_files, 1):
        name = sdf_path.stem
        pdbqt_path = out_dir / f"{name}.pdbqt"

        if pdbqt_path.exists() and not args.force:
            print(f"  SKIP [{i}/{len(sdf_files)}] {name} already exists")
            success_count += 1
            continue

        ok = sdf_to_pdbqt(str(sdf_path), str(pdbqt_path))
        if ok:
            success_count += 1
            print(f"  OK   [{i}/{len(sdf_files)}] {name}")
        else:
            failed.append(name)
            print(f"  FAIL [{i}/{len(sdf_files)}] {name}")

    print(f"\nDone: {success_count}/{len(sdf_files)} succeeded, {len(failed)} failed")
    if failed:
        print("Failed ligands:", ", ".join(failed))


if __name__ == "__main__":
    main()