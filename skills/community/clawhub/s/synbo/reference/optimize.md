## Optimize

The `optimize.py` script runs Bayesian optimization with previous reaction data to recommend new experimental conditions. This is used after initial sampling or previous optimization rounds.

**Script Location:** `scripts/optimize.py`

**Prerequisites:**
- Working directory and project name configured in `config.json`
- Reaction space data in `project_wd/rxn_space` directory
- Condition descriptors in `project_wd/descriptors` directory
- Optimization settings file (`optimization_settings.json`) in `project_wd` directory
- Previous reaction data in CSV format in `project_wd/results` directory
- The reaction results provided by the user should be written into the 'project_wd/results' file, in the one with the largest batch_id. Ensure that there is no [exp_data] in all csv files of results. If there is, inform the user of the missing information of the xxx reaction.

**Usage:**
```bash
python scripts/optimize.py --project-dir <project_directory>
```

**Key Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--project-dir` | Required | Project directory containing configuration files |
| `--input-dir` | `results` | Directory containing previous reaction data (relative to project-dir) |
| `--output-dir` | `results` | Output directory for results (relative to project-dir) |
| `--name-suffix` | `_RDKit` | Name suffixes for descriptor files |
| `--index-col` | `name` | Index column for descriptor files |
| `--batch-size` | `5` | Number of new conditions to recommend |
| `--desc-normalize` | `zscore` | Descriptor normalization method (`minmax`, `zscore`, `l2`) |
| `--optimize-method` | `default_BO` | Optimization algorithm to use |
| `--accuracy` | `medium` | Optimization accuracy level (`tiny`, `low`, `medium`, `high`, `ultra`). Lower values are faster and use less memory |
| `--acq-func` | `EHVI` | Acquisition function (`EHVI`, `UCB`, `ParEGO`, `NEI`) |
| `--random-seed` | `42` | Random seed for reproducibility |
| `--quiet` | - | Suppress verbose output |

**Examples:**
```bash
# Optimize with default settings
python scripts/optimize.py --project-dir examples

# Optimize with custom batch size
python scripts/optimize.py --project-dir examples \
    --batch-size 5

# Faster optimization for large search spaces
python scripts/optimize.py --project-dir examples \
    --accuracy low
```

**Timeout Handling:**
If optimization times out or is too slow, first reduce the accuracy level. Prefer `low` first, then `tiny` if `low` still cannot finish:
```bash
python scripts/optimize.py --project-dir examples --accuracy low
python scripts/optimize.py --project-dir examples --accuracy tiny
```

If optimization still times out with `--accuracy tiny`, switch the acquisition function to `UCB`, which is usually cheaper to evaluate:
```bash
python scripts/optimize.py --project-dir examples \
    --accuracy tiny \
    --acq-func UCB
```

**Workflow Steps:**
1. Load optimization settings from `optimization_settings.json`
2. Load descriptors from `project_wd/descriptors` directory
3. Create `ReactionOptimizer` instance with `opt_type="auto"`
4. Load reaction space
5. Load descriptors
6. Load previous reaction data from `project_wd/results` directory
7. Run Bayesian optimization to recommend new conditions
8. Save recommended conditions to `project_wd/results` directory

**Input Data Format:**
Previous reaction data should be stored in `project_wd/results` directory as `batch-*.csv` files. Each file should contain columns corresponding to:
- Reagent types (matching those specified in `optimization_settings.json`)
- Optimization metrics (matching those defined in `optimization_settings.json`)
- `batch` column indicating batch numbers

**Output:**
- Excel file (`batch-x_yyyymmdd.xlsx`) containing recommended experimental conditions
- Summary including number of exploit vs explore recommendations
- Results saved to the `project_wd/results` directory


**ATTENTION:** You should send the Excel file to USER and ask them to run the experiments with the recommended conditions.

**ATTENTION:** Optimize could cost a lot of time. The Timeout period should be more than 10 min. If it times out, try `--accuracy low`, then `--accuracy tiny`, and finally `--acq-func UCB`.
