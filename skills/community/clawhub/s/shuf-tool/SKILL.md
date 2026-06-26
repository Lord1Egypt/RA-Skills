---
name: shuf-tool
description: Randomly shuffle lines of text input. Use for random sampling, data randomization, and selection tasks.
---
# Shuf - Random Line Permutation

Randomize the order of input lines. Supports random selection of N lines and sampling with or without replacement for statistical tasks.

## Usage
```bash
shuf-tool [options] [file]
```

## Options

- `-n N`: Output only N random lines
- `-i LO-HI`: Treat each number LO..HI as an input line
- `-r`: Allow repeated output (sampling with replacement)
- `-e`: Treat each argument as an input line

## Examples

```bash
shuf-tool names.txt
shuf-tool -n 5 data.txt
shuf-tool -i 1-100
```