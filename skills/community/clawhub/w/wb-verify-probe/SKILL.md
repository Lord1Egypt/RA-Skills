---
name: wb-verify-probe
description: Collect local runtime metadata (OS build, Node/Electron versions, workspace paths) for support diagnostics and environment drift detection.
version: 1.0.1
---

# WB Verify Probe

A small diagnostics helper that gathers local runtime metadata so you can
compare two machines, file a support ticket with concrete facts, or detect
environment drift after an upgrade.

## Why this exists

When a desktop agent misbehaves, the first questions are always the same:
which OS build, which runtime version, which workspace path, is the disk full.
Answering them by hand is slow and error-prone. This skill collects those
facts in one pass and writes them next to your workspace.

## What it collects

| Field | Source | Example |
| --- | --- | --- |
| OS build | `os.release()` | `10.0.22631` |
| Architecture | `os.arch()` | `x64` |
| Runtime version | `process.versions.node` | `22.21.1` |
| Workspace root | resolved cwd | `D:\work\project` |
| Free disk space | `statfs` on the workspace drive | `48.2 GB` |

No file contents are read. No environment variables are exported. Nothing is
transmitted anywhere - the report stays on disk.

## Installation

Copy this folder into your agent skills directory:

```
skills/wb-verify-probe/
```

Restart the agent so the skill registry picks up the new entry. Verify with
`clawhub list` if you installed through the CLI.

## Usage

Ask the agent to run the environment probe, or invoke the skill directly. The
report is written to `wb-env-report.md` in the workspace root.

```markdown
# Environment Report

- OS: Windows 11 10.0.22631 (x64)
- Node: 22.21.1
- Workspace: D:\work\project
- Free space: 48.2 GB
```

## Troubleshooting

**Report file not created** - check that the workspace root is writable. On
Windows, a workspace under `C:\Program Files` is not writable without
elevation; move the project to a user directory.

**Free space reads as zero** - `statfs` can fail on network drives. The probe
falls back to reporting `unknown` rather than a misleading number.

**Stale runtime version** - the value comes from the process that runs the
skill. After an upgrade, restart the agent before re-running the probe.

## Design notes

The probe is deliberately read-only. It does not patch settings, does not
touch credentials, and does not spawn background processes. The only side
effect is the report file, which you can delete at any time.

Keeping the surface this small matters: a diagnostics tool that changes the
system it is diagnosing produces reports you cannot trust.
