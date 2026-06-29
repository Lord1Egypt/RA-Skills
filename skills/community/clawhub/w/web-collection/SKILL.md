---
name: web-collection
description: 通过云端连接器优先执行浏览器插件数据采集，也可回退到本地连接器；适用于抖音、TikTok、小红书、Amazon、Bilibili 的采集任务，以及 web-collection 首次上手、配置、付费使用说明和 QA 排障。
---

# Web Collection

Use this skill for browser-extension collection tasks on:

- Douyin
- TikTok
- Xiaohongshu
- Amazon
- Bilibili

## Online Documentation Routing

The online documents are the source of truth for user-facing guidance. Do not duplicate their long-form onboarding, paid-access, UI operation, or QA content in this skill. When a user asks for guidance, read the relevant online document if tools can access it; if not, give the user the link and say the online document should be used as the current guide.

- Quick start / first-time use / UI operation guide:
  - https://vcn5grhrq8y0.feishu.cn/wiki/MoXrwwUN7iiUFkk8eWycs9JqntA?from=from_copylink
  - Use when the user asks how to use the plugin, how to start, how to configure it for the first time, where to click, how paid access works, or needs step-by-step human instructions.
- Demo scenarios / example collection scenes:
  - https://vcn5grhrq8y0.feishu.cn/wiki/GO11wlXkriSwNakXrt2ck0GanEe
  - Use when introducing what this skill can do, when the user asks for examples, or after a successful run to point the user to more collection scenarios.
- Browser extension and connector installation guide:
  - https://vcn5grhrq8y0.feishu.cn/wiki/R6f2w6o7ci1db1kYLK4cgJIYnWh
  - Use before the user's first collection run, or when the user needs to install, download, update, or reconnect the browser extension or connector.
  - The browser extension and connector must be downloaded from this document. Do not tell users to search or install the extension from the Chrome Web Store / Google Store.
- Bitable configuration, connector verification, and authorization guide:
  - https://vcn5grhrq8y0.feishu.cn/wiki/EAtJw2irFiDvMpkZXb4cBjYonNg
  - Use after installation is complete and before first collection. It covers plugin-side bitable configuration, connector status verification, and manual fallback details.
- Bitable template direct link:
  - https://vcn5grhrq8y0.feishu.cn/base/UKQsbVHpMac293s0cnFc1hq1nDd?table=tblTXM4lclXM6Jzr&view=vew8OdcKHw
  - When guiding the user to copy the bitable template, send this direct link in the response so the user does not need to open the guide first to find it.
- QA / troubleshooting guide:
  - https://vcn5grhrq8y0.feishu.cn/wiki/F83hw2w6Xi7EOFkIScrccrQYnnd?from=from_copylink
  - Use when the user asks about errors, failed export, missing data, connector/cloud/local issues, access problems, supported scenarios, or other common questions.

Decision rule:

- If the user asks what this skill is, what it can do, or generally says "how do I use this skill" without explicitly asking to configure now, give only the lightweight intro response. Do not show the full operation flow, setup checklist, or screenshots yet. End by asking whether they want to continue with first-time setup/configuration.
- If the user confirms they want to continue setup/configuration, or asks for first-time setup, installation, binding bitable, connector verification, or credential collection, enter the onboarding flow below and show the relevant screenshots inline.
- If the user asks to collect data but first-time setup is not confirmed, guide installation first, then bitable configuration and connector authorization. Wait for the user's confirmation before proceeding between those phases.
- If the user reports a problem, asks whether a behavior is normal, or asks how to recover a failed run/export, send the QA link first and answer from that document when accessible.
- If the user asks to collect data now, continue with the execution contract below.

For collection execution, keep using this `SKILL.md` and the bundled scripts as the agent contract. For complex or ambiguous execution requests, read [references/learning-guide.md](references/learning-guide.md) as an offline routing and recovery summary after checking whether the QA guide applies.

## Visual Guidance Assets

This skill may include local screenshots or GIFs under `assets/` for concise user guidance. For onboarding steps, guide the user in this order:

1. Show the relevant local screenshot or GIF when it exists. Resolve image files relative to this `SKILL.md` file, under the bundled `assets/` directory. Use the image/attachment mechanism supported by the current Agent host. If the host supports Markdown images with relative packaged assets, use paths like `assets/bitable-step-00-personal-center.png`; if the host requires attachments, attach that asset file.
2. Add a short step-specific instruction paragraph.
3. Then provide the detailed Feishu document link as the full reference.

If an asset is missing, still give a short text instruction first, then send the matching online document link and say the document contains the current visual guide.

When the user has confirmed setup/configuration, asks to bind bitable, or asks how to obtain connector credentials, do not provide a text-only setup answer if matching assets exist. The answer must include the bundled screenshots inline or as attachments, placed next to the corresponding step. Do not invent machine-specific absolute paths; always resolve files from this skill package's `assets/` directory.

Do not show screenshots in the lightweight intro response. Screenshots are only for the setup/configuration flow after the user confirms they want to continue.

Image/text placement rules:

- For configuration guidance, pair each operation with its matching image immediately before or after that operation. Do not put all images at the bottom of the answer.
- The bitable binding step must be rendered as step text plus the corresponding image for each substep:
  - `登录媒讯助手` text with `assets/bitable-step-00-personal-center.png`
  - `复制多维表格模板` text with `assets/bitable-step-01-template-copy.png`
  - `获取授权码` text with `assets/bitable-step-02-auth-code.png`
  - `测试并保存多维表格配置` text with `assets/bitable-step-03-config-save.png`
- The only exception is the connector step: `assets/connector-step-01-status-token.png` is an overview image for the whole third major step and must appear once at the end of that major step.

Connector guidance constraints:

- Do not ask the user to manually copy `device_id`, `connector_token`, `Token`, or `API token` during normal Agent-led use.
- When connector authorization is missing or expired, generate the website login confirmation link through the bundled scripts and ask the user to click it.
- The user's action should be described simply as: open the Agent-provided link, finish website login/authorization, then return to the Agent.
- Do not tell the user to click `免费获取云端连接器凭证`.
- Do not tell the user to enter an email address to receive a credential.
- Do not tell the user to choose or switch `云端连接器` / `本地连接器` mode in this onboarding step.
- Do not split the connector step into repeated substeps with the same screenshot. Treat `assets/connector-step-01-status-token.png` as an optional overview image only when explaining the connector UI for troubleshooting or manual fallback.

Expected optional assets:

- `assets/install-extension-connector.gif` or `assets/install-extension-connector.png`
  - Use with the browser extension and connector installation guide.
- `assets/configure-bitable.gif` or `assets/configure-bitable.png`
  - Use when guiding plugin-side bitable export configuration.
- `assets/bitable-step-00-personal-center.png`
  - Use when telling the user to open the browser extension, enter `个人中心`, and log in.
- `assets/bitable-step-01-template-copy.png`
  - Use when telling the user to open the direct bitable template link and create a copy.
- `assets/bitable-step-02-auth-code.png`
  - Use when telling the user to open `多维表格插件` -> `自定义插件` and copy the authorization code.
- `assets/bitable-step-03-config-save.png`
  - Use when telling the user to fill in bitable URL plus authorization code, test the connection, and save.
- `assets/verify-connector.gif` or `assets/verify-connector.png`
  - Legacy optional asset. Prefer `assets/connector-step-01-status-token.png` and do not show a separate connector verification image.
- `assets/copy-device-token.gif` or `assets/copy-device-token.png`
  - Legacy optional asset. Prefer `assets/connector-step-01-status-token.png` and do not show a separate credential-copy image.
- `assets/connector-step-01-status-token.png`
  - Use only as a manual fallback/troubleshooting overview. It covers connector authorization and green status verification. Do not repeat it below multiple substeps.
- `assets/view-results.gif` or `assets/view-results.png`
  - Use after successful collection to show where to view exported results.

Do not block onboarding when these files are absent. The Feishu documents remain the source of truth for screenshots, GIFs, and current UI details.

