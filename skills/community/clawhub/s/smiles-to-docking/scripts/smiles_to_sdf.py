#!/usr/bin/env python3
"""
Step 1: Batch SMILES to SDF with 3D conformer generation.
Usage:
    python smiles_to_sdf.py --smiles_file ligands.txt --output_dir ./step1

Input format (ligands.txt):
    CCO
    c1ccccc1
    CC(=O)Oc1ccccc1C(=O)O

Or with names (tab-separated):
    CCO    Ethanol
    c1ccccc1    Benzene
"""

import argparse
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter


def load_smiles_file(filepath: str) -> list[tuple[str, str]]:
    """Load SMILES from file. Each line: SMILES or SMILES<TAB>name."""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            smiles = parts[0].strip()
            name = parts[1].strip() if len(parts) > 1 else f"lig_{lineno:04d}"
            entries.append((smiles, name))
    return entries


def build_3d_molecule(smiles: str, name: str, random_seed: int = 42):
    """Convert SMILES to RDKit Mol with 3D conformer and UFF optimization."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None, False
        mol.SetProp("_Name", name)
        mol.SetProp("SMILES", smiles)
        mol = Chem.AddHs(mol)
        result = AllChem.EmbedMolecule(mol, randomSeed=random_seed)
        if result == -1:
            params = AllChem.ETKDGv3()
            params.randomSeed = random_seed
            result = AllChem.EmbedMolecule(mol, params)
            if result == -1:
                return None, False
        AllChem.UFFOptimizeMolecule(mol, maxIters=500)
        return mol, True
    except Exception as e:
        print(f"  WARNING [{name}] failed: {e}")
        return None, False


def main():
    parser = argparse.ArgumentParser(
        description="Batch SMILES to SDF with 3D conformer generation"
    )
    parser.add_argument("--smiles_file", required=True, help="Input SMILES file")
    parser.add_argument("--output_dir", required=True, help="Output directory")
    parser.add_argument("--random_seed", type=int, default=42, help="Random seed")
    parser.add_argument("--max_mols", type=int, default=0, help="Max molecules to process (0=all)")
    args = parser.parse_args()

    entries = load_smiles_file(args.smiles_file)
    if args.max_mols > 0:
        entries = entries[: args.max_mols]

    out_dir = Path(args.output_dir)
    ligands_dir = out_dir / "ligands"
    ligands_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failed = []

    for i, (smiles, name) in enumerate(entries, 1):
        sdf_path = ligands_dir / f"{name}.sdf"
        if sdf_path.exists():
            print(f"  SKIP [{i}/{len(entries)}] {name} already exists")
            success_count += 1
            continue

        mol, ok = build_3d_molecule(smiles, name, args.random_seed)
        if ok:
            with SDWriter(str(sdf_path)) as w:
                w.write(mol)
            success_count += 1
            print(f"  OK   [{i}/{len(entries)}] {name}")
        else:
            failed.append((name, smiles))
            print(f"  FAIL [{i}/{len(entries)}] {name}")

    summary_path = out_dir / "step1_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("Step 1: SMILES to SDF completed\n")
        f.write(f"Input file: {args.smiles_file}\n")
        f.write(f"Successful: {success_count}/{len(entries)}\n")
        f.write(f"Output directory: {ligands_dir}\n")
        f.write("Failed entries:\n")
        for nm, sm in failed:
            f.write(f"  {nm}\t{sm}\n")

    print(f"\nDone: {success_count}/{len(entries)} succeeded, {len(failed)} failed")
    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()