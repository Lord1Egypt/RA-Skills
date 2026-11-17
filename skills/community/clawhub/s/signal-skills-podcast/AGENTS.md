# Podcast skill — harness-agnostic entry point

If you're being invoked by a harness that doesn't natively read Claude
Code's `SKILL.md` frontmatter/Skill-tool convention (OpenCode, Codex CLI,
or anything else driving an agent loop over this repo), read `SKILL.md` in
this directory in full and follow it exactly as written. It is the single
source of truth for this skill's behavior — this file is only a pointer to
it, not a second copy of the instructions.

Everything `SKILL.md` tells you to run (`resolve.py`, `ledger.py`,
`render_report.py`) is plain Python invoked via subprocess/Bash — no
Claude-specific API, so it runs unmodified under any tool-use loop that can
execute shell commands.

Three steps in `SKILL.md` DO assume Claude Code specifics. If your harness
lacks the equivalent, degrade as follows instead of failing:

- **Step 3 (fan out extractors to subagents).** This assumes parallel
  sub-agent spawning (Claude Code's `Agent`/`Task` tool). If your harness
  has an equivalent (OpenCode's own subagent mechanism, etc.), use it the
  same way: one subagent per 1-2 episodes, transcript never re-enters the
  main/orchestrating context. If it doesn't, process episodes sequentially
  in the main loop instead — read one transcript, extract, discard, move
  to the next. Note explicitly in your output that isolation is weaker
  this way (the transcript did pass through the main context that run),
  don't silently claim the same guarantee.
- **Step 5 (publish).** This assumes Claude's `Artifact` tool for hosting.
  Elsewhere, `render_report.py`'s `--open` flag opens the rendered HTML in
  the local default browser (cross-platform via Python's `webbrowser`
  module) — use that, or just report the output file path if there's no
  browser available in the environment.
- **Step 3.7 (web cross-check, optional).** This assumes Claude Code's
  `WebSearch` tool. If your harness has no equivalent, skip this step
  entirely and say so explicitly — it's optional by design, findings just
  stay at their extracted confidence tag instead of picking up
  `web-corroborated`/`web-contradicted`.

> `render_report.py` and `template.html` in this directory are generated
> copies of `plugins/signal-report/{render_report.py,template.html}` (the
> SSOT) - kept as physical files, not symlinks, so this plugin still
> installs standalone via `/plugin install podcast@oren-signal-skills`. Never
> hand-edit them; edit the signal-report originals and run
> `scripts/sync-shared-files.sh` from the repo root.
