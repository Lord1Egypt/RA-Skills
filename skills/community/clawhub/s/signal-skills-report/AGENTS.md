# Signal-report skill — harness-agnostic entry point

If you're being invoked by a harness that doesn't natively read Claude
Code's `SKILL.md` frontmatter/Skill-tool convention (OpenCode, Codex CLI,
or anything else driving an agent loop over this repo), read `SKILL.md` in
this directory in full and follow it exactly as written. It is the single
source of truth for this skill's behavior — this file is only a pointer to
it, not a second copy of the instructions.

`render_report.py` is plain Python invoked via subprocess/Bash — no
Claude-specific API, so it runs unmodified under any tool-use loop that can
execute shell commands. Build the JSON payload per its docstring, run it,
and you get a static `out.html` regardless of harness.

One step assumes Claude Code specifics:

- **Publish.** `SKILL.md` assumes Claude's `Artifact` tool for hosting.
  Elsewhere, run `render_report.py` with `--open` to open the rendered
  HTML in the local default browser (cross-platform, Python stdlib
  `webbrowser` module, no extra dependency) — or just report the output
  file path if there's no browser available in the environment.
