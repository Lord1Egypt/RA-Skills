# ToolFlow OpenClaw Operator

Bundled ClawHub installer for operating ToolFlow from within OpenClaw.

This package now includes:
- the OpenClaw-facing operator skill
- a bundled local ToolFlow plugin/runtime payload
- installer and verification scripts

## Quick install after ClawHub install

From the installed skill folder, run:

```sh
./scripts/install-toolflow-openclaw.sh
```

Then verify:

```sh
./scripts/verify-toolflow-openclaw.sh
```

What the installer does:
- links the bundled ToolFlow plugin into OpenClaw with `openclaw plugins install --link`
- keeps the runtime and plugin payload together inside the installed skill folder
- runs a ToolFlow doctor check
- works on plain Bash hosts, including clean Ubuntu VPS installs

Repository:
- <https://github.com/mcg-tries-to-code/ToolFlow>

Use it for:
- multi-step workflows
- approval-bound elevated work
- recoverable long-running jobs
- progress-visible execution
