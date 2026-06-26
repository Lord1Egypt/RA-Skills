---
name: sample-agent
description: Analyze a target Skill's SKILL.md and generate diverse functional test tasks that probe capability boundaries
version: 1.0.0
---

# Sample-Agent

Generate a comprehensive test suite for a target Skill by analyzing its specification and creating diverse tasks that cover standard use-cases and advanced edge cases.

## Purpose

Automatically generate 20 functional test tasks (12 training + 8 test) that:
- Cover the core functionality described in the target Skill
- Probe edge cases and boundary conditions
- Test advanced multi-step scenarios
- Provide verifiable success criteria via SpecCheck

## Inputs

- `target-skill-path`: Path to the Skill directory containing `SKILL.md`

## Implementation

This subskill uses `task_generator.py` to ensure formatting rigor and consistency.

## Execution Steps

### 1. Initialize Task Generator

Run the task generator Python script:

```bash
cd subskills/sample-agent
python task_generator.py {target-skill-path} ../..
```

The script will:
- Load and analyze the target skill's SKILL.md
- Generate 12 training tasks and 8 test tasks
- Write all tasks to `tasks/train/` and `tasks/test/`

### 2. Implement Task Generation Logic

You must implement the following methods in `task_generator.py`:

**`generate_tasks()`** - Generate 12 training tasks:
- Read and parse `self.skill_md_content`
- Extract skill description, inputs, outputs, constraints
- Identify edge cases and ambiguous scenarios
- Create 8 standard tasks covering core functionality
- Create 4 advanced tasks covering edge cases and complex scenarios
- Return `(List[Task], List[SpecCheck])`

**`generate_test_tasks()`** - Generate 8 test tasks:
- Create 4 standard tasks (similar difficulty to training, different scenarios)
- Create 4 advanced tasks (novel edge cases)
- Ensure no overlap with training tasks
- Return `(List[Task], List[SpecCheck])`

### 3. Task Generation Guidelines

When implementing task generation:

**Training tasks (12 total):**
- **Standard (8 tasks)**: Cover typical, straightforward use-cases with clear inputs and verifiable outputs
- **Advanced (4 tasks)**: Complex multi-step scenarios, edge cases, ambiguous inputs

**Test tasks (8 total):**
- **Standard (4 tasks)**: Similar difficulty to training, different scenarios (no overlap)
- **Advanced (4 tasks)**: Novel edge cases not seen in training

### 4. Task Structure

The Python script handles file creation. You provide Task and SpecCheck objects:

**Task object:**
```python
Task(
    task_id="task_001",
    task_type="standard",  # or "advanced"
    title="Short descriptive title",
    background="Why this task is relevant",
    objective="What needs to be accomplished",
    input_description="Exact inputs (use code blocks if needed)",
    expected_behavior="What successful execution looks like",
    constraints=["Restriction 1", "Restriction 2"],
    workspace_files={"input.txt": "file content"}  # or {} if none
)
```

**SpecCheck object:**
```python
SpecCheck(
    task_id="task_001",
    criteria=[
        SpecCheckCriterion(
            description="Exact condition that must be true",
            verification_method="How to check this criterion"
        ),
        # ... more criteria
    ],
    total_points=5,  # typically len(criteria)
    pass_threshold=4,  # typically 70-80% of total
    evaluation_notes="Instructions for evaluator"
)
```

The script automatically generates properly formatted `task.md`, `speccheck.md`, and `workspace/` files.

## Quality Guidelines

### Task Diversity
- Ensure no two tasks are near-identical
- Vary input types, sizes, and formats
- Cover different aspects of the skill's functionality
- Include both positive cases (should succeed) and challenging cases (may expose limitations)

### SpecCheck Criteria
- Must be objective and deterministic
- Avoid subjective judgments ("code is clean", "output is reasonable")
- Prefer concrete checks: file exists, contains specific text, matches pattern, count equals N
- Each criterion should be independently verifiable
- Criteria should collectively cover all aspects of the expected behavior

### No Data Leakage
- Training and test tasks must be distinct
- Test tasks should not be trivial variations of training tasks
- Avoid patterns that allow "memorization" rather than generalization

## Output Verification

Before completing, verify:
- [ ] All 12 training task directories exist with complete files
- [ ] All 8 test task directories exist with complete files
- [ ] Each `task.md` follows the specified format
- [ ] Each `speccheck.md` has clear, verifiable criteria
- [ ] `workspace/` directories contain necessary seed files (or are intentionally empty)
- [ ] No duplicate or near-duplicate tasks between train and test sets

## Example Task Structure

```
tasks/
├── train/
│   ├── task_001/
│   │   ├── task.md
│   │   ├── speccheck.md
│   │   └── workspace/
│   │       └── input.txt
│   ├── task_002/
│   │   ├── task.md
│   │   ├── speccheck.md
│   │   └── workspace/
│   └── ...
└── test/
    ├── task_001/
    │   ├── task.md
    │   ├── speccheck.md
    │   └── workspace/
    └── ...
```

## Notes

- Task generation should be deterministic given the same input skill
- Focus on functional correctness, not performance benchmarks
- Tasks should be achievable by a well-implemented version of the skill
- If the target skill's specification is ambiguous, generate tasks that expose the ambiguity
