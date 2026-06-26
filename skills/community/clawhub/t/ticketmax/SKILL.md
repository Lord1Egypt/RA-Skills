---
name: ticketmax
description: Print markdown files to an ESC/POS thermal receipt printer over TCP, USB, or serial. Supports headings, bold, underline, tables, images, QR codes, paper cuts, and buzzer.
version: 0.1.3
metadata:
  openclaw:
    emoji: "🖨️"
    homepage: https://github.com/yatesdr/ticketmax
    requires:
      env:
        - PRINTER_ADDR
      bins:
        - ticketmax
    primaryEnv: PRINTER_ADDR
    install:
      - kind: go
        package: github.com/yatesdr/ticketmax@latest
        bins:
          - ticketmax
---

# ticketmax

Print markdown files to a thermal receipt printer. Write a `.md` file with standard markdown and ticketmax renders it on any ESC/POS printer over TCP, USB, or serial.

## Setup

Set `PRINTER_ADDR` to your printer's address:

```bash
# TCP:
export PRINTER_ADDR=192.168.1.100:9100
# USB:
export PRINTER_ADDR=/dev/usb/lp0
# Serial:
export PRINTER_ADDR=/dev/ttyUSB0
```

## Usage

```bash
# Print a markdown file
ticketmax report.md

# Pipe from stdin
echo "# Hello World" | ticketmax -

# Check printer connectivity
ticketmax -status

# Print a test receipt
ticketmax -test
```

## Flags

| Flag | Default | Description |
|---|---|---|
| `-addr` | `127.0.0.1:9100` | Printer host:port or device path (env: `PRINTER_ADDR`) |
| `-baud` | `9600` | Baud rate for serial connections |
| `-timeout` | `5s` | Network connection timeout |
| `-width` | `46` | Paper width in characters (1–120) |
| `-spacing` | `20` | Line spacing in printer units (0–255) |
| `-test` | | Print test receipt and exit |
| `-status` | | Check connectivity and exit |

## Markdown Syntax

| Markdown | Printer Output |
|---|---|
| `# Heading` | Bold, double-size, centered |
| `## Heading` | Bold, double-width, centered |
| `### Heading` | Bold |
| `**bold text**` | Bold line |
| `<u>text</u>` | Underlined line |
| `---` | Separator line |
| `\| A \| B \|` | Two columns (right-aligned values) |
| `\| A \| B \| C \|` | Three columns |
| `![alt](path)` | Print image (PNG, JPEG, GIF) |
| `` ```qr `` | QR code block |
| `<!-- cut -->` | Cut paper |
| `<!-- beep -->` | Buzzer (1 beep) |
| `<!-- beep N -->` | Buzzer (N beeps) |

## Example

To print a report, write markdown to a temp file and pipe it to ticketmax:

```bash
cat <<'EOF' > /tmp/report.md
# Morning Report

## Sales

| Item | Revenue |
| --- | --- |
| Widget A | $1,234 |
| Gadget B | $567 |

---

**Low stock: Widget A (3 units)**

```qr
https://dashboard.example.com
```

<!-- beep -->
EOF

ticketmax /tmp/report.md
```

Or pipe directly from stdin:

```bash
echo "# Alert\n\n**Server down at $(date)**\n\n<!-- beep 3 -->" | ticketmax -
```
