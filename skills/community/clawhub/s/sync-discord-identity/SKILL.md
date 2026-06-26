---
name: sync-discord-identity
description: Sync a Discord bot profile into an OpenClaw agent IDENTITY.md, save the avatar under workspace/avatars, and safely add Avatar and Discord metadata.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - curl
    homepage: https://github.com/0xli/sync-discord-identity
---

# OpenClaw Skill (Identity • Discord bot profile sync • Avatar bootstrap)

Use this skill when you need to inspect or update an OpenClaw agent identity for the **current workspace**, especially when that workspace is connected to a Discord bot and you want to synchronize Discord profile data into `IDENTITY.md`.

## Scope

This skill is for:
- reading or updating `IDENTITY.md`
- reading the Discord channel config from the current workspace `openclaw.json`
- bootstrapping `**Avatar:**` from the Discord bot profile
- saving a local copy of the Discord avatar under `workspace/avatars/`
- writing a `**Discord:**` metadata section into `IDENTITY.md`
- preserving existing identity content unless a specific field should be added or changed

This skill is **not** for changing the Discord bot account itself. It only reads bot metadata from the Discord API and reflects it into OpenClaw identity files.

## Behavior rules

When using this skill, follow these rules:

1. **Operate on the current workspace only.**
   Read `openclaw.json` from the workspace where the skill is installed or where the user explicitly points you.

2. **Use the correct Discord config for this workspace.**
   Read the Discord channel token from this workspace's `openclaw.json`, not from another agent or workspace.

3. **If multiple Discord channels exist in the same workspace, do not guess silently.**
   Prefer the single enabled Discord channel. If there are multiple candidates, ask the user which channel to use, or require an explicit channel name.

4. **Do not assume OpenClaw auto-imports the Discord avatar.**
   If `IDENTITY.md` has no `**Avatar:**`, populate it explicitly.

5. **Prefer a static CDN avatar URL for `**Avatar:**`.**
   Use the non-animated static Discord CDN URL:
   `https://cdn.discordapp.com/avatars/<BOT_ID>/<AVATAR_HASH>.png`

6. **Also save a local copy under the workspace.**
   Save the image as:
   `workspace/avatars/discord-<discord-username-or-bot-id>.png`

7. **If `**Avatar:**` is missing, set it.**
   Default behavior: write the static Discord CDN URL into `**Avatar:**`.

8. **If `**Avatar:**` already exists and differs, do not silently overwrite it.**
   Ask the user whether they want to replace the existing avatar value.

9. **Add `**Discord:**` if Discord metadata is available.**
   Save only non-empty fields among:
   - username
   - locale
   - email
   - bio

10. **Do not write empty Discord fields.**
    For example, omit `email` if it is `null`, and omit `bio` if it is empty.

11. **Preserve all unrelated identity fields.**
    Only make local, minimal edits.

12. **If a token appears in conversation or files, treat it as sensitive.**
    Do not echo it. Recommend rotation if it has been exposed.

## Expected inputs

You may receive one or more of the following:
- path to the current agent workspace
- path to `IDENTITY.md`
- path to `openclaw.json`
- an optional Discord channel name when multiple Discord channels exist in one workspace
- an explicit avatar URL

Example Discord bot profile payload returned by Discord `/users/@me`:

```json
{
  "id": "1471414603580838030",
  "username": "Andrew",
  "avatar": "650ada97187f9be350f13bf25ae136d8",
  "discriminator": "9171",
  "public_flags": 0,
  "flags": 0,
  "bot": true,
  "banner": null,
  "accent_color": null,
  "global_name": null,
  "avatar_decoration_data": null,
  "collectibles": null,
  "display_name_styles": null,
  "banner_color": null,
  "clan": null,
  "primary_guild": null,
  "mfa_enabled": true,
  "locale": "en-US",
  "premium_type": 0,
  "email": null,
  "verified": true,
  "bio": ""
}
```

## Output policy

When editing identity data, the desired result is:
- local avatar file saved under `workspace/avatars/`
- `**Avatar:**` present in `IDENTITY.md`
- `**Discord:**` present in `IDENTITY.md` if there is any non-empty Discord metadata to store

