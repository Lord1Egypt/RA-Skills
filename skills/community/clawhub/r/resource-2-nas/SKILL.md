---
name: resource-2-nas
description: Use when a user asks to search for movie, TV, animation, or other media resources; provides a Quark/Baidu share link to save; wants to verify saved resources through OpenList; wants to view/cancel OpenList transfer task progress; or wants to copy saved resources to NAS/SMB storage.
---

# Resource 2 NAS

Use this skill when the user enters any stage of a media-to-NAS workflow:

- Search stage: they ask to search a movie, TV show, animation, or media title and need ranked Baidu/Quark resource links.
- Share-link stage: they already have a Quark or Baidu share URL and want it saved into their own cloud drive.
- Verification stage: they want to check whether a saved resource is visible in OpenList.
- Task stage: they want to view, diagnose, or cancel OpenList copy/offline-download task progress.
- Backup stage: they want to copy a saved cloud-drive resource into a NAS/SMB-backed OpenList path.

The default search upstream is the PanSou instance at `https://so.252035.xyz/`, backed by the `fish2018/pansou` API.

Use `scripts/quark-save.mjs` when the user wants to save a Quark share link into their own Quark cloud drive folder. Use `scripts/baidu-save.mjs` when the user wants to save a Baidu Netdisk share link into their own Baidu cloud drive path. These workflows transfer the resource into the user's cloud drive only; they do not download files to the local filesystem.

For OpenClaw, Hermes, or any delegated sub Agent, read `SUBAGENT.md` first. Sub Agents should prefer `--format json`, follow the preview-confirm-save protocol, and never parse Markdown when a JSON result is available.

## Sub-Agent Quick Start

| Task | Sub-Agent command |
| --- | --- |
| Search | `node scripts/search-rrdynb.mjs "$KW" --format json --max-candidates 50` |
| Full readiness check | `npm run check-ready` |
| ENV check | `npm run check-env -- --json` |
| Cookie check | `npm run check-cookies` |
| Quark preview | `node scripts/quark-save.mjs "$SHARE_URL" "$DEST_URL" --dry-run --format json` |
| Baidu preview | `node scripts/baidu-save.mjs "$SHARE_URL" "$DEST_PATH_OR_URL" --dry-run --format json` |
| OpenList task progress | `npm run openlist-tasks -- list copy undone --format json` |
| OpenList cancel preview | `npm run openlist-tasks -- cancel copy undone --provider baidu --format json` |
| OpenList copy preview | `npm run openlist-copy -- "$SRC_DIR" "$DST_DIR" "$NAME" --format json` |
| Confirmed save | Re-run the preview command with `--yes --format json` after user/supervisor confirmation. |
| Confirmed OpenList copy/cancel | Re-run the preview command with `--yes --format json` after user/supervisor confirmation. |

## First-Time ENV Setup

Before editing `.env`, point the user to the setup guide if they need help collecting Cookies, OpenList tokens, or save/copy paths: https://guantou.site/archives/N2CmhISt

Before the first operation that needs Quark saving, Baidu saving, OpenList verification, or NAS/SMB backup copying, run the full read-only readiness check:

```bash
npm run check-ready
```

`check-ready` is Agent-oriented and outputs JSON by default. It checks:

- `.env` shape and required core keys.
- Quark/Baidu Cookie validity.
- At least one usable cloud-drive provider: Quark or Baidu. Both are not required.
- The configured Quark/Baidu save directory can be reached.
- The OpenList/NAS backup target can be listed with `refresh:true`.

Use `nextAction` to decide what to do:

- `ready`: configuration and read-only connectivity are usable; save/copy flows can continue.
- `configure_core`: ask for OpenList URL, OpenList Token, or NAS backup path.
- `configure_provider`: ask the user to configure at least one complete provider: Quark or Baidu.
- `configure_core_and_provider`: both core and provider config are incomplete.
- `fix_openlist_target`: OpenList/NAS backup target cannot be listed.
- `fix_provider_target`: the configured Quark/Baidu save directory cannot be reached.
- `refresh_invalid_cookies`: ask the user to log in again and copy fresh Cookies.
- `retry_network_or_check_access`: the current machine cannot reach the provider or the request timed out.

