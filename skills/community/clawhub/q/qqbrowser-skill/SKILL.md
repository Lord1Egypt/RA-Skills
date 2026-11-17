---
name: qqbrowser-use
description: "Browser automation CLI for AI agents. Use when: (1) open, navigate, or interact with a website (fill forms, click, screenshot, download, inspect); (2) extract structured data; (3) analyze already-open tabs without a new tab; (4) record, save, or reuse a browser task (保存为脚本, 录一下, 下次还要用); (5) run an existing playbook. Fallback when web_fetch hits captcha (wappoc)/login/empty SPA. Do NOT use for HTML/CSS/JS questions without a browser task, or bookmarks/history."
source: https://pypi.org/project/qqbrowser-skill/
homepage: https://browser.qq.com/
permissions:
  - network: Required for browser navigation and web page interaction
  - filesystem: Required for downloading files and saving screenshots to temporary directories
---
# qqbrowser-use

Browser automation CLI for AI agents. Wraps every task in an isolated Chrome Tab Group, supports both live automation and reusable playbook replay.

## Platform Support

Linux x86_64, Windows, macOS. Other Linux architectures (ARM, etc.) are not supported.

## Installation

```bash
# Linux / macOS
pipx install qqbrowser-skill
qqbrowser-skill install   # Download and install QQ Browser

# Windows
pip install qqbrowser-skill
qqbrowser-skill install
```

## Quick Start

```bash
qqbrowser-skill browser_start_session --sessionId task-demo-001 --initialUrl https://example.com
qqbrowser-skill playbook_list                          # Check existing playbooks first
qqbrowser-skill browser_snapshot                       # Get elements with encoded indices
qqbrowser-skill browser_click_element --index "<index-from-snapshot>"
qqbrowser-skill browser_end_session --sessionId task-demo-001
```

---

## Commands

### Session Management

```bash
browser_start_session --sessionId <id> [--title "<title>"] [--color <color>] [--initialUrl <url>]
browser_end_session --sessionId <id>
browser_attach_session --tabIds "[<tabId1>,<tabId2>]" [--primaryTabId <id>] [--sessionId <id>] [--focus]
```

> `--initialUrl`: 启动会话时直接导航到指定 URL，省去单独调用 `browser_go_to_url` 的步骤。如果提供了该参数，会话创建后会自动打开对应页面。
>
> Isolation mode is fixed to `enforce` — `browser_start_session` does not accept an `--isolation` flag.
>
> `browser_attach_session`: 接管**已打开**的 tab 作为 AI 会话的交互对象（click / input / scroll / keys），补齐 `browser_start_session` 必然新建 tab 无法覆盖的场景。**前置步骤：标签的 `tabId` 无法凭空猜测或构造，必须先调用 `browser_tab_list` 获取当前打开标签的 `tabId`，再将返回的 `tabId` 作为 `--tabIds` 传入。** 仅需读取页面文本时改用 `browser_get_tab_content`（无需 session、无需激活、无需切换）。不传 `sessionId` 时由服务端生成并回传。

### Navigation

```bash
browser_go_to_url --url <url>
browser_go_back
browser_wait --seconds <n>              # Default 3s
```

### Snapshot & Screenshot

```bash
browser_snapshot                        # Element indices (for interaction)
browser_snapshot --markdown             # Markdown (for reading)
browser_screenshot [--full] [--annotate]
```

**`browser_snapshot --markdown`** returns clean Markdown of the page (ads/nav/scripts stripped, no element indices). Use it when AI needs to read/summarize page content in one-off tasks (Branch C). Do NOT use it inside `task_begin`/`task_end` (Branch B) or when you need structured data — use `browser_eval_content_js` instead.

### Click & Input

```bash
browser_click_element --index <id>
browser_dblclick_element --index <id>
browser_focus_element --index <id>
browser_input_text --index <id> --text "<content>"
```

### Scroll

```bash
browser_scroll_down [--amount <px>]
browser_scroll_up [--amount <px>]
browser_scroll_to_text --text "<text>"
browser_scroll_to_top
browser_scroll_to_bottom
browser_scroll_by --direction <dir> --pixels <n> [--index <id>]
browser_scroll_into_view --index <id>
```

### Keyboard

```bash
browser_keypress --key <key>
browser_keyboard_op --action type --text "<content>"
browser_keyboard_op --action inserttext --text "<content>"
browser_keydown --key <key>
browser_keyup --key <key>
```

