# Background Router Artifact Launches

Use this pattern when a user asks to run super-router in background mode and produce a durable artifact such as an HTML report.

## Pattern

1. Build small, auditable support files before launching:
   - a source/context collection script, if the task depends on local code or data;
   - a router prompt file for complex/multiline task text;
   - a wrapper script that records `run_dir`, status, router stream log, final artifact path, and verification results.
2. Launch the wrapper with `exec(background=true, notify_on_complete=true)`.
3. If the launch succeeds, immediately poll once to verify the process is actually running or completed with useful output.
4. The wrapper should tee router stdout/stderr to a log and preserve the exact prompt/context used for the run.
5. For artifact-producing jobs, generate or finalize the artifact only from real collected context and router output. If router/provider execution fails, the artifact may still be created only if it truthfully records the failure/log tail and uses verified local context; never hide a failed router run behind a polished report.
6. Verify the final artifact directly before claiming success, e.g. `wc -c`, section/card counts, and any required source-derived sections.
7. If the command guard blocks the launch, do not retry, rephrase, or work around it. Report the prepared files and the exact blocked launch scope, then wait for user approval.

## Wrapper skeleton

```bash
#!/usr/bin/env bash
set -u
SRC="$HOME/path/to/source"
RUN_DIR="$HOME/.openclaw/logs/task_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RUN_DIR"
CTX="$RUN_DIR/source_context.md"
PROMPT="$RUN_DIR/router_prompt.txt"
LOG="$RUN_DIR/super_router_stream.log"
OUT="$HOME/path/to/output.html"
STATUS="$RUN_DIR/status.txt"

python3 collect_context.py "$SRC" "$CTX" 2>&1 | tee -a "$STATUS"
{
  /bin/cat prompt_base.txt
  printf '\n\n# Source-derived context\n\n'
  /bin/cat "$CTX"
} > "$PROMPT"

ROUTER_EXIT=0
(
  export ROUTER_TASK="$(/bin/cat "$PROMPT")"
  /opt/homebrew/Caskroom/miniforge/base/bin/python \
    "$HOME/.openclaw/skills/super-router/scripts/router.py" --stream
) 2>&1 | tee "$LOG" || ROUTER_EXIT=${PIPESTATUS[0]}

python3 generate_artifact.py "$SRC" "$CTX" "$LOG" "$OUT" 2>&1 | tee -a "$STATUS"
BYTES=$(wc -c < "$OUT" | tr -d ' ')
SECTIONS=$(grep -Eo '<section id="[^"]+"' "$OUT" | wc -l | tr -d ' ')
printf '[verify] html=%s bytes=%s sections=%s router_exit=%s\n' \
  "$OUT" "$BYTES" "$SECTIONS" "$ROUTER_EXIT" | tee -a "$STATUS"
```

## Why this matters

Background router jobs otherwise become opaque: the user sees only that a process was launched, while the prompt, source evidence, partial provider output, and artifact verification may be scattered or lost. A wrapper turns the job into a reproducible run directory and makes blocked launches safe to report without pretending work is still running.