For focused checks, use `npm run check-env -- --json` or `npm run check-cookies`. For a human-readable view, run `npm run check-ready -- --format text`. These scripts mask Cookie/Token values and never print raw secrets.

If `.env` is missing, tell the user to copy `.env.example` to `.env` and fill in the required values. Never ask the user to paste secrets into docs or commit them.

Required `.env` values:

| Key | Required | Meaning |
| --- | --- | --- |
| `OPENLIST_TOKEN` | yes | Fixed OpenList API token used for `fs/list`, `fs/get`, `fs/copy`, and task APIs. |
| `OPENLIST_BASE_URL` | yes | OpenList service base URL, e.g. `http://127.0.0.1:5244`. |
| `OPENLIST_DEFAULT_COPY_DST_PATH` | yes | Default OpenList path backed by SMB/NAS storage for backup copies. |
| `QUARK_COOKIE` + `QUARK_DEFAULT_SAVE_URL` | conditional | Quark provider config. Required only if using Quark. `QUARK_DEFAULT_SAVE_URL` may be `/备份资源` or a full Quark folder URL. |
| `BAIDU_COOKIE` + `BAIDU_DEFAULT_SAVE_PATH` | conditional | Baidu provider config. Required only if using Baidu. `BAIDU_DEFAULT_SAVE_PATH` may be `/NAS资源下载` or a Baidu folder URL. |

Security rules:

- `.env` contains full credentials. It is ignored by git and must not be committed.
- Print only masked secret values. `scripts/check-env.mjs` masks `QUARK_COOKIE`, `BAIDU_COOKIE`, and `OPENLIST_TOKEN`.
- If any value is missing or invalid, stop before saving/copying and explain the specific missing key.
- Quark and Baidu are alternative providers. At least one must be fully configured, but both are not required.
- `QUARK_DEFAULT_SAVE_URL` may be a Quark cloud-drive path such as `/备份资源`, or a full Quark folder URL such as `https://pan.quark.cn/list#/list/all/<fid>-<folder-name>`. It is not a local filesystem path.
- `BAIDU_DEFAULT_SAVE_PATH` must be a Baidu cloud-drive path such as `/NAS资源下载`, or a Baidu folder URL copied from the address bar such as `https://pan.baidu.com/disk/main#/index?category=all&path=%2FNAS%E8%B5%84%E6%BA%90%E4%B8%8B%E8%BD%BD`. It is not a local filesystem path.
- `OPENLIST_DEFAULT_COPY_DST_PATH` must be an OpenList path such as `/影视资源备份/影视`, not an OS path such as `/mnt/nas/movies`.

Use these values as defaults:

- When the user provides a Quark share but no save folder, use `QUARK_DEFAULT_SAVE_URL`.
- When the user provides a Baidu share but no save folder, use `BAIDU_DEFAULT_SAVE_PATH`.
- Before a real Quark/Baidu save on a new install or after an auth failure, run `npm run check-ready` and require `nextAction: "ready"`.
- When calling OpenList APIs, use `OPENLIST_BASE_URL` and `OPENLIST_TOKEN`.
- When the user asks to back up/copy a saved resource but does not name a target, use `OPENLIST_DEFAULT_COPY_DST_PATH`.
- Still tell the user the source path, copied object, target path, and final naming before `fs/copy`.

## Default Endpoint

- Site: `https://so.252035.xyz/`
- API base: `https://so.252035.xyz/api`
- Health/config: `GET /api/health`
- Search: `GET /api/search` or `POST /api/search`
- Link check: `POST /api/check/links`
- Auth endpoints, only if `health.auth_enabled` is true:
  - `POST /api/auth/login`
  - `POST /api/auth/verify`
  - `POST /api/auth/logout`

