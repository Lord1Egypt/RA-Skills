---
name: smiles-to-docking
description: End-to-end virtual screening workflow: SMILES to 3D SDF, ligand/receptor preparation to PDBQT, batch AutoDock Vina docking, affinity ranking, and Top-N complex export.
---

# SMILES-to-Docking: End-to-End Virtual Screening Skill

## Overview

This skill provides a complete small-molecule virtual screening workflow:

1. **SMILES → SDF + 3D conformer generation**
2. **Ligand/Receptor preparation → PDBQT**
3. **Batch AutoDock Vina docking**
4. **Affinity ranking + Top-N complex export**

It is designed for:
- hit discovery
- lead prioritization
- library-scale virtual screening
- receptor–ligand docking automation

---

## Dependencies

Install the required dependencies before running:

```bash
pip install "numpy<2"
pip install rdkit-pypi meeko biopython
conda install -c conda-forge openbabel autodock-vina
```

> Note: `rdkit-pypi` commonly requires `numpy<2` in many environments.

---

## File Structure

```text
smiles-to-docking/
├── SKILL.md
├── _meta.json
├── scripts/
│   ├── main.py
│   ├── smiles_to_sdf.py
│   ├── prepare_ligand.py
│   ├── prepare_protein.py
│   ├── batch_docking.py
│   └── rank_results.py
└── references/
    ├── vina_param_guide.md
    └── pocket_from_ligand.py
```

---

## Usage

### One-shot full workflow

```bash
python scripts/main.py \
  --protein 8V1R.pdb \
  --smiles_file ligands.txt \
  --pocket "center_x=141.47 center_y=145.24 center_z=125.87 size_x=26 size_y=26 size_z=28" \
  --output_dir ./docking_results \
  --top_n 10 \
  --exhaustiveness 8 \
  --cpu 1 \
  --vina_path /path/to/vina
```

### SMILES input format

Supported formats:

```text
CCO
c1ccccc1
CC(=O)Oc1ccccc1C(=O)O
```

or with names:

```text
CCO	Ethanol
c1ccccc1	Benzene
CC(=O)Oc1ccccc1C(=O)O	Aspirin
```

---

## Output

```text
output_dir/
├── step1_smiles_to_sdf/
├── step2_preparation/
├── step3_docking/
└── step4_ranking/
```

Main outputs:
- `docking_scores.csv`
- `docking_summary.txt`
- `rank*_*.pdb`

---

## Full Python Source Code

Below is the full source code for each Python file.

---

## scripts/smiles_to_sdf.py

```python
#!/usr/bin/env python3
"""
Step 1: Batch SMILES -> SDF with 3D conformer generation.
Usage:
    python smiles_to_sdf.py --smiles_file ligands.txt --output_dir ./step1
"""

import argparse
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter


def load_smiles_file(filepath: str) -> list[tuple[str, str]]:
    """Load a SMILES file. Each line may contain either:
    1. SMILES
    2. SMILES<TAB>name
    """
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
    """Convert SMILES to an RDKit molecule with hydrogens and a 3D conformer."""
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
    except Exception:
        return None, False


def main():
    parser = argparse.ArgumentParser(description="Batch SMILES to SDF conversion with 3D conformer generation")
    parser.add_argument("--smiles_file", required=True, help="Input SMILES file")
    parser.add_argument("--output_dir", required=True, help="Output directory")
    parser.add_argument("--random_seed", type=int, default=42, help="Random seed")
    parser.add_argument("--max_mols", type=int, default=0, help="Maximum number of molecules to process (0 = all)")
    args = parser.parse_args()

    entries = load_smiles_file(args.smiles_file)
    if args.max_mols > 0:
        entries = entries[:args.max_mols]

    out_dir = Path(args.output_dir)
    ligands_dir = out_dir / "ligands"
    ligands_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failed = []

    for i, (smiles, name) in enumerate(entries, 1):
        sdf_path = ligands_dir / f"{name}.sdf"
        if sdf_path.exists():
            print(f"[SKIP {i}/{len(entries)}] {name} already exists")
            success_count += 1
            continue

        mol, ok = build_3d_molecule(smiles, name, args.random_seed)
        if ok:
            with SDWriter(str(sdf_path)) as writer:
                writer.write(mol)
            success_count += 1
            print(f"[OK {i}/{len(entries)}] {name} -> {sdf_path.name}")
        else:
            failed.append((name, smiles))
            print(f"[FAIL {i}/{len(entries)}] {name}")

    summary_path = out_dir / "step1_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("SMILES to SDF completed\n")
        f.write(f"Input file: {args.smiles_file}\n")
        f.write(f"Successful: {success_count}/{len(entries)}\n")
        f.write(f"Output directory: {ligands_dir}\n")
        f.write("Failed entries:\n")
        for name, smiles in failed:
            f.write(f"{name}\t{smiles}\n")

    print(f"Done: {success_count}/{len(entries)} succeeded, {len(failed)} failed")
    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()
```