## Installation Guidance Constraints

When guiding browser extension and connector installation, follow these constraints exactly:

1. Browser extension source:
   - Tell users to download and install the browser extension from the installation guide:
     `https://vcn5grhrq8y0.feishu.cn/wiki/R6f2w6o7ci1db1kYLK4cgJIYnWh`
   - Do not say "open the Chrome Web Store", "visit the Chrome app store", "search the Chrome extension store", or similar.
   - Do not invent any public store listing or alternate download source.
2. Connector platform variants:
   - The connector has separate Mac and Windows versions.
   - If the user's operating system is known, give only the matching instruction.
   - If the user's operating system is unknown, briefly mention both Mac and Windows instructions, or ask which system they use if choosing the wrong installer would be risky.
3. Mac connector behavior:
   - Tell Mac users to download and install the Mac version from the installation guide.
   - After installation, the connector runs in the background by default; the user generally does not need to manually manage it.
4. Windows connector behavior:
   - Tell Windows users to download the Windows version from the installation guide.
   - After installation/download, the user needs to double-click the `.exe` file to run the connector.
5. Onboarding response order:
   - First show the local image/GIF if available.
   - Then give the short installation instruction with the correct source and OS-specific connector note.
   - Finally attach the detailed installation guide link.

## Onboarding Flow

Use this flow before a user's first collection or whenever setup status is unclear.

### Lightweight intro response

Use this when the user asks what the skill is, what it can do, or how to use it in general, but has not explicitly asked to start setup/configuration.

- Briefly explain that Web Collection is a browser-extension data collection skill for Douyin, TikTok, Xiaohongshu, Amazon, and Bilibili.
- Mention what it can collect in the intro, using a compact platform list when helpful:
  - Douyin: video keyword search, creator search, video comments, video details.
  - TikTok: keyword search, user videos, comments, creator search.
  - Xiaohongshu: note keyword search, creator notes, note comments, note details.
  - Amazon: product keyword search, product details, product reviews.
  - Bilibili: video keyword search, video details, creator videos, comments.
- Mention that results can be exported to Feishu bitable or CSV.
- Provide the demo scenarios / example collection scenes link:
  `https://vcn5grhrq8y0.feishu.cn/wiki/GO11wlXkriSwNakXrt2ck0GanEe`
- End with this next-step prompt, and then stop:

```text
如果你要继续使用，我可以带你完成首次配置。你回复「继续配置」后，我会按步骤发操作指引、截图和配置文档。
```

Do not include install steps, bitable binding steps, connector credential steps, or screenshots in this intro response.

### First-time setup flow

Use this only after the user confirms setup/configuration, or when they explicitly ask for installation, binding, connector verification, or credential collection.

Do not repeat the "what this skill can do" platform/capability explanation in the setup flow. That content belongs only in the lightweight intro response. The setup flow starts directly with installing the browser extension and connector.

1. Guide browser extension and connector installation.
   - If `assets/install-extension-connector.*` exists, show it with a short instruction.
   - Tell the user to download the browser extension from the installation guide, not from the Chrome Web Store / Google Store.
   - Tell the user to install the connector version matching their operating system:
     - Mac: download and install the Mac connector. It runs in the background by default after installation.
     - Windows: download the Windows connector, then double-click the `.exe` file to run it.
   - Provide the detailed installation guide after the short instruction:
     `https://vcn5grhrq8y0.feishu.cn/wiki/R6f2w6o7ci1db1kYLK4cgJIYnWh`
   - Ask the user to finish installation and reply `我已装完`.
   - Do not ask for collection parameters or start collection before this confirmation.
