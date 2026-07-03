# Source-to-HTML Background Router Wrapper

Use this pattern when the user asks Super-Router to analyze a local source tree and produce a durable HTML explainer/diagram/report while explicitly requesting `background=true + notify_on_complete=true`.

## What to build before launch

Create a reproducible run directory under `~/.openclaw/logs/<task>_<timestamp>/` with:

- `collect_<topic>_context.py` — deterministic source scanner that writes JSON. Keep it source-derived: file inventory, line counts, key build/config files, exported symbols, representative function names, doc comments, and subsystem buckets.
- `make_router_prompt.py` — converts the JSON inventory into a compact prompt. Avoid stuffing entire source files into `ROUTER_TASK`; summarize evidence and include paths.
- `generate_<topic>_html.py` — creates the final self-contained HTML from the source JSON plus the router stream log. If the router fails, the HTML may still be generated only if it truthfully records the failure/log excerpt and relies on verified local context.
- `run_<topic>_router.sh` — wrapper that runs collection, prompt generation, `router.py --stream`, artifact generation, and verification.

## Wrapper requirements

The wrapper should:

1. `set -uo pipefail`, create/clear `status.txt`, and print run scope (`src`, `out`, `router`).
2. Run the context collector first and fail immediately if collection fails.
3. Build the prompt file, then launch router via `ROUTER_TASK="$(/bin/cat "$PROMPT")"`.
4. Use `zsh -lic` for the router invocation so the same environment/profile setup as interactive Super-Router is visible.
5. Tee router stdout/stderr to `super_router_stream.log` and preserve `ROUTER_EXIT` without preventing artifact generation.
6. Generate the HTML after router completion from real `context.json` and `super_router_stream.log`.
7. Verify the artifact directly with objective thresholds: byte count, `<section>` count, workflow/card/detail counts, and final path.
8. Exit non-zero only for real collection/generation/verification failure, not merely because the router provider failed, as long as the artifact clearly reports that failure.

## Launch and immediate response

Launch exactly with `exec(background=true, notify_on_complete=true)` when the user requested background mode. Immediately poll once with `process(action="poll")` to verify the process is actually running or has already completed.

The user-facing reply after launch is not a success claim. It should include:

- process session id;
- `background=true` and `notify_on_complete=true` confirmation;
- run directory;
- wrapper path;
- expected final artifact path;
- immediate poll status (`running`, `completed`, or failed with log/status hint).

Do not say the artifact is done until the background completion notification arrives and the artifact has been verified directly.

## HTML artifact notes

For source hierarchy explainers, pair this with `html-artifact` conventions:

- self-contained file: inline CSS/SVG, no CDN, no remote assets;
- source-derived metrics near the top;
- an elaborated SVG hierarchy picture;
- workflow cards for the main execution paths;
- subsystem guide grouped by source buckets;
- key symbol/function anchors extracted deterministically from the source tree when the source language makes that practical;
- a Super-Router section that records run dir, context JSON, router log path, router exit code, and phase/token excerpt.

If the router provider partially fails but the wrapper can still generate the artifact from verified local context, the HTML must say that explicitly in the provenance section. Do not claim the failed provider analysis succeeded; make the source inventory plus verification thresholds the source of truth.

## Minimal verification line

At the end of the wrapper, write something like:

```bash
BYTES=$(wc -c < "$OUT" | tr -d ' ')
SECTIONS=$(grep -Eo '<section' "$OUT" | wc -l | tr -d ' ')
WORKFLOWS=$(grep -Eo 'class="workflow"' "$OUT" | wc -l | tr -d ' ')
DETAILS=$(grep -Eo '<details' "$OUT" | wc -l | tr -d ' ')
printf '[verify] html=%s bytes=%s sections=%s workflows=%s details=%s router_exit=%s\n' \
  "$OUT" "$BYTES" "$SECTIONS" "$WORKFLOWS" "$DETAILS" "$ROUTER_EXIT" | tee -a "$STATUS"
```

Use task-appropriate thresholds so a half-written artifact fails loudly.
