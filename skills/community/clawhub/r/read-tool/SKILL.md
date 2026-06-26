---
name: read-tool
description: Read a line from standard input into a variable. Use for interactive shell prompts and script input handling.
---
# Read - Input Capture Utility

Read a line of text from standard input and store it for use in scripts. Supports prompts, timeouts, and silent input mode for passwords.

## Usage
```bash
read-tool [options] [variable_name]
```

## Options

- `-p PROMPT`: Display prompt before reading
- `-t N`: Timeout after N seconds
- `-s`: Silent mode (don't echo input)

## Examples

```bash
read-tool -p "Enter name: " NAME
read-tool -s -p "Password: " PASS
read-tool -t 5 TIMEOUT_VAR
```