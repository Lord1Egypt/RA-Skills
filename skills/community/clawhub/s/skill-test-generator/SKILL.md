---
name: skill-test-generator
description: Automatically generate test documentation for existing skills that have scripts but lack testing guidance. Use when a skill has scripts/ directory but no TESTING.md or testing section in SKILL.md. Analyzes scripts to create test cases covering normal and edge cases, generates test command examples, and creates or updates testing documentation.
---

# Skill Test Generator

## Overview

This skill analyzes existing skill scripts and automatically generates comprehensive test documentation. It identifies scripts in the `scripts/` directory, analyzes their functionality, and produces test cases covering both normal and exceptional scenarios.

## When to Use This Skill

Use this skill when:
- A skill has scripts but lacks testing documentation
- You need to create TESTING.md for a skill
- You want to add a testing section to an existing SKILL.md
- You need test case examples for skill scripts

## Workflow

### Step 1: Analyze Scripts

First, identify and analyze the scripts in the target skill:

1. List all files in the skill's `scripts/` directory
2. Read each script to understand its purpose and parameters
3. Identify entry points, inputs, outputs, and dependencies

### Step 2: Generate Test Cases

For each script, generate test cases covering:

**Normal Cases:**
- Standard usage with valid inputs
- Typical parameter combinations
- Expected successful execution paths

**Edge Cases:**
- Empty or minimal inputs
- Boundary values (max/min lengths, sizes)
- Special characters and encoding
- Invalid file paths or missing files
- Permission issues
- Malformed arguments

**Error Cases:**
- Missing required parameters
- Invalid parameter types
- Non-existent input files
- Network failures (if applicable)
- Resource exhaustion scenarios

### Step 3: Create Test Documentation

Generate documentation in one of two formats:

**Option A: Create TESTING.md**
Create a standalone testing document with:
- Test case tables (ID, Description, Input, Expected Output, Command)
- Test execution instructions
- Environment setup requirements

**Option B: Update SKILL.md**
Add a "Testing" section to the existing SKILL.md with:
- Overview of test approach
- Test case summaries
- Example commands

### Step 4: Provide Test Commands

Include concrete test command examples that can be copied and executed:

```bash
# Example test commands for a hypothetical script
python scripts/process_data.py --input test_data/valid.json
python scripts/process_data.py --input test_data/empty.json  # Edge case
python scripts/process_data.py --input nonexistent.json      # Error case
```

## Test Case Format

Use this standard format for test cases:

| ID | Script | Type | Description | Input | Expected Output | Command |
|----|--------|------|-------------|-------|-----------------|---------|
| TC001 | process.py | Normal | Process valid JSON | `{"key": "value"}` | Success, output file created | `python scripts/process.py input.json` |
| TC002 | process.py | Edge | Process empty file | Empty file | Graceful handling, empty output | `python scripts/process.py empty.json` |
| TC003 | process.py | Error | Missing input file | N/A | Error message, exit code 1 | `python scripts/process.py missing.json` |

## Resources

### scripts/

- `test_template.py` - Template generator for creating test case documentation

## Example Output

When run against a skill with scripts, this skill produces:

1. **TESTING.md** (or updated SKILL.md section) containing:
   - Test case inventory
   - Test execution commands
   - Expected results for each test

2. **Test commands** ready to copy-paste and execute

## Best Practices

1. **Cover the happy path first** - Ensure basic functionality works
2. **Test boundaries** - Check min/max values, empty inputs
3. **Verify error handling** - Scripts should fail gracefully
4. **Document prerequisites** - Note any required test data or environment setup
5. **Make commands executable** - Provide copy-paste ready commands