### Dropdown & Checkbox

```bash
browser_get_dropdown_options --index <id>
browser_select_dropdown_option --index <id> --text "<option>"
browser_check_op --index <id> --value / --no-value
```

### Semantic Locators (Find and Act)

```bash
browser_find_and_act --by <role|text|label|placeholder|testid|css> --value "<v>" --action <click|fill|type> [--actionValue "<v>"] [--name "<n>"] [--nth <n>]
```

> `--nth`: 1-based index for list iteration (`--nth 1` = first match). Use `by: "css"` + `--nth` for loops.

### Get Information & State

```bash
browser_get_info --type <text|url|title|html|value|attr|count|box|styles|list_selector> [--index <id>] [--attribute <name>]
browser_check_state --state <visible|enabled|checked> --index <id>
```

> **`list_selector`**: Auto-detect CSS selector for list iteration. Pass any list item's index → returns `{"selector": "...", "count": N, "samples": [...]}`.

### JavaScript Evaluation

```bash
browser_eval_content_js --script "<js_code>"
browser_eval_content_js --script "<base64>" --base64
```

### Download

```bash
browser_download_file --index <id>
```

After a download succeeds, return the saved file path to the user or the next processing step. If the user asked to analyze the downloaded file, treat that path as the output of the browser sub-task and continue outside the browser workflow.

### Tab Management

```bash
browser_tab_open --url <url>
browser_tab_list
browser_tab_switch --tabId <n>
browser_tab_reload --tabId <n>
browser_tab_close --tabId <n>
browser_get_tab_content --tabId <n>
```

> **`browser_get_tab_content`** extracts the readable text content of the tab identified by `--tabId` (from `browser_tab_list`). The target tab does **not** need to be active. Use it to read a specific tab's page content without switching to it.

> **`browser_tab_list`** returns a JSON array of tab objects. Each element has:
>
> | Field | Type | Notes |
> |-------|------|-------|
> | `tabId` | integer | Tab identifier. Use it for `browser_tab_switch` / `browser_tab_reload` / `browser_tab_close`, `browser_attach_session`, and `browser_tabgroup_*` commands. |
> | `tabTitle` | string | Page title. |
> | `tabUrl` | string | Page URL. |
> | `active` | boolean | Whether this is the currently active tab. |
> | `groupId` | integer | The tab group the tab belongs to (`-1` = not in any group). Use it to look up group details via `browser_tabgroup_get`. |
> | `sessionId` | string | The AI session this tab belongs to; empty string `""` if the tab is not part of any AI session. |
> | `inSession` | boolean | Whether the tab belongs to an AI session group. |
>
> It returns **all** open tabs. Example:
>
> ```json
> [
>   {"tabId": 79655104, "tabTitle": "腾讯网", "tabUrl": "https://www.qq.com/", "active": false, "groupId": 2088091078, "sessionId": "", "inSession": false},
>   {"tabId": 79655221, "tabTitle": "小红书 - 你的生活兴趣社区", "tabUrl": "https://www.xiaohongshu.com/explore", "active": false, "groupId": 2088091078, "sessionId": "", "inSession": false},
>   {"tabId": 79655222, "tabTitle": "上网导航 - 轻快上网 从这里开始", "tabUrl": "https://daohang.qq.com/?fr=hmpage", "active": true, "groupId": 2088091078, "sessionId": "", "inSession": false}
> ]
> ```
>
> Use `tabId` as the `--tabId` argument for `browser_tab_switch` / `browser_tab_reload` / `browser_tab_close`, as the `--tabIds` / `--primaryTabId` argument for `browser_attach_session`, and as the `--tabIds` argument for `browser_tabgroup_create` / `browser_tabgroup_add_tabs` / `browser_tabgroup_remove_tabs`. Use `groupId` to look up group details via `browser_tabgroup_get`. Use `sessionId` / `inSession` to tell which tabs already belong to an AI session.

### Tab Group Management

Manage tab groups — create, inspect, update, reorder and close them.

```bash
browser_tabgroup_create --tabIds "[<tabId1>,<tabId2>]" [--title "<title>"] [--color <color>]
browser_tabgroup_list
browser_tabgroup_get --groupId <n>
browser_tabgroup_update --groupId <n> [--title "<title>"] [--color <color>] [--collapsed | --no-collapsed]
browser_tabgroup_add_tabs --groupId <n> --tabIds "[<tabId1>,<tabId2>]"
browser_tabgroup_remove_tabs --tabIds "[<tabId1>,<tabId2>]"
browser_tabgroup_move --groupId <n> --index <n>
browser_tabgroup_close --groupId <n>
```

