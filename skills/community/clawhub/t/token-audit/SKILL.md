---
name: token-audit
version: 0.2.0
description: >
  Workspace token consumption analyzer for OpenClaw agents. Scans workspace
  files, estimates token counts across 6 major models (GPT-4, Claude, Gemini,
  Llama, Mistral, Qwen), and surfaces hidden cost drivers. Identifies bloated
  context, redundant files, and optimization opportunities. Free, zero
  dependencies, no API keys.
author: "Cael (@CaelMaximus)"
license: MIT
tags:
  - security
  - tokens
  - cost
  - optimization
  - workspace
  - caelguard
---

# Token Audit

Analyze your OpenClaw workspace token consumption and costs across multiple models.

## Usage

### Scan your workspace
```bash
python3 scripts/token-audit.py
```

### Scan a specific path
```bash
python3 scripts/token-audit.py --workspace /path/to/workspace
```

### JSON output
```bash
python3 scripts/token-audit.py --json
```

## What It Finds

- Total token count per model (GPT-4, Claude 3, Gemini, Llama 3, Mistral, Qwen)
- Per-file token breakdown sorted by size
- Estimated costs per model at current pricing
- Files that are disproportionately large vs their utility
- Optimization recommendations

## Part of Caelguard

Free, open-source agent security toolkit. See also: [shellguard-scanner](https://clawhub.com/Justincredible-tech/shellguard-scanner)
