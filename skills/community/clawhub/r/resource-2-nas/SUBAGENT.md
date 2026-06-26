# Sub-Agent Runbook

Use this file when OpenClaw, Hermes, or another sub Agent is delegated a media search, direct share-link save, OpenList visibility check, OpenList task progress/cancel, or NAS/OpenList copy task.

## Hard Rules

- Never print, persist, or commit `QUARK_COOKIE`, `BAIDU_COOKIE`, `OPENLIST_TOKEN`, raw cookies, or raw auth headers.
- Do not use `--yes` until the user or supervising Agent has confirmed the preview payload, unless the task explicitly includes `confirmed: true`.
- Prefer `--format json` or `--json` for every script call that supports it. Do not parse Markdown when JSON is available.
- Search defaults to Baidu Netdisk and Quark Netdisk with a 50-result candidate cap. Only broaden `--cloud-types` when the user asks for other providers.
- If the user specifies a provider, such as "只要夸克" or "取消百度", act only on that provider. Do not start, retry, copy, or report another provider as an acceptable substitute.
- Do not create background retry loops, cron jobs, or recurring automations unless the user explicitly asks for them.
- Readiness validation is an Agent JSON tool. Run `npm run check-ready` before real saves/copies on fresh installs or after auth/path errors, and continue only when `nextAction` is `ready`.
- Quark and Baidu are alternatives. A complete configuration needs at least one reachable provider, not both.
- Quark save targets may be full folder URLs or cloud-drive paths like `/备份资源`.
- In JSON mode, use `--dry-run` for preview or `--yes` for confirmed save. Do not invoke interactive save prompts in JSON mode.
- For cloud saves, always run a preview first, classify the resource, and produce a confirmation payload before mutation.
- A Baidu path like `/NAS资源下载` is still a Baidu cloud-drive path. It is not a NAS copy unless OpenList `fs/copy` is executed after the cloud save.

## Decision Table

| User intent | First command | Mutating command |
| --- | --- | --- |
| Search title | `node scripts/search-rrdynb.mjs "$KW" --format json --max-candidates 50` | none |
| Full readiness check | `npm run check-ready` | none |
| Check install config | `npm run check-env -- --json` | none |
| Check Cookie validity | `npm run check-cookies` | none |
| Save Quark share | `node scripts/quark-save.mjs "$SHARE_URL" "$DEST_URL" --dry-run --json` | Same command with `--yes --json` after confirmation |
| Save Baidu share | `node scripts/baidu-save.mjs "$SHARE_URL" "$DEST_PATH_OR_URL" --dry-run --json` | Same command with `--yes --json` after confirmation |
| View OpenList copy progress | `npm run openlist-tasks -- list copy undone --format json` | none |
| View OpenList offline download progress | `npm run openlist-tasks -- list offline_download undone --format json` | none |
| Cancel OpenList tasks | `npm run openlist-tasks -- cancel copy undone --provider "$PROVIDER" --format json` | Same command with `--yes --format json` after confirmation |
| Copy saved resource to NAS/OpenList | `npm run openlist-copy -- "$SRC_DIR" "$DST_DIR" "$NAME" --format json` | Same command with `--yes --format json` after confirmation |

## JSON Preview Contract

The Quark and Baidu preview commands return one JSON object:

```json
{
  "ok": true,
  "provider": "baidu",
  "mode": "preview",
  "nextAction": "confirm_before_save",
  "source": {
    "shareUrl": "https://pan.baidu.com/s/...",
    "shareId": "..."
  },
  "target": {
    "provider": "baidu",
    "pathOrUrl": "/NAS资源下载"
  },
  "resource": {
    "shareTitle": "暗影蜘蛛",
    "canonicalName": "暗影蜘蛛",
    "type": "collection",
    "label": "合集",
    "isSeries": false,
    "reason": "Agent 根据上下文判定为合集"
  },
  "selection": {
    "defaultSelection": "all",
    "selectedRanks": [1],
    "selectedItems": []
  },
  "renamePlan": [],
  "confirmation": {
    "source": "https://pan.baidu.com/s/...",
    "selectedItems": [],
    "target": {
      "provider": "baidu",
      "pathOrUrl": "/NAS资源下载"
    },
    "finalNaming": [],
    "commandHint": "Re-run ... with --yes after the user confirms this payload."
  }
}
```

Before any save/copy mutation, report these exact fields to the user or supervising Agent:

- Source: `confirmation.source`
- Selected items: `confirmation.selectedItems[].name`
- Target: `confirmation.target.pathOrUrl`
- Final naming: `confirmation.finalNaming`, or "keep original names" when empty
- Resource type: `resource.label` and `resource.reason`
- Next command: the same command with `--yes --format json`

