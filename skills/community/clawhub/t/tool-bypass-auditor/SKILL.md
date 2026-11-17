---
name: tool-bypass-auditor
description: Detect tool bypass attempts and exec/shell overuse in local session/evolution artifacts, then produce a concise bypass audit report with low/medium/high findings.
---

# Tool Bypass Auditor

## Usage

```bash
node skills/tool-bypass-auditor/index.js
node skills/tool-bypass-auditor/index.js C:/Users/Admin/.openclaw/workspace
```

## Features

- Scans local JSONL artifacts for likely tool bypass patterns
- Correlates repeated exec/shell usage against available registered tools
- Flags unsafe flags, ad-hoc scripts, and temporary execution workarounds
- Outputs a concise report with severity levels

## Output

```
=== Tool Bypass Audit ===
Workspace: <workspace>
Time: <timestamp>

Summary:
  total_findings: N
  bypass_likely: N
  exec_overuse: N
  recommendations: [...]
```

## Safety

- Read-only skill. Never edit, delete, or exfiltrate files.
- Do not execute discovered scripts or payloads.
