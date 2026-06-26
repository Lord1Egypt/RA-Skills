#!/usr/bin/env python3
"""
Step 4: Parse docking scores, rank ligands, and export Top-N complexes.
Usage:
    python rank_results.py \
        --docking_dir ./step3 \
        --protein_pdb 8V1R.pdb \
        --top_n 10 \
        --output_dir ./step4
"""

import argparse
import csv
import subprocess
from pathlib import Path


def parse_vina_log(log_path: Path) -> list[dict]:
    """Extract all binding modes from a Vina log file."""
    results = []
    if not log_path.exists():
        return results
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 4 and parts[0].isdigit():
                results.append({
                    "mode": int(parts[0]),
                    "affinity_kcal_mol": float(parts[1]),
                    "rmsd_lb": float(parts[2]),
                    "rmsd_ub": float(parts[3]),
                })
    return results


def split_pdbqt_to_pdbs(pdbqt_path: Path, out_dir: Path) -> list[Path]:
    """Split a multi-model PDBQT into individual PDB files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pdb_files = []
    content = pdbqt_path.read_text(encoding="utf-8", errors="ignore")
    records = content.split("MODEL")
    for i, record in enumerate(records[1:], 1):
        record = record.strip()
        if not record:
            continue
        out_pdb = out_dir / f"{pdbqt_path.stem}_mode{i}.pdb"
        out_pdb.write_text(record, encoding="utf-8")
        pdb_files.append(out_pdb)
    return pdb_files


def merge_complex_obabel(protein_pdb: str, ligand_pdb: str, out_complex: str) -> bool:
    """Merge protein and ligand PDBs into a complex using Open Babel."""
    cmd = f'obabel "{protein_pdb}" "{ligand_pdb}" -O "{out_complex}" --sort'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.returncode == 0


def export_top_complexes(docking_dir: Path, protein_pdb: str,
                         ranked_results: list[tuple], top_n: int,
                         output_dir: Path) -> list[str]:
    """Export Top-N complex PDB files (protein + ligand)."""
    exported = []
    for rank, (name, aff, _log_path, _mode) in enumerate(ranked_results[:top_n], 1):
        ligand_dir = docking_dir / name
        docked_pdbqt = None

        for ext in ["_out.pdbqt", "dummy_out.pdbqt", "docked.pdbqt"]:
            matches = list(ligand_dir.glob(f"*{ext}"))
            if matches:
                docked_pdbqt = matches[0]
                break

        if not docked_pdbqt:
            pdbqts = [p for p in ligand_dir.glob("*.pdbqt") if "config" not in p.name]
            if pdbqts:
                docked_pdbqt = pdbqts[0]

        if not docked_pdbqt:
            continue

        split_dir = ligand_dir / "split"
        split_pdbs = split_pdbqt_to_pdbs(docked_pdbqt, split_dir)
        if not split_pdbs:
            continue

        best_ligand_pdb = split_pdbs[0]
        complex_pdb = output_dir / f"rank{rank}_{name}_aff{aff:.2f}.pdb"

        if merge_complex_obabel(protein_pdb, str(best_ligand_pdb), str(complex_pdb)):
            exported.append(str(complex_pdb))
            print(f"  OK   rank{rank}: {name} ({aff:.2f} kcal/mol) -> {complex_pdb.name}")

    return exported


def main():
    parser = argparse.ArgumentParser(
        description="Rank docking results and export Top-N complex structures"
    )
    parser.add_argument("--docking_dir", required=True, help="Step 3 output directory")
    parser.add_argument("--protein_pdb", required=True, help="Original protein PDB file")
    parser.add_argument("--top_n", type=int, default=10, help="Number of top complexes to export")
    parser.add_argument("--output_dir", required=True, help="Output directory")
    args = parser.parse_args()

    docking_dir = Path(args.docking_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ligand_dirs = [d for d in docking_dir.iterdir() if d.is_dir()]
    if not ligand_dirs:
        raise SystemExit(f"No ligand subdirectories found in {docking_dir}")

    all_results = []
    for lig_dir in ligand_dirs:
        name = lig_dir.name
        log_files = list(lig_dir.glob("vina_log.txt"))
        if not log_files:
            continue
        modes = parse_vina_log(log_files[0])
        if not modes:
            continue
        best_mode = min(modes, key=lambda m: m["affinity_kcal_mol"])
        aff = best_mode["affinity_kcal_mol"]
        all_results.append((name, aff, log_files[0], best_mode))

    all_results.sort(key=lambda x: x[1])

    # Write ranked CSV
    csv_path = out_dir / "docking_scores.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "ligand_name", "affinity_kcal_mol", "mode", "rmsd_lb", "rmsd_ub"])
        for rank, (name, aff, _lp, mode) in enumerate(all_results, 1):
            writer.writerow([rank, name, f"{aff:.3f}", mode["mode"],
                             f"{mode['rmsd_lb']:.3f}", f"{mode['rmsd_ub']:.3f}"])

    # Write text summary
    summary_path = out_dir / "docking_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("Docking Ranking Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Docking directory : {docking_dir}\n")
        f.write(f"Protein           : {args.protein_pdb}\n")
        f.write(f"Ligands ranked    : {len(all_results)}\n")
        if all_results:
            affs = [r[1] for r in all_results]
            f.write(f"Affinity range    : {min(affs):.2f} to {max(affs):.2f} kcal/mol\n")
            f.write(f"Mean affinity     : {sum(affs)/len(affs):.2f} kcal/mol\n\n")
        f.write(f"{'Rank':<6} {'Ligand':<30} {'Affinity (kcal/mol)':<18}\n")
        f.write("-" * 56 + "\n")
        for rank, (name, aff, _, _) in enumerate(all_results, 1):
            f.write(f"{rank:<6} {name:<30} {aff:.3f}\n")

    # Export Top-N complexes
    exported = export_top_complexes(docking_dir, args.protein_pdb, all_results, args.top_n, out_dir)

    print(f"\nRanked: {len(all_results)} ligands")
    print(f"CSV    : {csv_path}")
    print(f"Summary: {summary_path}")
    print(f"Exported Top-{len(exported)} complex structures to: {out_dir}")


if __name__ == "__main__":
    main()