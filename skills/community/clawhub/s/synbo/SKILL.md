---
name: synbo
description: Bayesian optimization for chemical reactions using the synbo package. This skill provides Python scripts to set up reaction spaces, build descriptors, run optimization, download recommended conditions, and upload results.
---

# synbo

Bayesian optimization for chemical reactions using the `synbo` package. This skill provides Python scripts to set up reaction spaces, build descriptors, run optimization, download recommended conditions, and upload results.

---

## CRITICAL: BO Optimization Prerequisites

**Before executing ANY Bayesian Optimization (synbo) tasks, you MUST sequentially verify the following 5 prerequisites. Do NOT proceed with the optimization process until ALL criteria are met:**

**1. Find Conda Environment and `synbo` package**
- Verify if conda is installed in the current environment. If not, confirm with the user to install Miniconda (see [reference/installation.md](reference/installation.md)).
- Check if the `synbo_env` conda environment exists. If not, create it; if it exists, activate it.
- Verify if the `synbo` package is installed in `synbo_env`. If not, run `pip install synbo`

**2. Working Directory (`project_wd`) & Project Name (`project_name`)**
* **Initial Check:** Read `config.json` located in the skill's directory. If both `project_wd` and `project_name` are found, display the project name to the user (e.g., "Found existing project: [Project Name]") and use them.
* **If NOT found:** Stop and prompt the user to input a **Working Directory** and a **Project Name**.
* **Validation & Saving (CRITICAL):** Upon receiving the user's input:
    1. **Verify Path:** Check if the provided working directory actually exists on the local file system. If it does NOT exist, inform the user "The path is invalid/does not exist" and prompt them to re-enter it.
    2. **Sanitize & Save:** If the path exists, sanitize the project name (replace spaces and special characters with underscores). Then, immediately write/update the `config.json` file with this format: `{"project_wd": "xxx", "project_name": "xxx"}`.
    3. Use this path and sanitized project name to define the `save_dir` for all subsequent outputs.

**3. Reaction Space**
* **Check:** Verify if standard reaction space data exists specifically within the `project_wd/rxn_space` directory.
* **If NOT found:** Stop and prompt the user: "Reaction space data is missing in the `project_wd/rxn_space` directory. Please provide the standard reaction space data." Do not proceed until provided.

**4. Condition Descriptors**
* **Check:** Verify if the corresponding Condition Descriptors exist specifically within the `project_wd/descriptors` directory.
* **If NOT found:** Stop and prompt the user: "Condition Descriptors are missing in the `project_wd/descriptors` directory. Please provide the standard Condition Descriptors, OR let me know if you would like me to automatically generate them for you."

**5. Optimization Metrics**
* **Check:** Verify if the optimization settings file (e.g., `optimization_settings.json`) exists directly within the `project_wd` directory.
* **If NOT found:** Stop and prompt the user: "Optimization metrics are not defined. Please specify the target metrics you want to optimize (e.g., yield, ee), along with their optimization direction (max/min), expected numerical ranges, and relative weights (default 1.0)."
* **Validation & Saving (CRITICAL):** Upon receiving the user's optimization goals, format the data and immediately save it as `optimization_settings.json` in the `project_wd`. The JSON file MUST strictly adhere to the following structure:
```json
{
    "reagent_types": ["reagent1", "reagent2", "condition1", "condition2"],
    "opt_metrics": ["target1", "target2"],
    "opt_direct_info": [
        {
            "opt_direct": "max",
            "opt_range": [0, 100],
            "metric_weight": 1.0
        },
        {
            "opt_direct": "min",
            "opt_range": [0, 100],
            "metric_weight": 1.0
        }
    ]
}
```

**Execution Block:**
You are strictly forbidden from executing any initialization (`initialize`), optimization (`optimize`), or other synbo tasks until **Steps 1 through 4** are fully verified and resolved.

---

## Reaction Space

When the user is required to provide the reaction space data, they may submit it via one of two methods:
1. **Direct Input:** Providing the SMILES strings for the corresponding molecules directly in the chat.
2. **File Upload:** Providing tabular files containing the SMILES strings.

**Naming Conventions:** 
It is highly recommended that the user assigns a specific name to each molecule. If no names are provided, you must automatically assign names using a sequential format based on the reagent type: `{reagent_type}-1`, `{reagent_type}-2`, etc.

**Data Storage Rules:** 
Regardless of the user's submission method, all reaction space data must be formatted and saved strictly into the `project_wd/rxn_space` directory.
* Each reagent type must be saved as an individual file named `{reagent_type}.csv`.
* The CSV files must contain exactly two headers: `SMILES` (for the SMILES strings) and `name` (for the molecule names).

---

## Condition Descriptors

see `[reference/get_desc.md](reference/get_desc.md)`

---

## Initialize

see `[reference/initialize.md](reference/initialize.md)`

---

## Optimize

see `[reference/optimize.md](reference/optimize.md)`