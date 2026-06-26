---
name: xxd-tool
description: Create hex dumps of binary files, convert hex dumps back to binary, and perform bit-level analysis and patching. Essential for reverse engineering, binary analysis, and protocol debugging.
---

# XXD Tool — Hex Dump & Binary Converter

Create hex/ASCII dumps from binary files, convert hex representations back to binary, perform bit-level editing, binary patching, and file comparison at the byte level.

## Quick Start

```bash
# Hex dump a binary file
xxd-tool file.bin

# Convert hex dump back to binary
xxd-tool -r dump.hex > output.bin

# Show first 100 bytes only
xxd-tool -l 100 file.bin
```

## Usage

```bash
xxd-tool FILE [OPTIONS]
xxd-tool -r INPUT [OPTIONS]  # Reverse mode (hex → binary)

Options:
  -l, --len N         Stop after N bytes
  -s, --skip N        Skip N bytes from start
  -r, --reverse       Convert hex dump back to binary
  -p, --plain         Plain hex output (no ASCII, no offsets)
  -c, --cols N        Format N octets per line (default: 16)
  -g, --groupsize N   Group output in N-byte chunks
  -b, --bits          Bit dump instead of hex
  -E, --endian        Show little-endian byte order
  -o, --offset N      Start at file offset N
  -i, --include       C-style include file output
  --patch OFFSET:HEX  Apply hex patch at byte offset
  --json              Output as structured JSON
```

## Examples

```bash
# Full hex dump
xxd-tool firmware.bin

# Skip first 256 bytes, show next 64 bytes
xxd-tool -s 256 -l 64 firmware.bin

# Plain hex output (no formatting, for piping)
xxd-tool -p file.bin

# Reverse: hex dump back to binary
xxd-tool -r dump.hex > restored.bin

# Binary patching
xxd-tool --patch "0x100:4A4B4C4D" firmware.bin

# Bit-level dump
xxd-tool -b config.bin

# C-style include output (embeds binary in C code)
xxd-tool -i icon.png > icon.h

# Byte-by-byte JSON output
xxd-tool file.bin --json
```

## Features

- **Standard hex dump** — offset, hex, ASCII side-by-side
- **Reverse mode** — hex dump back to original binary
- **Plain hex** — pipeline-friendly raw hex output
- **Bit-level dump** — individual bit display
- **Binary patching** — in-place byte modification
- **Selective dump** — skip/limit bytes for focused analysis
- **C-style output** — embed binary data in C source code
- **Configurable formatting** — columns, groupsize, endianness
- **JSON output** — structured byte-level data
