# Skills-Coach v2.3.1

An intelligent skill optimization system that uses Training-Free GRPO (Generalized Reward Policy Optimization) to automatically improve skill documentation and implementation quality.

## 🆕 What's New in v2.3.1

- **Documentation Consistency**: Unified version numbers across all files
- **File Organization**: Cleaned up archive directory and removed duplicates
- **Maintenance Release**: Bug fixes and documentation improvements

Previous updates (v2.3.0):
- **Auto-Fix Integration**: Automatically fixes common issues (missing dependencies, parameters, etc.)
- **Iterative Improvement**: Fix → Test → Reanalyze loop (max 2 iterations)
- **LLM-Powered Fixes**: Uses Claude API to intelligently add missing parameters to scripts
- **Reduced Manual Intervention**: ~70% reduction in manual fixes needed for common issues

## Overview

Skills-Coach analyzes, optimizes, and evaluates skills through a multi-agent pipeline:

1. **Code Capability Detection** - Analyzes skill structure and capabilities
2. **Sample-Agent** - Generates comprehensive training and test tasks with multi-dimensional evaluation criteria
3. **Optimize-Agent** - Applies Training-Free GRPO optimization
4. **Exec-Agent** - Executes both original and optimized versions
5. **Failure-Analyzer** - Analyzes execution failures
6. **Auto-Fixer** - Automatically fixes common issues (NEW in v2.3.0)
7. **Evaluate-Agent** - Evaluates results with enhanced multi-dimensional criteria

## Key Features

### Training-Free GRPO Optimization
- No parameter updates required
- Uses experience library for semantic learning
- Separate strategies for markdown vs code optimization
- Rollout-based exploration with advantage extraction

### Enhanced Multi-Dimensional Evaluation

**8 Evaluation Dimensions (49+ criteria):**
1. Structural Completeness & Organization (7 criteria)
2. Practical Usability & Learnability (6 criteria)
3. Example Quality & Coverage (6 criteria)
4. Technical Depth & Accuracy (6 criteria)
5. Clarity & Readability (6 criteria)
6. Completeness of Command Coverage (6 criteria)
7. Error Handling & Troubleshooting (6 criteria)
8. Advanced Scenarios & Best Practices (6 criteria)

**Task Types:**
- Standard tasks: 5 criteria, 60% pass threshold
- Advanced tasks: 7 criteria, 57% pass threshold

### Evaluation Methods
- **Primary**: Deep LLM-based evaluation with structured JSON responses
- **Fallback**: Enhanced heuristic evaluation with dimension-specific checks
- **Evidence-based**: Each criterion includes detailed evidence and reasoning

## Quick Start

### Prerequisites

1. **Set up API key** (required):
   ```bash
   export ANTHROPIC_API_KEY='sk-ant-xxxxx'
   ```
   Get your API key from: https://console.anthropic.com/

2. **Install dependencies**:
   ```bash
   pip install anthropic psutil
   ```

### Basic Usage

```bash
# Optimize a single skill with prompt
Please optimize {skill-name} using Skills-Coach in Real Mode.

# Optimize a single skill
python3 orchestrator.py /path/to/skill

# Batch optimize multiple skills
./batch_optimize.sh /path/to/skills/directory
```

**Note**: If API key is not set, you'll be prompted to enter it during execution.

### Configuration

Edit `config.yaml` to customize:

```yaml
optimization:
  method: training_free_grpo  # or 'grpo'
  
grpo_execution:
  mode: real  # or 'simulated'
  
evaluation_execution:
  mode: real  # or 'simulated'
```

## Architecture

```
skills-coach/
├── orchestrator.py              # Main coordinator
├── config.yaml                  # Configuration
├── subskills/
│   ├── code-capability-detector/
│   ├── sample-agent/           # Task generation with 8 dimensions
│   │   ├── smart_task_generator.py
│   │   └── ...
│   ├── optimize-agent/         # Training-Free GRPO
│   │   ├── training_free_grpo_optimizer.py
│   │   ├── grpo_optimizer.py
│   │   └── ...
│   ├── exec-agent/             # Skill execution
│   ├── failure-analyzer/       # Failure analysis
│   └── evaluate-agent/         # Enhanced evaluation
│       └── evaluator.py
└── skills-coach-runs/          # Output directory
```

## Output Structure

Each run creates a timestamped directory:

```
skills-coach-runs/run_YYYY-MM-DD_HH-MM-SS/
├── results_report.md           # Comprehensive evaluation report
├── metadata.json               # Run metadata
├── tasks/
│   ├── train/                  # Training tasks (12 tasks)
│   └── test/                   # Test tasks (8 tasks)
├── exec_results/               # Execution outputs
└── [skill-name]-optimized/     # Optimized version (if retained)
```

## Evaluation Report

The results report includes:

- **Pass Rate**: Percentage of tasks passed
- **Per-Task Breakdown**: Detailed scores for each task
- **Criterion-Level Analysis**: Evidence for each evaluation criterion
- **Capability Boundary Analysis**: Strengths and weaknesses identified
- **Retention Decision**: Whether optimized version is kept or deleted
- **Recommendations**: Actionable improvement suggestions

## Recent Improvements (v2.0.0)

### Sample-Agent Enhancements
- Expanded from 4 to 8 evaluation dimensions
- 49+ detailed, measurable criteria
- Stricter thresholds: Standard 60%, Advanced 57%

### Evaluate-Agent Enhancements
- Enhanced LLM evaluation with 7-point guidelines
- Structured JSON responses with scores, evidence, strengths, weaknesses
- Multi-dimensional heuristic fallback with specific checks
- Score threshold: 70+ for satisfaction

### Results
- **Before**: 100% pass rate (too lenient)
- **After**: 50% pass rate with clear quality distinctions
- Can now identify specific improvement areas

## Examples

### Successful Optimization
```
Training Set: 48/60 → 60/60 (+20% improvement)
Test Set: Identifies specific gaps in documentation
```

### Quality Distinctions
```
Standard Tasks: 60% pass (3/5 criteria)
Advanced Tasks: 14% pass (1/7 criteria)
→ Clear capability boundaries identified
```

## Troubleshooting

### LLM Evaluation Unavailable
The system automatically falls back to enhanced heuristic evaluation with dimension-specific checks.

### Optimization Not Retained
This is expected when optimization doesn't generalize to test set. The system correctly identifies overfitting.

### Low Pass Rates
This indicates the evaluation is working correctly - it can now distinguish quality levels that were previously masked.

## Archive

Historical documentation and backup files are stored in:
- `archive/docs/` - Old documentation files
- `archive/backups/` - Backup and redundant implementation files

## Version History

- **v2.3.1** (2026-04-17): Documentation consistency and file organization
- **v2.3.0** (2026-04-16): Auto-fix integration and iterative improvement
- **v2.2.0** (2026-04-15): Enhanced task diversity and stability improvements
- **v2.1.0** (2026-04-15): Process monitoring and auto-termination
- **v2.0.0** (2026-04-15): Enhanced multi-dimensional evaluation system
- **v1.5.0**: Training-Free GRPO optimization
- **v1.0.0**: Initial release with basic GRPO

## License

Internal tool for skill optimization.