## Search Parameters

For ordinary user searches, use:

```bash
node scripts/search-rrdynb.mjs "蜘蛛侠"
```

Default behavior: search Baidu Netdisk and Quark Netdisk results first, then return a Markdown table with only the top 50 PanSou-ranked results after local disk-type filtering. Do not show hundreds of raw upstream matches to the user unless they explicitly ask for a larger export. For programmatic JSON output, use `--format json` or `--json`.

The helper calls `GET /api/search` with these parameters:

| Parameter | GET type | POST type | Required | Meaning |
| --- | --- | --- | --- | --- |
| `kw` | string | string | yes | Search keyword/title. |
| `channels` | comma string | string[] | no | Telegram channels to search. Omit for server defaults. |
| `plugins` | comma string | string[] | no | Plugin names to search. Omit for all enabled plugins. |
| `conc` | number | number | no | Search concurrency. Omit for server auto setting. |
| `refresh` | `"true"` | boolean | no | Force refresh and bypass cache. |
| `res` | string | string | no | `merge` default, `all`, or `results`. |
| `src` | string | string | no | `all` default, `tg`, or `plugin`. |
| `cloud_types` | comma string | string[] | no | Limit returned disk types. |
| `ext` | JSON string | object | no | Plugin extension parameters, e.g. `{"title_en":"Spider-Man","is_all":true}`. |
| `filter` | JSON string | object | no | Include/exclude filter, e.g. `{"include":["4K"],"exclude":["预告"]}`. |

Supported `cloud_types`: `baidu`, `aliyun`, `quark`, `guangya`, `tianyi`, `uc`, `mobile`, `115`, `pikpak`, `xunlei`, `123`, `magnet`, `ed2k`, `others`.

When `cloud_types` is requested, the helper also filters normalized `results[]` locally, because the public instance may still include other disk types inside ranked result messages.

Useful helper options:

```bash
node scripts/search-rrdynb.mjs "蜘蛛侠" \
  --cloud-types baidu,quark \
  --res all \
  --src all \
  --max-candidates 50
```

- `--channels tgsearchers4,Aliyun_4K_Movies`
- `--plugins wanou,zhizhen`
- `--include 4K,合集`
- `--exclude 预告,花絮`
- `--refresh`
- `--ext-json '{"title_en":"Spider-Man"}'`
- `--filter-json '{"include":["4K"],"exclude":["预告"]}'`
- `--api-base https://so.252035.xyz/api`
- `--format markdown|json`

## Search Response