Preferred `IDENTITY.md` structure:

```md
# IDENTITY

- **Name:** Andrew
- **Avatar:** https://cdn.discordapp.com/avatars/1471414603580838030/650ada97187f9be350f13bf25ae136d8.png
- **Discord:**
  - username: Andrew
  - locale: en-US
```

If `email` is not null and `bio` is not empty, include them too:

```md
- **Discord:**
  - username: Andrew
  - locale: en-US
  - email: andrew@example.com
  - bio: Agent for the noodles workspace.
```

## Recommended workflow

### Case A: `IDENTITY.md` does not exist yet
1. Determine the current workspace root.
2. Read that workspace's `openclaw.json`.
3. Choose the correct Discord channel for this workspace.
4. Call Discord `/users/@me` using that channel token.
5. Build the static Discord avatar URL.
6. Download the image into `workspace/avatars/`.
7. Create `IDENTITY.md` with at least `**Avatar:**` and `**Discord:**` entries.

### Case B: `IDENTITY.md` exists but has no `**Avatar:**`
1. Read the current workspace `openclaw.json`.
2. Choose the correct Discord channel for this workspace.
3. Call Discord `/users/@me`.
4. Build the static Discord avatar URL.
5. Download the image into `workspace/avatars/`.
6. Insert `**Avatar:** <static_url>`.
7. Add or extend `**Discord:**` with the non-empty metadata fields.

### Case C: `IDENTITY.md` already has `**Avatar:**`
1. Read the existing avatar value.
2. Read the current workspace `openclaw.json` and fetch the Discord bot profile.
3. If it already matches the desired static Discord URL, do nothing.
4. If it differs, ask the user whether to replace it.
5. Regardless of avatar replacement, you may still add missing `**Discord:**` metadata fields.

## Minimal parsing rules for `IDENTITY.md`

Treat the file as Markdown with bold field labels such as:
- `- **Name:** value`
- `- **Avatar:** value`
- `- **Discord:**` followed by nested bullet items

Accept small formatting variations, but preserve the user’s original style where possible.

## Suggested CLI and filesystem assumptions

Common layouts:
- workspace root: `~/.openclaw/workspace`
- identity file: `~/.openclaw/workspace/IDENTITY.md`
- config file: `~/.openclaw/workspace/openclaw.json`
- avatar folder: `~/.openclaw/workspace/avatars`

If the user has multiple agents or workspaces, operate only on the explicitly targeted one.

## Safe edit strategy

- make a backup before writing when practical
- do surgical edits
- avoid reformatting the whole file
- never drop unrelated sections

## Reference implementation notes

If you need automation, see `scripts/sync_discord_identity.py` in this skill package. It:
- reads the current workspace `openclaw.json`
- finds the correct Discord channel token for that workspace
- calls Discord `/users/@me`
- downloads the static avatar to `workspace/avatars/`
- updates `IDENTITY.md`
- asks for confirmation before overwriting a different existing avatar unless `--force-avatar` is used
- supports `--channel` when multiple Discord channels exist in one workspace

## Example commands

```bash
python scripts/sync_discord_identity.py \
  --workspace ~/.openclaw/workspace
```

```bash
python scripts/sync_discord_identity.py \
  --workspace ~/.openclaw/workspace-beagle-profile
```

```bash
python scripts/sync_discord_identity.py \
  --workspace ~/.openclaw/workspace \
  --channel noodles
```

```bash
python scripts/sync_discord_identity.py \
  --workspace ~/.openclaw/workspace \
  --force-avatar
```

## Install and publish notes

To publish this skill to ClawHub:

```bash
clawhub publish . --version 0.1.0 --changelog "Initial release" --tags latest
```

For users to install it:

```bash
openclaw skills install sync-discord-identity
```

Start a new OpenClaw session after installing so the skill is loaded.

## Success criteria

This skill is complete only when all applicable conditions are satisfied:
- avatar file exists under `workspace/avatars/`
- `IDENTITY.md` contains `**Avatar:**` if missing before
- existing conflicting avatar is not overwritten silently
- `**Discord:**` includes non-empty username/locale/email/bio fields only
- the token comes from the correct Discord config for the current workspace
- unrelated identity content remains intact
