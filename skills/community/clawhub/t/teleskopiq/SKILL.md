---
name: teleskopiq
description: Create, edit, and manage Teleskopiq YouTube scripts, AI conversations, metadata, thumbnails, history, and publishing schedules through its authenticated API with browser OAuth or an API key. Use when the user asks to automate teleskopiq.com or work with Teleskopiq content.
metadata:
  openclaw:
    requires:
      bins: [python3]
    homepage: https://teleskopiq.com
    envVars:
      - name: TELESKOPIQ_API_KEY
        required: false
        description: Optional fallback API key; browser OAuth login is preferred.
      - name: TELESKOPIQ_OAUTH_FILE
        required: false
        description: Private OAuth credential-file path; defaults to ~/.config/teleskopiq/oauth.json.
      - name: TELESKOPIQ_ENDPOINT
        required: false
        description: API endpoint override; defaults to https://teleskopiq.com/api/graphql.
      - name: TELESKOPIQ_ENV_FILE
        required: false
        description: Private credential-file path; defaults to ~/.config/teleskopiq/env.
---

# Teleskopiq

Use the bundled client for channel-scoped content work. Teleskopiq also provides an OAuth-enabled MCP endpoint;
see [references/oauth.md](references/oauth.md) for MCP setup and OAuth deployment requirements.

## Run

Set `SKILL_DIR` to the absolute directory containing this `SKILL.md`. Use the actual installed location;
do not assume an OpenClaw or Codex directory layout. For a fresh installation:

```bash
python3 -m venv "$SKILL_DIR/.venv"
"$SKILL_DIR/.venv/bin/python" -m pip install -r "$SKILL_DIR/requirements.txt"
"$SKILL_DIR/.venv/bin/python" "$SKILL_DIR/scripts/teleskopiq.py" --help
```

Reuse an existing `.venv` when the dependencies are already installed.
Connect once with browser OAuth (Linux/macOS):

```bash
"$SKILL_DIR/.venv/bin/python" "$SKILL_DIR/scripts/teleskopiq.py" login --no-browser
```

Show the verification link and code to the user. Keep login running while they sign in, select a channel,
complete onboarding if their channel is not set up, and approve access. Never approve on their behalf. The CLI waits up to one hour; it stores tokens privately
in `~/.config/teleskopiq/oauth.json` (0600), renews access before requests, and never prints tokens.
`auth-status` shows saved connection metadata (it does not verify server access); `logout` revokes that connection.
OAuth takes precedence when a saved login exists. Revoked/expired logins require `login` again; never silently
fall back to a broader API key. Changing endpoints requires a separate `TELESKOPIQ_OAUTH_FILE` or a new login.

For API-key fallback, the client loads `TELESKOPIQ_API_KEY` from the environment or `~/.config/teleskopiq/env` (mode 0600).
`TELESKOPIQ_ENV_FILE` overrides that file. It reads assignments as data and never executes shell code.
Environment values take precedence. Never display or commit credentials.
The default endpoint is `https://teleskopiq.com/api/graphql`; `TELESKOPIQ_ENDPOINT` overrides it.

OAuth connections and API keys are channel-bound. Read scripts/history with `scripts:read`, modify scripts or run AI/metadata/ideas with
`scripts:write`, read channel/style with `channel:read`, and generate/upload thumbnails with `thumbnails:write`.
Full production workflows need all four. Delegated connections cannot manage keys, billing, channel membership,
style changes, or channel memory administration. Use the web app for those account operations.

Output is JSON on stdout; progress and created script IDs go to stderr. Exit codes: 0 success, 1 failure,
2 AI question awaiting an answer, 130 interrupted. `--timeout SECONDS` goes before the command and controls
generation read timeout. Mutations are never automatically retried. On an interrupted request, inspect the existing
script/history before deciding whether to retry; generation may already have completed server-side.

## Workflows

- Fetch `get-style` before writing content; use its tone, vocabulary, structure, speakers, and pacing. A null profile
  means none exists. A profile access error is not an empty profile: stop and report the actual error.
