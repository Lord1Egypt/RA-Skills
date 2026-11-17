# Message Workflow Reference

Use this reference when the user expects Codex, Hermes, OpenClaw, or another host agent to guide them by conversation instead of using a page or form. For polished wording, result-list UX, and recovery microcopy, also read `interaction-design.md`.

## Contents

- Intent Detection
- Interaction Principles
- Conversation State
- Anti-Guessing Rule
- Configuration-First Routing
- Manual History Import
- Field Collection Rules
- Add Downloader
- Search
- Search Result Presentation
- Send Result
- Downloader Status
- Confirmation Pattern
- Message Examples
- Error Handling

## Intent Detection

Map user messages to intents:

- Add PT site: "添加站点", "新增 PT", "配置 tracker", "add site".
- Add downloader: "添加下载器", "下载服务器", "qBittorrent", "Transmission", "add downloader".
- Search resources: "搜索", "查找", "找资源", "search".
- Send selected result: "发送到下载器", "推送", "下载这个", "send to".
- Downloader status: "下载器状态", "服务器状态", "检查 qBittorrent".
- Health check: "检查站点", "登录状态", "selector drift".
- First-run setup: "第一次使用", "初始化", "怎么配置", "开始使用", "first run", "setup".

If intent is ambiguous, ask the user to choose one of: initialization, add site, add downloader, search, send result, status.

## Interaction Principles

Use a guided-message style, not a form dump.

- Ask for the minimum fields needed to unblock the next action.
- Prefer one focused question with 2-4 concrete options over a long field list.
- Extract and reuse anything the user already provided.
- Persist reusable site/downloader facts as drafts or configs as soon as the host can safely store them.
- When persistent storage is empty but remembered/manual usage exists, treat that information as an import candidate and ask for confirmation before saving it.
- After tracker credentials validate, fetch and persist tracker account stats when supported.
- Infer safe local defaults, then show them in confirmation instead of asking upfront.
- Do not ask optional fields until they matter.
- Preserve the original task when routing into setup.
- Keep each response action-oriented: what is missing, why it matters, and exactly what the user can send next.
- Keep generic guidance free of hardcoded tracker names. Use `{displayName}`, `{trackerId}`, `{站点名}`, or "这个站点" in reusable wording; only render a concrete tracker name after the user supplied it, it was loaded from saved config, or it appears in a search result.
- Use redacted summaries before state-changing actions.
- If a host tool exists, call it or emit the capability payload only after confirmation for create/update/send actions.
- Do not offload routine operation to the user by showing local script commands. Scripts, CLI commands, host capability names, runtime checks, payloads, local file paths, and "我运行了 ..." details are internal implementation details. User-facing replies should say the current PT state, risk, and next action in plain language.

Safe defaults:

- Site `id`: lower-case normalized site name, for example `站点A` -> `site-a`.
- Site `displayName`: preset display name when available.
- Site `adapterId`: mapped adapter from `site-preset-catalog.json` or user-selected bridge adapter.
- Site `rateLimit`: conservative default from adapter/host policy.
- Downloader `id`: lower-case normalized name/type, for example `NAS qBittorrent` -> `nas-qb`.
- Downloader tags: host default or `["pt"]` only if the user accepts it in confirmation.
- Add mode: default to start immediately for selected downloads; use paused only when the user asks.

Do not default:

- Credential references.
- Proxy binding.
- Save path.
- Category/label when sending to downloader.
- Tracker endpoint for API/RSS/Torznab/Prowlarr/Jackett.

Memory policy:

