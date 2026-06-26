---
name: reverse-tool
description: Reverse the order of lines or characters in text input. Use for text transformation, palindrome checking, and data reordering.
---
# Reverse - Text Reversal Utility

Reverse lines of text or characters within each line. Supports line-level reversal (last line first) and character-level reversal within lines.

## Usage
```bash
reverse-tool [options] <file>
```

## Options

- `-c`: Reverse characters within each line (not lines)
- `-w`: Reverse word order within each line

## Examples

```bash
# Reverse line order
reverse-tool file.txt

# Reverse characters per line
reverse-tool -c palindrome.txt

# Pipe input
echo "hello world" | reverse-tool -c
```