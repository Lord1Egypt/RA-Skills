---
name: openclaw-vmake-ai
description: "Process image or video watermark removal and quality restoration with Vmake AI. Always discover the remote catalog before naming or selecting a task: V2 uses the returned server task metadata; legacy aliases are allowed only when the legacy config explicitly returns them. Video tasks use spawn-run-task plus OpenClaw sessions_spawn; image tasks use blocking run-task. Paid API (consumes tenant quota); never claim the service is free or invent pricing."
metadata: {"openclaw":{"emoji":"🖼️","requires":{"bins":["python3"],"env":{"MT_AK":{"required":true},"MT_SK":{"required":true}}},"tags":["image-processing","watermark-removal","image-restoration","vmake","paid-api"]}}
---

# Vmake Skill

## When to Use This Skill

Activate when the user wants any of the following:

- **Watermark removal** on images or video (remove watermark, eraser watermark, etc.)
- **Image quality restoration** (restore, upscale, enhance, super-resolution)
- **Video quality restoration** (video restore, upscale, hdvideo-style enhancement)

## Billing and user-facing claims (MANDATORY)

- **Fact:** Each successful **`run-task`** (including inside a **`sessions_spawn`** worker) goes through server-side **quota / credit consumption** for the **MT_AK** tenant. This is a **paid, metered commercial API**, not free compute bundled with the skill or the host.
- **Forbidden:** Do **not** state or imply that the service is **free**, costs nothing, uses **no quota**, has **unlimited trial**, or similar. Do **not** invent **prices**, **plan names**, **promotions**, or **trial rules**.
- **Allowed:** Neutral wording — e.g. processing **uses the Vmake account quota** tied to the configured keys; **billing and plans** are **per your console or administrator**. If the user asks about cost, point them to **admin / official billing docs / console**; do not guess. When the API returns quota or membership errors, follow **Step 3 — MANDATORY (quota / consume failures)** using server **`detail`** and **`pricing_url`** when present.
- **On success too:** Success summaries must stay factual (task completed, delivery). Do **not** add “free” or zero-cost implications.

## Execution authorization and attachment reuse (MANDATORY)

- A media attachment already present in the conversation is the current input. Do not ask the user to upload it again, restate its media type, or provide its file location when that information is already available.
- Before the first upload to Vmake, quota consumption, or task submission, ask for one concise authorization that covers both uploading the current media and using the configured Vmake account quota.
- If the user's current request already explicitly authorizes both the upload and quota use, treat that as authorization and do not ask again.
- After the user authorizes the operation, immediately reuse the current attachment and continue through input resolution, upload, quota consumption, task submission, polling, and delivery. Do not ask for another confirmation merely because execution continues in another turn or worker session.
- Refer to chat media as “received” before authorization. Do not say that the media “has not been uploaded” without clarifying that it has not yet been sent to Vmake.
- Ask for the media again only when the attachment is genuinely unavailable to the execution environment.
- Authorization applies to the current media and selected single task. For a multi-stage pipeline, disclose the number of quota-consuming stages and request authorization for the complete pipeline.

## Agent metadata (v2)

For `catalog`, `run-task`, and `spawn-run-task`, make a best effort to provide `--agent-name`, `--agent-version`, and `--agent-model` from information you actually know about your own runtime. The name is the host (e.g. `codex`, `claude-code`, `openclaw`); version is the host software version, not the skill version. Use only explicit self/runtime information: never guess, fabricate, derive a host from its model, or probe for unavailable details. If a value is not known with confidence, omit it.

Explicit arguments override `SKILL_AGENT_NAME`, `SKILL_AGENT_VERSION`, `SKILL_AGENT_MODEL`; an explicit empty value suppresses that field. Metadata is optional and sent only to WAPI as `X-Agent-Name`, `X-Agent-Version`, `X-Agent-Model` before signing. The server stores it for effective v2 consume records. `spawn-run-task` preserves the caller's metadata in its worker command; the model field describes the initiating caller, not a discovered worker model.

## Capabilities and remote task discovery

The local skill defines capabilities, not authoritative executable IDs:

| Capability | Input |
|---|---|
| Watermark / subtitle removal | Image or video |
| Quality restoration / enhancement | Image or video |

Before naming a task to the user, asking for execution authorization, uploading media, or building a worker, run the read-only catalog command:

```bash
python3 {baseDir}/scripts/vmake_ai.py install-deps
python3 {baseDir}/scripts/vmake_ai.py catalog [--media-type image|video]
```

`catalog` only calls `/skill/config.json`; it does not upload media, call `/skill/consume.json`, or submit an algorithm task.

### Dual-stack selection (MANDATORY)

1. **V2 first:** When `config_mode` is `v2`, use the returned `description`, `name`, and `media_type` to select the task, then pass that entry's exact returned `material_id` as the CLI `--task` value. Never invent or substitute a local/legacy algorithm name. A unique display `name` remains accepted only for backward compatibility; use `material_id` for new calls so duplicate names remain unambiguous.
2. **Legacy compatibility:** When `config_mode` is `legacy`, an alias such as `videoscreenclear` may be used only if that exact alias appears in the command's returned `tasks`. Absence means unavailable; local documentation or memory is not evidence.
3. **Failure stops the flow:** If catalog exits non-zero, returns `config_unavailable`, `config_catalog_empty`, or has no matching tasks, tell the user that no matching Vmake task is currently available, then stop. Include any server notice messages in that reply. If those notices provide no next step, advise the user to contact Vmake official support without inventing a support URL or contact method. Do not infer a local task, request media for execution, upload, consume quota, or submit an algorithm job.
4. **Execution revalidates:** `run-task` and `spawn-run-task` fetch config again and reject tasks not advertised by that response before upload or consume.

For a V2 task selection, present the returned display fields localized to the conversation language. For example:

```text
Task: Subtitle
- Capability: Video subtitle removal
- Input type: Video
```

### Video tasks — default execution

