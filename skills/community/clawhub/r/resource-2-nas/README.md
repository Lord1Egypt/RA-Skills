# Resource 2 NAS Skill

Codex skill for the whole media-to-NAS path. Users can enter from different stages: search a title through PanSou, provide a Quark/Baidu share link directly, verify saved resources through OpenList, inspect/cancel current OpenList transfer tasks, or copy saved resources into NAS/SMB-mounted OpenList storage.

## Features

- Search PanSou and return the top 50 ranked Baidu/Quark resource links as Markdown or JSON by default.
- Preserve concrete download links, extraction codes, provider names, source notes, and timestamps.
- Preview Quark and Baidu share contents before saving.
- Validate Quark and Baidu Cookies with Agent-friendly JSON before real saves.
- Save Quark shares to a configured Quark folder.
- Save Baidu shares to a configured Baidu path or Baidu folder URL.
- Let the Agent classify resources as movie, series, or collection before saving.
- Verify saved resources through OpenList and copy them to an SMB/NAS-backed OpenList path.
- List OpenList copy/offline-download task progress and cancel matched stuck tasks after confirmation.

## Requirements

- Node.js 20 or newer.
- A configured `.env` file for operations that need account or OpenList access.
- PanSou API access through the default public endpoint or a custom endpoint.

Search-only usage does not require cookies or OpenList credentials.

## Setup

Copy the example environment file and fill in real values:

```bash
cp .env.example .env
npm run check-ready
```

Configuration guide:

https://guantou.site/archives/N2CmhISt

Never commit `.env`. It contains full account credentials.

## Configuration

| Key | Purpose |
| --- | --- |
| `QUARK_COOKIE` | Quark web Cookie used to save Quark share links. |
| `BAIDU_COOKIE` | Baidu Netdisk web Cookie used to save Baidu share links. |
| `OPENLIST_TOKEN` | Fixed OpenList API token for list, get, copy, and task APIs. |
| `OPENLIST_BASE_URL` | OpenList base URL, for example `http://127.0.0.1:5244`. |
| `OPENLIST_DEFAULT_COPY_DST_PATH` | Default OpenList path backed by SMB/NAS storage. |
| `QUARK_COOKIE` + `QUARK_DEFAULT_SAVE_URL` | Quark provider config. `QUARK_DEFAULT_SAVE_URL` can be `/备份资源` or a full Quark folder URL. |
| `BAIDU_COOKIE` + `BAIDU_DEFAULT_SAVE_PATH` | Baidu provider config. `BAIDU_DEFAULT_SAVE_PATH` can be `/NAS资源下载` or a Baidu folder URL. |

Quark and Baidu are alternatives. At least one provider must be fully configured; both are not required.

## Usage

Search resources:

```bash
npm run search -- "蜘蛛侠"
```

Check whether the whole setup is usable:

```bash
npm run check-ready
```

This prints JSON by default for Agents and tests ENV, Cookie validity, provider save target connectivity, and OpenList/NAS connectivity. For a human-readable view:

```bash
npm run check-ready -- --format text
```

Preview a Quark share:

```bash
npm run quark-save -- "$QUARK_SHARE_URL" "$QUARK_DEFAULT_SAVE_URL" --dry-run
```

Preview a Baidu share:

```bash
npm run baidu-save -- "$BAIDU_SHARE_URL" "$BAIDU_DEFAULT_SAVE_PATH" --dry-run
```

List current OpenList copy tasks:

```bash
npm run openlist-tasks -- list copy undone --format json
```

Preview a NAS/OpenList copy:

```bash
npm run openlist-copy -- "/pan/quark/备份资源" "$OPENLIST_DEFAULT_COPY_DST_PATH" "资源名" --format json
```

Save after review:

```bash
npm run baidu-save -- "$BAIDU_SHARE_URL" "$BAIDU_DEFAULT_SAVE_PATH" \
  --context-name "资源名" \
  --resource-type collection \
  --yes
```

Run tests:

```bash
npm test
```

## Safety Notes

- Treat cookies and OpenList tokens as full credentials.
- Print only masked secrets.
- Do not place real cookies, tokens, private links, or private OpenList paths in commits.
- When a save target is unclear, run the relevant script with `--dry-run` first.
- For NAS backups, use OpenList paths, not local OS paths.

## Repository Layout

```text
agents/              Agent metadata
scripts/             CLI helpers for search, env/Cookie checks, cloud saves, OpenList tasks, and OpenList copy
tests/               Node test suite
SKILL.md             Main skill instructions
SUBAGENT.md          Sub-agent runbook for OpenClaw, Hermes, and similar agents
.env.example         Safe configuration template
```

## Open Source Status

This repository does not currently include a license file. Choose and add a license before publishing as an open-source project. This is practical engineering guidance, not legal advice.
