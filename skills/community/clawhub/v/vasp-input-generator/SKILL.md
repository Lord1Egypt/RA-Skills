---
name: vasp-input-generator
description: Generate VASP DFT calculation input files (INCAR, KPOINTS, POSCAR, POTCAR). Use when Codex needs to create, modify, or validate VASP input files for: (1) Structural optimization, (2) Electronic structure calculations, (3) MD simulations, (4) Band structure calculations, (5) DOS calculations, or any other VASP-related tasks.
---

# VASP Input Generator

Generate complete VASP input files for density functional theory calculations.

## Quick Start

For a standard structural optimization:

```bash
python scripts/generate_vasp_inputs.py --type relaxation --structure POSCAR
```

## Input File Types

| File | Description | Script Support |
|------|-------------|----------------|
| INCAR | Calculation parameters | Full generation |
| KPOINTS | k-point mesh | Full generation |
| POSCAR | Structure file | Template generation |
| POTCAR | Pseudopotentials | Guidance only |

## Calculation Types

- **Relaxation**: `--type relaxation` - Structural optimization
- **Static**: `--type static` - Single-point energy
- **MD**: `--type md` - Molecular dynamics
- **Band**: `--type band` - Band structure
- **DOS**: `--type dos` - Density of states

## Parameter Reference

For detailed INCAR parameter descriptions, see [references/incar-parameters.md](references/incar-parameters.md).

## Best Practices

1. Always check `ENCUT` matches pseudopotential recommendations
2. Verify k-point density is appropriate for system size
3. For metals, use appropriate smearing (`ISMEAR = 1` or `2`)
4. For insulators, use `ISMEAR = 0` with small `SIGMA`
5. Set `ISPIN = 2` for magnetic systems

## Output

The generator creates:
- `INCAR` - Calculation parameters
- `KPOINTS` - k-point mesh
- `POSCAR.template` - Structure template (if no existing POSCAR)

POTCAR must be generated separately by concatenating pseudopotential files.
