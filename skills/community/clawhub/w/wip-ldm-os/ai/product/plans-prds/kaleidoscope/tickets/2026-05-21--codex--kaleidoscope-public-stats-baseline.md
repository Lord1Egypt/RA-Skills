# Kaleidoscope Public Stats Baseline

**Date:** 2026-05-21
**Filed by:** Codex, with Parker
**Status:** open
**Priority:** P0 launch metrics and live-wall correctness
**Master:** `../kaleidoscope-master-ticket.md`
**Roadmap:** `../kaleidoscope-roadmap.md`
**Surface:** `src/hosted-mcp/server.mjs`, `src/hosted-mcp/demo/index.html`, `wip.computer/visualizations/kaleidoscope/onboarding/live/`, tests if needed

## Goal

Keep the current Kaleidoscope live-wall totals visible, but define a server-side baseline date and counting model so future public stats can separate launch-era/test history from new activity.

This is a stats and accounting contract ticket. Do not delete wall images. Do not reset the live wall. Do not change generation behavior.

## Product Decision

Start the public count from the launch snapshot instead of trying to clean up old rows manually.

Baseline:

```text
Baseline date: 2026-05-21 Pacific time
Keys Created baseline: 3
Generic Kaleidoscopes baseline: 11
Image Based Kaleidoscopes baseline: 3
```

Public display should preserve the current totals and add future activity on top:

```text
Generic Kaleidoscopes: 11 plus new generic Kaleidoscopes after baseline
Image Based Kaleidoscopes: 3 plus new image-based Kaleidoscopes after baseline
Keys Created: 3 plus new non-test keys after baseline
```

## Test And Internal Account Rule

Going forward, Parker will use account handles beginning with:

```text
wiptest-
```

Any account handle beginning with `wiptest-` is internal/test and excluded from the public `Keys Created` count.

Do not infer external users from generic account labels such as:

```text
passkey-*
user-*
```

Those names are implementation artifacts, not product classification.

## Date Window Function

Add server-side date/window helpers so the stats API can compute:

- created since baseline
- created in the last 24 hours
- latest created timestamp

Use server-side timestamps. Do not use client time.

Use the Pacific date boundary for the baseline.

## Suggested Public Stats

The live wall can show six public stats:

```text
Generic Kaleidoscopes
Image Based Kaleidoscopes
Public Wall Images
Keys Created
New Since Baseline
Last Created
```

If the UI needs to stay simpler for launch, the server should still return the expanded fields and the UI can choose which ones to display.

## Implementation Requirements

- Keep existing live-wall image entries.
- Keep the existing public wall images.
- Do not delete, reset, or hide existing cool wall images.
- Add constants or config for the baseline date and baseline counts.
- Compute `Keys Created` as baseline plus post-baseline non-test key count.
- Compute generic and image-based Kaleidoscope counts as their baselines plus post-baseline generated counts.
- Exclude `wiptest-*` accounts from public `Keys Created`.
- Preserve an internal raw total if useful, but do not show raw internal/test totals publicly.
- Keep existing live-wall image archival behavior unchanged.

## Non-Goals

- No image generation changes.
- No prompt changes.
- No xAI archival changes.
- No wall image deletion.
- No wallet changes.
- No WebAuthn ceremony changes.
- No QR login changes.
- No footer, legal, or homepage layout changes.
- No nginx changes.
- No API key or credential material should be exposed publicly.

## Acceptance Criteria

- The live-wall stats endpoint has explicit baseline constants or config for `2026-05-21` Pacific time.
- The endpoint can return public counts that start from:
  - `Keys Created: 3`
  - `Generic Kaleidoscopes: 11`
  - `Image Based Kaleidoscopes: 3`
- A newly created non-test key after the baseline increments public `Keys Created`.
- A newly created `wiptest-*` key after the baseline does not increment public `Keys Created`.
- New generic and image-based generated outputs after baseline increment the corresponding public count.
- Existing live-wall images remain present.
- Public responses do not expose API keys, WebAuthn public key bytes, or full credential material.

## Validation

Minimum expected checks:

- `git diff --check`
- `node --check src/hosted-mcp/server.mjs`
- focused test or fixture for the baseline math
- focused test or fixture proving `wiptest-*` keys are excluded
- focused test or fixture proving non-test post-baseline keys are included
- smoke check that existing live-wall images are not removed

## Coder Handoff

Report:

- exact baseline constants used
- exact fields returned by the stats endpoint
- whether UI display changed or only server fields changed
- proof that `wiptest-*` keys are excluded
- proof that existing wall images remain
- exact files changed

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
