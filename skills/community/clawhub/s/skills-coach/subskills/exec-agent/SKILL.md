---
name: exec-agent
description: Execute both original and optimized Skill versions against test tasks and capture outputs for evaluation
version: 1.0.0
---

# Exec-Agent

Execute both the original and optimized versions of the target Skill against all test tasks, capturing outputs and execution logs for subsequent evaluation.

## Purpose

Provide a fair, controlled comparison between skill versions by:
- Running both versions against identical test tasks
- Capturing all outputs, side effects, and errors
- Maintaining execution isolation between runs
- Preserving complete execution traces for analysis

## Inputs

- `target-skill-path`: Path to the original Skill directory
- `{target-skill-name}-optimized/`: Path to the optimized Skill directory
- Test tasks: `tasks/test/task_001/` through `tasks/test/task_008/`

## Execution Steps

### 1. Prepare Execution Environment

Create result directories:
```bash
mkdir -p exec_results/original
mkdir -p exec_results/optimized
```

### 2. Execute Original Skill

For each test task (`task_001` through `task_008`):

**A. Set Up Task Environment**

1. Create result directory: `exec_results/original/task_XXX/`
2. Create output directory: `exec_results/original/task_XXX/output/`
3. Copy task workspace to a temporary execution directory:
   ```bash
   cp -r tasks/test/task_XXX/workspace /tmp/exec_original_task_XXX
   ```

**B. Execute Skill**

1. Read `tasks/test/task_XXX/task.md` to understand the task requirements
2. Invoke the original skill from `{target-skill-path}/SKILL.md` with the task input
3. Execute in the temporary workspace directory
4. Capture:
   - All files created or modified in the workspace
   - Standard output and standard error
   - Execution time
   - Any errors or exceptions
   - Return values or exit codes

**C. Capture Outputs**

1. Copy all files from the temporary workspace to `exec_results/original/task_XXX/output/`
2. Write `exec_results/original/task_XXX/run_log.md`:

```markdown
# Execution Log: Original Skill - Task XXX

## Metadata
- **Task**: {task title from task.md}
- **Skill**: {original skill name}
- **Timestamp**: {ISO 8601 timestamp}
- **Execution Time**: {duration in seconds}
- **Status**: {SUCCESS | ERROR | TIMEOUT}

## Task Input

{Paste the Input section from task.md}

## Execution Steps

{Chronological log of what the skill did}

Step 1: {Action taken}
- Output: {Relevant output or file changes}

Step 2: {Action taken}
- Output: {Relevant output or file changes}

...

## Final Outputs

### Files Created/Modified
- `{filename}`: {brief description}
- `{filename}`: {brief description}

### Standard Output
```
{stdout content}
```

### Standard Error
```
{stderr content if any}
```

## Errors/Warnings

{Any errors, exceptions, or warnings encountered}
{If status is SUCCESS, write "None"}

## Notes

{Any observations about the execution}
```

**D. Clean Up**

Remove temporary execution directory:
```bash
rm -rf /tmp/exec_original_task_XXX
```

### 3. Execute Optimized Skill

Repeat Step 2 for the optimized skill, with the following changes:
- Use `{target-skill-name}-optimized/SKILL.md` as the skill source
- Write outputs to `exec_results/optimized/task_XXX/`
- Use temporary directory `/tmp/exec_optimized_task_XXX`
- Update run_log.md to reference "Optimized Skill"

### 4. Execution Isolation

Ensure complete isolation between runs:
- Each execution starts with a fresh copy of the task workspace
- No state persists between executions
- Original and optimized runs do not interfere with each other
- Execution order should not affect results (run original first for all tasks, then optimized)

### 5. Error Handling

If a skill execution fails:
- **Do not abort the entire process**
- Log the error in `run_log.md` with status ERROR
- Set execution time to the time until failure
- Capture any partial outputs produced before failure
- Continue with the next task

If a skill execution times out (>5 minutes):
- Terminate the execution
- Log status as TIMEOUT
- Capture any outputs produced before timeout
- Continue with the next task

## Output Structure

After execution, the following structure will exist:

```
exec_results/
├── original/
│   ├── task_001/
│   │   ├── output/
│   │   │   └── {files produced by skill}
│   │   └── run_log.md
│   ├── task_002/
│   │   ├── output/
│   │   └── run_log.md
│   └── ...
└── optimized/
    ├── task_001/
    │   ├── output/
    │   │   └── {files produced by skill}
    │   └── run_log.md
    ├── task_002/
    │   ├── output/
    │   └── run_log.md
    └── ...
```

## Quality Guidelines

### Execution Fidelity
- Execute skills exactly as they would be invoked in production
- Do not modify or sanitize inputs
- Do not intervene if a skill makes mistakes
- Capture the raw, unfiltered behavior

### Output Completeness
- Capture all files, not just "important" ones
- Include hidden files and directories if created
- Preserve file permissions and timestamps
- Log all stdout/stderr, even if verbose

### Reproducibility
- Document the execution environment (OS, shell, working directory)
- Use consistent execution parameters for both skill versions
- Ensure deterministic execution where possible (avoid randomness)

## Output Verification

Before completing, verify:
- [ ] All 8 original skill result directories exist
- [ ] All 8 optimized skill result directories exist
- [ ] Each result directory contains `output/` and `run_log.md`
- [ ] Each `run_log.md` is complete and well-formed
- [ ] Execution status is recorded for every task
- [ ] Errors are logged but did not halt execution

## Notes

- This subskill does not evaluate or score outputs; it only captures them
- Evaluation is performed by the evaluate-agent subskill
- Execution time limits prevent runaway processes
- Isolation ensures fair comparison between skill versions
