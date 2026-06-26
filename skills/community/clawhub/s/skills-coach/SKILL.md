---
name: skills-coach
description: Explore capability boundaries of a target Skill, analyze optimization potential, generate an optimized version using Training-Free GRPO, and compile results into a structured report
version: 2.3.1
trigger: |
  Use when user asks to:
  - Improve, enhance, fix, or optimize an existing Skill
  - Identify weaknesses or limitations of a Skill
  - Compare performance between original and improved Skill versions
  - Generate a structured report on Skill quality and optimization
---

# Skills-Coach v2.3.1

Systematically analyze and optimize OpenClaw skills through automated task generation, **Training-Free GRPO optimization**, real command execution, comprehensive failure analysis, and detailed evaluation reporting.

## What's New in v2.3.1

- 📝 **Documentation Consistency** — Unified version numbers across all files
- 🗂️ **File Organization** — Cleaned up archive directory and removed duplicates
- 🔧 **Maintenance Release** — Bug fixes and documentation improvements

Previous updates (v2.3.0):
- 🔧 **Auto-Fix Integration** — Automatically fixes common issues
- 🔄 **Iterative Improvement** — Fix → Test → Reanalyze loop (max 2 iterations)
- 🤖 **LLM-Powered Fixes** — Uses Claude API to intelligently add missing parameters
- ⚡ **Optimized Performance** — Disabled LLM summaries to prevent API timeouts
- 🔧 **Better Stability** — Improved API timeout handling and retry mechanisms

Previous updates (v2.0.0):
- 🚀 **Training-Free GRPO** — Revolutionary optimization method based on arXiv:2510.08191
- 🧠 **Experience Library** — Learns from optimization attempts
- 📊 **Group Relative Semantic Advantage** — Compares rollouts to extract insights
- 💰 **Cost-Effective** — Minimal training data, no fine-tuning required

## Training-Free GRPO vs Vanilla GRPO

| Feature | Training-Free GRPO (v2.0) | Vanilla GRPO (v1.x) |
|---------|---------------------------|---------------------|
| Parameter Updates | ❌ None | ✅ Gradient-based |
| Advantage Type | Semantic (natural language) | Numerical (scores) |
| Knowledge Storage | External experience library | Model weights |
| Generalization | Excellent (frozen model) | Limited (overfitting risk) |
| Data Requirements | Minimal (dozens of samples) | Large (thousands) |
| Cost | Very low (~$20) | High ($10,000+) |
| Speed | Fast (inference only) | Slow (training required) |

## Configuration Options

Key settings in `config.yaml`:

```yaml
# Optimization Method Selection (NEW v2.0.0)
optimization:
  method: "training_free_grpo"  # training_free_grpo | vanilla_grpo

# Training-Free GRPO Parameters
training_free_grpo:
  group_size: 5                  # Number of rollouts per group
  num_epochs: 3                  # Number of optimization epochs
  temperature_learning: 0.7      # Temperature during learning
  temperature_eval: 0.3          # Temperature during evaluation
  
  # Experience Library Management
  max_experiences: 10            # Max experiences per domain
  
  # Domain-Specific Optimization
  markdown_optimization:
    enabled: true
    focus_areas: [clarity, structure, examples, completeness]
  
  code_optimization:
    enabled: true
    focus_areas: [bug_fixes, error_handling, performance, code_quality]
  
  # LLM Configuration
  llm_model: "claude-sonnet-4-6"
```

## Usage

```bash
python orchestrator.py <target-skill-path>
```

Or via Claude:
```
Use skills-coach on <target-skill-path>
```

## Parameters

- `target-skill-path` (required): Path to the directory containing the Skill to analyze and optimize. Must contain a valid `SKILL.md`.

## Execution Flow

This skill orchestrates 6 steps that execute sequentially:

```
immutability → code-capability → sample-agent → optimize-agent → exec-agent → failure-analyzer → evaluate-agent
```

**CRITICAL IMMUTABILITY RULE:**
- The original {target-skill} is NEVER modified
- All changes are made to {target-skill}-optimized
- This ensures the original skill remains intact for comparison

**Do not proceed to the next step until the current one has fully completed and its outputs are verified.**

## Step-by-Step Instructions

### Pre-flight Checks

1. Validate that `target-skill-path` exists and contains a `SKILL.md` file
2. If validation fails, abort and report the error to the user
3. Initialize run manager (if versioned runs enabled):
   ```python
   from subskills.run-manager.run_manager import RunManager
   manager = RunManager()
   run_dir = manager.create_run(target_skill_path, config)
   ```
4. Create the working directory structure:
   ```
   # If versioned runs enabled:
   skills-coach-runs/run_YYYY-MM-DD_HH-MM-SS/
     ├── tasks/{train,test}
     ├── exec_results/{original,optimized}
     ├── optimization/
     ├── code_capabilities.json
     ├── failure_analysis_{original,optimized}.json
     └── {target-skill}-optimized/
   ```
