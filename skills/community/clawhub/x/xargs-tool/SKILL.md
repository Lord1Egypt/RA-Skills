---
name: xargs-tool
description: Build and execute command lines from standard input — batch process arguments, parallel execution, argument substitution, and delimiter control.
---

# Xargs Tool — Command Builder & Batch Executor

Read items from stdin and execute a command with those items as arguments. Essential for batch processing large file lists, parallel task execution, and chaining complex command pipelines.

## Quick Start

```bash
# Delete multiple files
echo "file1.txt file2.txt" | xargs-tool rm -f

# Process output from another command
ls *.log | xargs-tool gzip
```

## Usage

```bash
xargs-tool COMMAND [ARGS...] [OPTIONS]
SOURCE_ITEMS | xargs-tool COMMAND [ARGS...] [OPTIONS]

Options:
  -n, --max-args N    Maximum arguments per command invocation
  -P, --parallel N    Run N processes in parallel
  -I, --replace STR   Replace STR in command with each input line
  -d, --delimiter C   Input delimiter character (default: whitespace)
  -0, --null          Input items are null-separated (for find -print0)
  -p, --interactive   Prompt before each execution
  -t, --verbose       Print each command before executing
  --show-limits       Show system limits for command length
  --dry-run           Print what would be done without executing
```

## Examples

```bash
# Process a find result safely (null-separated)
find . -name "*.tmp" -print0 | xargs-tool -0 rm -f

# Parallel compression (4 processes at once)
ls *.log | xargs-tool -P 4 gzip

# Custom replacement (one command per item)
ls *.txt | xargs-tool -I {} cp {} /backup/{}

# Interactive removal
ls old-files/ | xargs-tool -p rm

# Batch 10 args per invocation (reduce process count)
cat image-list.txt | xargs-tool -n 10 convert --resize 800x600

# Dry-run to preview
echo "*.py" | xargs-tool --dry-run -I {} cp {} /backup/
```

## Features

- **Batch processing** — split large inputs into manageable command invocations
- **Parallel execution** — speed up batch jobs with -P N
- **Custom substitution** — place input items anywhere in the command with -I
- **Null-separated input** — safe handling of filenames with spaces/special chars
- **Interactive mode** — confirm each operation
- **Dry-run** — preview without executing
- **Verbose mode** — see each command as it runs
- **System-aware** — respects ARG_MAX limits