2. Guide bitable configuration.
   - Show local screenshots inline or as attachments with the relevant steps when present. Resolve files from the bundled `assets/` directory.
   - Do not list all bitable screenshots first or place them all at the end. Pair text and image in this exact sequence:
     - Step text: Click the browser extension icon, enter `个人中心`, then log in to the media assistant account if the user is not already logged in.
       Image: `assets/bitable-step-00-personal-center.png`
     - Step text: Send the direct bitable template link: `https://vcn5grhrq8y0.feishu.cn/base/UKQsbVHpMac293s0cnFc1hq1nDd?table=tblTXM4lclXM6Jzr&view=vew8OdcKHw`. Tell the user to open that template link directly, choose `创建副本`, and make sure the copy is created in a bitable space. Tell the user to select `仅多维表格结构` when the copy dialog asks for the copy range.
       Image: `assets/bitable-step-01-template-copy.png`
     - Step text: In the newly copied bitable, click `多维表格插件`, choose `自定义插件`, click `获取授权码`, enable the authorization code, then copy it.
       Image: `assets/bitable-step-02-auth-code.png`
     - Step text: Go back to `媒讯助手`, open `配置中心` with the gear icon, expand the bitable configuration section, paste the newly copied bitable link and the personal authorization code, click `测试连接`, wait for `Connection successful` or green success text, then click `保存配置`.
       Image: `assets/bitable-step-03-config-save.png`
   - Ask the user to finish this step and reply `多维表格已绑定`.
   - When responding to the user, put the detailed guide link at the end of the message, after all operations and screenshots:
     `https://vcn5grhrq8y0.feishu.cn/wiki/EAtJw2irFiDvMpkZXb4cBjYonNg`
3. Guide connector authorization.
   - Do not ask the user to copy credentials by default.
   - When authorization is needed, run the normal collection entry point or `scripts/ensure_connector_auth.sh`; it will generate a website login confirmation link.
   - Tell the user: open the link, finish website login/authorization, then return to the Agent and retry/continue.
   - After confirmation, the connector/App writes `connector_token`, `ws_url`, and `device_id` into its own state. The Skill should reuse that state automatically.
   - Only use `assets/connector-step-01-status-token.png` as a manual fallback/troubleshooting overview, not as the primary Agent-led flow.
   - When responding to the user, put the detailed guide link at the end if they need the full connector UI reference:
     `https://vcn5grhrq8y0.feishu.cn/wiki/EAtJw2irFiDvMpkZXb4cBjYonNg`
4. Continue to first-run preferences.
   - Do not persist connector credentials manually unless the user explicitly provides them or an environment/runtime source already has them.
   - Then continue with the `First-run flow` below.
5. After collection succeeds, guide result viewing and further learning.
   - If bitable export succeeds and `export.tableUrl` exists, put the table link first and tell the user to open it to view results.
   - If CSV export is used, state that the result was exported as CSV.
   - Then point the user to the demo scenarios / knowledge base link for more platforms, scenarios, and advanced usage:
     `https://vcn5grhrq8y0.feishu.cn/wiki/GO11wlXkriSwNakXrt2ck0GanEe`

## Core Rules

1. Use the user's normal Chrome environment, not the isolated `openclaw` browser profile.
2. Prefer the Agent-led connector flow. Do not expose local/cloud mode choices to the user unless they explicitly ask for troubleshooting details.
3. Never ask for configuration that is already present in environment variables.
4. Connector credentials should be discovered from environment variables, stored preferences, connector/App state, or the website login confirmation callback.
5. When credentials are missing or expired, provide a website login confirmation link instead of asking the user to copy token values.
6. Default to synchronous closed-loop execution.
7. Do not reply before the collection script finishes.
8. Internally choose one execution mode first:
   - `cloud`: default; call the connector dispatch API and only run the cloud send-command script
   - `local`: troubleshooting/manual fallback; talk to the local bridge directly and only run the local send-command script
9. In `cloud` mode, do not rewrite the collection payload. Only wrap it in:
   - `device_id`
   - `action`
   - `payload`
10. For personal bitable export, do not send `personalSmart` from this skill. Send `personal` plus `deduplication.enabled=true`; the new plugin switches to its smart personal export internally.

## First-Time Setup

This skill uses one preferences file:

`$OPENCLAW_STATE_DIR/skill-state/web-collection/preferences.json`

Fallback:

`$HOME/.openclaw/skill-state/web-collection/preferences.json`

Helper script:

```bash
bash {baseDir}/scripts/export_preference.sh show
bash {baseDir}/scripts/export_preference.sh check
bash {baseDir}/scripts/export_preference.sh apply-recommended
bash {baseDir}/scripts/export_preference.sh set-key defaultConnectionMode cloud
bash {baseDir}/scripts/export_preference.sh set-key defaultExportMode csv
bash {baseDir}/scripts/export_preference.sh set-key defaultDeduplicationEnabled true
bash {baseDir}/scripts/export_preference.sh set-key defaultDeduplicationStrategy keepOld
```

Required defaults:

- `defaultExportMode`
- `defaultMaxItems`
- `defaultFetchDetail`
- `defaultDetailSpeed`

Optional defaults with built-in fallback:

- `defaultDeduplicationEnabled` defaults to `true`
- `defaultDeduplicationStrategy` defaults to `keepOld`

Connector authorization defaults:

- The cloud base URL is fixed to `https://i-sync.cn` by default.
- `defaultCloudDeviceId` and `defaultCloudToken` are optional manual overrides, not first-run questions.
- `run.sh` first tries environment variables, stored preferences, App state, and connector state.
- If no valid connector token is available, `run.sh` prints a website login confirmation link and stops with an authorization-required message.
- After the user confirms login in the browser, rerun/continue the collection; the Skill should reuse the newly written connector state.

### First-run flow

On first use:

1. Default to the Agent-led connector flow.
2. Do not ask for `defaultCloudDeviceId` or `defaultCloudToken`.
3. If connector authorization is missing, run the collection entry point and give the user the generated website login confirmation link.
4. Then handle the common defaults:
   - 导出方式
   - 默认采集条数
   - 是否默认采集详情
   - 默认采集速度
   - 是否开启导出去重
   - 去重保留策略
5. Ask only one question for the common defaults:
   - `推荐配置`
   - `自己配置`
6. If the user chooses `推荐配置`, run:

```bash
bash {baseDir}/scripts/export_preference.sh apply-recommended
```

7. If the user chooses `自己配置`, ask for all common values in one message, not one by one.
8. Only continue when the common defaults are complete. Connector authorization can be resolved automatically by the scripts.

Preferred cloud prompt:

```text
需要确认一次连接器授权。请打开下面这个登录确认链接，完成网站登录/授权后回到这里，我会继续执行采集：

<login_url>
```

Preferred quick-reply prompt for common defaults:

```text
常用配置还需要确认一次。
这些配置包括：
- 导出方式
- 默认采集条数
- 是否默认采集详情
- 默认采集速度
- 是否开启导出去重
- 去重保留策略
你可以直接用推荐配置，也可以自己配置。
[[quick_replies: 推荐配置, 自己配置]]
```

Preferred custom-config prompt:

```text
好，我们一次性把默认配置定好。请直接按下面格式回复：

导出方式：CSV / 多维表格
默认采集条数：10 / 20 / 50 / 100
是否默认采集详情：是 / 否
默认采集速度：fast / medium / slow
是否开启导出去重：是 / 否
去重保留策略：保留原始数据 / 保留新数据

说明：
- 多维表格：适合查看、筛选、分享
- CSV：适合本地保存
- 采集详情：开启后结果更完整，但一般更慢
- 采集速度：推荐 fast
- 导出去重：推荐开启
- 保留原始数据：重复数据保留第一次导入版本
```

Recommended defaults:

- 运行位置：`cloud`
- 导出方式：`多维表格`
- 采集条数：`20`
- 采集详情：`true`
- 采集速度：`fast`
- 导出去重：`true`
- 去重保留策略：`keepOld`（保留原始数据）

### Direct default config flow

Do not send Feishu cards for default configuration. When the user needs the recommended defaults, send the default values directly in plain text and apply them with the bundled preference helper.

Default values to send:

- 运行位置：`cloud`
- 导出方式：`多维表格`
- 采集条数：`20`
- 采集详情：`true`
- 采集速度：`fast`
- 导出去重：`true`
- 去重保留策略：`keepOld`（保留原始数据）