PanSou may return either direct data or a wrapper:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 15,
    "results": [],
    "merged_by_type": {}
  }
}
```

Prefer `data.merged_by_type` for user-facing output because it is already grouped by disk type. Each merged link has:

- `url`: cloud disk, magnet, or ed2k link.
- `password`: extraction code/password.
- `note`: resource note/title.
- `datetime`: resource update time.
- `source`: `tg:<channel>`, `plugin:<name>`, or `unknown`.
- `images`: optional images from Telegram messages.

The helper normalizes this into:

- `candidates[]`: ranked resource rows, each with one `downloadLinks[]` entry.
- `downloadLinks[]`: flat list containing `provider`, `diskType`, `url`, `extractionCode`, `note`, `datetime`, and `source`.
- `availableTotal`: upstream total count, for reference only.
- `returnedCount` / `total`: number of results actually returned to the user, capped by `--max-candidates` and defaulting to 50.
- `providerCounts`: counts by disk type among returned results only.

## User-Facing Table

When answering a search request, output a Markdown table sorted by PanSou relevance. Include clickable links directly in the table so the user can open and download without digging through JSON.

Use these columns:

| # | 资源 | 网盘 | 链接 | 提取码 | 来源 | 时间 |
|---:|---|---|---|---|---|---|
| 1 | 示例资源 | 夸克网盘 | [打开](https://pan.quark.cn/s/example) | - | plugin:example | 2026-01-01 |

Rules:

- The table is the primary answer. Do not provide only a summary when links are available.
- Use `[打开](url)` for the link cell.
- Use `-` when extraction code, source, or datetime is absent.
- Keep the table to the returned top 50 by default.
- Put a short line above the table: `按 PanSou 相关度排序，返回前 N 条。上游可用结果约 M 条。`

## Link Check Parameters

Use link checks only when the user asks to verify whether returned links are alive, or when checking results would materially improve the answer:

```bash
node scripts/search-rrdynb.mjs "蜘蛛侠" --check-links --max-candidates 5
```

`POST /api/check/links` body:

| Parameter | Type | Required | Meaning |
| --- | --- | --- | --- |
| `items` | object[] | yes | Links to check. |
| `items[].disk_type` | string | yes | Disk type. |
| `items[].url` | string | yes | Full share URL. |
| `items[].password` | string | no | Extraction code if not already in URL. |
| `view_token` | string | no | View/batch token for frontend-style checks. |
| `proxy_url` | string | no | Per-request proxy. Supports `http://`, `https://`, `socks5://`, `socks5h://`. |
| `proxy` | string | no | Alias for `proxy_url`; `proxy_url` wins if both exist. |

Checkable disk types: `baidu`, `aliyun`, `quark`, `tianyi`, `uc`, `mobile`, `115`, `xunlei`, `123`. Magnet and ed2k are search results, but not link-check targets.

The PanSou project documents `/api/check/links`, and the frontend API panel also references it. If the public `https://so.252035.xyz/api/check/links` instance returns `404`, keep the search results and report that link checking is unavailable on the current public instance instead of treating the whole search as failed.

Check states:

- `ok`: link valid.
- `bad`: link invalid.
- `locked`: extraction code required or wrong.
- `unsupported`: platform not supported by checker.
- `uncertain`: check failed or result uncertain.

## Quark Cloud Save

When the user provides a Quark share URL and a destination Quark cloud-drive path or folder URL, first preview the share contents:

```bash
node scripts/quark-save.mjs \
  "https://pan.quark.cn/s/bcbd9d24fe5a#/list/share" \
  "/备份资源" \
  --dry-run
```

The preview reads the public share. If the destination is a path like `/备份资源`, actual saving resolves that path to a Quark `fid` with the user's Cookie. Actual saving requires the user's Quark Cookie through an environment variable:

```bash
QUARK_COOKIE='...' node scripts/quark-save.mjs \
  "https://pan.quark.cn/s/bcbd9d24fe5a#/list/share" \
  "/备份资源" \
  --context-name "你的友好邻居蜘蛛侠 第一季" \
  --resource-type series
```

Security rules:

- Treat `QUARK_COOKIE` as a full login credential. Never print it, commit it, or put it in docs.
- Prefer `--cookie-env QUARK_COOKIE`; if the user uses another env var, pass that name with `--cookie-env`.
- Keep the default interactive confirmation. Use `--yes` only when the user explicitly asked for non-interactive execution or has already confirmed the selected rows.

Agent responsibility before saving:

- The Agent must inspect the dry-run table plus the conversation/search context and decide the canonical resource name. Do not rely only on obfuscated share titles.
- If the resource is a series, tell the user it is a series and pass `--resource-type series`.
- If the share title contains separators or evasive characters, correct the resource name from context and pass it with `--context-name`.
- For non-trivial naming, pass an explicit Agent decision plan with `--rename-plan-json`. The script applies this plan after Quark returns the saved top-level fids.

Example Agent rename plan:

```bash
node scripts/quark-save.mjs "$SHARE_URL" "$DEST_URL" \
  --context-name "你的友好邻居蜘蛛侠 第一季" \
  --resource-type series \
  --rename-plan-json '[{"rank":1,"name":"你的友好邻居蜘蛛侠 第一季","reason":"Agent 根据搜索上下文修正规避字符和季名"}]'
```

