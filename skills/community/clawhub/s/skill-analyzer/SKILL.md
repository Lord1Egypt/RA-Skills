---
name: skill-analyzer
description: Quality scanner for OpenClaw skills. Evaluates functionality, security, usability, documentation, and best practices with weighted scoring. Use when: (1) Analyzing skill quality before publishing, (2) Finding improvement opportunities, (3) Security review of third-party skills. Pure Python - no dependencies.
---

# Skill Analyzer - Comprehensive Skill Analysis Tool

## Overview

Skill Analyzer evaluates OpenClaw skills across 5 dimensions to provide a comprehensive quality assessment. It helps identify strengths, weaknesses, and improvement opportunities. Built with pure Python - no external dependencies required.

## Analysis Dimensions (5 total)

### 1. Functionality Analysis (25%)
- Core features implementation completeness
- Edge cases handling
- Error handling and robustness
- Command-line interface quality

### 2. Security Analysis (25%)
- Input validation
- Credential handling
- No hardcoded secrets
- Safe execution patterns

### 3. Usability Analysis (20%)
- User experience quality
- Documentation clarity
- Installation complexity
- Example availability

### 4. Documentation Quality (15%)
- SKILL.md completeness
- Frontmatter (name, description)
- Usage examples
- Tag coverage

### 5. Best Practices (15%)
- Code structure and organization
- Error handling patterns
- Configuration management

## Usage

### Requirements
- Python 3.7+ (no external dependencies - uses only stdlib)

### Analyze a Skill

```bash
# Analyze a local skill
python3 scripts/analyzer.py --path /path/to/skill

# Analyze with detailed output
python3 analyzer.py --path /path/to/skill --verbose

# Output to JSON
python3 analyzer.py --path /path/to/skill --output report.json

# Compare two skills
python3 analyzer.py --compare skill1 skill2
```

### Dimensions Scoring

Each dimension is scored 0-10:
- 8-10: Excellent
- 6-7: Good
- 4-5: Average
- 2-3: Below Average
- 0-1: Poor/Needs Improvement

## Example Output

```
==========================================
Skill Analysis Report: example-skill
==========================================

Overall Score: 7.5/10

Dimension Scores:
  Functionality:    8/10 ████████░░
  Security:         9/10 █████████░
  Usability:        7/10 ███████░░░
  Documentation:    6/10 ██████░░░░
  Best Practices:   7/10 ███████░░░

Strengths:
  ✓ Good security practices
  ✓ Clean code structure
  ✓ Proper error handling

Risk Level: LOW
```

## Notes

- Run from any directory containing skills
- Pure Python - no pip install needed
- Safe to run on any skill
- Does not modify analyzed skills