5. **IMMUTABILITY: Create optimized copy**
   ```bash
   cp -r {target-skill} {work-dir}/{target-skill}-optimized
   ```
   All subsequent modifications will ONLY affect the optimized copy.

### Step 0: Code Capability Detection (NEW v1.5.0)

Analyze scripts to detect their actual capabilities:

```bash
cd subskills/code-capability-detector
python code_capability_detector.py <target-skill-path> <work-dir>
```

This analyzes:
- Command-line parameters supported by scripts
- Input/output formats
- Dependencies
- Error handling and validation presence

**Expected outputs:**
- `code_capabilities.json` - Machine-readable capability data
- `code_capabilities.md` - Human-readable report

**Purpose:** Ensures generated test tasks only use features the scripts actually support.

**Verification:** Confirm capability files exist before proceeding.

### Step 1: Generate Test Tasks (sample-agent)

Execute the task generator:

```bash
cd subskills/sample-agent
python task_generator.py <target-skill-path> ../..
```

The script generates:
- 12 base training tasks (6 standard + 6 advanced)
- 8 base test tasks (4 standard + 4 advanced)
- If boundary probing is enabled and generates boundary tasks:
  - Training: 6 standard + 4 advanced + 6 boundary = 16 total
  - Test: 4 standard + 3 advanced + 3 boundary = 10 total

**Expected outputs:**
- `tasks/train/task_001/` through `tasks/train/task_012/` (or task_016 with boundary tasks)
- `tasks/test/task_001/` through `tasks/test/task_008/` (or task_010 with boundary tasks)
- Each task directory contains: `task.md`, `speccheck.md`, and `workspace/`

**Verification:** Confirm all task directories exist before proceeding.

### Step 2: Optimize the Skill (optimize-agent)

**IMPORTANT:** This step works on `{target-skill}-optimized`, NOT the original.

Execute the GRPO optimizer:

```bash
cd subskills/optimize-agent
python grpo_optimizer.py <work-dir>/{target-skill}-optimized ../..
```

The script runs GRPO optimization with:
- 4 candidate variants per iteration
- 3-10 iterations with early stopping
- SKILL.md and optional code-level optimization
- All changes applied to the optimized copy only

**Expected outputs:**
- `{target-skill-name}-optimized/` directory containing the optimized `SKILL.md`
- `optimization_log.md` documenting the GRPO optimization process

**Verification:** Confirm the optimized skill directory and log file exist before proceeding.

### Step 3: Execute Both Skill Versions (exec-agent + Claude)

**Part A: Generate Task Manifest**

Execute the executor to generate task manifest:

```bash
cd subskills/exec-agent
python executor.py <target-skill-path> ../..
```

**Expected outputs:**
- `task_manifest.json` containing all tasks to execute

**Part B: Execute Tasks via Skill Tool**

Claude reads the manifest and executes each task using the Skill tool:

```python
import json
manifest = json.load(open('task_manifest.json'))

for task in manifest['tasks']:
    # Execute original skill
    Use skill at manifest['target_skill_path'] with task['task_content']
    Save output to task['original_result_dir']/output/
    
    # Execute optimized skill
    Use skill at manifest['optimized_skill_path'] with task['task_content']
    Save output to task['optimized_result_dir']/output/
```

**Expected outputs:**
- `exec_results/original/task_001/` through `exec_results/original/task_010/`
- `exec_results/optimized/task_001/` through `exec_results/optimized/task_010/`
- Each result directory contains: `output/` with real skill execution results and `run_log.md`

**Verification:** Confirm all result directories exist with real outputs before proceeding.

### Step 4: Failure Analysis (NEW v1.5.0)

Analyze failed tasks to identify root causes and suggest fixes:

```bash
cd subskills/failure-analyzer
python failure_analyzer.py <work-dir>/exec_results/original <work-dir>
python failure_analyzer.py <work-dir>/exec_results/optimized <work-dir>
```

This analyzes:
- Error messages and categorizes them (missing_parameter, missing_dependency, etc.)
- Root causes of failures
- Specific fix suggestions with code examples
- Affected files and estimated fix difficulty

**Expected outputs:**
- `failure_analysis_original.json` - Machine-readable failure data
- `failure_analysis_original.md` - Human-readable report
- `failure_analysis_optimized.json` - Optimized version failures
- `failure_analysis_optimized.md` - Optimized version report

**Verification:** Confirm failure analysis files exist before proceeding.

### Step 5: Evaluate and Report (evaluate-agent)

Execute the evaluator to analyze results:

```bash
cd subskills/evaluate-agent
python evaluator.py <target-skill-path> <work-dir>
```

This script:
1. Analyzes execution results from both skill versions
2. Generates the comprehensive report
3. Makes retention decision based on performance comparison

**Expected outputs:**
- `results_report.md` containing comprehensive evaluation metrics and analysis
- Retention decision: either keep or delete `{target-skill-name}-optimized/`