---

## scripts/prepare_ligand.py

```python
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
    """Convert one SDF ligand into PDBQT using Meeko, with Open Babel fallback."""
    try:
        mol = Chem.SDMolSupplier(str(sdf_path), removeHs=False)[0]
        if mol is None:
            print(f"Could not read SDF: {sdf_path}")
            return False

        preparator = MoleculePreparation()
        setup_list = preparator.prepare(mol)
        preparator.write_pdbqt_file(out_pdbqt, setup_list)
        return True
    except Exception as e:
        print(f"Meeko failed for {Path(sdf_path).name}, fallback to Open Babel: {e}")
        cmd = f'obabel "{sdf_path}" -O "{out_pdbqt}" --partialcharge gasteiger -h'
        result = subprocess.run(cmd, shell=True, capture_output=True)
        return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Batch ligand preparation: SDF to PDBQT")
    parser.add_argument("--sdf_dir", required=True, help="Input SDF directory")
    parser.add_argument("--output_dir", required=True, help="Output PDBQT directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output files")
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
            print(f"[SKIP {i}/{len(sdf_files)}] {name} already exists")
            success_count += 1
            continue

        ok = sdf_to_pdbqt(str(sdf_path), str(pdbqt_path))
        if ok:
            success_count += 1
            print(f"[OK {i}/{len(sdf_files)}] {name}")
        else:
            failed.append(name)
            print(f"[FAIL {i}/{len(sdf_files)}] {name}")

    print(f"Done: {success_count}/{len(sdf_files)} succeeded, {len(failed)} failed")
    if failed:
        print("Failed ligands:", ", ".join(failed))


if __name__ == "__main__":
    main()
```

---

## scripts/prepare_protein.py

```python
#!/usr/bin/env python3
"""
Step 2b: Receptor preparation from PDB to PDBQT.
Usage:
    python prepare_protein.py --protein 8V1R.pdb --output_dir ./step2
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
    """Keep only standard amino-acid residues and remove waters."""
    def accept_residue(self, residue):
        if residue.get_id()[0] == "W":
            return False
        return residue.get_resname() in STANDARD_RESIDUES


def parse_pocket_from_ligand(pdb_path: str, ligand_chain: str = None, ligand_resname: str = None, padding: float = 10.0) -> dict:
    """Estimate docking box coordinates from a co-crystallized ligand."""
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
    """Clean protein PDB and convert it to PDBQT using Open Babel."""
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
        raise RuntimeError(result.stderr)

    return str(out_pdbqt)


def main():
    parser = argparse.ArgumentParser(description="Prepare receptor: PDB to PDBQT")
    parser.add_argument("--protein", required=True, help="Input protein PDB file")
    parser.add_argument("--output_dir", required=True, help="Output directory")
    parser.add_argument("--ligand_chain", default="", help="Ligand chain ID for pocket estimation")
    parser.add_argument("--ligand_resname", default="", help="Ligand residue name for pocket estimation")
    parser.add_argument("--pocket_padding", type=float, default=10.0, help="Padding in angstroms")
    parser.add_argument("--output_pocket", default="", help="Optional output text file for the computed pocket string")
    args = parser.parse_args()

    pdbqt_path = prepare_protein(args.protein, args.output_dir)
    print(f"Protein prepared: {pdbqt_path}")

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
        print(f"Pocket: {pocket_str}")
        if args.output_pocket:
            with open(args.output_pocket, "w", encoding="utf-8") as f:
                f.write(pocket_str + "\n")
            print(f"Pocket saved to: {args.output_pocket}")


if __name__ == "__main__":
    main()
```