Recommended apply path:

```bash
bash {baseDir}/scripts/export_preference.sh apply-recommended
```

If the user wants to customize values, ask for the complete set in one message and then persist them through `scripts/export_preference.sh set-key`. Do not introduce a card callback server, interactive card form, or Feishu card delivery step for this configuration flow.

## Cloud Mode

Use `cloud` mode when the collection request should be sent to the platform backend first, and then dispatched to the user's connected local connector.

Cloud responsibilities:

- call `/api/v1/connector/cloud/dispatch`
- authenticate with `Authorization: Bearer <user_api_key>`
- include `device_id`
- keep the collection body unchanged inside `payload`
- enforce a strict cloud payload template before dispatch to avoid missing fields
  - default fallback when missing: `maxItems=20`, `mode=search`, `interval=300`, `fetchDetail=true`, `detailSpeed=fast`
- poll `/api/v1/connector/cloud/commands/{command_id}` for final status and result
- if single-command query is unavailable, fallback to `/api/v1/connector/cloud/commands?device_id=...`
- treat `result` + `task_updates` as the source of completion snapshot

Do not:

- call the user's local `19820` port from the cloud path
- rewrite `payload` semantics
- mix local admin token logic into cloud requests

## Filter Pass-through

Advanced filters, including time-based filtering, must be passed through via the request `filters` object.

Rules:

- Do not invent one universal time-filter schema in this skill.
- Do not rename or normalize platform-specific filter keys when the connector/plugin already expects a specific shape.
- When the user asks for time filtering, treat it as a `filters` payload question first, not as a standalone top-level argument.
- Prefer `--filters-json '<json-object>'` when calling `scripts/run.sh`; this becomes `payload.filters` in the final collect body.
- Different platforms and methods may require different filter keys or value formats. For example, one method may expect `startTime` and `endTime`, while another may only support keys such as `sortBy`, relative publish-time options, or other method-specific fields.
- If the exact filter shape is unclear, check `GET /api/filters` first, or the platform/method-scoped filter capability endpoint if available, before guessing.
- Keep local mode and cloud mode behavior identical for filters: the same `filters` object should be preserved inside `payload`.

Time-filter guidance:

- Time filtering is supported only through `filters`, not through a fixed top-level skill parameter such as `--time-range`.
- If the underlying method supports absolute time bounds, pass them inside `filters`, for example `startTime` / `endTime`.
- If the underlying method supports relative or semantic time filters instead, pass that method's native key/value shape unchanged.
- Treat published-time examples as method-specific examples, not as a stable cross-platform contract.

Examples:

```bash
bash {baseDir}/scripts/run.sh \
  --platform douyin \
  --method videoKeyword \
  --keyword "AI" \
  --filters-json '{"startTime":1717171200000,"endTime":1719763199000}' \
  --ensure-bridge
```

```bash
bash {baseDir}/scripts/run.sh \
  --platform amazon \
  --method productReview \
  --link "https://www.amazon.com/dp/B0..." \
  --filters-json '{"sortBy":"recent"}' \
  --ensure-bridge
```

## Connector Command Ladder

When collection fails, parameters look incomplete, or status is unclear, run connector checks in this order instead of guessing.

Layer 1: capability

- `GET /api/help`
- `GET /api/routes`
- `GET /api/filters` (or platform/method scoped)

Layer 2: diagnostics

- `GET /api/status`
- `GET /api/platform-state`
- `GET /api/cloud/status`
- `POST /api/preflight` with the final request body

Layer 3: execution and tracking

- `POST /api/collect`
- `GET /api/tasks/:id` (local mode)
- `GET /api/v1/connector/cloud/commands/{command_id}` (cloud mode, preferred)
- `GET /api/v1/connector/cloud/commands?device_id=...` (cloud fallback)
- `POST /api/stop` or `POST /api/reset` when stuck

Local command template (admin token required):

```bash
TOKEN="$(cat ~/.meixi-connector/bridge-admin-token.txt)"
curl -s -H "x-connector-admin-token: $TOKEN" "http://127.0.0.1:19820/api/status"
```

