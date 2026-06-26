---
name: random-tool
description: Generate random numbers, passwords, and strings with configurable length and character sets. Use for security tokens, testing data, and randomization.
---
# Random - Data Generator

Generate cryptographically secure random values including integers within a range, random passwords with customizable character sets, and random strings for testing.

## Usage
```bash
random-tool [options]
```

## Options

- `-l N`: Generate string of length N
- `-n MIN MAX`: Random integer between MIN and MAX
- `-p`: Generate a random password (alphanumeric + symbols)

## Examples

```bash
random-tool -l 32
random-tool -n 1 100
random-tool -p -l 16
```