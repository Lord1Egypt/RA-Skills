---
name: test-tool
description: Evaluate conditional expressions for file testing, string comparison, and arithmetic checks. Use for shell script conditionals.
---
# Test - Condition Evaluator

Evaluate expressions and return exit status 0 (true) or 1 (false). Used for file attribute testing, string comparison, and numeric checks in scripts.

## Usage
```bash
test-tool <expression>
```

## Common Tests

- `-f file`: True if file exists
- `-d dir`: True if directory exists
- `-z str`: True if string is empty
- `n1 -eq n2`: True if numbers equal
- `s1 = s2`: True if strings equal

## Examples

```bash
test-tool -f /etc/passwd
test-tool -d /home/user
test-tool 5 -gt 3
```