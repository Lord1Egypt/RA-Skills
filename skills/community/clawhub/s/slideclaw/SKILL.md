---
name: slideclaw
description: Use this for SlideClaw/Marp deck tasks (e.g. "SlideClawでスライド作って", "MarpをPDF化して", "テンプレ保存して").
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/akamichikota/SlideClaw","requires":{"bins":["node"]},"install":[{"id":"node","kind":"node","package":"slideclaw","bins":["slideclaw"],"label":"Install SlideClaw CLI"}]}}
---

# SlideClaw Skill (OpenClaw + ClawHub)

Use this skill to run end-to-end Marp slide production with SlideClaw.

## When to use

- User asks to create slides with Marp.
- User asks to turn a topic or requirements into a deck.
- User asks to render `slides.md` to PDF/HTML/PPTX/PNG.
- User asks to reuse or save slide design templates.

## When not to use

- Task is not about slides/Marp.
- User only wants generic writing without file operations.
- User asks for a different slide stack (e.g., Google Slides API directly).

## ClawHub-first assumptions

This skill is designed to work even when installed from ClawHub into a workspace that does not have this repository cloned.

- Prefer a local `slideclaw` binary when available.
- Otherwise use `npx -y slideclaw@latest`.
- If this is not yet a SlideClaw workspace, initialize it in the current directory.

## Command resolver (use this order)

1. If `slideclaw` exists on PATH, use it.
2. Else if `./bin/slideclaw.js` exists, use `node ./bin/slideclaw.js`.
3. Else use `npx -y slideclaw@latest`.

In steps below, treat `<SC>` as the resolved command prefix.

Examples:

```bash
<SC> doctor
<SC> --json template list
<SC> render <project-id> --format pdf
```

## Bootstrap flow (required before doing slide work)

1. Run health check:

```bash
<SC> doctor
```

2. If workspace marker `.slideclaw/` is missing, initialize in current directory:

```bash
<SC> init . --with-starter-template
```

3. Re-check:

```bash
<SC> doctor
```

If any required dependency is missing, report clearly and stop before content work.

## Inputs to collect from user

Ask only what is required:

- Purpose (required)
- Audience (required)
- Topic (required)
- Duration / slide count (optional)
- Tone (optional)

Limit to 4 questions in one round.

## End-to-end workflow

```
[1] Resolve <SC> and bootstrap workspace
[2] Confirm requirements
[3] Pick template (or create new design)
[4] Create project
[5] Fill requirements.md
[6] Write slides.md
[7] Render HTML for fast validation
[8] Render PDF for final output
[9] Confirm with user, iterate if needed
[10] Mark done and optionally save template
[11] Update profile/user.md
```

## Step 1. Template selection

Always use CLI JSON output:

```bash
<SC> --json template list
```

Rules:

- Do not force one template without user confirmation.
- Present all candidates in one short list.
- Include "create a new design" as an option.

If no template exists, continue with project creation without template and create style in project `theme.css`.

## Step 2. Create project

Always pass explicit kebab-case ID:

```bash
<SC> project new "<name>" \
  --id 2026-04-09-topic-name \
  --template <template-id> \
  --title "<title>" \
  --audience "<audience>" \
  --goal "<goal>"
```

If no template is selected, omit `--template`.

## Step 3. Update requirements.md

Edit:

- Background
- Must-include points
- Open questions

Then share a 3-5 line summary and wait for user confirmation.

## Step 4. Write slides.md

Use pure Marp frontmatter only:

```yaml
marp: true
theme: <theme_name>
paginate: true
size: 16:9
```

Rules:

- Separator is `---` on its own line.
- Put assets under `assets/` and reference with relative paths.
- Keep slide density aligned with `profile/user.md` preferences.
- Do not add SlideClaw-specific keys to `slides.md` frontmatter.

## Step 5. Render and validate

1. Fast render first:

```bash
<SC> render <project-id> --format html
```

2. Final render:

```bash
<SC> render <project-id> --format pdf
```

3. Share the output path with the user. Prefer the Downloads path when reporting, because it is easier for the user to open:

- Primary (workspace): `projects/<project-id>/build/slides.pdf`
- User-facing (Downloads): `<OS Downloads dir>/<project-id>.pdf`

`slideclaw render` automatically copies the rendered file to the user's OS-standard Downloads folder (macOS `~/Downloads`, Linux `xdg-user-dir DOWNLOAD`, WSL Windows-side `/mnt/c/Users/<user>/Downloads`, Windows `%USERPROFILE%\Downloads`). Use `<SC> --json render ...` and read `downloadsPath` to get the exact path. To disable: `--no-copy-to-downloads` or `SLIDECLAW_NO_DOWNLOADS=1`.

## Step 6. Iterate and complete

- Apply feedback loops until approved.
- After approval, update `requirements.md`:
  - `status: done`
  - `updated_at: <now>`

Avoid `project finish` in interactive review loops because it can run actions before user confirmation.

## Step 7. Optional template promotion

When user likes the design, save it:

```bash
<SC> template new <new-id> --from <project-id> \
  --name "<display name>" \
  --description "<short description>" \
  --tags "tag1,tag2" \
  --when-to-use "<usage guidance>"
```

If a draft template was created in `templates/.drafts/`, do not leave it orphaned. Promote or delete it.

## Step 8. Update user profile

Update `profile/user.md` with durable preferences only:

- Do / Don't patterns
- Preferred style density
- Topic tendencies
- Known constraints

Validate after edit:

```bash
<SC> profile validate
```

## Hard constraints

- Do not manually edit tool-managed files unless necessary:
  - `templates/INDEX.md`
  - `meta.md`
  - template `used_in`
- Do not run destructive commands without explicit user intent.
- Do not claim success without render output path verification.

## Failure handling

- If `slideclaw` is unavailable and `npx` fails, tell the user exactly which dependency is missing.
- If Chrome is missing, explain PDF will fail and suggest HTML output first.
- If schema validation fails, fix frontmatter against `docs/SCHEMAS.md` when available.