---

## scripts/batch_docking.py

```python
#!/usr/bin/env python3
"""
Step 3: Batch AutoDock Vina docking.
Usage:
    python batch_docking.py --protein_pdbqt protein.pdbqt --ligand_pdbqt_dir ligands/ \
        --pocket "center_x=10.5 center_y=20.3 center_z=-5.2 size_x=22 size_y=22 size_z=22" \
        --output_dir ./step3
"""

import argparse
import os
import re
import shlex
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


def find_vina(vina_path: str = "") -> str:
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
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return candidate
    result = subprocess.run(["which", "vina"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def parse_pocket(pocket_str: str) -> dict:
    pattern = r"center_x\s*=\s*([-\d.]+)\s+center_y\s*=\s*([-\d.]+)\s+center_z\s*=\s*([-\d.]+)\s+size_x\s*=\s*([\d.]+)\s+size_y\s*=\s*([\d.]+)\s+size_z\s*=\s*([\d.]+)"
    m = re.search(pattern, pocket_str, re.IGNORECASE)
    if not m:
        raise ValueError("Could not parse pocket string")
    return {
        "cx": float(m.group(1)),
        "cy": float(m.group(2)),
        "cz": float(m.group(3)),
        "sx": float(m.group(4)),
        "sy": float(m.group(5)),
        "sz": float(m.group(6)),
    }


def write_vina_config(protein_pdbqt: str, ligand_pdbqt: str, pocket: dict, config_path: str, num_modes: int = 9, exhaustiveness: int = 8):
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
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ligand_out_dir), timeout=600)
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
        return name, 999.0, "Timeout (600 s)"
    except Exception as e:
        return name, 999.0, str(e)


def main():
    parser = argparse.ArgumentParser(description="Batch AutoDock Vina docking")
    parser.add_argument("--protein_pdbqt", required=True)
    parser.add_argument("--ligand_pdbqt_dir", required=True)
    parser.add_argument("--pocket", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--exhaustiveness", type=int, default=8)
    parser.add_argument("--num_modes", type=int, default=9)
    parser.add_argument("--cpu", type=int, default=0)
    parser.add_argument("--vina_path", default="")
    parser.add_argument("--max_workers", type=int, default=4)
    args = parser.parse_args()

    vina_bin = find_vina(args.vina_path)
    if not vina_bin:
        raise SystemExit("AutoDock Vina executable not found")

    ligand_pdbqts = sorted(Path(args.ligand_pdbqt_dir).glob("*.pdbqt"))
    if not ligand_pdbqts:
        raise SystemExit("No ligand PDBQT files found")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tasks = [
        (args.protein_pdbqt, str(lp), args.pocket, str(out_dir), args.exhaustiveness, args.num_modes, args.cpu, vina_bin)
        for lp in ligand_pdbqts
    ]

    results = []
    with ProcessPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {executor.submit(run_vina_single, t): t for t in tasks}
        done = 0
        for future in as_completed(futures):
            done += 1
            name, aff, err = future.result()
            results.append((name, aff, err))
            if err:
                print(f"[FAIL {done}/{len(tasks)}] {name}: {err}")
            else:
                print(f"[OK {done}/{len(tasks)}] {name}: {aff:.2f} kcal/mol")

    results.sort(key=lambda x: x[1])
    summary_path = out_dir / "batch_summary.csv"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("rank,ligand_name,affinity_kcal_mol,status\n")
        for rank, (name, aff, err) in enumerate(results, 1):
            status = "OK" if not err else f"FAIL: {err}"
            f.write(f"{rank},{name},{aff:.3f},{status}\n")

    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()
```