- Do not rely on chat context as memory. Use host config APIs or `scripts/pt_store.py`.
- For first-run or setup messages, start with `python3 "$SKILL_ROOT/scripts/pt_runtime.py" first-run` when local scripts are available.
- At the start of site/download/search/status intents, read existing config/drafts from `pt.config.summary` or `python3 "$SKILL_ROOT/scripts/pt_store.py" summary`.
- When using the local fallback store, run `python3 "$SKILL_ROOT/scripts/pt_store.py" audit-secrets` if a stored config looks ready but validation fails or after migrating legacy config. If it reports paths, do not use or repeat those values; ask for replacement secret/profile references.
- Before asking for site fields, check existing tracker configs and drafts by id, display name, alias, URL host, and `sitePresetId`.
- If no stored config exists but the user or host memory mentions previously manual tracker/downloader use, do not present it as configured. Build an `importCandidate` from non-secret facts, resolve the preset/adapter, and ask whether to import it as a draft.
- Persist import candidates from memory only after confirmation. Store only non-secret fields and references such as `profileRef`, `secret://`, or `env://`; never store raw cookies, passkeys, passwords, auth headers, private download URLs, or torrent bytes.
- If the user provides any site-related non-secret field, save or update a tracker draft immediately with `tracker.config.draft.upsert` when available.
- If `tracker.config.draft.upsert` is unavailable, run `scripts/pt_store.py upsert-tracker --draft --json ...`.
- If the user provides fields for an existing tracker, treat the message as an update to that tracker draft/config rather than a new setup.
- Never ask again for a field that is already present and still compatible with the resolved adapter.
- If stored information conflicts with new information, show the conflict and ask whether to update.
- If the user provides raw secret material, do not store or repeat it; ask them to create a secret reference and store only the reference.
- Store sanitized account stats snapshots separately from tracker config after validation: upload/download, ratio, bonus, seeding count/size, invites, unread messages, warnings, and HnR risk when available.

## Conversation State

The agent should keep lightweight state while guiding the user:

```json
{
  "pendingIntent": {
    "type": "search",
    "keyword": "沙丘 2160p"
  },
  "setupStage": "tracker",
  "draftTracker": {
    "id": "site-a",
    "sitePresetId": "site-a",
    "adapterId": "nexusphp",
    "authMode": "browser_profile"
  },
  "knownTrackers": [
    {
      "id": "site-a",
      "sitePresetId": "site-a",
      "adapterId": "nexusphp",
      "authMode": "browser_profile",
      "profileRef": "profile://trackers/site-a",
      "status": "pendingHealthCheck"
    }
  ],
  "draftDownloader": {},
  "importCandidates": [
    {
      "kind": "tracker",
      "id": "site-a",
      "sitePresetId": "site-a",
      "adapterId": "nexusphp",
      "baseUrl": "https://tracker.example",
      "authMode": "cookie",
      "status": "needs_confirmation"
    }
  ],
  "lastSearch": {
    "query": "沙丘 2160p",
    "resultIds": []
  }
}
```

Use this state to resume:

- After adding a tracker for a pending search, ask whether to search the original keyword now.
- After adding a downloader for a pending send, ask whether to send the selected result with the newly added downloader.
- After credential validation fails, keep the draft tracker and ask only for a replacement credential reference.
- When the user mentions a known tracker later, reuse stored fields and ask only for missing or invalid pieces.
- If the user says "确认", apply it to the latest redacted summary only.

## Anti-Guessing Rule

Do not simulate or improvise live site calls. The assistant must not say "let me try another API path" for a private tracker unless the host has an explicit adapter with that path. If an endpoint returns 404, empty response, or redirects to login, stop and ask for the correct access method.

Bad behavior:

- Trying `/api/v1`, then RSS, then cookie login after failures.
- Treating `api_token` as a cookie or passkey.
- Declaring a site is NexusPHP and guessing standard RSS/API paths.

Correct behavior:

- Ask whether the token is for Torznab/Prowlarr/Jackett/RSS/native site API.
- Ask for the exact endpoint or secret reference.
- For a known site name, ask the host for `tracker.site.presets` and use the named preset only if it exists.
- Offer browser profile/cookie-based HTML adapter when no API endpoint is available and the chosen schema supports it.
- If the provided credential type is incompatible with the selected adapter, say it cannot be used and ask for a compatible credential. Do not submit `tracker.config.create`.
- Emit one confirmed adapter payload and let the host execute it.

## Configuration-First Routing

The assistant must not dead-end when configuration is missing. Before preparing or calling an action, check whether required host configuration exists when the host exposes a config/list capability.

Routing rules:

- Search requires at least one enabled tracker or a default search solution.
- Sending a result requires at least one enabled downloader or a default downloader.
- Downloader status requires at least one downloader, unless the user is asking to add one.
- Tracker health check requires the named tracker to exist.

If required configuration is missing:

