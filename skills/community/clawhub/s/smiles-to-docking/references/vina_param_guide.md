# AutoDock Vina Parameter Guide

## Core Parameters

| Parameter | Meaning | Typical Value |
|-----------|---------|---------------|
| `--exhaustiveness` | Search thoroughness; higher = slower but more accurate | 8 (fast screen) / 32 (refine) |
| `--num_modes` | Number of binding modes to output | 9 (default) / 1 (best only) |
| `--energy_range` | Max energy gap from best mode (kcal/mol) | 3.0 |
| `--cpu` | CPU cores per Vina process (0 = all) | 0 |

## Pocket Size Guidelines

- Box must be at least 5 Å larger than the ligand in each dimension.
- Minimum recommended size: 20 Å per dimension.
- Oversized boxes (> 30 Å per dimension) significantly increase runtime.
- Rule of thumb: each 5 Å increase in box size roughly doubles computation time.

## Batch Performance Tips

1. **Parallelism**: use `--max_workers N` to parallelize across ligands (N = number of CPU cores).
2. **CPU per process**: set `--cpu 1` when running many parallel Vina processes to avoid resource contention.
3. **Memory**: each ligand typically needs 200–500 MB; for 100+ ligands ensure >= 32 GB RAM.
4. **Timeout**: the default per-ligand timeout is 600 s; long-running ligands may be stuck in a bad pocket — consider lowering exhaustiveness.

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Cannot open output file` | Path with spaces or non-ASCII characters | Use quotes or ASCII-only paths |
| `Segmentation fault` | Malformed PDBQT | Re-generate PDBQT with Open Babel |
| All scores > -5 kcal/mol | Pocket location wrong | Recompute pocket from co-crystal ligand |
| Large score variance for same ligand | `exhaustiveness` too low | Increase to 16 or 32 |
| `No space left on device` | Disk full | Free space or redirect output elsewhere |

## Affinity Interpretation

| Affinity (kcal/mol) | Binding strength |
|--------------------|-----------------|
| < -9 | Strong ✅ |
| -7 to -9 | Moderate to strong ✅ |
| -5 to -7 | Moderate ⚠️ |
| > -5 | Weak ❌ |

## Comparison with Other Tools

| Tool | Pros | Cons |
|------|------|------|
| AutoDock Vina | Open-source, fast, well-validated | No covalent docking |
| QuickVina 2 | 5–10× faster than Vina | Slightly lower accuracy |
| rDock | Fast, easy parallelization | Complex parameterization |
| PLANTS | Optimized for protein-ligand | Commercial license |