**Verification:** Confirm `results_report.md` exists.

### Final Step: Present Results to User

Read and present the contents of `results_report.md` to the user, highlighting:
- Overall performance comparison (original vs. optimized)
- Key strengths and weaknesses identified
- Retention decision and rationale
- Recommendations for further improvement

## Output Structure

**Versioned Runs (Default)**:
```
skills-coach-runs/
├── run_2026-04-13_14-30-00/
│   ├── config.yaml                    # Config used for this run
│   ├── metadata.json                  # Run metadata (duration, scores, decision)
│   ├── tasks/
│   │   ├── train/                     # 12-16 training tasks (depends on boundary probing)
│   │   └── test/                      # 8-10 test tasks (depends on boundary probing)
│   ├── optimization/
│   │   ├── iteration_001/
│   │   │   ├── variant_a/
│   │   │   ├── variant_b/
│   │   │   ├── variant_c/
│   │   │   └── variant_d/
│   │   └── iteration_002/
│   ├── exec_results/
│   │   ├── original/                  # 10 tasks
│   │   └── optimized/                 # 10 tasks
│   ├── optimization_log.md
│   ├── results_report.md
│   └── {target-skill}-optimized/      # If retained
│
├── run_2026-04-13_15-45-00/
│   └── ... (same structure)
│
└── latest -> run_2026-04-13_15-45-00/ # Symlink to latest run
```

**Legacy Flat Structure (if versioned runs disabled)**:
```
./
├── tasks/
│   ├── train/          # 12-16 training tasks (depends on boundary probing)
│   └── test/           # 8-10 test tasks (depends on boundary probing)
├── exec_results/
│   ├── original/       # 8-10 tasks
│   └── optimized/      # 8-10 tasks
├── {target-skill}-optimized/  # If retained
├── optimization_log.md
└── results_report.md
```

## Configuration

Features can be controlled via `config.yaml`:

```yaml
# Task generation
task_generation:
  num_training_tasks: 16          # 12 for legacy mode
  num_test_tasks: 10              # 8 for legacy mode
  probe_boundaries: true          # Set to false for legacy 20-task mode
  boundary_types:
    - input_minimal
    - input_maximal
    - input_invalid
    - resource_limits
    - failure_modes
    - combinations

# GRPO optimization
grpo:
  optimization_levels:
    - skill_md                    # Always enabled
    - code                        # Remove to disable code optimization
    - config                      # Remove to disable config optimization
  code_mutations:
    - add_caching
    - add_validation
    - add_error_handling
    - optimize_algorithm

# Output structure
output:
  use_versioned_runs: true        # Set to false for legacy flat structure
  runs_directory: "skills-coach-runs"
  keep_latest_symlink: true
  max_runs_to_keep: 10            # Auto-cleanup old runs
  save_intermediate_variants: true
  save_execution_logs: true
  save_metadata: true

# Run comparison
comparison:
  enable_comparison_tool: true
  auto_compare_with_previous: true
  comparison_metrics:
    - baseline_score
    - final_score
    - improvement
    - duration
    - iterations
```

## Run Management Commands

Use run-manager CLI for analysis:

```bash
# List all runs
python subskills/run-manager/run_manager.py list

# Compare two runs
python subskills/run-manager/run_manager.py compare run_2026-04-13_14-30-00 run_2026-04-13_15-45-00

# Cleanup old runs (keep latest 10)
python subskills/run-manager/run_manager.py cleanup 10
```

## Error Handling

- If any subskill fails, stop execution and report the error to the user
- If `sample-agent` cannot parse the target `SKILL.md`, abort before task generation
- If `optimize-agent` fails to improve scores after 10 iterations, proceed with the best variant found
- If `exec-agent` encounters runtime errors, log them in `run_log.md` and continue with remaining tasks
- If `evaluate-agent` determines the optimized skill performs worse, delete the optimized directory

## Constraints

- All subskills operate autonomously without user input between steps
- The original target Skill is never modified in place
- SpecCheck evaluation must be deterministic
- No data leakage between train and test task sets
- GRPO optimization runs 3-10 iterations, stopping early if no improvement for 2 consecutive iterations
- v1.2.0: Generates 12-26 tasks depending on boundary probing:
  - Without boundary probing: 12 training + 8 test = 20 tasks
  - With boundary probing (if boundaries detected): 16 training + 10 test = 26 tasks
- Can optimize code files in addition to SKILL.md (if enabled in config)
- Creates versioned run directories (if enabled in config)

## Notes

- This is a meta-skill that operates on other skills
- Execution may take significant time depending on the complexity of the target skill
- The GRPO approach is training-free and does not require gradient computation
- All intermediate outputs are preserved for transparency and debugging
- Boundary probing tests capability limits with 6 types of edge cases
- Code optimization can modify Python/shell scripts in addition to SKILL.md
- Versioned runs preserve all optimization attempts for historical tracking
- Run comparison tool enables analysis of optimization strategies over time