**Read-only vs mutating** — tab group commands fall into two categories:

| Category | Commands | Effect |
|----------|----------|--------|
| Read-only (查询) | `browser_tabgroup_list`, `browser_tabgroup_get` | Never change any tab group |
| Mutating (操作) | `browser_tabgroup_create`, `browser_tabgroup_update`, `browser_tabgroup_add_tabs`, `browser_tabgroup_remove_tabs`, `browser_tabgroup_move`, `browser_tabgroup_close` | Change tab group membership / properties / position |

**Parameters**

| Flag | Type | Notes |
|------|------|-------|
| `groupId` | integer | Group ID from `browser_tabgroup_list`. `-1` means "no group". |
| `tabIds` | JSON array string | e.g. `'[123, 456]'`. Get real IDs from `browser_tab_list` — never guess them. |
| `title` | string | Group name. |
| `color` | enum | `grey` `blue` `red` `yellow` `green` `pink` `purple` `cyan` `orange` |
| `collapsed` | boolean | Whether the group is collapsed. Pass the flag alone: `--collapsed` (true) or `--no-collapsed` (false). |
| `index` | integer | Position in the window; `-1` moves to the end. |
| `windowId` | integer | Target window; defaults to the current one. |

**Output** — `list` / `update` / `add_tabs` return a group object; `get` additionally returns the group's tabs:

```json
{"groupId": 7, "title": "Research", "color": "blue", "collapsed": false, "shared": false, "windowId": 1, "tabCount": 3, "isSessionGroup": false, "sessionId": ""}
```

`browser_tabgroup_get` also returns a `tabs` array with each tab's `tabId`, `tabTitle`, `tabUrl` and `active`:

```json
{"group": { "...": "as above" }, "tabs": [{"tabId": 12, "tabTitle": "Docs", "tabUrl": "https://...", "active": true}]}
```

> **Prerequisite**: `groupId` and `tabId` cannot be guessed or constructed. Always call `browser_tab_list` (for `tabIds`) or `browser_tabgroup_list` (for `groupId`) first.
>
> **`browser_tabgroup_close`** closes every tab in the group; Chrome has no destroy API, so the group disappears once empty.
>
> **⚠️ AI session group protection**: the group created by `browser_start_session` is the AI's own workspace. While an AI task is **actively running**, all **mutating** commands — `browser_tabgroup_create`, `browser_tabgroup_update`, `browser_tabgroup_add_tabs`, `browser_tabgroup_remove_tabs`, `browser_tabgroup_move` and `browser_tabgroup_close` — **refuse** to touch the active session group and return an error. Read-only commands (`browser_tabgroup_list`, `browser_tabgroup_get`) are always allowed. The check is based on the session→group mapping maintained by the extension (not the group title), so it still holds when a custom `--title` is used. Once the AI task has ended (via `browser_end_session` or idle timeout), the group is no longer protected and can be mutated freely. To dispose of a session group, call `browser_end_session`.
>
> `browser_tabgroup_list` / `browser_tabgroup_get` also return `isSessionGroup` and `sessionId`, so you can tell which groups are AI workspaces at a glance.

### Dialog

```bash
browser_dialog --action <accept|dismiss> [--text "<input>"]
```

### Task Recording

```bash
task_begin --description "<desc>"
task_end
task_latest                                # Get most recent recording
```

