#!/usr/bin/env python3
"""
End-to-end molecular docking workflow.
Steps:
    1. SMILES -> SDF + 3D conformers
    2. PDB/SDF -> PDBQT (ligand + receptor)
    3. Batch AutoDock Vina docking
    4. Ranking and Top-N complex export

Usage:
    python main.py --protein 8V1R.pdb --smiles_file ligands.txt \
        --pocket "center_x=141.47 center_y=145.24 center_z=125.87 size_x=26 size_y=26 size_z=28" \
        --output_dir ./docking_results --top_n 10 --max_workers 8
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()


def step1_smiles_to_sdf(smiles_file: str, output_dir: str) -> str:
    script = SCRIPT_DIR / "smiles_to_sdf.py"
    subprocess.run([sys.executable, str(script),
                    "--smiles_file", smiles_file,
                    "--output_dir", output_dir], check=True)
    return output_dir


def step2_prepare(sdf_dir: str, protein_pdb: str, output_dir: str) -> tuple[str, str]:
    lig_script = SCRIPT_DIR / "prepare_ligand.py"
    lig_out = os.path.join(output_dir, "ligands")
    subprocess.run([sys.executable, str(lig_script),
                    "--sdf_dir", sdf_dir,
                    "--output_dir", lig_out], check=True)

    prot_script = SCRIPT_DIR / "prepare_protein.py"
    subprocess.run([sys.executable, str(prot_script),
                    "--protein", protein_pdb,
                    "--output_dir", output_dir], check=True)

    prot_pdbqt = os.path.join(output_dir, "protein_prepared.pdbqt")
    return prot_pdbqt, lig_out


def step3_batch_dock(protein_pdbqt: str, ligand_pdbqt_dir: str,
                     pocket: str, output_dir: str,
                     exhaustiveness: int, cpu: int,
                     vina_path: str, max_workers: int) -> str:
    script = SCRIPT_DIR / "batch_docking.py"
    cmd = [
        sys.executable, str(script),
        "--protein_pdbqt", protein_pdbqt,
        "--ligand_pdbqt_dir", ligand_pdbqt_dir,
        "--pocket", pocket,
        "--output_dir", output_dir,
        "--exhaustiveness", str(exhaustiveness),
        "--cpu", str(cpu),
        "--max_workers", str(max_workers),
    ]
    if vina_path:
        cmd += ["--vina_path", vina_path]
    subprocess.run(cmd, check=True)
    return output_dir


def step4_rank(docking_dir: str, protein_pdb: str, top_n: int, output_dir: str) -> str:
    script = SCRIPT_DIR / "rank_results.py"
    subprocess.run([sys.executable, str(script),
                    "--docking_dir", docking_dir,
                    "--protein_pdb", protein_pdb,
                    "--top_n", str(top_n),
                    "--output_dir", output_dir], check=True)
    return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="End-to-end docking workflow: SMILES -> SDF -> PDBQT -> Vina -> ranking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --protein 8V1R.pdb --smiles_file ligands.txt \\
      --pocket "center_x=141.47 center_y=145.24 center_z=125.87 size_x=26 size_y=26 size_z=28" \\
      --output_dir ./docking_results --top_n 10 --max_workers 8

  # Resume from Step 3 (skip steps 1 & 2)
  python main.py --protein 8V1R.pdb --smiles_file ligands.txt --pocket "..." \\
      --skip_step1 --skip_step2 \\
      --sdf_dir ./step1_smiles_to_sdf/ligands \\
      --prep_dir ./step2_preparation \\
      --dock_dir ./step3_docking \\
      --output_dir ./docking_results

Input ligands.txt format (SMILES or SMILES<TAB>name):
  CCO    Ethanol
  c1ccccc1    Benzene
  CC(=O)Oc1ccccc1C(=O)O    Aspirin
"""
    )
    parser.add_argument("--protein", required=True, help="Protein PDB file")
    parser.add_argument("--smiles_file", required=True, help="SMILES input file")
    parser.add_argument("--pocket", required=True,
                        help="Docking box (center_x=... center_y=... center_z=... size_x=... size_y=... size_z=...)")
    parser.add_argument("--output_dir", default="./docking_results", help="Root output directory")
    parser.add_argument("--top_n", type=int, default=10, help="Number of top complexes to export")
    parser.add_argument("--exhaustiveness", type=int, default=8, help="Vina exhaustiveness")
    parser.add_argument("--cpu", type=int, default=0, help="CPU cores per Vina process (0=all)")
    parser.add_argument("--max_workers", type=int, default=4, help="Parallel worker count")
    parser.add_argument("--vina_path", default="", help="Path to Vina binary")
    # Skip options
    parser.add_argument("--skip_step1", action="store_true")
    parser.add_argument("--skip_step2", action="store_true")
    parser.add_argument("--skip_step3", action="store_true")
    parser.add_argument("--skip_step4", action="store_true")
    # Skip-step directories
    parser.add_argument("--sdf_dir", default="")
    parser.add_argument("--prep_dir", default="")
    parser.add_argument("--dock_dir", default="")
    parser.add_argument("--rank_dir", default="")
    args = parser.parse_args()

    base = Path(args.output_dir)
    step1_dir = base / "step1_smiles_to_sdf"
    step2_dir = base / "step2_preparation"
    step3_dir = base / "step3_docking"
    step4_dir = base / "step4_ranking"

    os.makedirs(base, exist_ok=True)

    # Step 1
    if args.skip_step1:
        if not args.sdf_dir:
            raise ValueError("--skip_step1 requires --sdf_dir")
        sdf_dir = args.sdf_dir
    else:
        print("\n===== Step 1: SMILES -> SDF =====")
        sdf_dir = step1_smiles_to_sdf(args.smiles_file, str(step1_dir))

    # Step 2
    if args.skip_step2:
        if not args.prep_dir:
            raise ValueError("--skip_step2 requires --prep_dir")
        prot_pdbqt = os.path.join(args.prep_dir, "protein_prepared.pdbqt")
        lig_pdbqt_dir = os.path.join(args.prep_dir, "ligands")
    else:
        print("\n===== Step 2: PDB/SDF -> PDBQT =====")
        prot_pdbqt, lig_pdbqt_dir = step2_prepare(sdf_dir, args.protein, str(step2_dir))

    # Step 3
    if args.skip_step3:
        if not args.dock_dir:
            raise ValueError("--skip_step3 requires --dock_dir")
        dock_dir = args.dock_dir
    else:
        print("\n===== Step 3: Batch Vina Docking =====")
        dock_dir = step3_batch_dock(prot_pdbqt, lig_pdbqt_dir, args.pocket, str(step3_dir),
                                     args.exhaustiveness, args.cpu, args.vina_path, args.max_workers)

    # Step 4
    if args.skip_step4:
        if not args.rank_dir:
            raise ValueError("--skip_step4 requires --rank_dir")
        rank_dir = args.rank_dir
    else:
        print("\n===== Step 4: Ranking & Export =====")
        rank_dir = step4_rank(dock_dir, args.protein, args.top_n, str(step4_dir))

    print(f"""
============================================================
  Workflow Completed Successfully
============================================================
  Ranked CSV  : {rank_dir}/docking_scores.csv
  Summary     : {rank_dir}/docking_summary.txt
  Top Structs : {rank_dir}/rank*_*.pdb
============================================================
""")


if __name__ == "__main__":
    main()