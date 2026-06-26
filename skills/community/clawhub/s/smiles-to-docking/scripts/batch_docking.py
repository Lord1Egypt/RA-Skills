#!/usr/bin/env python3
"""
Step 3: Batch AutoDock Vina docking.
Usage:
    python batch_docking.py \
        --protein_pdbqt protein.pdbqt \
        --ligand_pdbqt_dir ligands/ \
        --pocket "center_x=10.5 center_y=20.3 center_z=-5.2 size_x=22 size_y=22 size_z=22" \
        --output_dir ./step3 \
        --max_workers 8
"""

import argparse
import os
import re
import shlex
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


def find_vina(vina_path: str = "") -> str:
    """Locate the vina executable."""
    if vina_path and os.path.isfile(vina_path):
        return vina_path
    candidates = [
        vina_path,
        "vina",
        "/usr/local/bin/vina",
        "/usr/bin/vina",
        os.path.expanduser("~/miniconda3/bin/vina"),
        os.path.expanduser("~/anaconda3/bin/vina"),
    ]
    for candidate in candidates:
        if candidate and (os.path.isfile(candidate) or candidate == "vina"):
            result = subprocess.run(
                shlex.split(f"{candidate} --version") if candidate != "vina" else ["vina", "--version"],
                capture_output=True, text=True,
            )
            if result.returncode == 0:
                print(f"  Found Vina: {candidate}")
                return candidate
    result = subprocess.run(["which", "vina"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def parse_pocket(pocket_str: str) -> dict:
    """Parse pocket string into center/size dict."""
    pattern = r"center_x\s*=\s*([-\d.]+)\s+center_y\s*=\s*([-\d.]+)\s+center_z\s*=\s*([-\d.]+)\s+size_x\s*=\s*([\d.]+)\s+size_y\s*=\s*([\d.]+)\s+size_z\s*=\s*([\d.]+)"
    m = re.search(pattern, pocket_str, re.IGNORECASE)
    if not m:
        raise ValueError(f"Cannot parse pocket string: {pocket_str}")
    return {
        "cx": float(m.group(1)), "cy": float(m.group(2)), "cz": float(m.group(3)),
        "sx": float(m.group(4)), "sy": float(m.group(5)), "sz": float(m.group(6)),
    }


def write_vina_config(protein_pdbqt: str, ligand_pdbqt: str, pocket: dict,
                     config_path: str, num_modes: int = 9, exhaustiveness: int = 8):
    """Write a Vina configuration file."""
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(f"receptor = {protein_pdbqt}\n")
        f.write(f"ligand = {ligand_pdbqt}\n")
        f.write(f"center_x = {pocket['cx']}\n")
        f.write(f"center_y = {pocket['cy']}\n")
        f.write(f"center_z = {pocket['cz']}\n")
        f.write(f"size_x = {pocket['sx']}\n")
        f.write(f"size_y = {pocket['sy']}\n")
        f.write(f"size_z = {pocket['sz']}\n")
        f.write(f"num_modes = {num_modes}\n")
        f.write(f"exhaustiveness = {exhaustiveness}\n")
        f.write("out = dummy_out.pdbqt\n")


def run_vina_single(task: tuple) -> tuple[str, float, str]:
    """Dock one ligand with AutoDock Vina. Returns (name, best_affinity, error_msg)."""
    protein_pdbqt, ligand_pdbqt, pocket_str, output_dir, exhaustiveness, num_modes, cpu, vina_bin = task

    name = Path(ligand_pdbqt).stem
    ligand_out_dir = Path(output_dir) / name
    ligand_out_dir.mkdir(parents=True, exist_ok=True)

    config_path = ligand_out_dir / "vina_config.txt"
    pocket = parse_pocket(pocket_str)
    write_vina_config(protein_pdbqt, ligand_pdbqt, pocket, str(config_path), num_modes, exhaustiveness)

    cmd = [vina_bin, "--config", str(config_path)]
    if cpu > 0:
        cmd += ["--cpu", str(cpu)]

    log_path = ligand_out_dir / "vina_log.txt"
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            cwd=str(ligand_out_dir), timeout=600,
        )
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\n=== STDERR ===\n")
                f.write(result.stderr)

        if result.returncode != 0:
            return name, 999.0, f"returncode={result.returncode}"

        best_aff = None
        for line in result.stdout.splitlines():
            m = re.match(r"\s*1\s+([-\d.]+)", line)
            if m:
                best_aff = float(m.group(1))
                break

        if best_aff is None:
            return name, 999.0, "Could not parse Vina output"

        return name, best_aff, ""

    except subprocess.TimeoutExpired:
        return name, 999.0, "Timeout (600s)"
    except Exception as e:
        return name, 999.0, str(e)


def main():
    parser = argparse.ArgumentParser(description="Batch AutoDock Vina docking")
    parser.add_argument("--protein_pdbqt", required=True, help="Receptor PDBQT file")
    parser.add_argument("--ligand_pdbqt_dir", required=True, help="Ligand PDBQT directory")
    parser.add_argument("--pocket", required=True, help="Docking box (e.g. center_x=10.5 center_y=20.3 ...)")
    parser.add_argument("--output_dir", required=True, help="Output directory")
    parser.add_argument("--exhaustiveness", type=int, default=8, help="Vina exhaustiveness")
    parser.add_argument("--num_modes", type=int, default=9, help="Number of output modes")
    parser.add_argument("--cpu", type=int, default=0, help="CPU cores per Vina process (0=all)")
    parser.add_argument("--vina_path", default="", help="Path to Vina binary")
    parser.add_argument("--max_workers", type=int, default=4, help="Parallel worker count")
    args = parser.parse_args()

    vina_bin = find_vina(args.vina_path)
    if not vina_bin:
        raise SystemExit("AutoDock Vina executable not found. Install with: conda install -c conda-forge autodock-vina")

    ligand_pdbqts = sorted(Path(args.ligand_pdbqt_dir).glob("*.pdbqt"))
    if not ligand_pdbqts:
        raise SystemExit(f"No ligand PDBQT files found in {args.ligand_pdbqt_dir}")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tasks = [
        (args.protein_pdbqt, str(lp), args.pocket, str(out_dir),
         args.exhaustiveness, args.num_modes, args.cpu, vina_bin)
        for lp in ligand_pdbqts
    ]

    print(f"Starting batch docking: {len(tasks)} ligands, max_workers={args.max_workers}")
    print(f"Pocket: {args.pocket}")
    print(f"Vina binary: {vina_bin}")

    results = []
    with ProcessPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {executor.submit(run_vina_single, t): t for t in tasks}
        done = 0
        for future in as_completed(futures):
            done += 1
            name, aff, err = future.result()
            results.append((name, aff, err))
            if err:
                print(f"  FAIL [{done}/{len(tasks)}] {name}: {err}")
            else:
                print(f"  OK   [{done}/{len(tasks)}] {name}: {aff:.2f} kcal/mol")

    results.sort(key=lambda x: x[1])
    summary_path = out_dir / "batch_summary.csv"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("rank,ligand_name,affinity_kcal_mol,status\n")
        for rank, (name, aff, err) in enumerate(results, 1):
            status = "OK" if not err else f"FAIL: {err}"
            f.write(f"{rank},{name},{aff:.3f},{status}\n")

    ok_count = sum(1 for _, _, e in results if not e)
    print(f"\nDone: {ok_count}/{len(results)} succeeded")
    print(f"Summary: {summary_path}")
    print("Top 3:")
    for name, aff, _ in results[:3]:
        print(f"  {aff:.3f}  {name}")


if __name__ == "__main__":
    main()