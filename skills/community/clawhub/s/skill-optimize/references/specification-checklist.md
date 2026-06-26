# Specification Checklist

Use this when running the **Dimension 1** (Specification) audit. Each item is binary — pass or fail. Source: [agentskills.io/specification](https://agentskills.io/specification).

## Mechanical checks (run `scripts/audit_skill.py`)

The bundled script covers these. The audit report should still list each as Pass / Fail with the offending value when failed.

### File structure

- [ ] `SKILL.md` exists at the skill root.
- [ ] No files at the skill root that shouldn't be there (e.g., a stray `skill.md` in mixed case — case matters).
- [ ] Optional directories (`scripts/`, `references/`, `assets/`) are present only when they contain content.

### Frontmatter presence & shape

- [ ] File starts with `---` on line 1.
- [ ] Frontmatter closes with `---` (and only one closing fence).
- [ ] Frontmatter is a valid YAML dictionary.
- [ ] All keys in frontmatter are in the allowed set: `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`. Any other key is a hard fail.

### `name` field

- [ ] Present.
- [ ] Is a string.
- [ ] Length is 1–64 characters.
- [ ] Matches the regex `^[a-z0-9-]+$` (lowercase letters, digits, hyphens only).
- [ ] Does not start or end with `-`.
- [ ] Does not contain consecutive hyphens (`--`).
- [ ] **Matches the parent directory name** — this is a hard rule from the spec, often missed.

Invalid examples: `PDF-Processing` (uppercase), `-pdf` (leading hyphen), `pdf--processing` (consecutive hyphens), `pdf_processing` (underscore).

### `description` field

- [ ] Present.
- [ ] Is a string.
- [ ] Length is 1–1024 characters.
- [ ] Non-empty after stripping whitespace.
- [ ] Does not contain `<` or `>`.
- [ ] Describes both **what the skill does** and **when to use it**. (Content check — see `description-guide.md`.)

### `license` field (optional)

- [ ] If present, is a short string naming the license or a bundled file. The spec recommends keeping it brief.

### `compatibility` field (optional)

- [ ] If present, is 1–500 characters.
- [ ] Is a string, not a list.
- [ ] Most skills should NOT have this field — only add it when there are real environment requirements (specific product, system packages, network access, etc.).

### `metadata` field (optional)

- [ ] If present, is a map of string keys to string values.
- [ ] Key names are reasonably unique (e.g., namespace them: `author`, `version`).

### `allowed-tools` field (optional, experimental)

- [ ] If present, is a space-separated string of pre-approved tool patterns.
- [ ] Format example: `Bash(git:*) Bash(jq:*) Read`.

## Body checks (judgment-based, but scriptable)

- [ ] Body length is under ~500 lines. (Spec recommends; 5000 tokens is the rough upper bound.)
- [ ] Body has at least one clear instruction (not just commentary). A skill that contains only metadata has no value.
- [ ] File references use **relative paths from the skill root** (e.g., `references/foo.md`, `scripts/bar.py`).
- [ ] File references are **one level deep** — no `references/foo/bar/baz.md` chains.
- [ ] Referenced files actually exist. (Spot-check; the agent will load them.)

## What to do on failure

For each failed check, record in the report:

- **Severity**: Blocker (file won't load or won't trigger) / Major (spec violation, may behave incorrectly) / Minor (style).
- **Evidence**: Quote the offending value or describe the file state.
- **Fix**: The exact change needed. Be specific: "Rename `PDF-Processing` to `pdf-processing` in the frontmatter, and rename the parent directory accordingly."

Don't apply fixes without user approval. Show the diff and wait.
