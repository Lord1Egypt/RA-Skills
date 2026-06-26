---
name: seq-tool
description: Generate sequences of numbers with configurable start, end, and increment values. Use for creating numbered lists, loops, and ranges.
---
# Seq - Number Sequence Generator

Print sequences of numbers from START to END with optional INCREMENT. Supports integer and decimal sequences for various use cases.

## Usage
```bash
seq-tool [options] [first] [increment] <last>
```

## Options

- `-w`: Equal-width padding with leading zeros
- `-s STR`: Use STR as separator (default: newline)
- `-f FORMAT`: Use printf-style format string

## Examples

```bash
seq-tool 1 10
seq-tool 0 2 10
seq-tool -w 1 100
```