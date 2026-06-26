#!/usr/bin/env python3
"""
Pocket estimation from a co-crystallized ligand.
Usage:
    python pocket_from_ligand.py --protein 8V1R.pdb --ligand_resname DOC
"""

import argparse
from pathlib import Path

from Bio.PDB import PDBParser


def compute_pocket(pdb_path: str, ligand_chain: str = None, ligand_resname: str = None,
                   padding: float = 10.0) -> dict:
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_path)

    xs, ys, zs = [], [], []
    found = False

    for model in structure:
        for chain in model:
            if ligand_chain and chain.get_id() != ligand_chain:
                continue
            for residue in chain:
                if residue.get_id()[0] not in (" ", "H"):
                    continue
                resname = residue.get_resname()
                if ligand_resname and resname.upper() != ligand_resname.upper():
                    continue
                found = True
                for atom in residue:
                    x, y, z = atom.get_coord()
                    xs.append(x); ys.append(y); zs.append(z)

    if not found:
        raise ValueError(
            f"Ligand not found (chain={ligand_chain}, resname={ligand_resname}). "
            "Use PyMOL or another viewer to identify the ligand's chain ID and residue name."
        )

    cx, cy, cz = sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)
    rx = max((max(xs)-min(xs))/2 + padding, 20.0)
    ry = max((max(ys)-min(ys))/2 + padding, 20.0)
    rz = max((max(zs)-min(zs))/2 + padding, 20.0)

    return {
        "center_x": round(cx, 2), "center_y": round(cy, 2), "center_z": round(cz, 2),
        "size_x": round(rx * 2, 1), "size_y": round(ry * 2, 1), "size_z": round(rz * 2, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="Estimate docking pocket from co-crystal ligand")
    parser.add_argument("--protein", required=True, help="Protein PDB file")
    parser.add_argument("--ligand_chain", default="", help="Ligand chain ID")
    parser.add_argument("--ligand_resname", default="", help="Ligand residue name (e.g. DOC, LIG)")
    parser.add_argument("--padding", type=float, default=10.0, help="Padding in Angstroms")
    parser.add_argument("--output", default="", help="Output file for pocket string")
    args = parser.parse_args()

    if not args.ligand_chain and not args.ligand_resname:
        raise SystemExit("Provide --ligand_chain or --ligand_resname")

    pocket = compute_pocket(
        args.protein,
        args.ligand_chain or None,
        args.ligand_resname or None,
        args.padding,
    )

    pocket_str = (
        f"center_x={pocket['center_x']} center_y={pocket['center_y']} center_z={pocket['center_z']} "
        f"size_x={pocket['size_x']} size_y={pocket['size_y']} size_z={pocket['size_z']}"
    )
    print(f"Pocket: {pocket_str}")
    if args.output:
        Path(args.output).write_text(pocket_str + "\n", encoding="utf-8")
        print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()