# text-diff

A text comparison tool for OpenClaw.

## Overview

**text-diff** is a utility skill that shows line-by-line differences between two text files. It supports unified diff, context diff, and side-by-side comparison modes with colored output for better readability.

## Installation

1. Clone or copy the skill to your OpenClaw skills directory:
```bash
~/.openclaw/skills/text-diff/
```

2. Ensure Python 3 is installed on your system.

3. The skill is ready to use - no additional dependencies required.

## Usage

```bash
python ~/.openclaw/skills/text-diff/text_diff.py <command> <file1> <file2> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `unified` | Show unified diff format (similar to `diff -u`) |
| `context` | Show context diff format |
| `side-by-side` | Show line-by-line comparison |

### Options

| Option | Description |
|--------|-------------|
| `-c, --context` | Number of context lines (default: 3) |
| `-o, --output` | Save diff to file instead of stdout |
| `--no-color` | Disable colored output |

## Examples

### Example 1: Compare two configuration files

Compare two configuration files using unified diff:

```bash
python ~/.openclaw/skills/text-diff/text_diff.py unified config.old.json config.new.json
```

**Output:**
```
--- config.old.json
+++ config.new.json
@@ -1,5 +1,5 @@
 {
   "name": "my-app",
-  "version": "1.0.0",
+  "version": "1.1.0",
   "port": 3000
 }
```

### Example 2: Side-by-side comparison with output file

Compare two text files side-by-side and save the result:

```bash
python ~/.openclaw/skills/text-diff/text_diff.py side-by-side old.txt new.txt -o comparison.txt
```

**Output:**
```
OLD                          | NEW
---------------------------- | ----------------------------
line 1                       | line 1
line 2                       | line 2
line 3 (removed)             |                              
                             | line 3 (added)
line 4                       | line 4
```

### Additional Usage

```bash
# Context diff with 5 lines of context
python ~/.openclaw/skills/text-diff/text_diff.py context file1.txt file2.txt -c 5

# Unified diff without colors (for piping)
python ~/.openclaw/skills/text-diff/text_diff.py unified old.txt new.txt --no-color

# Save diff to file
python ~/.openclaw/skills/text-diff/text_diff.py unified old.txt new.txt -o diff.txt
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Files are identical |
| `1` | Files differ |
| `2` | File not found or permission error |
| `3` | Other error |

## Color Legend

When using colored output (default):
- **Red**: Removed lines
- **Green**: Added lines
- **Yellow**: Context markers (@@ lines)
- **Cyan**: File headers
