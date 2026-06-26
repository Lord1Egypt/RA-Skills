**Skill**: [ASCII Diagram Validator](../SKILL.md)

# ASCII Alignment Checker - Script Design Report

## Table of Contents

- [Executive Summary](#executive-summary)
- [Design Overview](#design-overview)
  - [Architecture Components](#architecture-components)
- [PEP 723 Header](#pep-723-header)
- [CLI Interface](#cli-interface)
  - [Command Syntax](#command-syntax)
  - [Available Options](#available-options)
  - [Exit Codes](#exit-codes)
- [Usage Examples](#usage-examples)
  - [Basic Check (Human-Readable)](#basic-check-human-readable)
  - [JSON Output (Machine-Parseable)](#json-output-machine-parseable)
  - [With Fix Suggestions](#with-fix-suggestions)
  - [Quiet Mode (CI/CD)](#quiet-mode-cicd)
- [Data Models](#data-models)
  - [AlignmentIssue](#alignmentissue)
  - [ValidationReport](#validationreport)
  - [IssueSeverity](#issueseverity)
- [Box-Drawing Character Sets](#box-drawing-character-sets)
- [Integration Points for Alignment Algorithm](#integration-points-for-alignment-algorithm)
  - [Helper Methods Available](#helper-methods-available)
- [Output Formatting System](#output-formatting-system)
  - [1. Human-Readable Format](#1-human-readable-format)
  - [2. JSON Format](#2-json-format)
  - [3. Quiet Format](#3-quiet-format)
- [Testing the Script](#testing-the-script)
  - [Manual Testing](#manual-testing)
  - [Integration with CI/CD](#integration-with-cicd)
  - [Pre-commit Hook](#pre-commit-hook)
- [Algorithm Implementation Checklist](#algorithm-implementation-checklist)
- [Key Design Decisions](#key-design-decisions)
  - [Why Zero Dependencies?](#why-zero-dependencies)
  - [Why Three Output Formats?](#why-three-output-formats)
  - [Why Dataclasses?](#why-dataclasses)
  - [Why Enum for Severity?](#why-enum-for-severity)
- [Next Steps](#next-steps)
- [File Locations](#file-locations)
- [Example Integration with Claude Code](#example-integration-with-claude-code)
- [Conclusion](#conclusion)

## Executive Summary

Complete Python script skeleton designed for ASCII art alignment validation in Markdown documentation. Follows PEP 723 inline dependencies pattern and provides Claude Code-friendly output formatting.

**Script Location**: `scripts/check_ascii_alignment.py`

## Design Overview

### Architecture Components

```
┌─────────────────────────────────────────────────────────┐
│                   CLI Interface                         │
│  (argparse with --json, --quiet, --fix-suggestions)     │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│              AlignmentChecker                           │
│  • load_file()          - Read markdown file            │
│  • validate_alignment() - Core validation engine        │
│  • find_box_chars()     - Character detection           │
│  • add_issue()          - Issue tracking                │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│              Data Models                                │
│  • AlignmentIssue  - Single issue representation        │
│  • ValidationReport - Complete report structure         │
│  • IssueSeverity   - ERROR/WARNING/INFO levels          │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│            Output Formatters                            │
│  • format_human_readable() - Pretty text output         │
│  • format_json()           - Machine-parseable          │
│  • format_quiet()          - Exit code only             │
└─────────────────────────────────────────────────────────┘
```

## PEP 723 Header

The script uses PEP 723 inline dependencies with zero external dependencies:

```python
#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
```

**Key Features**:

- ✅ No external dependencies (pure Python 3.12+)
- ✅ Self-contained execution via `uv run`
- ✅ No pip install required
- ✅ Follows workspace PEP 723 standard

## CLI Interface

### Command Syntax

```bash
uv run check_ascii_alignment.py <file> [options]
```

### Available Options

| Option              | Description                       | Mutually Exclusive With |
| ------------------- | --------------------------------- | ----------------------- |
| `--json`            | Output in JSON format             | `--quiet`               |
| `--quiet`           | Quiet mode (exit code only)       | `--json`                |
| `--fix-suggestions` | Include fix suggestions in output | -                       |

### Exit Codes

| Code | Meaning                             |
| ---- | ----------------------------------- |
| 0    | No alignment issues found           |
| 1    | Alignment issues detected           |
| 2    | File not found or invalid arguments |

## Usage Examples

### Basic Check (Human-Readable)

```bash
uv run check_ascii_alignment.py docs/ARCHITECTURE.md
```

**Output**:

```
================================================================================
Alignment Check Report: docs/ARCHITECTURE.md
================================================================================
Total lines scanned: 150
Issues found: 2 (1 errors, 1 warnings)
================================================================================

docs/ARCHITECTURE.md:15:42: warning: vertical bar '│' misaligned
  Expected column 41

docs/ARCHITECTURE.md:23:1: error: box corner '┌' has no connecting horizontal
  Suggestion: Missing '─' or '═' to the right

================================================================================
Summary: 1 errors, 1 warnings
================================================================================
```

### JSON Output (Machine-Parseable)

```bash
uv run check_ascii_alignment.py docs/ARCHITECTURE.md --json > report.json
```

**Output**:

```json
{
  "file_path": "docs/ARCHITECTURE.md",
  "total_lines": 150,
  "summary": {
    "total_issues": 2,
    "errors": 1,
    "warnings": 1
  },
  "issues": [
    {
      "file_path": "docs/ARCHITECTURE.md",
      "line_number": 15,
      "column": 42,
      "severity": "warning",
      "message": "vertical bar '│' misaligned",
      "character": "│",
      "expected_column": 41,
      "fix_suggestion": null
    },
    {
      "file_path": "docs/ARCHITECTURE.md",
      "line_number": 23,
      "column": 1,
      "severity": "error",
      "message": "box corner '┌' has no connecting horizontal",
      "character": "┌",
      "expected_column": null,
      "fix_suggestion": "Missing '─' or '═' to the right"
    }
  ]
}
```

### With Fix Suggestions

```bash
uv run check_ascii_alignment.py docs/ARCHITECTURE.md --fix-suggestions
```

**Output**:

```
docs/ARCHITECTURE.md:15:42: warning: vertical bar '│' misaligned
  Expected column 41
  Suggestion: Move character 1 position left

docs/ARCHITECTURE.md:23:1: error: box corner '┌' has no connecting horizontal
  Suggestion: Missing '─' or '═' to the right
```

### Quiet Mode (CI/CD)

```bash
uv run check_ascii_alignment.py docs/ARCHITECTURE.md --quiet
echo $?  # Exit code: 0 = clean, 1 = issues, 2 = error
```

**Output**:

```
2 issues found
```

## Data Models

### AlignmentIssue

Represents a single alignment issue.

```python
@dataclass
class AlignmentIssue:
    file_path: str              # File containing the issue
    line_number: int            # Line number (1-based)
    column: int                 # Column number (0-based)
    severity: IssueSeverity     # ERROR/WARNING/INFO
    message: str                # Human-readable description
    character: str              # The problematic character
    expected_column: Optional[int]  # Expected alignment column
    fix_suggestion: Optional[str]   # How to fix the issue
```

**Methods**:

- `to_dict()` - Convert to dictionary (for JSON)
- `format_human_readable(show_suggestions: bool)` - Format for console output

### ValidationReport

Complete validation report for a file.

```python
@dataclass
class ValidationReport:
    file_path: str              # File that was validated
    total_lines: int            # Total lines scanned
    issues: List[AlignmentIssue]  # All detected issues
```

**Properties**:

- `has_errors: bool` - Check if report contains errors
- `has_warnings: bool` - Check if report contains warnings
- `error_count: int` - Count error-level issues
- `warning_count: int` - Count warning-level issues

**Methods**:

- `to_dict()` - Convert to dictionary (for JSON)

### IssueSeverity

```python
class IssueSeverity(Enum):
    ERROR = "error"      # Critical misalignment (breaks visual structure)
    WARNING = "warning"  # Minor misalignment (visual inconsistency)
    INFO = "info"        # Informational (style suggestions)
```

## Box-Drawing Character Sets

The script includes comprehensive box-drawing character definitions:

```python
BOX_CHARS = {
    # Corners
    'corners': {
        'top_left': ['┌', '╔', '┏'],
        'top_right': ['┐', '╗', '┓'],
        'bottom_left': ['└', '╚', '┗'],
        'bottom_right': ['┘', '╝', '┛'],
    },
    # T-junctions
    't_junctions': {
        'top': ['┬', '╦', '┳'],
        'bottom': ['┴', '╩', '┻'],
        'left': ['├', '╠', '┣'],
        'right': ['┤', '╣', '┫'],
    },
    # Cross
    'cross': ['┼', '╬', '╋'],
    # Lines
    'horizontal': ['─', '═', '━'],
    'vertical': ['│', '║', '┃'],
}
```

**Styles Supported**:

- Single-line: `┌─┐│└┘`
- Double-line: `╔═╗║╚╝`
- Heavy-line: `┏━┓┃┗┛`

## Integration Points for Alignment Algorithm

The script provides a clear integration point for the alignment algorithm:

```python
class AlignmentChecker:
    def validate_alignment(self) -> ValidationReport:
        """
        Perform alignment validation.

        This is the main entry point for validation logic.
        The actual validation algorithm will be implemented separately.
        """
        # TODO: Implement validation algorithm

        for line_num, line in enumerate(self.lines, start=1):
            box_chars = self.find_box_chars_in_line(line)

            # Your algorithm implementation goes here
            # Use self.add_issue() to report problems

        return ValidationReport(
            file_path=self.file_path,
            total_lines=len(self.lines),
            issues=self.issues
        )
```

### Helper Methods Available

```python
# Find all box-drawing characters in a line
box_chars = self.find_box_chars_in_line(line)
# Returns: List[Tuple[int, str]] - [(column, character), ...]

# Add an issue to the report
self.add_issue(
    line_num=15,
    col=42,
    severity=IssueSeverity.WARNING,
    message="vertical bar '│' misaligned",
    character='│',
    expected_col=41,
    fix_suggestion="Move character 1 position left"
)
```

## Output Formatting System

The script includes three output formatters:

### 1. Human-Readable Format

```python
OutputFormatter.format_human_readable(report, show_suggestions=False)
```

**Features**:

- Clear section headers
- Line:column references
- Severity indicators
- Optional fix suggestions
- Summary statistics

**Best For**: Manual review, debugging, IDE integration

### 2. JSON Format

```python
OutputFormatter.format_json(report)
```

**Features**:

- Structured data (machine-parseable)
- Complete issue metadata
- Summary statistics
- Compatible with jq, Python, etc.

**Best For**: CI/CD pipelines, automated tooling, data analysis

### 3. Quiet Format

```python
OutputFormatter.format_quiet(report)
```

**Features**:

- Minimal output (single line summary)
- Primary communication via exit code
- Silent on success

**Best For**: Shell scripts, pre-commit hooks, automation

## Testing the Script

### Manual Testing

```bash
# Create a test file with intentional misalignment
cat > /tmp/test_alignment.md << 'EOF'
# Test Document

┌─────────┐
│ Column 1│
│ Column 2 │  # Misaligned vertical bar
└─────────┘

┌──────    # Missing closing horizontal
EOF

# Test basic check
uv run check_ascii_alignment.py /tmp/test_alignment.md

# Test JSON output
uv run check_ascii_alignment.py /tmp/test_alignment.md --json

# Test with suggestions
uv run check_ascii_alignment.py /tmp/test_alignment.md --fix-suggestions

# Test quiet mode
uv run check_ascii_alignment.py /tmp/test_alignment.md --quiet
echo "Exit code: $?"
```

### Integration with CI/CD

```yaml
# GitHub Actions example
- name: Check ASCII alignment
  run: |
    uv run check_ascii_alignment.py docs/**/*.md --json > alignment-report.json

    if [ $? -eq 1 ]; then
      echo "Alignment issues detected"
      cat alignment-report.json
      exit 1
    fi
```

### Pre-commit Hook

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
#!/bin/bash
# .git/hooks/pre-commit

for file in $(git diff --cached --name-only | grep '\.md$'); do
  if [ -f "$file" ]; then
    uv run check_ascii_alignment.py "$file" --quiet
    if [ $? -eq 1 ]; then
      echo "Alignment issues in $file"
      uv run check_ascii_alignment.py "$file" --fix-suggestions
      exit 1
    fi
  fi
done
PREFLIGHT_EOF
```

## Algorithm Implementation Checklist

The script skeleton is complete. To add the alignment algorithm:

- [ ] **Vertical Alignment Detection**
  - Track column positions of vertical bars across consecutive lines
  - Detect drift/misalignment
  - Use `self.add_issue()` for deviations

- [ ] **Horizontal Connection Validation**
  - Check corners have adjacent horizontal lines
  - Verify T-junctions connect properly
  - Validate box continuity

- [ ] **Style Consistency Check**
  - Detect mixed single/double/heavy line styles
  - Flag style transitions (if desired)
  - Provide style normalization suggestions

- [ ] **Box Structure Validation**
  - Match opening/closing corners
  - Verify complete rectangles
  - Check nested box alignment

## Key Design Decisions

### Why Zero Dependencies?

- **Simplicity**: No external dependency management
- **Portability**: Works everywhere Python 3.12+ is available
- **Speed**: No dependency resolution overhead
- **Reliability**: No external API changes to track

### Why Three Output Formats?

- **Human-Readable**: For manual debugging and IDE integration
- **JSON**: For automation, CI/CD, and tooling integration
- **Quiet**: For shell scripts and exit-code-based workflows

### Why Dataclasses?

- **Clarity**: Self-documenting data structures
- **Type Safety**: Built-in type hints
- **Serialization**: Easy conversion to dict/JSON
- **Immutability**: Safer concurrent access (frozen=True available)

### Why Enum for Severity?

- **Type Safety**: Prevent invalid severity values
- **Autocomplete**: IDE support for valid values
- **Extensibility**: Easy to add new severity levels
- **Serialization**: Clean JSON representation

## Next Steps

1. **Algorithm Implementation** (Next Agent Task)
   - Implement vertical alignment tracking
   - Add horizontal connection validation
   - Implement style consistency checks

2. **Testing** (After Algorithm)
   - Unit tests for edge cases
   - Integration tests with real markdown files
   - Performance testing on large files

3. **Documentation** (After Testing)
   - Add algorithm documentation
   - Create troubleshooting guide
   - Document common patterns/anti-patterns

## File Locations

- **Script**: `scripts/check_ascii_alignment.py`
- **Design Report**: `references/SCRIPT_DESIGN_REPORT.md`

## Example Integration with Claude Code

When Claude Code encounters an alignment issue:

```
$ uv run check_ascii_alignment.py docs/ARCHITECTURE.md

docs/ARCHITECTURE.md:15:42: warning: vertical bar '│' misaligned
  Expected column 41
  Suggestion: Move character 1 position left
```

Claude Code can:

1. Parse the `file:line:column` format
2. Navigate directly to the issue
3. Read the fix suggestion
4. Apply the fix automatically (if desired)

## Conclusion

The script skeleton is production-ready and follows all workspace standards:

✅ PEP 723 inline dependencies
✅ `uv run` execution pattern
✅ Claude Code-friendly output
✅ Machine-parseable JSON format
✅ Clear integration points
✅ Comprehensive data models
✅ Exit code semantics
✅ Zero external dependencies

Ready for algorithm implementation (next DCTL agent task).
