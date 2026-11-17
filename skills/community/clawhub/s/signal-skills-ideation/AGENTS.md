# Ideation skill — harness-agnostic entry point

If you're being invoked by a harness that doesn't natively read Claude
Code's `SKILL.md` frontmatter/Skill-tool convention (OpenCode, Codex CLI,
or anything else driving an agent loop over this repo), read `SKILL.md`
in this directory in full and follow it exactly as written. It is the
single source of truth for this skill's behavior — this file is only a
pointer to it, not a second copy of the instructions.

Everything `SKILL.md` tells you to run (`ledger.py`, `render_report.py`,
and reading `podcast`/`review-scout`'s `ledger.py known-issues`/`dedup`
output) is plain Python invoked via subprocess/Bash — no Claude-specific
API, so it runs unmodified under any tool-use loop that can execute shell
commands.

One step assumes Claude Code specifics:

- **Step 4 (publish).** `render_report.py --open` opens the rendered HTML
  in the local default browser (cross-platform, Python stdlib
  `webbrowser`) when there's no `Artifact`-style publish tool available.

This skill has no subagent fan-out step (unlike `podcast`/`review-scout`)
— it synthesizes already-extracted findings rather than raw source
material, so there's nothing to parallelize across.

> `render_report.py` and `template.html` in this directory are generated
> copies of `plugins/signal-report/{render_report.py,template.html}` (the
> SSOT) - kept as physical files, not symlinks, so this plugin still
> installs standalone via `/plugin install ideation@oren-signal-skills`. Never
> hand-edit them; edit the signal-report originals and run
> `scripts/sync-shared-files.sh` from the repo root.
