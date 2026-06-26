---
name: resoul
description: Fully reset OpenClaw's persona/bootstrap state and restore the latest official BOOTSTRAP.md after an explicit second confirmation. Use when the user wants to resoul, reset or reinitialize the assistant, restore the default official bootstrap, start over from a fresh identity setup, or clear SOUL.md, USER.md, and IDENTITY.md to begin again. Triggers on requests like "resoul", "reset your soul", "reset your persona", "reinitialize yourself", "restore default bootstrap", "start over with a fresh identity", "重置你的人设", "恢复初始人格", "清空你的身份设定重新开始", or similar full-reset phrasing. Do not use for ordinary edits to SOUL.md, USER.md, or IDENTITY.md.
---

# ReSoul

Reset the workspace bootstrap state so the next fresh session can start from the official upstream `BOOTSTRAP.md`.

## Primary workflow

1. Warn that running `resoul` will fetch the official `BOOTSTRAP.md`, then archive the current `SOUL.md`, `USER.md`, and `IDENTITY.md` into `.trash/` and remove them from the workspace root if they exist.
2. Require an explicit second confirmation before executing anything. Do not treat vague replies like "ok" or "继续" as sufficient; require a clear confirmation that the user agrees to archive and remove the current `SOUL.md`, `USER.md`, and `IDENTITY.md` from the workspace root.
3. Fetch the latest official upstream template to a temporary file first, and only continue if the fetch succeeds.
4. Archive the current `SOUL.md`, `USER.md`, and `IDENTITY.md` into `.trash/` if they exist.
5. Write the fetched template to the workspace root as `BOOTSTRAP.md`.
6. Tell the user to run `/new` after completion so the next session starts from the restored bootstrap flow.

Use the bundled script:

```bash
bash {{SKILL_DIR}}/scripts/fetch_official_bootstrap.sh <workspace-dir>
```

Example:

```bash
bash {{SKILL_DIR}}/scripts/fetch_official_bootstrap.sh /root/.openclaw/workspace
```

Upstream source:

```bash
https://raw.githubusercontent.com/openclaw/openclaw/main/docs/reference/templates/BOOTSTRAP.md
```

## Constraints

- Do not execute this skill without a second explicit confirmation in the current conversation.
- Do not hand-author a replacement bootstrap unless the user explicitly asks for a customized variant after syncing the official file.
- Only archive and remove `SOUL.md`, `USER.md`, and `IDENTITY.md` from the workspace root; do not delete memory, project files, skills, or other workspace content.
- Fetch the official template successfully before archiving or removing any existing identity files.
- Archive existing `SOUL.md`, `USER.md`, and `IDENTITY.md` into `.trash/` before removing them from the workspace root when those files exist.
- Do not execute the bootstrap ritual automatically after syncing; stop after preparing the workspace and instruct the user to run `/new`.
- Mention that the official template is written for a fresh workspace and should be reviewed before reuse in an existing workspace.

## Fallback

If the script cannot be used, run equivalent shell commands that (1) fetch the official `BOOTSTRAP.md` to a temporary file first, (2) archive existing `SOUL.md`, `USER.md`, and `IDENTITY.md` into `.trash/` if present, (3) write the fetched template to the workspace root as `BOOTSTRAP.md`, and (4) avoid touching memory, project files, skills, or other workspace content.

## Report back

Briefly report:
- that the user gave the destructive confirmation
- whether `SOUL.md`, `USER.md`, and `IDENTITY.md` were archived/cleared
- that the latest official upstream template was fetched
- the destination path
- that the user should run `/new` to trigger the re-bootstrap flow