Useful options:

- `--select all|1,3|2-5`: choose which rows to save.
- Destination positional argument accepts either `/夸克目录` or a full Quark folder URL.
- `--yes`: skip the confirmation prompt and save the selected rows immediately.
- `--dry-run`: preview only; no Cookie needed and no save happens.
- `--format json` / `--json`: output a single structured JSON object for sub Agents.
- `--no-rename`: save without post-save rename.
- `--resource-type auto|series|movie|collection`: pass the Agent's resource classification.
- `--rename-plan-json '[{"rank":1,"name":"...","reason":"..."}]'`: pass Agent-decided final names. `rank` refers to the row number in the preview table.

Quark API flow used by the helper:

- `POST /1/clouddrive/share/sharepage/token`: obtain `stoken` for the share URL.
- `GET /1/clouddrive/share/sharepage/detail`: list share rows for user confirmation.
- `POST /1/clouddrive/share/sharepage/save`: save selected `fid_list` + `fid_token_list` to `to_pdir_fid`.
- `GET /1/clouddrive/task`: poll the async save task until completion.
- `POST /1/clouddrive/file/rename`: apply the Agent-approved rename plan to saved top-level files/folders.

## Baidu Netdisk Save

When the user provides a Baidu Netdisk share URL and a destination Baidu cloud-drive path, first preview the share contents:

```bash
node scripts/baidu-save.mjs \
  "https://pan.baidu.com/s/1abcDEF?pwd=8888" \
  "/NAS资源下载" \
  --dry-run
```

If the user omits the destination path, use `BAIDU_DEFAULT_SAVE_PATH` from `.env`. This value may be either a direct Baidu path like `/NAS资源下载` or a Baidu folder URL like `https://pan.baidu.com/disk/main#/index?category=all&path=%2FNAS%E8%B5%84%E6%BA%90%E4%B8%8B%E8%BD%BD`; the helper decodes the URL to `/NAS资源下载` before calling `share/transfer`. Links in `/share/init?surl=...&pwd=...` form are also supported. If the extraction code is not in the URL, pass it with `--passcode`:

```bash
node scripts/baidu-save.mjs "$SHARE_URL" "$BAIDU_DEFAULT_SAVE_PATH" \
  --passcode 8888 \
  --context-name "你的友好邻居蜘蛛侠 第一季" \
  --resource-type series
```

Actual saving requires the user's Baidu Netdisk Cookie through `BAIDU_COOKIE`:

```bash
BAIDU_COOKIE='...' node scripts/baidu-save.mjs \
  "https://pan.baidu.com/s/1abcDEF?pwd=8888" \
  "/NAS资源下载" \
  --context-name "蜘蛛侠：平行宇宙" \
  --resource-type movie
```

Security rules:

- Treat `BAIDU_COOKIE` as a full login credential. Never print it, commit it, or put it in docs.
- Prefer `--cookie-env BAIDU_COOKIE`; if the user uses another env var, pass that name with `--cookie-env`.
- Keep the default interactive confirmation. Use `--yes` only when the user explicitly asked for non-interactive execution or has already confirmed the selected rows.

Agent responsibility before saving:

- Detect provider from the link. Baidu links use `pan.baidu.com`; Quark links use `pan.quark.cn`.
- Inspect the dry-run table plus the conversation/search context and decide the canonical resource name.
- If the dry-run table shows a single top-level folder and the type is unclear, inspect one level deeper with `GET /share/list` using that row's `path` before deciding `--resource-type`.
- If the resource is a series, tell the user it is a series and pass `--resource-type series`.
- If child folders/files look like quality or version variants, such as `1080p`, `4K`, `SDR`, `彩色版`, or `黑白版`, treat it as `collection`, not `series`.
- If the share title contains separators or evasive characters, correct the resource name from context and pass it with `--context-name`.
- Before executing the save, tell the user: source share URL, selected rows, target Baidu path, and final naming/rename plan.
- For non-trivial naming, pass an explicit Agent decision plan with `--rename-plan-json`. The script attempts a post-transfer Baidu rename through `/api/filemanager`.
- The Baidu target is always a Baidu cloud-drive path. A folder named `/NAS资源下载` is still a Baidu folder unless the user explicitly asks for an OpenList/NAS copy after cloud save.