- `get-channel` returns the connected channel and preferred publishing day. `list-scripts` and `search-scripts --query TEXT`
  find records; `get-script --script-id ID` retrieves complete content, comments, metadata, and generated thumbnails.
- `create-script --title TITLE --content-file script.md` creates a draft. `update-script --script-id ID --content-file script.md`
  edits it and snapshots existing content first. `--title`, `--status`, or `--input-file update.json` update other fields.
  `delete-script --script-id ID` permanently deletes a script; run only when the user's task calls for deletion.
- `ai-write --title TITLE [--prompt TEXT]` creates and writes a script. Supply `--script-id ID` to reuse an existing script.
  `chat --script-id ID --prompt TEXT` edits or discusses it using current content and visible chat history.
- AI may ask a question. Show the returned question/options, obtain the user's answer, and resume with
  `chat --script-id ID --call-id CALL_ID --answer TEXT`. Do not invent answers or create another script.
  `history --script-id ID` can recover the question after interruption. A completed chat can be a discussion with no
  script change. The server owns saved content, title, patches, and checkpoints; do not overwrite it with streamed text.
- Chat accepts `--apply-comments`, `--request-kind lengthen|shorten`, `--pacing-file pacing.json`, `--files-json files.json`,
  and `--selection-file selection.json`. `set-comments --script-id ID --comments-file comments.json` replaces the entire
  comment list: fetch existing comments and preserve unrelated entries.
- `generate-metadata --script-id ID` waits for the metadata SSE completion/error event and returns the persisted script.
  Metadata generation also creates thumbnail ideas. `ideas [--script-id ID]` generates topic ideas without creating a script.
- `generate-thumbnails --script-id ID` generates all idea slots, using both each visual description and text overlay.
  `--idea-index 0|1|2` regenerates one slot; `--prompt TEXT` targets the single custom slot instead.
  Repeat `--asset IMAGE` to provide references. Each request returns its own completed result; old thumbnails are not
  treated as completion of a new job. Slots are limited to three ideas plus one custom thumbnail.
- `save-asset --script-id ID --file IMAGE` and `remove-asset --script-id ID --url URL` manage saved thumbnail references.
  `select-thumbnail --script-id ID --url URL` selects an existing generated thumbnail.
- `auto-schedule --script-id ID` finds the next free preferred publishing day. `--urgent` displaces other scripts;
  use it only when the user requests that behavior. `schedule --script-id ID --date YYYY-MM-DD` sets a day explicitly.
  Omitting the date auto-schedules. Publishing schedules represent **days, not times**; legacy `--time` is ignored with
  a warning. Scheduling preserves status unless `--status` is explicitly supplied.
- `full-flow --title TITLE --content-file script.md` runs create → metadata → thumbnails → schedule.
  Use `--ai-write [--prompt TEXT]` instead of supplied content for AI writing. Any error or unanswered question stops
  later stages. Use the emitted script ID to inspect/reuse the record; do not restart blindly and create duplicates.
  `full-flow --script-id ID` processes an existing script. `--date`, `--urgent`, `--status`, and `--asset` are optional.
- `versions --script-id ID`, `save-version --script-id ID`, `restore-version --script-id ID --version-id ID`, and
  `revert-checkpoint --script-id ID --version-id CHECKPOINT_ID` expose the server's grouped history and restoration.

For JSON inputs and operations outside the named commands, read [references/api.md](references/api.md).

## Script format

Content is Markdown: `# Title`, `## Section`, `### Subsection`, with spoken narration as normal text.
Use relevant non-spoken directions: `[B-ROLL: footage]`, `[VISUAL: action]`, `[GRAPHIC: overlay]`,
`[MUSIC: mood]`, and `[SFX: sound]`. Do not force every tag into every script.
Do not add `[END]`, `[FADE OUT]`, or other script-end markers.

## Compatibility

Maintained source: `skills/teleskopiq/` in the Teleskopiq repository. The client is checked against that repository's
GraphQL schema. OAuth and MCP require the new server routes to be deployed; a skill update alone does not enable login.
Older deployments may still reject API-key `styleProfile` reads; that needs the accompanying server
fix deployed, not a different key or repeated retries. Keep account changes in the app until explicit key scopes exist.
