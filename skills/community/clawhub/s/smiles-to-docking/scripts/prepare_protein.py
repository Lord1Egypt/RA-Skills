#!/usr/bin/env python3
"""
Step 2b: Receptor preparation from PDB to PDBQT.
Usage:
    python prepare_protein.py --protein 8V1R.pdb --output_dir ./step2

Optional pocket estimation from co-crystallized ligand:
    python prepare_protein.py --protein 8V1R.pdb --output_dir ./step2 \
        --ligand_resname DOC --output_pocket pocket.txt
"""

import argparse
import os
import subprocess
from pathlib import Path

from Bio.PDB import PDBParser, PDBIO, Select


STANDARD_RESIDUES = {
    "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE",
    "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
    "MSE",
}


class NonWaterStandardSelect(Select):
    """Keep only standard amino-acid residues; remove water molecules."""
    def accept_residue(self, residue):
        if residue.get_id()[0] == "W":
            return False
        return residue.get_resname() in STANDARD_RESIDUES


def parse_pocket_from_ligand(
    pdb_path: str,
    ligand_chain: str = None,
    ligand_resname: str = None,
    padding: float = 10.0,
) -> dict:
    """Estimate docking-box coordinates from a co-crystallized ligand."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_path)

    xs, ys, zs = [], [], []
    found = False

    for model in structure:
        for chain in model:
            for residue in chain:
                is_ligand = False
                if ligand_chain and chain.get_id() == ligand_chain and residue.get_id()[0] not in (" ", "H"):
                    is_ligand = True
                if ligand_resname and residue.get_resname().upper() == ligand_resname.upper() and residue.get_id()[0] not in (" ", "H"):
                    is_ligand = True
                if is_ligand:
                    found = True
                    for atom in residue:
                        x, y, z = atom.get_coord()
                        xs.append(x)
                        ys.append(y)
                        zs.append(z)

    if not found:
        raise ValueError("Specified ligand not found in the input PDB")

    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    cz = sum(zs) / len(zs)
    rx = (max(xs) - min(xs)) / 2 + padding
    ry = (max(ys) - min(ys)) / 2 + padding
    rz = (max(zs) - min(zs)) / 2 + padding

    return {
        "center_x": round(cx, 2),
        "center_y": round(cy, 2),
        "center_z": round(cz, 2),
        "size_x": round(rx * 2, 1),
        "size_y": round(ry * 2, 1),
        "size_z": round(rz * 2, 1),
    }


def prepare_protein(pdb_path: str, output_dir: str) -> str:
    """Remove waters and non-standard residues, then convert to PDBQT with Open Babel."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_path)
    temp_pdb = out_dir / "protein_no_water.pdb"

    io = PDBIO()
    io.set_structure(structure)
    io.save(str(temp_pdb), NonWaterStandardSelect())

    out_pdbqt = out_dir / "protein_prepared.pdbqt"
    cmd = f'obabel "{temp_pdb}" -O "{out_pdbqt}" -xr -h --partialcharge gasteiger'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if temp_pdb.exists():
        os.remove(temp_pdb)

    if result.returncode != 0:
        raise RuntimeError(f"Open Babel failed:\n{result.stderr}")

    print(f"  Protein prepared: {out_pdbqt}")
    return str(out_pdbqt)


def main():
    parser = argparse.ArgumentParser(description="Prepare receptor: PDB to PDBQT")
    parser.add_argument("--protein", required=True, help="Input protein PDB file")
    parser.add_argument("--output_dir", required=True, help="Output directory")
    parser.add_argument("--ligand_chain", default="", help="Ligand chain ID for pocket estimation")
    parser.add_argument("--ligand_resname", default="", help="Ligand residue name for pocket estimation")
    parser.add_argument("--pocket_padding", type=float, default=10.0, help="Padding in Angstroms")
    parser.add_argument("--output_pocket", default="", help="Output file for computed pocket string")
    args = parser.parse_args()

    pdbqt_path = prepare_protein(args.protein, args.output_dir)
    print(f"Receptor PDBQT: {pdbqt_path}")

    if args.ligand_chain or args.ligand_resname:
        pocket = parse_pocket_from_ligand(
            args.protein,
            args.ligand_chain or None,
            args.ligand_resname or None,
            args.pocket_padding,
        )
        pocket_str = (
            f"center_x={pocket['center_x']} center_y={pocket['center_y']} center_z={pocket['center_z']} "
            f"size_x={pocket['size_x']} size_y={pocket['size_y']} size_z={pocket['size_z']}"
        )
        print(f"  Pocket: {pocket_str}")
        if args.output_pocket:
            with open(args.output_pocket, "w", encoding="utf-8") as f:
                f.write(pocket_str + "\n")
            print(f"  Pocket saved to: {args.output_pocket}")


if __name__ == "__main__":
    main()