Example Agent rename plan:

```bash
node scripts/baidu-save.mjs "$SHARE_URL" "$BAIDU_DEFAULT_SAVE_PATH" \
  --context-name "你的友好邻居蜘蛛侠 第一季" \
  --resource-type series \
  --rename-plan-json '[{"rank":1,"name":"你的友好邻居蜘蛛侠 第一季","reason":"Agent 根据搜索上下文修正规避字符和季名"}]'
```

Useful options:

- `--select all|1,3|2-5`: choose which rows to save.
- `--yes`: skip the confirmation prompt and save the selected rows immediately.
- `--dry-run`: preview only; no save happens.
- `--format json` / `--json`: output a single structured JSON object for sub Agents.
- `--no-rename`: save without post-save rename.
- `--passcode 8888`: provide a Baidu extraction code if the URL does not include `pwd`.
- `--resource-type auto|series|movie|collection`: pass the Agent's resource classification.
- `--rename-plan-json '[{"rank":1,"name":"...","reason":"..."}]'`: pass Agent-decided final names. `rank` refers to the row number in the preview table.
- `--save-path` / positional destination accepts either `/百度目录` or a Baidu folder URL containing a `path` parameter.

Baidu API flow used by the helper:

- `GET /s/<share-id>`: read the share page and extract `bdstoken`, `shareid`, `share_uk`, and root files.
- Share page context may appear either as pure JSON such as `window.yunData.setData({...})`, or as the current two-part shape `window.yunData={...}; locals.mset({...})`. The helper supports both. If parsing fails with `无法解析百度分享页中的分享上下文`, inspect the page for these fields and add a parser regression test before changing the script.
- `POST /share/verify`: verify extraction code and collect `randsk`/share cookies when needed.
- `GET /share/list`: list share files when the share page does not include complete file rows.
- `POST /share/transfer`: save selected `fsidlist` to the target Baidu cloud-drive path.
- `GET /api/list`: list the target path after transfer when post-save rename or save verification is needed.
- `POST /api/filemanager?opera=rename`: apply the Agent-approved rename plan to saved top-level files/folders.

After Baidu save:

- Treat `share/transfer` response `errno: 0` as a successful cloud-drive save.
- Verify the target Baidu path with `GET /api/list` and match the Agent-approved resource name.
- If the saved folder already exists and Baidu creates a duplicate/new-copy name, report the actual name returned by the target directory listing and use that name for any later OpenList/NAS copy step.

## OpenList Verification and NAS Download

Use OpenList when the user wants to verify that a just-saved Quark or Baidu resource is visible through their NAS/OpenList mount, or when they want to download a mounted resource through OpenList APIs.

Authentication:

- Prefer the user's fixed OpenList API token for automation. Pass it as the `Authorization` header.
- Treat the token as a full API credential. Never print it, commit it, or place it in command history when avoidable.
- Do not cache OpenList download URLs for long periods. Call `POST /api/fs/get` immediately before downloading.

After Quark save:

- Always refresh the target OpenList directory with `refresh: true`.
- The observed working flow is:
  1. Save the Quark share with `scripts/quark-save.mjs`.
  2. Wait for the Quark task to finish and post-save rename to complete.
  3. Immediately call `POST /api/fs/list` on the OpenList target path with `refresh: true`.
  4. Match the saved resource by the Agent-approved canonical name.
- In the tested local instance, saving into Quark folder `备份资源` was visible through OpenList path `/pan/quark/备份资源` within the immediate refreshed list request.