Cloud command template (async result):

```bash
curl -s -H "Authorization: Bearer <token_or_api_key>" \
  "https://i-sync.cn/api/v1/connector/cloud/commands/<command_id>"
```

## Export Behavior

- `bitable`
  - run with `--export-target bitable`
  - expect `export.tableUrl` on success
  - keep the public connector mode as `personal`
  - default payload includes `export.deduplication.enabled=true` and `strategy=keepOld`
  - this intentionally triggers the new plugin's internal smart personal export path
- `csv`
  - run with `--export-target csv`
  - do not require a table link in the final reply
  - do not attach deduplication settings

Deduplication fields are owned by the connector/plugin. Do not ask the user to choose a field and do not pass a field from this skill.

### Smart Export Conversation Rule

For `bitable` export, this skill must treat personal export as a smart-export conversation, not as a plain success-or-fail step.

If collection succeeded but export failed:

- do not present the result as a full task failure first
- explicitly say collection completed and the failure happened while exporting to the original bitable table
- explain the likely causes in user-facing language
- then ask the user to choose one recovery path:
  - `新建表继续导出`
  - `导出为CSV`

Recommended failure explanation:

```text
采集已经完成，失败发生在导出到原多维表格这一步。

原表导出失败通常有几种原因：
- 原目标表不存在
- 原目标表字段结构与本次数据不一致
- 导出服务临时异常

为了避免这次结果丢失，我现在可以继续帮你导出。你可以选择：

- 新建表继续导出：在当前多维表格中创建一个新的数据表后继续导出
- 导出为CSV：直接把这次结果保存成 CSV 文件

[[quick_replies: 新建表继续导出, 导出为CSV]]
```

If the user chooses `导出为CSV`, switch the follow-up run to CSV export.

If the user chooses `新建表继续导出` or `导出为CSV` after a failed export and the previous result includes a connector `taskId`, do not start a new collection. Re-export from the cached task records:

```bash
bash {baseDir}/scripts/reexport_task.sh --task-id "<taskId>" --export-target csv
```

```bash
bash {baseDir}/scripts/reexport_task.sh --task-id "<taskId>" --export-target bitable --new-table
```

This uses `POST /api/tasks/:id/export` and must be described as reusing the previous task's cached records. If no task id is available, be honest that the skill cannot guarantee a no-recollect retry.

Expected bitable connector payload shape:

```json
{
  "autoExport": true,
  "exportMode": "personal",
  "export": {
    "enabled": true,
    "mode": "personal",
    "deduplication": {
      "enabled": true,
      "strategy": "keepOld"
    }
  }
}
```

Do not use this shape:

```json
{
  "exportMode": "personalSmart"
}
```

## Entry Point

Preferred wrapper:

```bash
bash {baseDir}/scripts/run.sh ...
```

The wrapper:

- runs `scripts/preflight_check.sh` first
- applies stored preferences
- enforces required setup
- defaults to cloud dispatch mode when no mode is specified
- cloud mode dispatches only through `scripts/cloud_dispatch_loop.sh`
- local mode dispatches only through `scripts/collect_and_export_loop.sh`
- never mixes the local and cloud send-command scripts

## Bundled Resources

- `scripts/preflight_check.sh`
  - validates required defaults before dispatch
  - treats environment-variable configuration as already satisfied and never asks for it
- `scripts/ensure_connector_auth.sh`
  - resolves connector authorization before dispatch
  - reads explicit values, App state, connector state, or generates a website login confirmation link when authorization is missing
- `scripts/run.sh`
  - chooses exactly one dispatch path based on `connection-mode`
  - calls `scripts/ensure_connector_auth.sh` before cloud dispatch
  - never mixes local and cloud send-command scripts
- `scripts/collect_and_export_loop.sh`
  - local-only send-command script
- `scripts/cloud_dispatch_loop.sh`
  - cloud-only send-command script
- `scripts/reexport_task.sh`
  - re-exports cached records from a previous connector task id
  - never starts a new collection
