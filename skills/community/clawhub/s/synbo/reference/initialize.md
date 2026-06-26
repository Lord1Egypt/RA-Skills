## Initialize

The `initialize.py` script is used for initial sampling without previous reaction data. This is the starting point for Bayesian optimization when NO experimental results are available yet.

**Script Location:** `scripts/initialize.py`

**Prerequisites:**
- Working directory and project name configured in `config.json`
- Reaction space data in `project_wd/rxn_space` directory
- Condition descriptors in `project_wd/descriptors` directory
- Optimization settings file (`optimization_settings.json`) in `project_wd` directory

**Usage:**
```bash
python scripts/initialize.py --project-dir <project_directory>
```

**Key Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--project-dir` | Required | Project directory containing configuration files |
| `--name-suffix` | `_RDKit` | Name suffixes for descriptor files |
| `--index-col` | `name` | Index column for descriptor files |
| `--batch-size` | `5` | Number of initial samples to generate |
| `--desc-normalize` | `minmax` | Descriptor normalization method (`minmax`, `zscore`, `l2`) |
| `--sampling-method` | `lhs` | Sampling strategy (`sobol`, `random`, `lhs`, `kmeans`) |
| `--random-seed` | `42` | Random seed for reproducibility |
| `--quiet` | - | Suppress verbose output |

**Examples:**
```bash
# Initialize with default settings
python scripts/initialize.py --project-dir examples

# Initialize with custom batch size and sampling method
python scripts/initialize.py --project-dir examples \
    --batch-size 5 --sampling-method lhs
```

**Workflow Steps:**
1. Load optimization settings from `optimization_settings.json`
2. Load descriptors from `project_wd/descriptors` directory
3. Create `ReactionOptimizer` instance with `opt_type="init"`
4. Load reaction space
5. Load descriptors
6. Run initialization with sampling (initial design generation)
7. Save recommended conditions to `project_wd/results` directory

**Output:**
- Excel file (`batch-0_yyyymmdd.xlsx`) containing recommended experimental conditions

**ATTENTION:** You should send the Excel file to USER and ask them to run the experiments with the recommended conditions.