OpenList list request:

```bash
curl "$OPENLIST_URL/api/fs/list" \
  -H "Authorization: $OPENLIST_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"path":"/pan/quark/备份资源","password":"","page":1,"per_page":100,"refresh":true}'
```

OpenList file download:

```bash
curl "$OPENLIST_URL/api/fs/get" \
  -H "Authorization: $OPENLIST_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"path":"/pan/quark/备份资源/example.srt","password":""}'
```

If `raw_url` is returned, download it immediately:

```bash
curl -L "$RAW_URL" -o "./example.srt"
```

Server/NAS-side download rules:

- Clicking "download" in the OpenList web UI downloads to the browser user's local computer. It does not make the OpenList server save the file to the server filesystem.
- To save files on the deployment server or a NAS-mounted disk, prefer mounting the NAS directory as an OpenList storage, for example `/影视资源备份/影视`, then use `POST /api/fs/copy` from the cloud-drive mount into that NAS-backed path.
- If copy is not possible, use OpenList offline download into the NAS-backed OpenList path, or run a server-side script on the OpenList/NAS host: call `POST /api/fs/get`, read the fresh `raw_url`, then `curl -L "$RAW_URL" -o "/mounted/nas/path/file.ext"`.

OpenList copy to NAS backup:

- Use this when the user specifies a backup directory, such as a NAS/SMB-mounted OpenList path.
- Before executing copy, tell the user:
  - Source: the OpenList source directory that contains the saved resource, for example `/pan/quark/备份资源`.
  - Object: the exact `names[]` item that will be copied, for example `钢铁侠与美国队长：英雄集结 (2014)`.
  - Destination and naming: the target OpenList directory, for example `/影视资源备份/影视`, and the final path/name that will appear there.
- Prefer `copy` over `move`. Use `move` only if the user explicitly asks to remove the source after backup.
- Always refresh source and target directories with `refresh: true` before and after copy.
- Prefer the bundled script instead of hand-written curl. It previews source and target first, then after confirmation calls `POST /api/fs/copy`, polls `/api/task/copy/undone` and `/api/task/copy/done`, and refreshes the target directory until the copied folder/file appears.
- Do not treat a task disappearing from `undone` as failure by itself. First check `done` tasks and the refreshed destination directory.
- If the preview output has `destination.existingTargetNames`, tell the user the target already contains same-named items and require explicit confirmation before `--yes`.

Copy preview:

```bash
npm run openlist-copy -- \
  "/pan/quark/备份资源" \
  "/影视资源备份/影视" \
  "钢铁侠与美国队长：英雄集结 (2014)" \
  --format json
```

Confirmed copy after the user/supervisor approves source, object, destination, and final naming:

```bash
npm run openlist-copy -- \
  "/pan/quark/备份资源" \
  "/影视资源备份/影视" \
  "钢铁侠与美国队长：英雄集结 (2014)" \
  --yes \
  --format json
```

OpenList task progress and cancellation:

- Use this when the user asks whether copy/offline-download/upload tasks are still running, or asks to cancel stuck tasks.
- Task groups: `copy`, `offline_download`, `offline_download_transfer`, `upload`, `decompress`, `decompress_upload`.
- Task states: `undone`, `done`.
- `openlist-tasks` defaults to `list copy undone` and outputs Agent JSON.
- Cancellation is preview-only unless `--yes` is passed.
- If the user says "only Quark" or "cancel Baidu", filter by provider before taking action. Do not start or continue the other provider.
- Do not create background retry loops or recurring jobs unless the user explicitly asks for them.

Task examples:

```bash
npm run openlist-tasks -- list copy undone --format json
npm run openlist-tasks -- list offline_download undone --format json
npm run openlist-tasks -- cancel copy undone --provider baidu --format json
npm run openlist-tasks -- cancel copy undone --provider baidu --yes --format json
```

