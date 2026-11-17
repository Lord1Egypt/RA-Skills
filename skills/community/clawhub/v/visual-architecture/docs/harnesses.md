# Harness Notes

visual-architecture is a plain local skill: JSON in, SVG/HTML/receipt out. It does not need a hosted renderer.

## OpenClaw

```bash
openclaw skills install visual-architecture
```

Ask Francis or another OpenClaw agent to use `visual-architecture` for a bounded architecture, workflow, sequence, data-flow, lifecycle, repo-evidence, or PR delta artifact.

## Codex

Copy this repo into the Codex skill directory or keep it in the target repo and point Codex at `SKILL.md`.

Useful prompt:

```text
Use visual-architecture to create a source-evidence architecture map for this repo.
Validate the JSON, deliver HTML, and return the receipt path.
```

## Claude Code

Copy the skill folder into Claude's local skills directory and keep generated artifacts inside the project. Prefer `deliver` over `render` so Claude has a receipt to cite.

## OpenCode

Place the repo or skill folder where OpenCode can read `SKILL.md`. Use the same command contract:

```bash
python3 scripts/render_architecture.py validate input.json --json
python3 scripts/render_architecture.py deliver input.json output.html --json
```

## Review Rule

For public artifacts, scan generated files for private paths, hostnames, tokens, internal context, and accidental client details before release or ClawHub sync.