1. Briefly say what is missing.
2. Preserve the original intent in conversation state.
3. Start the relevant setup guide with the smallest next question.
4. After the host confirms the setup was saved, offer to resume the original request using the preserved fields.

Example:

```text
你还没有配置 PT 站点，所以现在不能搜索。
我先帮你添加一个搜索源。你准备用哪种方式？
1. Prowlarr/Jackett/Torznab endpoint + API key
2. 已登录浏览器 profile
3. Cookie secret reference
```

If both tracker and downloader are missing for a send/download request, configure in this order:

1. PT site or tracker search source.
2. Downloader server.
3. Search again if needed.
4. Confirm selected result and send policy.

### Manual History Import

Use this path when the store has no matching tracker/downloader but the current turn, host memory, or user statement indicates the user previously used a site or downloader manually.

Rules:

- Say clearly that the item is known only as manual history, not as a saved PT Agent config.
- Resolve known tracker names against the preset catalog before asking for fields.
- Ask for one confirmation covering the non-secret draft fields that will be saved.
- Do not infer a valid credential from prior manual use. Ask for a compatible `profileRef`, cookie `secretRef`/`env://`, API key reference, or bridge endpoint based on the resolved adapter.
- After confirmation, upsert a draft with `status=pending_validation` or `pendingCredential`, then continue the normal credential gate and health-check flow.

Example:

```text
我找到两个手动使用过的站点，但它们还不是 PT Agent 配置。

准备导入为待校验草稿：
1. HDFans：NexusPHP，cookie/profile 接入
2. HHanClub：NexusPHP，cookie/profile 接入

确认后我只保存站点名、地址和接入方式，不保存 Cookie。接下来我会引导你选择安全凭据来源。
```

### First-Run Initialization

When the user asks to initialize or appears to be using the skill for the first time:

1. Run `python3 "$SKILL_ROOT/scripts/pt_runtime.py" first-run` or the host equivalent.
2. If nothing is configured, explain the two-step setup: PT site, then downloader.
3. Ask for only the first missing item, usually the tracker access method.
4. Do not present JSON first; show a message-first tutorial with concrete examples.
5. Merge reusable non-secret fields into a pending draft; do not enable a config before validation and confirmation.
6. After both tracker and downloader are usable, invite the first search.

Opening template:

```text
我先带你完成初始化。只需要两步：
1. 添加一个 PT 站点
2. 添加一个下载器

先从站点开始。你准备用哪种方式接入？
1. Prowlarr、Jackett 或 Torznab（推荐，稳定）
2. 已登录该站点的浏览器会话
3. 已保存在密码管理器或环境变量中的站点凭据
4. 站点提供的 RSS

告诉我选项和站点名即可。不要在聊天里发送 Cookie、密码或 passkey。
```

## Field Collection Rules

Ask for the fewest fields required for the next action. Prefer one compact question at a time unless the user already expects a setup wizard. If the user gives multiple fields in one message, parse all of them and continue from the first missing/invalid field.

### Add PT Site

Required:

- `id`: stable local id, lower-case recommended.
- `displayName`.
- `baseUrl`.
- `authMode`: `browser_profile`, `cookie`, `rss_token`, `api_token`, or `manual`.
- One auth reference when needed: `profileRef`, `credentialRef`, or `secretRefs.cookie`.
- `adapterId` or template: prefer `torznab`, `prowlarr`, `jackett`, `rss`, `unit3d-api`, `gazelle-json`, `nexusphp`, `unit3d`, `gazelle`, or a host-defined adapter id.

Optional:

- `proxyRef`.
- `categories`.
- `rateLimit`.
- `search` URL template.
- `selectors`.

Never ask users to paste raw cookies or passkeys. Ask them to store secrets in the host secret store and provide a reference such as `secret://trackers/site-a/cookie` or `env://SITE_COOKIE`.

Before confirming any site configuration, validate credential compatibility for every tracker:

1. Load matching saved config/draft.
2. Merge fields provided in the current message.
3. Persist the merged non-secret draft if it is not complete yet.
4. Resolve the site preset and adapter.
5. Read the adapter's allowed `authModes`.
6. Verify required fields for that auth mode are present.
7. Compare the user's credential type with those modes.
8. If it does not match, stop and tell the user exactly why the credential is not usable.
9. Ask for one of the compatible references or a separate documented bridge/API endpoint.
10. Do not emit `tracker.config.create` until the credential type and required references pass validation.

