---
name: skill-doc-enhancer
description: Automatically analyze and enhance content-short SKILL.md files by analyzing skill directory structure, adding usage examples, script documentation, common use cases, and best practices. Use when a skill's SKILL.md is too short (less than 3000 characters), lacks sufficient examples, missing script documentation, or needs content enrichment while preserving existing structure.
---

# Skill Doc Enhancer

Automatically analyze and enhance SKILL.md files that are too short or lack sufficient documentation.

## When to Use

Use this skill when:
- A skill's SKILL.md has less than 3000 characters
- The documentation lacks usage examples
- Scripts exist but aren't documented in SKILL.md
- Common use cases and best practices are missing
- The skill needs content enrichment while preserving structure

## Enhancement Process

### Step 1: Analyze Current State

Run the analysis script to understand what needs enhancement:

```bash
python3 scripts/analyze_skill.py <path/to/skill-directory>
```

This will output:
- Current character count
- Missing sections (examples, scripts, best practices)
- Directory structure analysis
- Enhancement recommendations

### Step 2: Generate Enhancement Content

Based on the analysis, the script will suggest:

1. **Directory Structure Analysis**
   - List all files in `scripts/`, `references/`, `assets/`
   - Identify undocumented resources

2. **Script Documentation**
   - For each script in `scripts/`, extract:
     - Purpose and functionality
     - Usage syntax
     - Example commands
     - Expected outputs

3. **Usage Examples**
   - Common task patterns
   - Input/output examples
   - Error handling examples

4. **Best Practices**
   - Recommended workflows
   - Common pitfalls to avoid
   - Tips for effective usage

### Step 3: Apply Enhancements

The enhancement script can automatically append content:

```bash
python3 scripts/enhance_skill.py <path/to/skill-directory> [--dry-run]
```

Options:
- `--dry-run`: Preview changes without modifying files
- `--sections examples,scripts,best-practices`: Choose which sections to enhance

## Enhancement Categories

### 1. Script Documentation

For skills with a `scripts/` directory, add:

```markdown
## Scripts Reference

### script-name.py
**Purpose**: Brief description of what the script does

**Usage**:
```bash
python3 scripts/script-name.py [arguments]
```

**Examples**:
```bash
# Example 1: Basic usage
python3 scripts/script-name.py input.txt

# Example 2: With options
python3 scripts/script-name.py input.txt --output result.txt
```
```

### 2. Usage Examples

Add concrete examples showing real-world usage:

```markdown
## Usage Examples

### Example 1: [Task Name]
**Scenario**: Describe when this example applies

**Input**: 
- File: `example.txt`
- Content: ...

**Command**:
```bash
# Command to execute
```

**Output**:
```
Expected output
```

### Example 2: [Another Task]
...
```

### 3. Best Practices

Document recommendations and pitfalls:

```markdown
## Best Practices

### Do's
- Recommendation 1
- Recommendation 2

### Don'ts
- Pitfall 1 and why to avoid it
- Pitfall 2 and why to avoid it

### Tips
- Pro tip for advanced usage
- Performance optimization suggestion
```

### 4. Common Use Cases

List typical scenarios where the skill applies:

```markdown
## Common Use Cases

1. **[Use Case 1]**: Brief description
   - When to use: Context
   - Expected outcome: Result

2. **[Use Case 2]**: Brief description
   - When to use: Context
   - Expected outcome: Result
```

## Manual Enhancement Guidelines

When automatic enhancement isn't sufficient:

1. **Preserve Existing Structure**: Don't reorganize unless necessary
2. **Append, Don't Replace**: Add new content after existing sections
3. **Match Style**: Follow the existing tone and formatting
4. **Be Specific**: Include concrete file names, paths, and commands
5. **Test Examples**: Ensure all code examples work as documented

## Quality Checklist

After enhancement, verify:

- [ ] Character count > 3000 (unless skill is intentionally minimal)
- [ ] All scripts in `scripts/` are documented
- [ ] At least 2-3 usage examples provided
- [ ] Best practices section exists
- [ ] Common use cases listed
- [ ] Examples are tested and accurate
- [ ] No TODO or XXX placeholders remain

## Scripts

### analyze_skill.py
Analyzes a skill directory and reports enhancement opportunities.

**Usage**:
```bash
python3 scripts/analyze_skill.py /path/to/skill-directory
```

**Output**: JSON report with:
- `char_count`: Current SKILL.md character count
- `has_examples`: Whether usage examples exist
- `scripts_documented`: Whether scripts are documented
- `has_best_practices`: Whether best practices section exists
- `recommendations`: List of suggested enhancements

### enhance_skill.py
Automatically enhances SKILL.md with missing content.

**Usage**:
```bash
python3 scripts/enhance_skill.py /path/to/skill-directory [options]
```

**Options**:
- `--dry-run`: Preview changes without writing
- `--sections SECTIONS`: Comma-separated list of sections to enhance
  - Available: `examples`, `scripts`, `best-practices`, `use-cases`
  - Default: all sections

**Example**:
```bash
# Preview enhancements
python3 scripts/enhance_skill.py /path/to/skill --dry-run

# Enhance only examples and scripts
python3 scripts/enhance_skill.py /path/to/skill --sections examples,scripts
```

## Example Enhancement Workflow

```bash
# 1. Analyze the skill
python3 scripts/analyze_skill.py skills/nano-pdf

# Output:
# {
#   "skill_name": "nano-pdf",
#   "char_count": 1850,
#   "has_examples": false,
#   "scripts_documented": false,
#   "has_best_practices": false,
#   "recommendations": [
#     "Add usage examples section",
#     "Document scripts/pdf_utils.py",
#     "Add best practices section"
#   ]
# }

# 2. Preview enhancements
python3 scripts/enhance_skill.py skills/nano-pdf --dry-run

# 3. Apply enhancements
python3 scripts/enhance_skill.py skills/nano-pdf

# 4. Review and edit manually if needed
# Edit skills/nano-pdf/SKILL.md
```

## Notes

- This skill focuses on **content enhancement**, not restructuring
- Always review automatic enhancements before committing
- Some skills may be intentionally minimal - use judgment
- When in doubt, prefer adding examples over explanations
