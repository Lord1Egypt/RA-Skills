---
name: "system-commander"
description: "Convert user tasks to optimal Linux/Python commands. Use when user needs file processing, data extraction, text manipulation, or any task that can be solved with system-level tools instead of AI inference."
version: "1.0.0"
author: "Frugal Orchestrator"
tags: ["system", "linux", "commands", "token-efficiency", "optimization"]
trigger_patterns:
  - "system command"
  - "linux command"
  - "bash script"
  - "one-liner"
  - "file processing"
  - "text extraction"
  - "data parsing"
  - "batch process"
  - "system first"
  - "token efficient"
allowed_tools: ["code_execution", "document_query", "search_engine"]
---

# System Commander

## When to Use

Activate this skill when:
- User asks for file processing, text manipulation, or data extraction
- Task can be solved with Linux/Python commands
- Goal is to minimize AI inference and maximize efficiency
- Keywords: "system command", "linux", "bash", "one-liner", "file processing"

## Core Philosophy: System First, AI Last

Before any AI reasoning, try these in order:

1. **Pure Linux tools** - `awk`, `sed`, `grep`, `cut`, `tr`, `sort`, `uniq`
2. **Linux + file tools** - `find`, `xargs`, `parallel`, `jq`, `csvkit`
3. **Python one-liners** - Quick scripts for complex logic
4. **AI subordinate** - Only when above won't suffice

## Command Patterns by Task Type

### File Operations

| Task | System Solution | AI Solution |
|------|-----------------|-------------|
| List large files | `find . -size +100M -ls` | ❌ Don't delegate |
| Count lines | `wc -l file.txt` | ❌ Don't delegate |
| Search text | `grep -r "pattern" .` | ❌ Don't delegate |
| Replace text | `sed -i 's/old/new/g' file` | ❌ Don't delegate |
| Extract column | `awk -F',' '{print $2}' file.csv` | ❌ Don't delegate |

### Data Processing

| Task | System Solution | AI Solution |
|------|-----------------|-------------|
| JSON query | `jq '.key.subkey' file.json` | ❌ Don't delegate |
| CSV manipulation | `csvcut -c 1,3 file.csv` | ❌ Don't delegate |
| Sort & unique | `sort file  uniq -c` | ❌ Don't delegate |
| Join files | `join -t',' file1 file2` | ❌ Don't delegate |

### Text Processing

| Task | System Solution | AI Solution |
|------|-----------------|-------------|
| Line extraction | `sed -n '5,10p' file` | ❌ Don't delegate |
| Word count | `tr ' ' '\n'  sort  uniq -c` | ❌ Don't delegate |
| Format conversion | `iconv -f UTF-8 -t ASCII` | ❌ Don't delegate |

## Response Format

When generating commands:

1. **Provide the command** (ready to copy-paste)
2. **Explain what it does** (brief)
3. **Show expected output** (example)
4. **Note alternatives** (if applicable)

## Examples

### Example 1: Extract Email Addresses

**User**: "Extract all email addresses from this log file"

**System Commander Response**:
```bash
# Extract emails using grep with regex
grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' logfile.txt | sort -u

# What it does:
# - -o: output only matching parts
# - -E: extended regex
# - Sorts and removes duplicates
```

### Example 2: Count Files by Extension

**User**: "Count how many files of each type are in this directory"

**System Commander Response**:
```bash
# Count files by extension
find . -type f | sed 's/.*\.//' | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -rn

# What it does:
# - Find all files
# - Extract extension (last . to end)
# - Normalize case
# - Count and sort by frequency
```

### Example 3: Parse JSON Values

**User**: "Get all 'status' values from this JSON file"

**System Commander Response**:
```bash
# Using jq (install with apt-get install jq)
jq -r '.[].status' data.json | sort | uniq -c

# Alternative using grep (if jq unavailable):
grep -oP '"status": "\K[^"]+' data.json | sort | uniq -c
```

### Example 4: Batch Rename Files

**User**: "Rename all .txt files to .bak"

**System Commander Response**:
```bash
# Dry run first (see what would happen)
ls *.txt | sed 's/\.txt$//' | xargs -I {} echo mv {}.txt {}.bak

# Execute if looks correct
ls *.txt | sed 's/\.txt$//' | xargs -I {} mv {}.txt {}.bak

# One-liner alternative:
for f in *.txt; do mv "$f" "${f%.txt}.bak"; done
```

## Advanced Patterns

### Parallel Processing

```bash
# Process files in parallel (4 jobs)
find . -name '*.log' | xargs -P 4 -I {} grep 'ERROR' {}

# Using GNU parallel (apt-get install parallel)
find . -name '*.json' | parallel 'jq .name {}'
```

### Complex Text Extraction

```bash
# Extract text between markers
sed -n '/START/,/END/p' file.txt

# Multi-line pattern replacement
sed '/pattern/{n;s/old/new/}' file.txt

# Process only matching files
grep -l 'pattern' *.txt | xargs sed -i 's/old/new/g'
```

### Data Transformation

```bash
# CSV to JSON (requires csvkit)
csvjson data.csv > data.json

# JSON to CSV
jq -r '.[] | [.key1, .key2] | @csv' data.json > output.csv

# Column statistics
awk -F',' '{sum+=$3} END {print "Sum:", sum, "Avg:", sum/NR}' data.csv
```

## Python One-Liners

When pure Linux isn't enough, use Python:

```bash
# Complex JSON processing
python3 -c "
import json,sys
data=json.load(open('file.json'))
print([x['name'] for x in data if x['active']])
"

# Text processing with regex
python3 -c "
import re,sys
for line in sys.stdin:
    m=re.search(r'pattern', line)
    if m: print(m.group(1))
" < input.txt
```

## When NOT to Use System Commands

Don't suggest system commands when:
- Task requires natural language understanding
- Contextual analysis of meaning
- Creative writing or content generation
- Complex multi-step reasoning
- Security-sensitive operations needing verification

## Token Efficiency Rules

1. **Never rewrite command output** - Use `§§include()` instead
2. **Prefer pipes over loops** - `|` chains are more efficient
3. **Use built-in tools** - `awk`, `sed` vs Python imports
4. **Batch operations** - Process all files at once with `xargs`

## Installation Prerequisites

Some commands need packages:

```bash
# JSON processing
apt-get install jq

# CSV processing
apt-get install csvkit

# Parallel execution
apt-get install parallel

# Text processing
apt-get install silversearcher-ag  # ag command
```

## Skill Integration

This skill works with:
- **agent-orchestrator**: System commands become subtask solutions
- **a0-token-optimizer**: Minimal tokens for maximum utility
- **toon-adoption**: Store command patterns in TOON format