Required field validation:

- `browser_profile`: requires `profileRef`.
- `cookie`: requires `secretRefs.cookie`.
- `api_token`: requires `secretRefs.apiToken` or adapter-specific API key reference, plus a documented endpoint/base URL for that adapter.
- `rss_token`: requires a feed URL reference or sanitized feed URL plus `secretRefs.rssKey` when separate.
- `credentialRef`: valid only when the resolved adapter declares username/password-style login support.

After static validation passes and before final save, prefer a host `tracker.auth.validate` or `tracker.health_check` call when available. If the host cannot perform a runtime check yet, state that only credential type was validated and the first health check may still return `auth_required`.

After runtime auth succeeds, run `tracker.user_stats` when the resolved adapter supports it. Persist the sanitized result through the host config API or `scripts/pt_store.py upsert-stats`. If stats fail:

- `auth_required`: keep the draft/config but mark account status as needing a fresh profile/cookie.
- `capability_unavailable`: say the site was saved, but the current access method cannot read account stats.
- parser/shape failure: say the site login worked, but account parsing needs adapter maintenance.

### User-Facing Setup Completion

When a tracker is added or repaired successfully, answer as the operator, not as a script manual:

- Confirm the site is usable.
- Show only sanitized account stats and user-relevant status.
- Offer concrete natural-language next actions, such as searching, filtering free torrents, refreshing status, or sending a selected result to the downloader.
- Keep implementation details out of the default reply: no script paths, command blocks, cookie file paths, private URLs, local storage locations, host/runtime details, capability names, payload JSON, or "I ran ..." narration.

Template:

```text
{displayName} 已接入并通过校验。
- 账户：{username}
- 分享率：2.960
- 上传/下载：4.505TB / 1.522TB
- 做种：1 个

现在可以直接说：
- 搜这个站点的免费资源
- 搜 “异形 2160p”，只看免费
- 查看这个站点当前账号状态
- 把第 1 个结果加入 qBittorrent
```

Do not block search solely because optional account stats are unavailable, unless the failure indicates authentication is invalid.

Setup success response should include the latest account status when available:

```text
已记住 {displayName}，并完成登录校验。
账户状态：上传 1.2TB，下载 300GB，分享率 4.00，做种 42 个，魔力 12345，HnR 0。

可以继续：搜索“沙丘 2160p”、刷新站点状态、添加下载器。
```

Example:

```text
这个凭据不能用于 {displayName} 的 {sitePresetId}/{adapterId} 适配器。
{displayName} 在当前 preset 中使用 {adapterId} 适配器，只接受：
- profileRef：已登录浏览器会话
- cookie secretRef：站点 Cookie 的安全引用

你给的是 api_token。除非它属于 Prowlarr/Jackett/Torznab/RSS 或该站点官方文档里的 API，否则不能用来认证这个适配器。
请改为提供 profileRef=profile://trackers/{trackerId}，或 cookie secretRef=secret://trackers/{trackerId}/cookie。
```

When the user only says a common site name, ask which access method they have:

```text
这个站点你准备用哪种方式接入？
1. Prowlarr、Jackett 或 Torznab（推荐，可直接搜索下载）
2. 站点 RSS 或官方 API
3. 已登录该站点的浏览器会话
4. 已安全保存的 Cookie
```

If the user names a known private site:

1. Query or prepare `tracker.site.presets` with the site name. If the host has no registry, resolve against `site-preset-catalog.json`.
2. If a supported preset exists, tell the user which schema it uses and ask only for missing user config, usually base URL and `profileRef` or cookie `secretRef`.
3. If the site is mapped but the schema adapter is unavailable, explain that the site is recognized but the host needs that adapter, then ask whether to use Torznab/Prowlarr/Jackett/RSS or install/enable the adapter.
4. If no preset exists, ask whether they want to use Torznab/Prowlarr/Jackett/RSS/API documentation, a generic HTML schema adapter, or install a preset package.
5. Do not use an `api_token` with the named preset unless the preset declares an API auth mode.
6. If the user already provided a credential not supported by the resolved adapter, explicitly say it is not accepted and ask for a supported credential/reference, unless the credential belongs to a separate bridge adapter with its own endpoint.

