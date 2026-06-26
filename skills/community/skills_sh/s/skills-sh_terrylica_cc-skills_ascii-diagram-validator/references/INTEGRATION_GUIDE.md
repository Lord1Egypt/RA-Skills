**Skill**: [ASCII Diagram Validator](../SKILL.md)

# ASCII Alignment Checker - Integration Guide

## Table of Contents

- [Quick Start](#quick-start)
- [Script Location](#script-location)
- [Integration Points for Algorithm](#integration-points-for-algorithm)
  - [1. Main Validation Method](#1-main-validation-method)
  - [2. Helper Methods](#2-helper-methods)
  - [3. Reporting Issues](#3-reporting-issues)
- [Data Structures Available](#data-structures-available)
  - [Box-Drawing Character Sets](#box-drawing-character-sets)
  - [Character Detection](#character-detection)
  - [Line Access](#line-access)
- [Testing Your Algorithm](#testing-your-algorithm)
  - [Create Test Files](#create-test-files)
  - [JSON Output for Automation](#json-output-for-automation)
  - [Integration with Unit Tests](#integration-with-unit-tests)
- [CI/CD Integration Examples](#cicd-integration-examples)
  - [GitHub Actions](#github-actions)
  - [Pre-commit Hook](#pre-commit-hook)
  - [Shell Script Batch Processing](#shell-script-batch-processing)
- [Output Format Examples](#output-format-examples)
  - [Human-Readable Output](#human-readable-output)
  - [JSON Output](#json-output)
- [Algorithm Implementation Checklist](#algorithm-implementation-checklist)
  - [Vertical Alignment](#vertical-alignment)
  - [Horizontal Connection](#horizontal-connection)
  - [Style Consistency](#style-consistency)
  - [Box Structure](#box-structure)
- [Performance Considerations](#performance-considerations)
  - [Memory](#memory)
  - [Speed](#speed)
  - [Scalability](#scalability)
- [Debugging Tips](#debugging-tips)
  - [Add Debug Output](#add-debug-output)
  - [Test Individual Lines](#test-individual-lines)
  - [Validate Data Structures](#validate-data-structures)
- [Next Steps](#next-steps)
- [Resources](#resources)
- [Support](#support)

## Quick Start

```bash
# Basic usage
uv run check_ascii_alignment.py <file.md>

# JSON output for automation
uv run check_ascii_alignment.py <file.md> --json

# With fix suggestions
uv run check_ascii_alignment.py <file.md> --fix-suggestions

# Quiet mode (CI/CD)
uv run check_ascii_alignment.py <file.md> --quiet
```

## Script Location

```
skills/ascii-diagram-validator/scripts/check_ascii_alignment.py
```

## Integration Points for Algorithm

### 1. Main Validation Method

The core algorithm should be implemented in the `validate_alignment()` method:

```python
class AlignmentChecker:
    def validate_alignment(self) -> ValidationReport:
        """
        Perform alignment validation.

        Replace the TODO with your algorithm implementation.
        """
        for line_num, line in enumerate(self.lines, start=1):
            # Find all box-drawing characters in this line
            box_chars = self.find_box_chars_in_line(line)

            # YOUR ALGORITHM IMPLEMENTATION HERE
            # Example: Check vertical alignment
            for col, char in box_chars:
                if char in BOX_CHARS['vertical']:
                    # Check if this vertical bar aligns with previous lines
                    expected_col = self._get_expected_vertical_position(line_num, char)
                    if expected_col and col != expected_col:
                        self.add_issue(
                            line_num=line_num,
                            col=col,
                            severity=IssueSeverity.WARNING,
                            message=f"vertical bar '{char}' misaligned",
                            character=char,
                            expected_col=expected_col,
                            fix_suggestion=f"Move character {abs(col - expected_col)} position{'s' if abs(col - expected_col) > 1 else ''} {'left' if col > expected_col else 'right'}"
                        )

        return ValidationReport(
            file_path=self.file_path,
            total_lines=len(self.lines),
            issues=self.issues
        )
```

### 2. Helper Methods

Add your algorithm-specific helper methods to the `AlignmentChecker` class:

```python
class AlignmentChecker:
    def __init__(self, file_path: str):
        # Existing initialization
        self.file_path = file_path
        self.lines: List[str] = []
        self.issues: List[AlignmentIssue] = []

        # Your algorithm state (add as needed)
        self.vertical_positions: Dict[str, List[int]] = {}
        self.horizontal_spans: List[Tuple[int, int, int]] = []  # (line, start_col, end_col)

    def _track_vertical_position(self, line_num: int, col: int, char: str):
        """Track vertical bar positions for alignment checking."""
        # Your implementation

    def _get_expected_vertical_position(self, line_num: int, char: str) -> Optional[int]:
        """Get expected column for vertical bar based on previous lines."""
        # Your implementation

    def _validate_horizontal_connection(self, line_num: int, col: int, char: str):
        """Validate that corners/junctions have proper horizontal connections."""
        # Your implementation
```

### 3. Reporting Issues

Use the `add_issue()` method to report problems:

```python
# Example: Misaligned vertical bar
self.add_issue(
    line_num=15,
    col=42,
    severity=IssueSeverity.WARNING,
    message="vertical bar '│' misaligned",
    character='│',
    expected_col=41,
    fix_suggestion="Move character 1 position left"
)

# Example: Missing horizontal connection
self.add_issue(
    line_num=23,
    col=1,
    severity=IssueSeverity.ERROR,
    message="box corner '┌' has no connecting horizontal",
    character='┌',
    fix_suggestion="Missing '─' or '═' to the right"
)

# Example: Style inconsistency
self.add_issue(
    line_num=30,
    col=5,
    severity=IssueSeverity.INFO,
    message="mixed box styles detected",
    character='═',
    fix_suggestion="Consider using consistent single-line style (┌─┐) or double-line style (╔═╗)"
)
```

## Data Structures Available

### Box-Drawing Character Sets

```python
# All characters organized by type
BOX_CHARS = {
    'corners': {
        'top_left': ['┌', '╔', '┏'],
        'top_right': ['┐', '╗', '┓'],
        'bottom_left': ['└', '╚', '┗'],
        'bottom_right': ['┘', '╝', '┛'],
    },
    't_junctions': {
        'top': ['┬', '╦', '┳'],
        'bottom': ['┴', '╩', '┻'],
        'left': ['├', '╠', '┣'],
        'right': ['┤', '╣', '┫'],
    },
    'cross': ['┼', '╬', '╋'],
    'horizontal': ['─', '═', '━'],
    'vertical': ['│', '║', '┃'],
}

# Quick detection set
ALL_BOX_CHARS = set(...)  # Contains all box-drawing characters
```

### Character Detection

```python
# Find all box-drawing characters in a line
box_chars = self.find_box_chars_in_line(line)
# Returns: [(column_index, character), ...]

# Example: [(0, '┌'), (10, '─'), (20, '┐')]
```

### Line Access

```python
# All lines are available in self.lines (List[str])
for line_num, line in enumerate(self.lines, start=1):
    # line_num is 1-based (for human-readable output)
    # line is the actual string content

# Access specific lines
line_15 = self.lines[14]  # 0-indexed access
```

## Testing Your Algorithm

### Create Test Files

```bash
# Test 1: Perfect alignment (should pass)
cat > /tmp/test_perfect.md << 'EOF'
┌─────────┐
│ Perfect │
│ Aligned │
└─────────┘
EOF

uv run check_ascii_alignment.py /tmp/test_perfect.md
# Expected: ✓ No alignment issues found

# Test 2: Misaligned vertical bar
cat > /tmp/test_misaligned.md << 'EOF'
┌─────────┐
│ Column 1│
│ Column 2 │
└─────────┘
EOF

uv run check_ascii_alignment.py /tmp/test_misaligned.md
# Expected: Warning about line 3 column X

# Test 3: Missing horizontal connection
cat > /tmp/test_incomplete.md << 'EOF'
┌──────
│ Box
└──────┘
EOF

uv run check_ascii_alignment.py /tmp/test_incomplete.md
# Expected: Error about missing top-right corner
```

### JSON Output for Automation

```bash
# Generate JSON report
uv run check_ascii_alignment.py /tmp/test_misaligned.md --json > report.json

# Parse with jq
cat report.json | jq '.summary'
cat report.json | jq '.issues[] | select(.severity == "error")'
```

### Integration with Unit Tests

```python
#!/usr/bin/env python3
# test_alignment_checker.py

from check_ascii_alignment import AlignmentChecker, IssueSeverity

def test_perfect_alignment():
    """Test that perfect alignment produces no issues."""
    with open('/tmp/test_perfect.md', 'w') as f:
        f.write("""
┌─────────┐
│ Perfect │
└─────────┘
""")

    checker = AlignmentChecker('/tmp/test_perfect.md')
    checker.load_file()
    report = checker.validate_alignment()

    assert len(report.issues) == 0
    assert report.error_count == 0
    assert report.warning_count == 0

def test_misaligned_vertical():
    """Test detection of misaligned vertical bars."""
    with open('/tmp/test_misaligned.md', 'w') as f:
        f.write("""
┌─────────┐
│ Col 1   │
│ Col 2    │
└─────────┘
""")

    checker = AlignmentChecker('/tmp/test_misaligned.md')
    checker.load_file()
    report = checker.validate_alignment()

    assert len(report.issues) > 0
    assert any(issue.severity == IssueSeverity.WARNING for issue in report.issues)
```

## CI/CD Integration Examples

### GitHub Actions

```yaml
name: Check ASCII Alignment

on:
  pull_request:
    paths:
      - "**/*.md"

jobs:
  check-alignment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v1

      - name: Check alignment
        run: |
          for file in $(find docs -name "*.md"); do
            echo "Checking $file..."
            uv run check_ascii_alignment.py "$file" --json > "${file}.alignment.json"

            if [ $? -eq 1 ]; then
              echo "::error file=${file}::Alignment issues detected"
              cat "${file}.alignment.json"
              exit 1
            fi
          done
```

### Pre-commit Hook

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
#!/bin/bash
# .git/hooks/pre-commit

echo "Checking ASCII alignment in markdown files..."

FAILED=0

for file in $(git diff --cached --name-only | grep '\.md$'); do
  if [ -f "$file" ]; then
    uv run skills/check_ascii_alignment.py "$file" --quiet
    if [ $? -eq 1 ]; then
      echo "❌ Alignment issues in $file"
      uv run skills/check_ascii_alignment.py "$file" --fix-suggestions
      FAILED=1
    fi
  fi
done

if [ $FAILED -eq 1 ]; then
  echo ""
  echo "Fix alignment issues before committing."
  exit 1
fi

echo "✓ All ASCII art properly aligned"
exit 0
PREFLIGHT_EOF
```

### Shell Script Batch Processing

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_2'
#!/bin/bash
# check_all_docs.sh

SCRIPT_PATH="skills/check_ascii_alignment.py"
DOCS_DIR="docs"
REPORT_DIR="alignment-reports"

mkdir -p "$REPORT_DIR"

echo "Scanning markdown files in $DOCS_DIR..."

find "$DOCS_DIR" -name "*.md" | while read -r file; do
  echo "Checking $file..."

  report_file="$REPORT_DIR/$(basename "$file" .md).json"
  uv run "$SCRIPT_PATH" "$file" --json > "$report_file"

  if [ $? -eq 1 ]; then
    echo "  ❌ Issues found (see $report_file)"
  else
    echo "  ✓ Clean"
    rm "$report_file"  # Remove empty reports
  fi
done

echo ""
echo "Summary:"
issue_count=$(ls "$REPORT_DIR"/*.json 2>/dev/null | wc -l)
if [ "$issue_count" -gt 0 ]; then
  echo "Files with issues: $issue_count"
  echo "Reports saved in: $REPORT_DIR/"
  exit 1
else
  echo "All files clean!"
  rmdir "$REPORT_DIR" 2>/dev/null
  exit 0
fi
PREFLIGHT_EOF_2
```

## Output Format Examples

### Human-Readable Output

```
================================================================================
Alignment Check Report: docs/ARCHITECTURE.md
================================================================================
Total lines scanned: 150
Issues found: 2 (1 errors, 1 warnings)
================================================================================

docs/ARCHITECTURE.md:15:42: warning: vertical bar '│' misaligned
  Expected column 41
  Suggestion: Move character 1 position left

docs/ARCHITECTURE.md:23:1: error: box corner '┌' has no connecting horizontal
  Suggestion: Missing '─' or '═' to the right

================================================================================
Summary: 1 errors, 1 warnings
================================================================================
```

### JSON Output

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
      "fix_suggestion": "Move character 1 position left"
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

## Algorithm Implementation Checklist

When implementing the alignment algorithm, consider:

### Vertical Alignment

- [ ] Track column positions of vertical bars (│, ║, ┃)
- [ ] Detect drift across consecutive lines
- [ ] Handle multiple vertical columns in same diagram
- [ ] Calculate expected position based on context
- [ ] Generate fix suggestions (move left/right)

### Horizontal Connection

- [ ] Verify corners have adjacent horizontal lines
- [ ] Check T-junctions connect properly on both sides
- [ ] Validate cross junctions (┼) have 4-way connections
- [ ] Detect incomplete boxes
- [ ] Suggest missing characters

### Style Consistency

- [ ] Detect mixing of single/double/heavy line styles
- [ ] Flag style transitions within same box
- [ ] Suggest style normalization
- [ ] Allow intentional style mixing (nested boxes)

### Box Structure

- [ ] Match opening corners with closing corners
- [ ] Verify complete rectangles
- [ ] Check nested box alignment
- [ ] Validate box dimensions (width/height consistency)

## Performance Considerations

### Memory

- File is loaded entirely into memory (`self.lines`)
- Suitable for typical documentation files (< 10MB)
- For very large files, consider streaming line-by-line

### Speed

- Single-pass scanning per validation run
- O(n) time complexity (n = total characters)
- Character detection uses set lookup (O(1))

### Scalability

```bash
# Benchmark on large file
time uv run check_ascii_alignment.py large_doc.md

# Profile memory usage
/usr/bin/time -l uv run check_ascii_alignment.py large_doc.md
```

## Debugging Tips

### Add Debug Output

```python
# In validate_alignment()
def validate_alignment(self) -> ValidationReport:
    import sys

    for line_num, line in enumerate(self.lines, start=1):
        box_chars = self.find_box_chars_in_line(line)

        # Debug output
        if box_chars:
            print(f"DEBUG: Line {line_num}: {box_chars}", file=sys.stderr)

        # ... rest of algorithm
```

### Test Individual Lines

```python
# Test character detection
checker = AlignmentChecker('/tmp/test.md')
test_line = "┌─────────┐"
chars = checker.find_box_chars_in_line(test_line)
print(f"Found: {chars}")
# Expected: [(0, '┌'), (1, '─'), (2, '─'), ..., (10, '┐')]
```

### Validate Data Structures

```python
# Check box character sets
from check_ascii_alignment import BOX_CHARS, ALL_BOX_CHARS

print(f"Total box characters: {len(ALL_BOX_CHARS)}")
print(f"Vertical chars: {BOX_CHARS['vertical']}")
print(f"Corner chars: {BOX_CHARS['corners']['top_left']}")
```

## Next Steps

1. **Implement Algorithm**: Add validation logic to `validate_alignment()`
2. **Test Thoroughly**: Use provided test files and edge cases
3. **Optimize**: Profile and improve performance if needed
4. **Document**: Add algorithm-specific documentation
5. **Integrate**: Add to Claude Code skills workflow

## Resources

- **Script**: `scripts/check_ascii_alignment.py`
- **Design Report**: `references/SCRIPT_DESIGN_REPORT.md`
- **This Guide**: `references/INTEGRATION_GUIDE.md`

## Support

For issues or questions:

1. Review the design report for architecture details
2. Check test files for expected behavior
3. Examine JSON output for debugging
4. Add debug output to trace algorithm behavior
