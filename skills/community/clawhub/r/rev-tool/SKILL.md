---
name: rev-tool
description: Reverse each line of text character by character. Use for text analysis, palindrome detection, and data format conversion.
---
# Rev - Character Reversal Utility

Reverse the characters on each line of input, mirroring the content left-to-right. Simple tool for text transformation and analysis tasks.

## Usage
```bash
rev-tool [file...]
```

Reads from stdin when no file is specified. Each line is independently reversed character by character.

## Examples

```bash
# Reverse lines in a file
rev-tool text.txt

# Reverse piped input
echo "stressed" | rev-tool
```