Optimized prompt when a preset is resolved:

```text
我识别到 {displayName}，当前支持已登录浏览器会话或安全保存的 Cookie。
你希望使用哪一种？不要在聊天里发送 Cookie 原文。
```

Optimized prompt when stored fields exist:

```text
我已有 {displayName} 的未完成配置，接入方式已保留。
现在只差站点地址。请发送地址，或回复“用默认地址”。
```

Example:

```text
这个站点可以通过站点 preset 或兼容的 HTML/API 接入方式配置。
请确认你有哪种接入方式：
1. 已有该站点 preset，并有 profileRef/cookie secret
2. Prowlarr/Jackett/Torznab endpoint + apiKeyRef
3. 官方 RSS/API 文档和 token reference
4. 只知道 api_token，不确定来源
```

If the user has Prowlarr, Jackett, Torznab, or RSS, use `references/common-site-apis.md` and do not ask for raw DOM selectors.

If the user says only "I have an API token", ask:

```text
这个 token 属于哪种接口？
1. Prowlarr/Jackett/Torznab
2. 站点官方 API
3. RSS/passkey
4. 不确定

请提供对应 endpoint 或文档链接；如果不确定，我建议使用已登录浏览器 profile。
```

If the adapter has already been resolved and does not support `api_token`, do not ask this generic question first. Give the concrete mismatch warning and list the supported modes.

### Add Downloader

Required:

- `id`.
- `displayName`.
- `type`: at minimum `qbittorrent` or `transmission`.
- `baseUrl`.
- `credentialRef` or separate username/password refs when authentication is needed.

Confirm before saving:

- default category/label,
- save path,
- add paused/start immediately,
- tags,
- excluded site policy.

Optimized first prompt:

```text
我可以添加 qBittorrent 或 Transmission。
请告诉我下载器类型和访问地址。密码不要发到聊天里；下一步我会根据当前环境选择安全凭据方式。
```

If the user already provided type and URL:

```text
还缺安全凭据来源。你可以使用当前宿主的密码管理器，或已经设置好的环境变量；不要发送密码原文。
```

### Search

Required:

- `keyword`.
- tracker ids or a default search solution.

Optional:

- category ids,
- sort,
- discount/freeleech filter,
- limit per tracker.

If no trackers or search solution exist, guide the user to add a PT site first. Do not emit an empty `tracker.search` payload.

After the PT site is added, run or propose a health check and then resume the original search keyword. If the site was configured with Torznab/Prowlarr/Jackett/RSS/API adapter, use that adapter directly for search.

For movie and television searches, take the fast path: execute one `media-search` command with the user's full query, optional site alias, inferred `movie`/`tv` kind, limit, and timeout. Do not perform a preflight summary, health check, stats refresh, CLI help call, or reference lookup when a usable configuration already exists. The runtime normalizes phrases such as “搜一下周星驰的电影” and resolves short aliases such as `hh`.

Treat the first runtime result as authoritative for the turn. If it succeeds, present results immediately. If it fails, surface the structured error and one repair action. Never inspect raw store fields or generate temporary HTTP scraping code as a fallback.

Search prompt policy:

- If exactly one enabled tracker/default solution exists, search immediately with it.
- If multiple trackers exist and no default solution exists, ask the user to choose tracker ids or "全部".
- If no enabled trackers exist but drafts exist, show the closest draft and ask only for missing validation fields.
- If no trackers or drafts exist, keep `pendingIntent.type=search` and route to add-site.
- If the user included filters such as "免费", "4K", "1080p", "电影", preserve them in the search payload when supported; otherwise keep them in keyword text.

### Search Result Presentation

After `tracker.search` returns, always show an actionable result list instead of only summarizing counts.

Default layout:

- Show the first page with 5 results unless the user requested a different page size.
- Number results starting at 1 for the visible page.
- Include enough fields to choose: title, site, size, seeders/leechers, discount/freeleech, publish time, and category when available.
- Keep each result to one compact line plus optional subtitle only when helpful.
- Do not display raw detail/download URLs.
- Do not invent editorial recommendations or reasons. If the user asks for the "best" results, rank only by returned operational signals and name those signals plainly.
- Distinguish preference from filtering: "优先免费" keeps non-Free matches after Free results; "只看免费" uses the hard free-only filter.
- For a hard free-only filter with zero results, never fall back to ordinary torrents in the same response. Offer clearing the filter as an explicit next action.
- Make one search call per user request. Do not silently retry with normalized variants, translated titles, different sites, or relaxed filters.
- Store `lastSearch.resultIds` in the visible order so "第 3 个" resolves correctly.
- Mention partial tracker failures after the list, not before it.

Example:

```text
找到 18 个结果，当前第 1/4 页：

1. Dune.Part.Two.2024.2160p.UHD.BluRay.x265 - 站点A - 82.4GB - 45/3 - Free
2. Dune.2021.2160p.WEB-DL.HEVC - 站点B - 24.1GB - 122/8 - 50%
3. Dune.2021.1080p.BluRay.x264 - 站点C - 14.8GB - 63/2
4. Dune.Collection.2160p.Remux - 站点A - 138GB - 19/1 - Free
5. Dune.Part.Two.2024.1080p.BluRay - 站点D - 18.2GB - 88/4

你可以回复：下载第 1 个、下一页、只看免费、按做种排序、换站点搜索。
```

Supported follow-up commands:

- `下载第 N 个` / `发送第 N 个`: select visible result `N` and enter send flow.
- `详情第 N 个`: call `tracker.torrent_detail` or show cached detail if available.
- `下一页` / `上一页` / `第 N 页`: change page over `lastSearch.resultIds`.
- `只看免费` / `只看 4K` / `只看 1080p` / `只看某站`: filter current result set when possible; otherwise rerun search with filter.
- `按做种排序` / `按时间排序` / `按大小排序`: sort current result set when enough fields exist; otherwise rerun search with sort.
- `换关键词 ...`: run a new search and replace `lastSearch`.
- `换站点 ...`: rerun search against selected tracker ids.

Pagination state:

- Keep `lastSearch.page`, `lastSearch.pageSize`, `lastSearch.total`, `lastSearch.visibleResultIds`, `lastSearch.filters`, and `lastSearch.sort`.
- When the user selects by number, resolve against `visibleResultIds`, not the entire result list.
- If the user asks for a page outside the range, show the valid range.
- If no results match a filter, say so and offer to clear filters or search again.

### Send Result

Required:

- `resultId` or a clear selection from the latest search results.
- `trackerId`.
- `downloaderId` or default downloader.

For ordinary selected-result downloads, do not confirm category/label/path/tags/start policy; use defaults and start immediately. Confirm only bulk/ambiguous destination changes.

If no downloader exists, guide the user to add a downloader first. After the downloader is configured, ask whether to send the selected result using that downloader.

Send prompt policy:

- If the user says "下载第 1 个", resolve against `lastSearch.visibleResultIds[0]`.
- If there is no latest search, ask what result to send or run a search first.
- If exactly one downloader/default exists, use it in the confirmation summary.
- If multiple downloaders exist, ask the user to choose one.
- For a clear selected result, send immediately with defaults and `--start`. Confirm only when the destination is ambiguous, bulk, or destructive.

### Downloader Status

Required:

- `downloaderId`, unless the host has exactly one downloader or a default downloader.

Return normalized health and queue summary. Distinguish unreachable, unauthorized, unsupported version, and malformed response.

Use one `downloader-status` call without `--downloader` when a default is configured. Do not list configs first.

If no downloader exists, guide the user to add one instead of returning a generic not-found error.

### Tracker Account Status

Required:

- `trackerId`, unless the host has exactly one enabled tracker or a default search solution with one tracker.

For “看看我的 PT 数据” or an all-site refresh, use one concurrent `overview --refresh` call. For configuration-only questions, use cached `overview` without network access. Do not refresh trackers and downloader through separate tool turns.

Use `tracker.user_stats` for live refresh when available. If only a stored snapshot exists, say when it was last checked and offer to refresh. Present concise operational fields:

