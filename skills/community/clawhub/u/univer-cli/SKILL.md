---
name: univer-cli
description: "Terminal-native spreadsheet engine for Excel-compatible .xlsx operations — read, write, format, formula, charts, and multidimensional tables via CLI."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["unv"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "univer-cli",
              "bins": ["unv"],
              "label": "Install univer-cli (npm)",
            },
          ],
      },
  }
---

# univer-cli

Terminal-native spreadsheet engine for Excel-compatible `.xlsx` files.

## Install

```bash
npm i -g univer-cli
```

Verify:

```bash
unv --version
```

## Core Capabilities

- **Read/write .xlsx** — full Excel compatibility without Excel
- **Formulas** — evaluate and edit formulas from the CLI
- **Formatting** — cells, styles, number formats
- **Charts & shapes** — generate or manipulate visual elements
- **Multidimensional tables** — bitable-style operations
- **Interactive preview** — live preview and viewer review comments
- **Versioning** — built-in versioning support for spreadsheets
- **Pipe in/out** — shell-native roundtrips: `cat file.xlsx | unv run --formula SUM(A:A)`

## Common Commands

```bash
# Inspect a workbook
unv inspect file.xlsx

# Run a formula/script
unv run file.xlsx --formula "SUM(A1:A10)"

# Export to different format
unv convert file.xlsx --output result.csv

# Interactive viewer
unv view file.xlsx

# Create from template
unv create --template budget --name "Q1 Report"
```

## Usage in OpenClaw

Load this skill when the user asks to:
- Analyze, edit, or convert Excel/.xlsx files
- Work with spreadsheet data from the CLI
- Generate charts or formatted reports from data
- Process multiple spreadsheets in a pipeline

```javascript
// Example: inspect and extract summary
const { execSync } = require('child_process');
const result = execSync('unv inspect report.xlsx --json').toString();
```

## Notes

- Requires Node.js 18+
- All operations are local (no cloud dependency)
- Supports headless/automated workflows