For a selected V2 entry with `media_type: "video"`, or a server-confirmed legacy video alias: **`spawn-run-task`** → pass **`sessions_spawn_args`** to **`sessions_spawn`** (main session does not block on **`run-task`**). Command shape, **`runTimeoutSeconds`** (default **3600**), polling and recovery: **[§3b](#3b--async-worker-sessions_spawn-video-tasks)** and **[docs/errors-and-polling.md](docs/errors-and-polling.md)**.

---

## Multi-stage pipelines (chaining tasks)

When the user asks for **more than one** Vmake step on the **same** media (e.g. remove watermark **then** restore quality), treat each step as a **separate job**:

| Typical chain | Stages |
|---|---|
| Image | catalog-selected watermark task name → catalog-selected restoration task name |
| Video | catalog-selected watermark task name → catalog-selected restoration task name |

**Rules:**

1. After stage A completes with `skill_status: "completed"`, use **`primary_result_url`** or **`output_urls[0]`** as **`--input`** for stage B with a **new** `--task`. That is a **new** job, not a retry of stage A. For **video**, stage B means a **new** **`spawn-run-task`** + **`sessions_spawn`** (each spawn embeds a **single** `run-task`), not a second `run-task` inside the same embed.
2. **“Do not re-run `run-task`”** in this skill means: **do not submit `run-task` again for the same `task_id` / the same submitted job** (use `query-task` to resume polling instead). It does **not** forbid the **next pipeline stage** with a different catalog-selected task name (or confirmed legacy alias) and the previous result URL as input.
3. **Step 4 (delivery):** Prefer **final-stage** native delivery when the user wanted the full pipeline; intermediate stages may still run embedded Step 4 per worker (one spawn per video stage) — tune the user-facing copy if they only care about the last asset.
4. **Video chains (medeo-style):** **One `sessions_spawn` = one embedded `run-task`.** Do **not** put two `run-task` calls in one spawn. Chain = **multiple spawns**: after stage A, read **`primary_result_url`** from stdout or **`last-task`** / **`history`**, then **`spawn-run-task`** for stage B with that URL as **`--input`**. No video **`run-task`** in the main session. Optional one-line user update before the second spawn.

See also Step 3 success bullets and **`agent_instruction`** in the JSON.

---

## API submission path (MANDATORY)

- **Discovery:** Fetch task choices only via **`python3 {baseDir}/scripts/vmake_ai.py catalog …`**. Production WAPI is `wapi-skill.vmake.ai`. Do not hand-craft config HTTP.
- **New jobs:** Submit **only** via **`python3 {baseDir}/scripts/vmake_ai.py run-task …`** (§3a / §3b), or the **same** `run-task` command embedded in **`spawn-run-task`** → `sessions_spawn`. **Do not** hand-craft HTTP to WAPI or AIGC / invoke endpoints to replace that flow — that skips **`POST /skill/consume.json`** (quota and permission) and breaks the supported pipeline.
- **Exception:** **`query-task --task-id`** is **only** for resuming status polling on an **existing** full `task_id` (no upload, no second consume). **Do not** use it instead of **`run-task`** for a **new** submission.
- **No curl replay:** This skill does not emit debug curl for API calls. **Do not** hand-craft HTTP to **wapi / AIGC** to mimic requests — always use the **CLI** above so **`/skill/consume.json`** runs before algorithm submit.

---

## 0. Pre-Flight Check (MANDATORY — run before anything else)

Verify AK/SK are configured (**only run this command**; do not read other Python sources first):

```bash
python3 {baseDir}/scripts/vmake_ai.py preflight
```

- Output `ok` → continue to Step 1
- Output `missing` → **stop** and send the user the configuration message below

**Feishu** — send an interactive card via the Feishu API (do not use the `message` tool for this):

```python
import json, urllib.request
cfg = json.loads(open("/home/ec2-user/.openclaw/openclaw.json").read())
feishu = cfg["channels"]["feishu"]["accounts"]["default"]
token = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    data=json.dumps({"app_id": feishu["appId"], "app_secret": feishu["appSecret"]}).encode(),
    headers={"Content-Type": "application/json"}
)).read())["tenant_access_token"]
card = {
    "config": {"wide_screen_mode": True},
    "header": {"title": {"tag": "plain_text", "content": "🖼️ Vmake — credentials required"}, "template": "blue"},
    "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": "1. Apply for **Access Key** and **Secret Key** at [Vmake Developers — API Key](https://vmake.ai/developers#api-key).\n2. Set **MT_AK** and **MT_SK** in `scripts/.env` (see `scripts/.env.example`), then reload env:\n```\nsource scripts/.env\n```\nIf keys are issued by your organization, ask your administrator."}}],
}
urllib.request.urlopen(urllib.request.Request(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    data=json.dumps({"receive_id": "<USER_OPEN_ID>", "msg_type": "interactive", "content": json.dumps(card)}).encode(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
))
```

**Telegram / Discord / other channels** — use the `message` tool with plain text:

```
🖼️ Vmake — credentials required

1. Get Access Key and Secret Key (apply here if needed):
   https://vmake.ai/developers#api-key

2. Set MT_AK and MT_SK in scripts/.env (see scripts/.env.example), then run:
   source scripts/.env

If keys are issued by your organization, ask your administrator.
```

---

## Step 1 — Discover task and resolve the current input

1. Run `install-deps`, then `catalog`. If the user or attachment already establishes the modality, filter with `--media-type image` or `--media-type video`; otherwise fetch all entries and ask one short image-or-video question.
2. In V2 mode, match the request against the server's `description`, `name`, and `media_type`, then pass the selected entry's exact returned `material_id` as `--task`. In user-visible replies, show the task `name`, capability `description`, and localized input type; do not show `material_id` unless debugging requires it. Do not invent or supplement missing catalog descriptions locally.
3. In legacy mode, map the request to a legacy alias only after confirming that exact alias appears in catalog output. Never report or execute a local legacy name before this confirmation.
4. Resolve the current input from the existing attachment, path, or URL. Infer the media type from attachment metadata or the file extension when available. Do not ask the user to repeat either one. Video extensions include `.mp4`, `.mov`, `.webm`, `.mkv`, `.m4v`; common static image extensions include `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`.
5. **Video plus preview/cover:** when one message includes a video and a sibling still, process only the video for a clip-targeted request. The cover is a delivery helper, not a second Vmake job, unless the user explicitly asks to process it.
6. **Unsupported media URL:** if `run-task` returns `error: "input_unavailable"` from `consume`, ask the user to upload the image or video file directly and do not retry the same URL. Suggested reply: `This media URL is currently unavailable. Please upload the image or video file directly.`

**Getting media from IM messages** (full detail: [docs/im-attachments.md](docs/im-attachments.md)):

| Platform | How to obtain |
|---|---|
| Feishu | Message resource URL / `image_key` + `message_id` → optional **`resolve-input`** |
| Telegram | `file_id` → **`resolve-input --telegram-file-id`** (needs `TELEGRAM_BOT_TOKEN`) |
| Discord | `attachments[0].url` — often usable directly as `--input` |
| Generic | URL or path |

```bash
python3 {baseDir}/scripts/vmake_ai.py resolve-input --file /tmp/saved.jpg --output-dir /tmp
# or: --url, --telegram-file-id, --feishu-image-key + --feishu-message-id
```

Use the JSON **`path`** field as **`--input`**.

**`--input` as `http(s)://` URL:** In shells, **quote the whole URL** so `&` in query strings (e.g. signed OSS links) is not split. Large or slow downloads: defaults are **120s read timeout** and **100MB** max (same as `resolve-input --url`); override with **`MT_AI_URL_READ_TIMEOUT`**, **`MT_AI_URL_CONNECT_TIMEOUT`**, **`MT_AI_URL_MAX_BYTES`**. For very large video or flaky links, prefer **`resolve-input --url`** then **`--input`** with the local **`path`**.

If the user already supplied an attachment, path, or URL, retain it as the current input. After execution authorization is granted, proceed automatically without asking for the media or its type again.

When authorization is still required, ask only one concise question, for example:

> "I've received the video. May I upload it to Vmake AI and use your account quota for quality restoration?"

After authorization, continue immediately and acknowledge execution without another question, for example:

> "Authorization received. Uploading and processing the video now."

---

## Step 2 — Confirm dependencies

```bash
python3 {baseDir}/scripts/vmake_ai.py install-deps
```

This is normally already completed before `catalog`; the command is idempotent. Then continue to Step 3.

---

## Step 3 — Run the task

Use the selected catalog entry's modality. `media_type: "video"` uses only **[§3b](#3b--async-worker-sessions_spawn-video-tasks)** (`spawn-run-task` + `sessions_spawn`); `media_type: "image"` uses only §3a. In legacy mode, use the known modality only after the alias was returned by catalog.

### 3a — Inline (blocking, image tasks only)

Use for the V2 entry selected with `media_type: "image"`, or a server-confirmed legacy image alias.

```bash
python3 {baseDir}/scripts/vmake_ai.py run-task \
  --task "<catalog_material_id_or_confirmed_legacy_alias>" \
  --input "<image_url_or_path>"
```

Replace the placeholders with the catalog-selected ID and real input.

Default params include `rsp_media_type: url`. For custom JSON params:

```bash
python3 {baseDir}/scripts/vmake_ai.py run-task \
  --task "<catalog_material_id_or_confirmed_legacy_alias>" \
  --input "<url_or_path>" \
  --params '{"parameter":{"rsp_media_type":"url"}}'
```

When remote config includes an input profile, use it as the default; when the
field is omitted, do not synthesize one. Use `--profile '<json-object>'` only
when an explicit per-run override is required; it is deep-merged over the
server-provided profile in the same way as `--params`.

**When `run-task` exits 0**, stdout is JSON that includes:

- **`skill_status`: `"completed"`** — the algorithm and polling are finished; the result is in this response. If the user asked for **only this** stage, **proceed to Step 4**. If they asked for a **multi-stage pipeline**, use **`primary_result_url`** as `--input` for the **next** `--task` (see **Multi-stage pipelines** above); **Step 4 after the last stage**. **Do not** re-submit `run-task` for the **same `task_id`** (same job); use `query-task` to resume polling if needed.
- **`output_urls`** — ordered `http(s)` links (same extraction as before: `data.result.urls`, `images`, `media_info_list`, etc.).
- **`primary_result_url`** — same as `output_urls[0]` when present; convenient for delivery scripts.
- **`task_id`** — full task id as a top-level string when known (from `data.result.id` or the polling session). Keep it for manual status recovery or support handoff; do not truncate. Some synchronous completions may omit it if the API does not return an id.
- **`agent_instruction`** — short reminder for the model.
- **`notices`** — optional server-controlled user notices collected from config, consume, and task responses. Each usable notice contains a non-empty **`message`**; fields such as **`code`**, **`level`**, **`dedupe_key`**, and **`action_url`** are metadata and may be extended by the server.
- **`meta` / `data`** — full API payload for debugging.

**MANDATORY (server notices):** When stdout JSON contains **`notices`**, include every non-empty notice **`message`** in the user-facing reply. Unknown notice codes must still be shown. A **warning** notice does not change a completed task into a failure. An **error** notice follows the accompanying **`skill_status`** / **`api_code`**; do not infer failure from notice level alone. Do not repeat notices with the same **`dedupe_key`** in one reply. When **`action_url`** is present, surface it as a clickable link. This overseas Skill expects the server-provided **`message`** to be English; show it as provided and do not translate it automatically. Locale selection belongs to the server.

**MANDATORY (user-visible outcome):** When stdout JSON has **`skill_status`: `"completed"`** (from **`run-task`** or **`query-task`**), you **must** (1) send the user a **short natural-language summary** (success + what was done), and (2) **complete Step 4** on their channel (delivery scripts below) using **`primary_result_url`** or **`output_urls[0]`**, unless the user explicitly asked **only** for the URL with no IM delivery. **Do not** end the turn with only raw JSON in the tool transcript — the user should see a normal reply and the media or link in the chat.

**When `run-task` exits non-zero**, stdout is JSON with **`skill_status`: `"failed"`** (or an `error` field) — explain it to the user; do not treat as success or Step 4 delivery.

**MANDATORY (quota / consume failures):** When stdout JSON has **`failure_stage`: `"consume_quota"`** and **`error`** is **`credit_required`** (typically **`api_code` 60002**): you **must** send the user a **clear, user-visible** message grounded in the server **`detail`** (API `msg`). If the JSON includes **`pricing_url`** (extracted from that message when it contains an `https` link), **must** include it as a **clickable link**; if **`pricing_url`** is absent, **must** quote or paste the full **`detail`** so any links or instructions from the API still reach the user. **Do not** only dump raw JSON; **do not** retry **`run-task`** expecting success from tweaking **`--task`** / **`--params`** alone. When **`error`** is **`membership_required`** (**60001**): same rule (**`pricing_url`** when present, else full **`detail`**). When **`error`** is **`consume_denied`**: follow every server notice message and action link even when its notice code is unknown; do not reinterpret it as a parameter error or retry unchanged. When **`error`** is **`consume_param_error`**: treat as **parameter / invocation** mistakes — fix **`--task`**, **`--input`**, **`--params`** per SKILL and remote config; **do not** tell the user to recharge.

**Video tasks** use **§3b** in the main session. Polling, stderr, **`MT_AI_*`**, timeouts, SIGKILL / host caps, **`query-task`** / **`last-task`** recovery: **[docs/errors-and-polling.md](docs/errors-and-polling.md)** and **§3c–§3d**. Optional: raise host tool/session wait limits — does not replace **§3b** for video.

### 3b — Async worker (`sessions_spawn`, video tasks)

**Forbidden:** Do not call `spawn-run-task` unless catalog confirms a V2 entry with `media_type: "video"`, or returns the selected legacy video alias. Image tasks use §3a only.

Same pattern as **medeo-video** `spawn-task`: the main agent does not block on polling; a sub-session runs `run-task` and is told exactly how to detect success and deliver.

1. Build the payload with the catalog-selected ID:

```bash
python3 {baseDir}/scripts/vmake_ai.py spawn-run-task \
  --task "<catalog_material_id_or_confirmed_legacy_alias>" \
  --input "<video_url_or_path>" \
  --deliver-to "<oc_xxx_or_ou_xxx_or_chat_id>" \
  --deliver-channel "feishu"
```

Optional: `--params '<json>'`, `--profile '<json-object>'` (same as `run-task`), `--deliver-channel telegram|discord|...`, `--run-timeout-seconds` (default **3600**, aligned with extended poll budget). **Do not reduce** `runTimeoutSeconds` below the payload default unless you accept timeout risk — wall time varies (often minutes to tens of minutes).

2. Call OpenClaw **`sessions_spawn`** with the printed **`sessions_spawn_args`** (`task`, `label`, `runTimeoutSeconds`) **without reducing** `runTimeoutSeconds` unless you intentionally accept timeout risk.

3. **Reply immediately** to the user that processing has started (same as Step 1 acknowledgment). The sub-agent completes **`install-deps`** (if needed), **`run-task`**, then Step 4 using **`skill_status` / `output_urls`** per the embedded task text. For **video** tasks on Feishu/Telegram, the payload instructs **`feishu_send_video.py`** / **`telegram_send_video.py`** after `curl` download.

**Multi-stage + spawn:** One embed = one **`run-task`** (medeo-style). Video chains: **Multi-stage pipelines** (rule 4). Image chains: **§3a** only — run **`run-task`** once per stage in the main session (or host-equivalent blocking shell); **do not** use **`spawn-run-task`** for image stages.

### 3c — Resume polling (`query-task`)

When you already have a **full `task_id`** (from a previous stdout JSON, e.g. success, `poll_timeout`, or `poll_aborted`, or from stderr `task_id=...` lines) and the job may still be running on the server — **do not run `run-task` again** for that id; resume polling only:

```bash
python3 {baseDir}/scripts/vmake_ai.py query-task \
  --task-id "<full_task_id>"
```

Optional **`--task`** sets the `task_name` field in the success JSON for your logs (default labels as `query_task`). Uses the same **`MT_AK` / `MT_SK`** and remote config as the original submit. **Stdout JSON and exit codes** match **`run-task`**: exit **0** with `skill_status: "completed"` when the task finishes successfully; exit **non-zero** with `skill_status: "failed"` / `error` on timeout, query errors, or API-reported failure.

### 3d — Last task and history (user-visible)

Local state under **`~/.openclaw/workspace/openclaw-vmake-ai/`** (`last_task.json`, `history/task_*.json`, last **50** records). For async **`run-task`**, **`last_task.json`** may briefly show **`skill_status`: `"polling"`** with **`task_id`** while the client is still polling (checkpoint so **`query-task`** can resume if the process is killed mid-poll):

```bash
python3 {baseDir}/scripts/vmake_ai.py last-task
python3 {baseDir}/scripts/vmake_ai.py history
```

Use when the user asks whether a recent job finished, or for a short history summary. Do not expose raw secrets.

---

## Step 4 — Deliver result to the channel

**Required after success:** When **`skill_status`** is **`completed`**, deliver here — the CLI does not post to IM by itself. Send the processed image or video back on the user’s platform (and keep the Step 3 **MANDATORY** summary in the same turn).

### Resolve deliver-to target

| Platform | Source | Format |
|---|---|---|
| Feishu group | `conversation_label` or `chat_id` without `chat:` prefix | `oc_xxx` |
| Feishu DM | `sender_id` without `user:` prefix | `ou_xxx` |
| Telegram | Inbound message `chat_id` | e.g. `-1001234567890` |
| Discord | `channel_id` | e.g. `123456789` |

### Feishu — image tasks

```bash
python3 {baseDir}/scripts/feishu_send_image.py \
  --image "<result_url>" \
  --to "<oc_xxx or ou_xxx>"
```

### Feishu — video tasks

```bash
curl -sL -o /tmp/vmake_result.mp4 "<primary_result_url_or_output_urls[0]>"
python3 {baseDir}/scripts/feishu_send_video.py \
  --video /tmp/vmake_result.mp4 \
  --to "<oc_xxx or ou_xxx>" \
  --video-url "<primary_result_url_or_output_urls[0]>" \
  [--cover-url "<optional_thumb_url>"] \
  [--duration <milliseconds_if_known>]
```

`--video-url` adds a second message with the download link. Optional cover/duration; details: [docs/feishu-send-video.md](docs/feishu-send-video.md).

### Telegram — image tasks

```bash
TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" python3 {baseDir}/scripts/telegram_send_image.py \
  --image "<result_url>" \
  --to "<chat_id>" \
  --caption "✅ Done"
```

### Telegram — video tasks

```bash
curl -sL -o /tmp/vmake_result.mp4 "<primary_result_url_or_output_urls[0]>"
TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" python3 {baseDir}/scripts/telegram_send_video.py \
  --video /tmp/vmake_result.mp4 \
  --to "<chat_id>" \
  --video-url "<primary_result_url_or_output_urls[0]>" \
  [--cover-url "<optional_thumb_url>"] \
  [--duration <seconds>] \
  --caption "✅ Done"
```

`--video-url` sends a follow-up text message with the download link. Max ~**50 MB** for Bot API video; larger files rely on the link line.

### Discord

Download the result, then send with the `message` tool (use **`.mp4`** for video, **`.jpg`** / **`.png`** for image):

```bash
curl -L "<result_url>" -o /tmp/result_image.jpg
```

Then:

```
message(action="send", channel="discord", target="<channel_id>", filePath="/tmp/result_image.jpg")
```

For files over ~25MB, send the result URL as a link instead.

### WhatsApp / Signal / others

Use the `message` tool with `media`, or send the result URL directly.

---

## Quick commands reference (agent)

| Command | Description | User-facing? |
|---------|-------------|--------------|
| `preflight` | AK/SK ok / missing | No |
| `install-deps` | pip install requirements | No |
| `catalog` | Fetch remote V2 catalog or legacy invoke aliases; no upload/consume | Yes — task discovery |
| `run-task` | Submit + poll until done | Indirectly |
| `query-task` | Resume poll by `task_id` | When recovering |
| `spawn-run-task` | Validate a remote-catalog video task and print `sessions_spawn` payload | No |
| `resolve-input` | IM/URL → local path for `--input` | No |
| `last-task` | Last job JSON | Yes — “last job?” |
| `history` | Up to 50 recent records | Yes — “history?” |

---

## Notes

- **Single business entrypoint**: catalog discovery, algorithm runs, and config fetch go through `vmake_ai.py`; agents do not need to open `client.py` / `ai/api.py`. **Must not** bypass this with direct HTTP to AIGC/WAPI — see **[API submission path (MANDATORY)](#api-submission-path-mandatory)** above. **`query-task`** is the supported way to resume polling when a **`task_id`** is already known.
- **Video tasks**: **`spawn-run-task` + `sessions_spawn`** in the main session (mandatory path); the worker runs **`run-task`** and delivery. **`run-task`** in the **main** session is for **image** tasks (§3a) and for **recovery** (`query-task`). Polling and env tuning: [docs/errors-and-polling.md](docs/errors-and-polling.md).
- **AK/SK loading**: environment variables `MT_AK` / `MT_SK` first; if unset, `scripts/.env` is read automatically (same as `SkillClient`).
- **Config is authoritative**: `catalog`, `run-task`, and `spawn-run-task` pull remote config. V2 catalog output exposes each entry's `material_id` alongside its display fields; pass that exact ID to `--task`. Legacy aliases are accepted only when the response explicitly contains them. Config failure stops new jobs before upload or consume.
- **Bot token safety**: pass `TELEGRAM_BOT_TOKEN` and similar only via environment variables — never as CLI arguments.
- **On failure**: stdout JSON has `skill_status: "failed"` / `error`, **exit code ≠ 0** — explain to the user; check AK/SK, network, quotas; timeouts / SIGKILL / no final JSON: **[docs/errors-and-polling.md](docs/errors-and-polling.md)**. URL input errors may mention **HTTP 403** (expired signed URL) or **timeout** — see **`MT_AI_URL_*`** env vars above.
- **More docs**: [README.md](README.md), [docs/multi-platform.md](docs/multi-platform.md), [docs/im-attachments.md](docs/im-attachments.md), [docs/feishu-send-video.md](docs/feishu-send-video.md).
