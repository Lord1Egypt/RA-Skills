# Review-scout skill — harness-agnostic entry point

If you're being invoked by a harness that doesn't natively read Claude
Code's `SKILL.md` frontmatter/Skill-tool convention (OpenCode, Codex CLI,
or anything else driving an agent loop over this repo), read `SKILL.md`
in this directory in full and follow it exactly as written. It is the
single source of truth for this skill's behavior — this file is only a
pointer to it, not a second copy of the instructions.

Everything `SKILL.md` tells you to run (`resolve.py`, `ledger.py`,
`render_report.py`) is plain Python invoked via subprocess/Bash — no
Claude-specific API, so it runs unmodified under any tool-use loop that
can execute shell commands.

Two steps assume Claude Code specifics. If your harness lacks the
equivalent, degrade as follows instead of failing:

- **Step 3 (fan out extractors to subagents).** Same fallback as
  `podcast`: if your harness has no parallel subagent mechanism, process
  review batches sequentially in the main loop instead, and say
  explicitly that isolation is weaker this run.
- **Step 5 (publish).** `render_report.py --open` opens the rendered HTML
  in the local default browser (cross-platform, Python stdlib
  `webbrowser`) when there's no `Artifact`-style publish tool available.

Nothing about product-type detection or review fetching (`resolve.py`) is
Claude-specific at all — the App Store RSS feed and Play Developer API
calls are plain HTTP, identical under any harness.

> `render_report.py` and `template.html` in this directory are generated
> copies of `plugins/signal-report/{render_report.py,template.html}` (the
> SSOT) - kept as physical files, not symlinks, so this plugin still
> installs standalone via `/plugin install review-scout@oren-signal-skills`. Never
> hand-edit them; edit the signal-report originals and run
> `scripts/sync-shared-files.sh` from the repo root.