## Save Commands

Quark:

```bash
node scripts/quark-save.mjs "$SHARE_URL" "$QUARK_DEFAULT_SAVE_URL" \
  --dry-run \
  --format json \
  --context-name "$CANONICAL_NAME" \
  --resource-type auto
```

Baidu:

```bash
node scripts/baidu-save.mjs "$SHARE_URL" "$BAIDU_DEFAULT_SAVE_PATH" \
  --dry-run \
  --format json \
  --context-name "$CANONICAL_NAME" \
  --resource-type auto \
  --passcode "$PASSCODE_IF_NEEDED"
```

After confirmation, replace `--dry-run` with `--yes`.

## Classification Rules

- If item names include `S01E01`, `EP01`, `第1集`, `第一季`, `全12集`, `完结`, `剧集`, or similar, use `--resource-type series` and tell the user it is a series.
- If a single top-level folder contains variants like `1080p`, `4K`, `SDR`, `彩色版`, `黑白版`, or multiple quality folders, use `--resource-type collection`.
- If the title is clearly one movie and the selected item is a single video file, use `--resource-type movie`.
- If uncertain, keep `auto`, but explain the uncertainty and do not invent a canonical title.

## Common Failures

| Symptom | Action |
| --- | --- |
| Missing `.env` or missing key | Run `npm run check-ready`, then ask user to follow `https://guantou.site/archives/N2CmhISt`. |
| `check-ready.nextAction` is `configure_provider` | Ask the user to configure at least one full provider: Quark or Baidu. Both are not required. |
| `check-ready.nextAction` is `fix_openlist_target` | Ask the user to fix `OPENLIST_BASE_URL`, `OPENLIST_TOKEN`, or `OPENLIST_DEFAULT_COPY_DST_PATH`. |
| `check-ready.nextAction` is `fix_provider_target` | Ask the user to verify the configured Quark/Baidu save directory exists. |
| `check-cookies.nextAction` is `configure_missing_cookies` | Ask the user to fill the missing Cookie env vars listed in `recommendations`. |
| `check-cookies.nextAction` is `refresh_invalid_cookies` | Ask the user to log in again, copy fresh Cookies, and re-run `npm run check-cookies`. |
| `check-cookies.nextAction` is `retry_network_or_check_access` | Do not claim the Cookie is invalid; ask the user to check network/provider access and retry. |
| Baidu target URL rejected | Ensure it is from `pan.baidu.com` and contains a `path` parameter in the hash or query. |
| Baidu page parse error | Inspect for `window.yunData` and `locals.mset`, then add a regression test before editing parser code. |
| Extraction code failure | Ask for the correct code; pass with `--passcode`. |
| `errno` is not `0` after Baidu save | Report the errno and message; do not claim success. |
| Quark save returns no `task_id` | Report the API response summary; do not retry blindly. |
| OpenList copy task disappears | Do not call it failed yet. Check `copy/done` and refresh the destination directory. |
| OpenList copy task fails | Use `npm run openlist-tasks -- list copy done --format json`, report task error, and verify both source and target with `refresh:true`. |

## OpenList Copy Protocol

Before `fs/copy`, state:

- Source directory: OpenList path containing the saved resource.
- Object: exact `names[]` entry.
- Destination directory: OpenList NAS/SMB path.
- Final path/name: expected resulting path.

Use the bundled copy script:

```bash
npm run openlist-copy -- "$SRC_DIR" "$DST_DIR" "$NAME" --format json
```

After confirmation:

```bash
npm run openlist-copy -- "$SRC_DIR" "$DST_DIR" "$NAME" --yes --format json
```

The script calls `fs/copy`, checks `copy/undone`, checks `copy/done`, and lists the destination with `refresh:true` until the copied item appears. A task missing from `undone` is not failure unless `done` or the destination check also shows failure.

If the preview returns `destination.existingTargetNames`, tell the user the target already contains same-named items and require explicit confirmation before `--yes`.

## OpenList Task Protocol

Use `openlist-tasks` when the user asks to inspect or cancel running OpenList jobs:

```bash
npm run openlist-tasks -- list copy undone --format json
npm run openlist-tasks -- list copy done --format json
npm run openlist-tasks -- cancel copy undone --provider baidu --format json
npm run openlist-tasks -- cancel copy undone --provider baidu --yes --format json
```

Available task groups: `copy`, `offline_download`, `offline_download_transfer`, `upload`, `decompress`, `decompress_upload`.

Cancellation rules:

- First run without `--yes` and show matched task ids/names/progress/errors.
- Only run with `--yes` after user/supervisor confirmation.
- Use `--provider baidu`, `--provider quark`, `--ids`, or `--match` to avoid canceling unrelated work.
