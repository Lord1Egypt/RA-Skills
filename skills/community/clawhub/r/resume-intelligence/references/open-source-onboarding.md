# Open-Source Onboarding

Use this reference when preparing the project for public use, helping a user install the plugin, or running in safe local-only mode.

## Setup Doctor

Run the setup doctor from the repository root when validating a local checkout:

```bash
python3 plugins/resume-intelligence/skills/resume-intelligence/scripts/setup_doctor.py .
```

The report checks required plugin files and optional tools such as `git`, `rg`, `gh`, `codex`, `claude`, `cursor`, `npx`, and `soffice`.

Missing optional commands should not block basic resume generation. Record limitations in `tool-usage-log.md` and use pasted text or local files as fallbacks.

## Safe Local-Only Mode

Use safe local-only mode when credentials or enterprise connectors are unavailable.

Rules:

- Use only user-approved folders, pasted LinkedIn exports, local notes, local Git exports, and local job postings.
- Do not connect to GitHub, Jira, Confluence, LinkedIn, Canva, Figma, or job boards unless the user approves.
- Keep generated outputs in `resume-runs/`.
- Redact private names by default.
- Record every skipped connector and unavailable tool.

Use `safe-local-mode-checklist.md` to document the mode. A fake example is available under `examples/sample-run-local-only/`.

## Prompt Library

Use `references/prompt-library.md` for copyable prompts that work in Codex, Claude, Cursor, or another agent environment. The prompts should request evidence-backed outputs and clearly state source scopes, target roles, and confidentiality preferences.

## Sample Runs

Sample runs must use fake data only. They should demonstrate output shape, not real candidate claims. Never commit real resumes, private documents, connector exports, profile photos, job applications, or credentials.

## Career Vault

Use `career-vault/` when users want reusable career knowledge across many resume and interview runs. The vault is plain Markdown and can be opened in Obsidian, VS Code, Codex, Claude, Cursor, or any editor. Keep real vaults under `resume-runs/` or a private local folder, not committed sample data.
