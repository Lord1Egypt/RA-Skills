# slim

A pluggable filter that strips verbose CLI output **before it reaches the LLM**,
so an agent spends its context budget on signal, not noise. Inspired by
[lowfat](https://github.com/zdk/lowfat).

Agents rarely need a 10k-line `kubectl get -o yaml`, a full `package-lock.json`,
or a 2,000-line diff to make the next decision. `slim` sits in the pipe, applies
always-safe cleanups, and clamps genuinely huge dumps to head + tail with a clear
elision marker the agent can act on (or re-run without `slim` for full fidelity).

## Usage

```bash
# pipe mode
kubectl get pods -o yaml | slim --cmd "kubectl get pods -o yaml"
some-build | slim --report          # savings summary on stderr

# exec wrapper
slim --report -- git log -p -8
```

`--report` prints a one-line savings summary to **stderr**; the filtered output
always goes to **stdout** so `slim` stays composable in a pipe.

## What it does

**Always-on (lossless of signal):**
- strips ANSI colour codes
- trims trailing whitespace
- collapses runs of blank lines
- collapses 3+ identical consecutive lines to `... (repeated Nx)`

**Opt-in clamp (lossy by design, per-command):**
- unrecognised commands: clamp only when > 250 lines, keeping 60 head + 30 tail
- `kubectl` (`-o yaml`/`-o json` dumps): clamp hard to 25 head + 10 tail
- `pip` install logs: drop download/progress-bar noise

Add a plugin by registering a `Callable[[str], str]` in `slim/plugins.py`.

## Why a filter, not a hook

On Claude Code, a `PostToolUse` hook **cannot rewrite** the tool output the model
sees — it can only add context alongside the full, unmodified dump. So the
token saving has to happen at the tool layer: pipe the command through `slim`.

## Measured savings

Reproduce with `python3 bench.py` (real command output on this machine):

| command               | raw chars | full slim % |
| --------------------- | --------: | ----------: |
| git log -p -8         |    78,230 |       95.7% |
| cat package-lock.json |   235,199 |       98.8% |
| npm ls --all          |    36,202 |       89.9% |
| git diff HEAD~3       |    55,451 |       94.8% |
| pip list -v           |    37,436 |        0.0% |

**Aggregate: 88.7% fewer characters (~110,600 → ~12,500 estimated tokens).**
Token figures are estimates (chars/4). The saving is dominated by clamping large
dumps; on already-clean output the lossless cleanups alone save little. `slim` is
opt-in per command precisely so you choose the fidelity tradeoff.

## Tests

```bash
python3 -m unittest discover -s tests
```