- OpenList's offline download feature downloads an external URL into storage managed by OpenList. It supports `SimpleHttp`, `aria2`, and `qBittorrent` tools. For API use, call:

```bash
curl "$OPENLIST_URL/api/fs/add_offline_download" \
  -H "Authorization: $OPENLIST_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "path":"/nas/movies",
    "urls":["https://example.com/file.mkv"],
    "tool":"SimpleHttp",
    "delete_policy":"delete_on_upload_succeed"
  }'
```

Notes:

- `path` is an OpenList path, not an arbitrary OS path. If the user wants `/mnt/nas/movies`, first mount that directory in OpenList and use its OpenList path.
- For NAS/SMB backup, `POST /api/fs/copy` is usually more reliable than offline download because OpenList handles cloud-to-mounted-storage transfer as a copy task.
- For an existing OpenList cloud file, use `POST /api/fs/get` to obtain a fresh `raw_url`, then pass that URL to `POST /api/fs/add_offline_download` targeting the NAS-backed OpenList path.
- If using `aria2` or `qBittorrent`, configure the tool in OpenList settings first. For Docker, make sure OpenList and the downloader share the documented temp directory mounts.
- Poll OpenList task APIs under `/api/task/offline_download/*` and `/api/task/offline_download_transfer/*` when the user needs progress or completion status.

## Workflow

1. For Quark save, Baidu save, OpenList verification, or NAS/SMB copy, run `npm run check-ready` first in a fresh install or whenever `.env` may be missing/stale. Continue only when `nextAction` is `ready`.
2. Search the exact user keyword first.
3. If results are thin or off-target, try 1-3 variants: remove book marks, remove spaces/punctuation, include original English title if the user gave one.
4. Default to `res=all` and `src=all` so the helper can rank by PanSou `results[]` order; use `cloud_types`, `plugins`, `channels`, `include`, or `exclude` only when the user asks or the result set needs narrowing.
5. Report the best ranked candidates with note/title, provider, source, URL, extraction code, and update time when present.
6. If the user asks whether links are valid, rerun with `--check-links` or call `/api/check/links` on the visible links and include each state/summary.
7. If `/api/health` reports `auth_enabled: true`, authenticate first or ask the user for credentials/token.
8. If the user asks to save a Quark result into their own drive, run `scripts/quark-save.mjs --dry-run`, tell the user what resource rows were found and whether the Agent judges it to be a series, then save only after confirmation/Cookie availability. Pass the Agent's canonical name and resource type to the script. Use `QUARK_DEFAULT_SAVE_URL` when the user does not specify a save folder.
9. If the user asks to save a Baidu result into their own drive, run `scripts/baidu-save.mjs --dry-run`, tell the user what resource rows were found and whether the Agent judges it to be a series, then save only after confirmation/Cookie availability. Pass the Agent's canonical name and resource type to the script. Use `BAIDU_DEFAULT_SAVE_PATH` when the user does not specify a save folder.
10. If the user asks whether the saved cloud-drive resource appears in OpenList, call `POST /api/fs/list` with `refresh: true` every time, then report whether the Agent-approved resource name was found.
11. If the user asks about current OpenList transfer progress, run `npm run openlist-tasks -- list copy undone --format json` or the matching task group; report task ids, names, progress, and errors. If they ask to cancel, preview first and require confirmation before adding `--yes`.
12. If the user asks to back up into a NAS/SMB OpenList storage, state the source path, exact object name, target backup directory, and final naming before execution; then use `npm run openlist-copy -- "$SRC_DIR" "$DST_DIR" "$NAME" --yes --format json` after confirmation. Use `OPENLIST_DEFAULT_COPY_DST_PATH` when the user does not specify a target.
13. If the user asks to download into NAS/server storage and copy is not suitable, do not click browser download. Use OpenList offline download into a NAS-backed OpenList storage path, or run a server-side download script using a fresh `raw_url` from `POST /api/fs/get`.
