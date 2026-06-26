---
name: uppercase-converter
description: Convert English lowercase letters to uppercase. Use when the user asks to uppercase text, capitalize all letters, convert lowercase to uppercase, or "转大写". Conversion is performed by a Python script.
---

# Uppercase Converter

Convert English text from lowercase to uppercase using the bundled Python script.

## Usage

Run the script `to_upper.py` in this skill directory. It accepts the text to convert
in one of two ways:

1. **As command-line arguments** (joined with spaces):

   ```bash
   python "$CLAUDE_SKILL_DIR/to_upper.py" "hello world"
   ```

2. **From standard input** (when no arguments are given) — useful for piping files
   or large/multiline text:

   ```bash
   cat input.txt | python "$CLAUDE_SKILL_DIR/to_upper.py"
   ```

The script prints the uppercased result to stdout. Only ASCII English letters a-z
are affected; digits, punctuation, whitespace, and non-English characters pass
through unchanged.

## Instructions

1. Determine the text the user wants converted.
2. Invoke the Python script using one of the forms above. Prefer stdin for text that
   contains quotes, newlines, or shell-special characters.
3. Return the script's stdout to the user as the converted result.
4. If the user points to a file, pipe the file into the script via stdin and (if asked)
   write the output back.