---

## scripts/rank_results.py

```python
#!/usr/bin/env python3
"""
Step 4: Parse docking scores, rank ligands, and export Top-N complexes.
Usage:
    python rank_results.py --docking_dir ./step3 --protein_pdb 8V1R.pdb --top_n 10 --output_dir ./step4
"""

import argparse
import csv
import subprocess
from pathlib import Path


def parse_vina_log(log_path: Path) -> list[dict]:
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
    cmd = f'obabel "{protein_pdb}" "{ligand_pdb}" -O "{out_complex}" --sort'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.returncode == 0


def export_top_complexes(docking_dir: Path, protein_pdb: str, ranked_results: list[tuple], top_n: int, output_dir: Path) -> list[str]:
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

    return exported


def main():
    parser = argparse.ArgumentParser(description="Rank docking results and export Top-N complexes")
    parser.add_argument("--docking_dir", required=True)
    parser.add_argument("--protein_pdb", required=True)
    parser.add_argument("--top_n", type=int, default=10)
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()

    docking_dir = Path(args.docking_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ligand_dirs = [d for d in docking_dir.iterdir() if d.is_dir()]
    if not ligand_dirs:
        raise SystemExit("No ligand subdirectories found in docking_dir")

    all_results = []
    for lig_dir in ligand_dirs:
        name = lig_dir.name
        log_files = list(lig_dir.glob("vina_log.txt"))
        if not log_files:
            continue
        log_path = log_files[0]
        modes = parse_vina_log(log_path)
        if not modes:
            continue
        best_mode = min(modes, key=lambda m: m["affinity_kcal_mol"])
        aff = best_mode["affinity_kcal_mol"]
        all_results.append((name, aff, log_path, best_mode))

    all_results.sort(key=lambda x: x[1])

    csv_path = out_dir / "docking_scores.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "ligand_name", "affinity_kcal_mol", "mode", "rmsd_lb", "rmsd_ub"])
        for rank, (name, aff, _log_path, mode) in enumerate(all_results, 1):
            writer.writerow([rank, name, f"{aff:.3f}", mode["mode"], f"{mode['rmsd_lb']:.3f}", f"{mode['rmsd_ub']:.3f}"])

    summary_path = out_dir / "docking_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("Docking ranking summary\n")
        f.write(f"Docking directory: {docking_dir}\n")
        f.write(f"Protein: {args.protein_pdb}\n")
        f.write(f"Ligands ranked: {len(all_results)}\n")
        if all_results:
            affs = [r[1] for r in all_results]
            f.write(f"Affinity range: {min(affs):.2f} to {max(affs):.2f} kcal/mol\n")
            f.write(f"Mean affinity: {sum(affs)/len(affs):.2f} kcal/mol\n")

    exported = export_top_complexes(docking_dir, args.protein_pdb, all_results, args.top_n, out_dir)
    print(f"Ranked results saved to: {csv_path}")
    print(f"Summary saved to: {summary_path}")
    print(f"Exported Top-N complexes: {len(exported)}")


if __name__ == "__main__":
    main()
```

---

## scripts/main.py

