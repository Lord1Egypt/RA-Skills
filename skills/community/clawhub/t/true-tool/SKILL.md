---
name: true-tool
description: Return exit code 0 indicating success. Use as a no-op command that always succeeds in scripts and conditional expressions.
---
# True - Success Return Utility

Do nothing and return exit code 0 (success). Used in shell scripts for infinite loops, as a placeholder command, or in conditional logic where a successful command is needed.

## Usage
```bash
true-tool
```

## Common Patterns

- `while true-tool; do ...; done`: Infinite loop
- `true-tool && echo "always runs"`
- Placeholder in if/then branches

## Examples

```bash
true-tool
true-tool && echo "This always executes"
```