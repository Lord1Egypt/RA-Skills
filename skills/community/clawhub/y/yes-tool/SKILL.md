---
name: yes-tool
description: Repeatedly output a string (or 'y' by default) for automated scripts, batch confirmation, and pipeline input generation.
---

# Yes Tool — Automatic Response Generator

Repeatedly output a string (default: "y") to automatically confirm prompts, fill form inputs, and generate repeated text for testing and automation. Essential for unattended script execution and batch processing.

## Quick Start

```bash
# Automatically confirm all prompts
yes-tool | apt-get install -y package-name

# Use a custom response
yes-tool "I agree to the terms" | setup-script.sh
```

## Usage

```bash
yes-tool [STRING] [OPTIONS]
yes-tool [OPTIONS]  # Default: outputs "y"

Options:
  --count N       Stop after N repetitions
  --lines N       Alias for --count (output N lines)
  --sleep SEC     Add delay between outputs (rate limiting)
  --newline       Include newline after each output (default)
  --no-newline    No trailing newline (contiguous output)
  --hex HEXBYTES  Output repeated hex bytes
  --json          Output as JSON stream
```

## Examples

```bash
# Default usage (outputs "y" forever until pipe closes)
yes-tool | rm -rf dir/*

# Custom response for unattended install
yes-tool "YESSIR" | ./configure

# Generate 10 lines of "test data"
yes-tool "test data" --count 10

# Rate-limited output (1 per second)
yes-tool "keepalive" --sleep 1 | nc server 8080

# Output hex bytes instead of text
yes-tool --hex "00FF"

# No newline (continuous single line)
yes-tool "x" --no-newline --count 100

# JSON streaming output
yes-tool "hello" --count 5 --json
```

## Features

- **Default response** — outputs "y" for automatic confirmation
- **Custom string** — repeat any text or character
- **Count limit** — stop after N repetitions
- **Rate limiting** — sleep between outputs
- **Hex mode** — output raw bytes
- **No-newline mode** — contiguous output stream
- **JSON output** — structured stream for pipeline testing
- **Pipe-friendly** — works with any stdin-consuming process