```python
#!/usr/bin/env python3
"""
Main entry point for the end-to-end docking workflow.
Steps:
1. SMILES -> SDF
2. SDF/PDB -> PDBQT
3. Batch AutoDock Vina docking
4. Ranking and structure export
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()


def step1_smiles_to_sdf(smiles_file: str, output_dir: str) -> str:
    script = SCRIPT_DIR / "smiles_to_sdf.py"
    cmd = [sys.executable, str(script), "--smiles_file", smiles_file, "--output_dir", output_dir]
    subprocess.run(cmd, check=True)
    return output_dir


def step2_prepare(sdf_dir: str, protein_pdb: str, output_dir: str) -> tuple[str, str]:
    lig_script = SCRIPT_DIR / "prepare_ligand.py"
    lig_out = os.path.join(output_dir, "ligands")
    subprocess.run([sys.executable, str(lig_script), "--sdf_dir", sdf_dir, "--output_dir", lig_out], check=True)

    prot_script = SCRIPT_DIR / "prepare_protein.py"
    subprocess.run([sys.executable, str(prot_script), "--protein", protein_pdb, "--output_dir", output_dir], check=True)

    prot_pdbqt = os.path.join(output_dir, "protein_prepared.pdbqt")
    return prot_pdbqt, lig_out


def step3_batch_dock(protein_pdbqt: str, ligand_pdbqt_dir: str, pocket: str, output_dir: str, exhaustiveness: int, cpu: int, vina_path: str, max_workers: int) -> str:
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
    cmd = [sys.executable, str(script), "--docking_dir", docking_dir, "--protein_pdb", protein_pdb, "--top_n", str(top_n), "--output_dir", output_dir]
    subprocess.run(cmd, check=True)
    return output_dir


def main():
    parser = argparse.ArgumentParser(description="End-to-end docking workflow: SMILES -> SDF -> PDBQT -> Vina -> ranking")
    parser.add_argument("--protein", required=True, help="Protein PDB file path")
    parser.add_argument("--smiles_file", required=True, help="SMILES input file")
    parser.add_argument("--pocket", required=True, help="Docking box string")
    parser.add_argument("--output_dir", default="./docking_results", help="Root output directory")
    parser.add_argument("--top_n", type=int, default=10, help="Number of top complexes to export")
    parser.add_argument("--exhaustiveness", type=int, default=8, help="Vina exhaustiveness")
    parser.add_argument("--cpu", type=int, default=0, help="CPU cores per Vina process (0 = all)")
    parser.add_argument("--max_workers", type=int, default=4, help="Parallel worker count")
    parser.add_argument("--vina_path", default="", help="Optional Vina binary path")
    parser.add_argument("--skip_step1", action="store_true")
    parser.add_argument("--skip_step2", action="store_true")
    parser.add_argument("--skip_step3", action="store_true")
    parser.add_argument("--skip_step4", action="store_true")
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

    if args.skip_step1:
        if not args.sdf_dir:
            raise ValueError("--skip_step1 requires --sdf_dir")
        sdf_dir = args.sdf_dir
    else:
        print("=== Step 1: SMILES -> SDF ===")
        sdf_dir = step1_smiles_to_sdf(args.smiles_file, str(step1_dir))

    if args.skip_step2:
        if not args.prep_dir:
            raise ValueError("--skip_step2 requires --prep_dir")
        prot_pdbqt = os.path.join(args.prep_dir, "protein_prepared.pdbqt")
        lig_pdbqt_dir = os.path.join(args.prep_dir, "ligands")
    else:
        print("=== Step 2: SDF/PDB -> PDBQT ===")
        prot_pdbqt, lig_pdbqt_dir = step2_prepare(sdf_dir, args.protein, str(step2_dir))

    if args.skip_step3:
        if not args.dock_dir:
            raise ValueError("--skip_step3 requires --dock_dir")
        dock_dir = args.dock_dir
    else:
        print("=== Step 3: Batch docking ===")
        dock_dir = step3_batch_dock(
            prot_pdbqt,
            lig_pdbqt_dir,
            args.pocket,
            str(step3_dir),
            args.exhaustiveness,
            args.cpu,
            args.vina_path,
            args.max_workers,
        )

    if args.skip_step4:
        if not args.rank_dir:
            raise ValueError("--skip_step4 requires --rank_dir")
        rank_dir = args.rank_dir
    else:
        print("=== Step 4: Ranking and export ===")
        rank_dir = step4_rank(dock_dir, args.protein, args.top_n, str(step4_dir))

    print("Workflow completed")
    print(f"Ranked CSV: {rank_dir}/docking_scores.csv")
    print(f"Top structures: {rank_dir}/")


if __name__ == "__main__":
    main()
```