- `scripts/export_preference.sh`
  - stores reusable defaults and masks cloud token in human-readable output
- `references/learning-guide.md`
  - compact guidance for complex requests and asking rules

## Common Commands

Douyin keyword search:

```bash
bash {baseDir}/scripts/run.sh \
  --platform douyin \
  --keyword "AI" \
  --ensure-bridge
```

Douyin keyword search via cloud dispatch:

```bash
bash {baseDir}/scripts/run.sh \
  --connection-mode cloud \
  --cloud-device-id desktop-local-smoke-fix \
  --cloud-token '<user_api_key>' \
  --platform douyin \
  --keyword "AI员工"
```

Amazon keyword search:

```bash
bash {baseDir}/scripts/run.sh \
  --platform amazon \
  --keyword "Chinese porcelain" \
  --ensure-bridge
```

Bilibili keyword search:

```bash
bash {baseDir}/scripts/run.sh \
  --platform bilibili \
  --keyword "古董" \
  --ensure-bridge
```

## Platform Defaults

Wrapper defaults:

- `douyin` => `videoKeyword`
- `tiktok` => `keywordSearch`
- `xiaohongshu` => `keywordSearch`
- `amazon` => `keywordSearch`
- `bilibili` => `keywordSearch`

Supported methods:

- `douyin`: `videoKeyword`, `creatorKeyword`, `creatorLink`, `creatorVideo`, `videoComment`, `videoInfo`, `videoLink`
- `tiktok`: `keywordSearch`, `userVideo`, `tiktokComment`, `tiktokCreatorKeyword`, `tiktokCreatorLink`
- `xiaohongshu`: `keywordSearch`, `creatorNote`, `creatorLink`, `creatorKeyword`, `noteLink`, `noteComment`
- `amazon`: `keywordSearch`, `productLink`, `productReview`
- `bilibili`: `keywordSearch`, `videoInfo`, `creatorVideo`, `bilibiliComment`

## Closed Loop

`local` mode:

1. verify `pluginConnected=true`
2. wait for idle state
3. start `/api/collect`
4. handle `TASK_RUNNING` via `stop -> wait idle -> retry`
5. poll `/api/tasks/<taskId>` until `completed` or `error`
6. if export is required, verify the expected export result

`cloud` mode:

1. query `/api/v1/connector/cloud/status?device_id=...`
2. dispatch `action=collect` to `/api/v1/connector/cloud/dispatch`
3. keep querying command result (`/api/v1/connector/cloud/commands/{command_id}` preferred)
4. after each poll, refresh current collection state from command status
5. wait for `completed` or terminal error state
6. on completion, read `result` and `task_updates` for records/count/export snapshot and include key fields in the final reply

Quick query examples:

```bash
curl -H "Authorization: Bearer <token_or_api_key>" \
  "https://i-sync.cn/api/v1/connector/cloud/commands?device_id=<device_id>"
```

```bash
curl -H "Authorization: Bearer <token_or_api_key>" \
  "https://i-sync.cn/api/v1/connector/cloud/commands/<command_id>"
```

## Final Reply

When successful:

1. Mention whether the run used `local` or `cloud` mode.
2. If `cloud` mode was used, include the command status.
3. If export mode is `bitable` and `export.tableUrl` exists, include the table link first.
4. If export mode is `csv`, explicitly say export mode is CSV.
5. Then include:
   - status
   - export status
   - collected count
   - short analysis

When `bitable` export is expected but no table link exists, explicitly say export did not finish correctly.

## Troubleshooting

- `pluginConnected=false`
  - Chrome/plugin is not connected to the bridge
- bridge/status mismatch
  - in `local` mode, ensure collect, status, and stop all use the same local base URL
- connector authorization is missing or expired
  - rerun the collection entry point and open the generated website login confirmation link
- cloud dispatch could not reach the connector
  - confirm the connector/App is running and the website login confirmation was completed
- `TASK_RUNNING`
  - use stop + retry, or `--force-stop-before-start`
- long record output hiding key fields
  - trust the connector loop's compact summary output rather than raw task JSON