```text
{displayName} 账户状态（刚刚刷新）
- 上传/下载：1.2TB / 300GB
- 分享率：4.00
- 做种：42 个，合计 8.0TB
- 魔力：12345（+12.3/h）
- 风险：HnR 0，警告 0，未读消息 0

可继续：搜索、刷新、检查登录、更新凭据。
```

If the stored snapshot is old or credential freshness is uncertain, do not mention scripts or where data came from. Use this shape:

```text
{displayName} 账户状态（上次记录：{checkedAt}，建议刷新）
- 上传/下载：131.4GB / 11.6TB
- 分享率：0.01
- 保级要求：2.0，未达标
- 等级：Power User
- 风险：12 个月内分享率未达标可能降级
- 下载器：已连接，5 个活跃任务

建议先刷新登录状态和账号数据。回复“刷新账号状态”即可。
```

If auth fails:

```text
{displayName} 配置还在，但账户状态刷新失败：profile/cookie 已失效。
我已记录这个状态。请重新登录 profile，或更新 cookie secretRef。
```

## Confirmation Pattern

Before state-changing actions, respond with:

```text
我将执行：
- 操作：添加下载器
- id：nas-qb
- 类型：qbittorrent
- 地址：http://nas:8080
- 凭据：credentialRef=secret://downloaders/nas-qb
- 默认保存：/downloads/pt

回复“确认”后我会保存；回复“修改 ...”可以继续改字段。
```

After confirmation, emit or call the capability payload described in `references/agent-contract.md`.

For tracker creation, include validation status:

```text
我将添加 PT 站点：
- 站点：{displayName} ({trackerId})
- adapter：{adapterId}
- 认证：profileRef=profile://trackers/{trackerId}
- 凭据校验：类型匹配；保存后检查登录状态

回复“确认”后我会保存；回复“修改 ...”可以调整。
```

## Message Examples

### Add Downloader

User:

```text
添加 qBittorrent 下载器，地址 http://nas:8080
```

Assistant:

```text
我会把这个下载器记为“nas-qb”。凭据请选择密码管理器或已经设置好的环境变量，不要发送密码原文。
```

### Add PT Site

User:

```text
添加 PT 站点 {站点名}，用 nexusphp 模板
```

Assistant:

```text
请提供站点地址，并选择登录方式：已登录浏览器会话，或已经安全保存的 Cookie。不要发送 Cookie 原文。
```

### Search

User:

```text
搜索 盗梦空间 1080p
```

Assistant behavior:

- If default search solution exists, prepare `tracker.search`.
- If trackers exist but no default search solution exists, ask which trackers to search.
- If no trackers exist, start the add-site guide.

### Missing Configuration

User:

```text
搜索 沙丘 2160p
```

Assistant:

```text
还没有可用的 PT 站点配置，所以不能搜索。我先帮你添加一个站点。
你可以发其中一种：
1. Prowlarr、Jackett 或 Torznab
2. 站点名 + 已登录浏览器会话
3. 站点名 + 已安全保存的站点凭据

我会保存原搜索词“沙丘 2160p”，站点添加后继续搜索。
```

### Credential Mismatch

User:

```text
添加 {站点名}，api_token=secret://trackers/site-a/token
```

Assistant:

```text
这个凭据不能用于 {displayName} 的 {sitePresetId}/nexusphp 适配器。
{displayName} 在当前 preset 中使用 NexusPHP HTML 适配器，只接受 profileRef 或 cookie secretRef。

请改发其中一个：
- profileRef=profile://trackers/site-a
- cookieRef=secret://trackers/site-a/cookie

如果这个 token 属于 Prowlarr/Jackett/Torznab/RSS，请同时提供对应 endpoint，我会改用桥接 adapter。
```

## Error Handling

- If a secret value appears in the user message, do not repeat it. Tell the user to rotate it if it was exposed in a shared environment.
- If the execution capability is unavailable in normal user conversation, say the action is not available in this environment and ask for the smallest next user decision. Only output JSON payloads or host/runtime details when the user explicitly asks for implementation/debug details.
- If the host returns `configuration_required`, switch to setup guidance and preserve the original intent.
- If selector parsing fails, ask for a sanitized DOM fragment, not a full private page.
- If API endpoint probing would be needed to proceed, stop and ask for official endpoint/adapter details instead.
