---
name: slim
description: A pluggable pipe filter that strips verbose CLI output (huge YAML/JSON dumps, lockfiles, long diffs) before it reaches the LLM, so an agent spends its context budget on signal, not noise. Lossless cleanups always-on; large dumps clamped to head+tail with a clear elision marker.
version: 0.1.0
homepage: https://workloft.ai/labs
metadata:
  openclaw:
    emoji: "✂️"
    requires:
      bins:
        - python3
        - bash
---

# slim

Agents rarely need a 10k-line `kubectl get -o yaml`, a full `package-lock.json`,
or a 2,000-line diff to make the next decision. `slim` sits in the pipe, applies
always-safe cleanups, and clamps genuinely huge dumps to head + tail with a clear
elision marker the agent can act on (or re-run without `slim` for full fidelity).
Pure Python standard library.

The executable is `{baseDir}/bin/slim`.

## When to use this

Pipe a command through `slim` when its output is likely to be large and mostly
noise — cluster dumps, dependency trees, lockfiles, long diffs, verbose install
logs — and you only need the signal. Do NOT use it when you need exact, complete
output (then run the command directly).

## How to use it

```
# pipe mode — pass the command so slim can pick the right clamp
kubectl get pods -o yaml | {baseDir}/bin/slim --cmd "kubectl get pods -o yaml"

# exec wrapper
{baseDir}/bin/slim --report -- git log -p -8

# savings summary printed to stderr; filtered output to stdout
some-build | {baseDir}/bin/slim --report
```

`--report` prints a one-line savings summary to **stderr**; filtered output always
goes to **stdout**, so `slim` stays composable in a pipe.

## What it does

**Always-on (lossless of signal):** strips ANSI colour codes, trims trailing
whitespace, collapses blank-line runs, collapses 3+ identical consecutive lines
to `... (repeated Nx)`.

**Opt-in clamp (lossy by design, per-command):** unrecognised commands clamp only
when > 250 lines (60 head + 30 tail); `kubectl -o yaml/json` clamps to 25 head +
10 tail; `pip` install logs drop download/progress noise.

## Notes for the agent

- Reference the tool as `{baseDir}/bin/slim` — never hardcode a path.
- The clamp is lossy: if a clamped result hides what you needed, re-run the
  command without `slim`.
- Add a plugin by registering a `Callable[[str], str]` in `slim/plugins.py`.
- On Claude Code specifically, a `PostToolUse` hook cannot rewrite tool output —
  so the saving has to happen at the tool layer, i.e. piping through `slim`.
- Built by Workloft (https://workloft.ai/labs). Inspired by lowfat.