> **When to use**: Only when user explicitly asks to record/save/reuse (trigger words: "record this", "save this", "保存为脚本", "录一下", "下次还要用"). Without explicit request, do NOT use these commands.
>
> **Before calling `task_begin`**: MUST read [references/playbook.md](./references/playbook.md) for recording quality rules — they are required to make the recording reusable.
>
> **After `task_end`**: Raw recordings are NOT replay-ready. Call `task_latest`, then follow [references/playbook.md → From Recording to Playbook](./references/playbook.md#from-recording-to-playbook) to generate, save, and verify the playbook JSON.

### Playbook & Replay

```bash
playbook_list                              # List available playbooks
browser_replay --script <path> [--variables '{"key":"value"}']
```

> **How to use**:
>
> 1. `playbook_list` returns available playbooks with `path`, `name`, `description`, and `params` (required variables).
> 2. Match the user's task against returned playbooks by name/description/URL.
> 3. Read the matched playbook's `params` to know which `--variables` keys are required.
> 4. Pass variables as JSON: `--variables '{"param1": "value1", "param2": "value2"}'`
>
> ⚠️ `browser_replay` can take **up to 10 minutes**. Wait patiently — do NOT interrupt, retry, or fall back to manual mode.
>
> For full output format (success/failure/step_results), see [references/commands-extended.md](./references/commands-extended.md#browser_replay-output-format).

### Utility

```bash
browser_done --success --text "<msg>"
status
list
```

> `browser_done` is a status/reporting utility only. It does **not** replace `browser_end_session`, and it does not release the session mapping.

---

## ⚠️ Core Workflow (MANDATORY)

> **Every browser automation MUST be wrapped in `browser_start_session` / `browser_end_session` (or `browser_attach_session` / `browser_end_session` when operating on already-open tabs), and you MUST run `playbook_list` before any `task_begin` or `browser_go_to_url`.** Never start manual automation without first checking for existing playbooks.

### Decision Flow

```
Step 0: Classify intent
        ├── ① Browser-internal assets (bookmarks, history, etc.)
        │      → This skill has NO such capability. Tell the user it is out of scope.
        │        Do NOT call any browser_* command.
        ├── ② Analyze already-open tabs (current tab, or tabs selected by title/meaning)
        │      → Use the "Analyzing Existing Tabs" path below. Do NOT open a new window.
        └── ③ New browser task (open a site, fill forms, click, etc.) or browser operation task
               → Continue to Step 1 ↓

Step 1: browser_start_session                 ← ⛔ MANDATORY for intent ③: first command, no exceptions
Step 2: playbook_list                         ← ⛔ MANDATORY: ALWAYS call before any navigation, even if you think no playbook exists
Step 3: Match?
        ├── YES → browser_replay              ← Branch A: Replay
        └── NO  → Manual automation
                  ├── Recording mode          ← Branch B: user explicitly asks to record
                  │     task_begin
                  │     browser_* operations...
                  │     task_end
                  │     → then continue with references/playbook.md
                  └── Non-recording mode      ← Branch C: one-off task
                        browser_* operations...
Step 4: browser_end_session                   ← ⛔ MANDATORY: ALWAYS execute, even on failure or early exit
```

> **⛔ Non-Negotiable Rules:**
>
> 1. **`playbook_list` MUST be called every time** after `browser_start_session`, before any `browser_go_to_url` or other browser commands — no exceptions, no shortcuts.
> 2. **`browser_end_session` MUST be called at the end** regardless of outcome (success, failure, error, early exit, user interrupt). Think of it as a `finally` block — it always runs.

**Recording (Branch B) triggers only on explicit user request.** Trigger words: "record this", "save this", "make reusable", "保存为脚本", "录一下", "下次还要用". Without an explicit request, use **Branch C** (non-recording) — do **not** wrap the operations in `task_begin` / `task_end`.

### Analyzing Existing Tabs (intent ② — do NOT open a new window)

When the user wants to analyze tabs that are **already open** (the current tab, or tabs selected by title or meaning), do **not** call `browser_start_session`. Instead:

```
1. browser_tab_list
   → Returns ALL open tabs (tabId / tabTitle / tabUrl / active / groupId / sessionId / inSession).
   → active=true means the currently active tab; active=false means an open but inactive tab.
   → inSession=true (sessionId non-empty) means the tab already belongs to an AI session group.
2. The LLM selects the target tab(s) based on the user's intent (title / URL / meaning).
3. Branch by analysis depth:
   ├── Content-only (read / summarize / Q&A)
   │     → browser_get_tab_content --tabId <id>
   │       (no session, no activation, no tab switch, no new window)
   └── Deep analysis / information mining (needs buttons, controls, links)
         → Record the currently active tab.
         → browser_attach_session --tabIds "[<targetTabId>]" [--primaryTabId <id>] [--sessionId <id>]
         → browser_snapshot   (default axtree — exposes buttons, controls, links)
         → ... interact as needed ...
         → browser_end_session --sessionId <id>   ← ⛔ MANDATORY: releases the sessionId context
```

> **`browser_snapshot` vs `browser_snapshot --markdown`:** the default `browser_snapshot` returns indexed interactive elements (buttons, controls, links) — use it for deep analysis or interaction. `browser_snapshot --markdown` returns clean Markdown text only and contains **no** button/control information — use it only for one-off content reading.

### Human-in-the-Loop Verification Points

If the site requires CAPTCHA, SMS code, email code, MFA/2FA, QR login, device confirmation, or any other human verification step:

- Pause automation at that point.
- Keep the current session alive.
- Ask the user to complete the verification manually — use an **interactive user-prompt / question dialog** (a tool that interrupts and asks the user, e.g. `ask_user_question` or `AskUserQuestion`) rather than plain chat text, so the prompt is prominent.
- Resume only after the verification step is finished.

Do **not** blindly retry replay or switch branches just because a human verification wall appears.

> **Tool discovery (do not hard-code tool names).** This SKILL may run on hosts that expose the same capability under different names. When you need a capability, identify it by **function**, then use whatever equivalent tool / skill is actually available in the current environment:
>
> - **Ask the user / interrupt for input** → look for a user-prompt, question, or interrupt tool (e.g. `ask_user_question`, `AskUserQuestion`, `ask_user`, `human_input`). If none exists, fall back to plain chat text.
> - **Read or describe an image** → look for a vision / image-understanding tool (OCR, image captioning, screenshot analysis). If none exists, skip visual confirmation and rely on DOM / text probes only.
> - **Locate a target in an image by text description** → look for a visual-grounding / VLM localization tool. If none exists, skip it and use DOM / text probes only.
>
> Never assume a specific tool name exists; match by capability and degrade gracefully when it is absent.

### Detecting Login, CAPTCHA & Anti-Bot Interception

**Trigger only on suspicion — do NOT run this check on every step.** Pages that load normally need no verification; adding a check to each step only slows the task. Start this check only when you observe at least one of:

- Expected content never renders: a list / search / task page stays on a placeholder (e.g. `加载中…` / `Loading…`) across 2+ samples after `browser_wait`, with no expected elements present.
- The page shell (header / nav / footer) is present but the main content area is empty.
- The tab URL or title contains `login` / `passport` / `captcha` / `verify`, or you were redirected to a login domain.
- `browser_snapshot` (axtree) shows an overlay-style `X` close control or an opaque full-page layer instead of the expected controls.

When suspicion is raised, verify in this order — **prefer this SKILL's own capabilities first**:

1. **DOM probe via `browser_eval_content_js` (preferred).** JS can see signals that snapshots cannot — most importantly login forms embedded in **cross-origin iframes** (e.g. `login.taobao.com`) that `browser_snapshot` will not expand. Check for:
   - a visible `<iframe>` whose `src` matches `login.|passport.|captcha.` (verify visibility via `getBoundingClientRect()` width/height > 0)
   - a full-screen mask / overlay (e.g. `[class*=mask]`, `[class*=dialog]`, `baxia`-style) sized close to the viewport
   - placeholder text still present (`加载中` / `Loading`) while expected content (product/report links, list items) is absent
2. **Page text via `browser_snapshot --markdown` or `browser_get_tab_content`.** Grep the readable text for `请重新登录` / `验证码` / `登录` / `滑动验证` etc. ⚠️ Text inside a cross-origin login iframe will NOT appear here — its absence does **not** rule out a login wall.
3. **Visual confirmation (fallback only)**. If steps 1–2 are still inconclusive, or you must visually confirm what the user is seeing: run `browser_screenshot`, then hand the image to a **vision / image-understanding tool** — use OCR mode to read the popup text, or caption/description mode to describe the popup; if a **visual-grounding / VLM localization** tool is available, use it to locate the target. Match these tools by capability (see "Tool discovery" above), not by a fixed name. Use this as **confirmation**, not as the default first move.

Once a login / CAPTCHA / anti-bot wall is confirmed, stop retrying and follow "Human-in-the-Loop Verification Points" above: pause, keep the session alive, and prompt the user with an **interactive user-prompt / question dialog** (e.g. options "已手动登录，请继续" / "暂不登录") to complete login or verification manually, then re-run the same DOM probe to confirm the wall is gone (login iframe disappeared, or expected content appeared) before resuming.

### Step 1: Start Session (REQUIRED for intent ③ only)

```bash
qqbrowser-skill browser_start_session --sessionId task-<purpose>-<counter> [--initialUrl <url>]
```

`sessionId` must be unique per task (e.g. `task-form-001`). Use `--initialUrl` to navigate directly on session start, combining session creation and navigation into one step. Full flags and idempotency rules: [references/session-lifecycle.md](./references/session-lifecycle.md).

> **Do NOT call `browser_start_session` for intent ② (analyzing already-open tabs).** Use `browser_get_tab_content` (content-only) or `browser_attach_session` (deep analysis) instead — see "Analyzing Existing Tabs" above. `browser_start_session` always creates a new tab inside a new Chrome Tab Group — the command does not operate on the tabs the user already has open.

### Step 2: Check Playbooks (⛔ MANDATORY — DO NOT SKIP, NO EXCEPTIONS)

```bash
qqbrowser-skill playbook_list
```

**This step is non-negotiable.** You MUST call `playbook_list` every single time, even if:

- You are sure no playbook exists for this task.
- You have just completed a sub-task in a composite pipeline and are starting the next one.
- The user's request seems trivial or one-off.

Match returned playbooks against the user's task by `name`, `description`, keywords, target URL, and side-effect profile.

- For **read-only / low-risk tasks** (read, extract, summarize, inspect), a high-confidence partial match may still prefer replay.
- For **side-effecting tasks** (post, submit, message, purchase, delete, publish), replay is allowed only when the task intent, target site, entry page, and key side effects are clearly equivalent.
- If equivalence is uncertain, do **not** replay blindly — ask the user or fall back to a safer path.

### Step 3: Branch by Match Result

#### Branch A — Playbook matched → Replay

> ⚠️ **`browser_replay` may run for up to 10 minutes.** Wait for it to return — **NEVER interrupt, retry, or fall back to manual mode while it is still running.** Replayed operations are usually **not idempotent** (posting, submitting, messaging), so a premature retry will cause duplicate side effects.

```bash
qqbrowser-skill browser_replay --script <path> --variables '{...}'
```

#### Safety Gate for Side-Effecting Tasks

Before replaying a playbook that may cause real-world side effects — such as posting, submitting, sending messages, purchasing, deleting, or publishing — verify all of the following:

1. The target site/account/page matches the user's intent.
2. Required variables are complete and unambiguous.
3. The expected outcome is the same as the original playbook's outcome.
4. The user has clearly authorized executing the live action.

If any of the above is uncertain, do not replay blindly. Prefer draft mode, test data, manual review, or explicit user confirmation.

### If `browser_replay` Returns Failure

When replay finishes with `success: false`:

1. Inspect the failed step and its error details first.
2. Do **not** immediately retry the same replay on live targets.
3. Do **not** automatically fall back to manual execution for side-effecting tasks.
4. For read-only tasks, manual fallback is acceptable if the failure is clearly non-destructive.
5. For side-effecting tasks, require user confirmation or a safer environment before retrying or manually continuing.

#### Branch B — No playbook + user asked to record → Manual with recording

> **Before calling `task_begin`, MUST read [references/playbook.md](./references/playbook.md).** These rules are required to make the recording reusable; do not start recording from the short example alone.

```bash
qqbrowser-skill task_begin --description "描述任务"
qqbrowser-skill browser_go_to_url --url <url>
qqbrowser-skill browser_snapshot
# ... interact using indices ...
qqbrowser-skill task_end
```

**After `task_end`**, continue following [references/playbook.md](./references/playbook.md#from-recording-to-playbook) to generate the playbook JSON.

#### Branch C — No playbook + no recording request → Plain manual

Default fallback for one-off tasks. Do **not** call `task_begin` / `task_end`. **Still call `playbook_list` first** (Step 2 is mandatory for all branches).

```bash
qqbrowser-skill playbook_list                  # ⛔ MANDATORY — do not skip
qqbrowser-skill browser_go_to_url --url <url>
qqbrowser-skill browser_snapshot
# ... interact using indices ...
```

### Step 4: End Session (⛔ MANDATORY — always executed, like a `finally` block)

```bash
qqbrowser-skill browser_end_session --sessionId task-<purpose>-<counter>
```

**This step is non-negotiable.** `browser_end_session` MUST be called at the end of every task, regardless of outcome:

- ✅ Task completed successfully → call `browser_end_session`
- ❌ Task failed with an error → call `browser_end_session`
- 🛑 Task interrupted or early exit → call `browser_end_session`
- ⏸️ Human verification needed (CAPTCHA, etc.) → keep session alive during verification, then call `browser_end_session` after

**Never leave a session dangling.** If you called `browser_start_session`, you MUST call `browser_end_session` before finishing.

---

## Common Patterns

### Form Submission

```bash
qqbrowser-skill browser_start_session --sessionId task-form-001 --initialUrl https://example.com/signup
qqbrowser-skill playbook_list
qqbrowser-skill browser_snapshot
qqbrowser-skill browser_input_text --index "<name-index>" --text "Jane Doe"
qqbrowser-skill browser_input_text --index "<email-index>" --text "jane@example.com"
qqbrowser-skill browser_select_dropdown_option --index "<state-index>" --text "California"
qqbrowser-skill browser_click_element --index "<submit-index>"
qqbrowser-skill browser_wait --seconds 2
qqbrowser-skill browser_snapshot                    # Verify result
qqbrowser-skill browser_end_session --sessionId task-form-001
```

### Data Extraction

| Approach | When | Replayable? |
| --- | --- | --- |
| `browser_snapshot --markdown` | AI reads/summarizes a page once (Branch C only) | ❌ |
| `browser_snapshot` + `browser_get_info` | Read one specific element's text/attribute | ❌ |
| `browser_eval_content_js` | Structured JSON / multiple items /**only safe option in Branch B** | ✅ |

```bash
qqbrowser-skill browser_start_session --sessionId task-extract-001 --initialUrl https://example.com/products
qqbrowser-skill playbook_list
qqbrowser-skill browser_eval_content_js --script "JSON.stringify(Array.from(document.querySelectorAll('.product-item')).slice(0,10).map(el=>({name:el.querySelector('.name')?.textContent?.trim(), price:el.querySelector('.price')?.textContent?.trim()})))"
qqbrowser-skill browser_end_session --sessionId task-extract-001
```

### Infinite Scroll

```bash
qqbrowser-skill browser_start_session --sessionId task-feed-001 --initialUrl https://example.com/feed
qqbrowser-skill playbook_list
qqbrowser-skill browser_scroll_to_bottom
qqbrowser-skill browser_wait --seconds 2
qqbrowser-skill browser_snapshot
qqbrowser-skill browser_end_session --sessionId task-feed-001
```

---

## Key Concepts

- **Element Index**: Encoded string like `2_sfli_qp0u` (`highlightIndex_attrHash_xpathHash`). Generated by `browser_snapshot`, used to target elements. **Indices are regenerated on every snapshot** — always re-snapshot before reusing indices. **Never invent numeric indices like `1` or `2`; always copy the encoded index exactly from the latest `browser_snapshot` output.**
- **Snapshot**: Returns page content with indexed elements. Re-snapshot after any DOM change (navigation, form submit, modal, AJAX). Most `browser_*` commands executed inside an active session already return updated page state in their response. Use standalone `browser_snapshot` only when you truly need a fresh interactive view or the previous response is not sufficient.
- **Session**: New browser tasks (intent ③) MUST be wrapped with `browser_start_session` / `browser_end_session` for tab group isolation. Tasks on already-open tabs (intent ②) use `browser_attach_session` / `browser_end_session` (deep analysis) or `browser_get_tab_content` (content-only, no session).
- **Task Recording**: Manual browser tasks intended for replay MUST be wrapped with `task_begin` / `task_end` for playbook generation.
- **Playbook**: Parameterized JSON script that replays a recorded task without AI.

---

## Reference Files (Load On Demand)

| Reference | Load when… |
| --- | --- |
| [references/commands-extended.md](./references/commands-extended.md) | You need extended details on`browser_snapshot --markdown` usage, `browser_replay` output format, or advanced flag semantics |
| [references/session-lifecycle.md](./references/session-lifecycle.md) | You need full session rules (start / attach / end), the user's request is a**composite task** with multiple browser sub-tasks or browser → AI → browser flow, or you are analyzing already-open tabs |
| [references/playbook.md](./references/playbook.md) | User asks to**record/save/reuse**, generate/edit a playbook JSON, or run a reusable browser task |

---

## Notes

- Refs (element indices) are stable per snapshot but change on navigation — always re-snapshot after page changes.
- Use `browser_input_text` for form fields to ensure existing text is cleared.
- Use `browser_find_and_act` with semantic locators when element indices are unstable across sessions.
- For full `browser_replay` output format and consumption guide, see [references/commands-extended.md](./references/commands-extended.md#browser_replay-output-format).

---

## Evaluation Report

See the full skill evaluation report: [QQBrowserUse](https://bak.res.qq.com/nav/qqbrowser_skills/QQBrowserSkillReport.html)
