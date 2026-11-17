# Playbook Guide

> Complete reference for recording, generating, editing, and replaying `qqbrowser-skill` playbooks.
>
> Load this file when the user asks to **record**, **save**, **reuse**, **generate**, **edit**, or **run** a browser automation playbook.

## Scope

A playbook is a parameterized JSON script generated from a real browser task recording. It lets future runs replay the same browser workflow without AI deciding every click again.

This guide covers the full Branch B lifecycle:

```text
explicit user request to record/save/reuse
  ↓
task_begin / browser operations / task_end
  ↓
task_latest
  ↓
convert recording into playbook JSON
  ↓
save under ~/.qqbrowser-skill/playbooks/
  ↓
verify safely with browser_replay
```

Main workflow constraints from `SKILL.md` still apply:

- Start `browser_start_session` before any browser operation.
- Run `playbook_list` before manual automation.
- Enter Branch B only when the user explicitly asks to record/save/reuse.
- End with `browser_end_session` even on failure.

---

## Branch B Recording Rules

> These rules apply **only inside `task_begin` / `task_end`**. They exist to make the recording clean enough to become a reusable playbook.
>
> In one-off Branch C tasks, exploratory trial-and-error, hardcoded indices, ad-hoc selectors, and multiple probes are acceptable because no reusable playbook will be generated.

### Rule 1: Task Classification

| Category | Replayable? | Strategy |
|---|---:|---|
| **A: Fixed-path** — navigate, click, fill | ✅ | Standard replayable browser commands |
| **B: Data extraction** | ⚠️ | Use `browser_eval_content_js` for replayable structured output |
| **C: Content understanding** — summarization, judgment, comparison | ❌ | Set `metadata.requires_ai: true`; include only replayable portions |
| **D: Dynamic iteration** — lists, search results, pagination | ⚠️ | Record stable selector and enough repeated iterations to convert to `loop` |

### Rule 2: Data Extraction — Prefer JS in Recordings

Inside `task_begin` / `task_end`, extract data with `browser_eval_content_js`, not `browser_snapshot --markdown`.

`browser_snapshot --markdown` is useful for AI reading in one-off tasks, but it is not a replayable structured extraction step.

```bash
# ✅ Replayable structured extraction
browser_eval_content_js --script "JSON.stringify(Array.from(document.querySelectorAll('.item')).slice(0,10).map(el=>({title:el.querySelector('.title')?.textContent?.trim()})))"
```

### Rule 3: Analyze First, Execute Once

Do not perform trial-and-error inside a recording. Use `browser_snapshot` to inspect the page, then execute one definitive operation.

**Prohibited inside `task_begin` / `task_end`:**

- Multiple `browser_eval_content_js` attempts with different guessed selectors.
- Hardcoding element indices inside JavaScript scripts.
- Using regular expressions on page text as the main selector strategy.

If the recorded path is wrong, call `task_end`, discard the bad recording, and re-record cleanly.

### Rule 4: JS Selector Priority

When writing extraction scripts, choose selectors in this order:

```text
id > data-* > ARIA > semantic class > structural path
```

Never use dynamic or hashed classes such as `.css-1a2b3c` unless no stable alternative exists and the playbook is marked `requires_ai` or requires manual maintenance.

### Rule 5: Loop Recording

When the task involves repeated list items, record **at least 2 iterations** using a stable selector and `browser_find_and_act --by css --nth`.

```bash
# Discover selector first.
# <index-from-snapshot> must be copied from the latest browser_snapshot output.
browser_get_info --type list_selector --index "<index-from-snapshot>"

# Record a probe for the playbook generator.
browser_eval_content_js --script "JSON.stringify({__list_probe__: true, selector: '.result-item h2 a', count: document.querySelectorAll('.result-item h2 a').length, samples: Array.from(document.querySelectorAll('.result-item h2 a')).slice(0,3).map(e=>e.textContent.trim())})"

# Iteration 1
browser_find_and_act --by css --value ".result-item h2 a" --action click --nth 1
# ... extract, then return to list or close/switch tab ...

# Iteration 2
browser_find_and_act --by css --value ".result-item h2 a" --action click --nth 2
# ... extract, then return to list or close/switch tab ...
```

**Key rules:**

- Use `browser_get_info --type list_selector` to discover a list-level CSS selector. Never guess selectors.
- Use `browser_find_and_act --by css --value "<selector>" --nth N` for list items.
- Avoid `browser_click_element --index ...` for dynamic list iteration; indices are snapshot-specific and not stable across replay.
- Keep the `__list_probe__` result available to the generator; it is the strongest signal for selector extraction and loop conversion.

### Rule 6: Multi-Tab Recording

When links open new tabs:

1. After click, use `browser_tab_list` to identify the new tab.
2. Use `browser_tab_switch` → extract/operate → `browser_tab_close` → switch back.
3. Do not use `browser_go_back` for cross-tab navigation.
4. Record 2+ iterations if this is part of a loop.

### Rule 7: Fixed vs Variable Parameters

| Fixed — never parameterize | Variable — replace with `{{param}}` |
|---|---|
| `index`, `action`, fixed base URLs, fixed UI buttons, `settings` | user text, emails, usernames, quantities, query params, file paths, user-specific URL segments, `actionValue` |

### Rule 8: Non-Replayable Commands Are Allowed During Recording

These commands are useful while recording because the AI needs to inspect the page, but they must be filtered out when generating final replay steps:

```text
browser_snapshot
browser_screenshot
browser_get_info
browser_check_state
browser_get_dropdown_options
browser_tab_list
task_begin / task_end / task_latest
browser_done
```

`browser_eval_content_js` is replayable and is not filtered by default. If it is only a selector probe, it may still be useful as a harmless validation/extraction step; otherwise the generator can use its output to build a cleaner loop step.

### Rule 9: Prefer Semantic Locators for Dynamic Content

```bash
# ✅ Stable across page changes when text is unique
browser_find_and_act --by text --value "{{target}}" --action click

# ⚠️ Only for stable structures; index must come from latest snapshot
browser_click_element --index "<index-from-latest-snapshot>"
```

Use `browser_find_and_act` whenever the target can be described by text, label, placeholder, role, test id, or stable CSS.

---

## From Recording to Playbook

After `task_end`, raw recordings are **not** replay-ready. Convert them into a parameterized playbook.

### Workflow

```bash
# 1. Load the most recent recording
qqbrowser-skill task_latest

# 2. AI analyzes the recording and generates a playbook:
#    2a: Filter excluded actions
#    2b: Extract selector signals such as __list_probe__
#    2c: Detect repeated sequences and convert them to loop
#    2d: Detect tab operations and convert physical tabId to semantic tab refs
#    2e: Cross-check loop + tab behavior
#    2f: Parameterize user data only
#    2g: Add metadata, params, settings, and descriptions

# 3. Save
mkdir -p ~/.qqbrowser-skill/playbooks
# Write JSON to ~/.qqbrowser-skill/playbooks/<kebab-case-name>.json

# 4. Verify safely
qqbrowser-skill browser_replay --script ~/.qqbrowser-skill/playbooks/<name>.json \
  --variables '{"param1": "value1"}'
```

### Safe Verification

`browser_replay` executes all playbook steps sequentially in the browser and can take **up to 10 minutes**.

- Wait for the command to return. Do not interrupt, retry, or fall back to manual mode while it is still running.
- Inspect `success`, `failed_step`, and `step_results` in the response.
- If a step fails, fix the playbook JSON and re-run only when safe.
- For non-idempotent or side-effecting tasks — posting, submitting, messaging, purchasing, deleting, sending email — do **not** replay against a live target without explicit user approval. Prefer draft mode, sandbox/test data, or manual JSON inspection.

---

## Critical Playbook Rules

1. A playbook **MUST** be generated from an actual `task_latest` recording. Never fabricate steps.
2. Use action names and stable replay parameters from the recording. Copy `index` values verbatim when they are part of fixed-path steps.
3. Only replace user-controlled data with `{{param_name}}`.
4. Never parameterize `action`, fixed workflow structure, `settings`, or element `index`.
5. Save playbooks to `~/.qqbrowser-skill/playbooks/<kebab-case-name>.json`.
6. JSON structure is `version` + `metadata` + `params` + `settings` + `steps`. The key is `params`, not `parameters`.

---

## Valid Actions

### Allowed Replay Actions

| Action | Parameterizable Fields |
|---|---|
| `browser_go_to_url` | `url` |
| `browser_click_element` / `browser_dblclick_element` / `browser_focus_element` | — |
| `browser_input_text` / `browser_keyboard_op` | `text` |
| `browser_keypress` / `browser_keydown` / `browser_keyup` | — |
| `browser_select_dropdown_option` | `text` |
| `browser_check_op` | — |
| `browser_scroll_down` / `browser_scroll_up` / `browser_scroll_to_top` / `browser_scroll_to_bottom` / `browser_scroll_by` / `browser_scroll_into_view` | — |
| `browser_scroll_to_text` | `text` |
| `browser_wait` | — |
| `browser_go_back` | — |
| `browser_dialog` | `text` |
| `browser_tab_open` | `url`, `as` alias |
| `browser_tab_switch` / `browser_tab_close` | `tab` semantic ref |
| `browser_download_file` / `browser_download_url` | — |
| `browser_eval_content_js` | `script` |
| `browser_find_and_act` | `value`, `actionValue`, `name`, `nth`, `openInNewTab` |
| `loop` | `count`, `variable`, `start`, `on_error`, nested `steps` |

### Excluded Actions

Filter these out from final playbook steps:

```text
browser_snapshot
browser_screenshot
browser_get_info
browser_check_state
browser_get_dropdown_options
browser_tab_list
task_begin / task_end / task_latest
browser_done
```

---

## Playbook JSON Format

```json
{
  "version": "1.0",
  "metadata": {
    "name": "小红书发布笔记",
    "description": "自动打开小红书并发布一篇笔记",
    "created_at": "2026-05-21T16:59:00Z",
    "url": "https://www.xiaohongshu.com/explore",
    "requires_ai": false
  },
  "params": {
    "notes_title": { "description": "笔记标题", "required": true },
    "notes_content": { "description": "笔记正文内容", "required": true }
  },
  "settings": {
    "default_delay_ms": 500,
    "default_retry_count": 1,
    "step_timeout_ms": 30000
  },
  "steps": [
    {
      "action": "browser_go_to_url",
      "params": { "url": "https://www.xiaohongshu.com/explore" },
      "description": "打开小红书探索页"
    },
    {
      "action": "browser_input_text",
      "params": { "index": "6_2vl4_txwg", "text": "{{notes_title}}" },
      "description": "输入笔记标题"
    },
    {
      "action": "browser_click_element",
      "params": { "index": "19_oxgq_ttmr" },
      "description": "点击发布"
    }
  ]
}
```

### Required Fields

- `version`: always `"1.0"`.
- `metadata.name`: human-readable name, Chinese is OK.
- `metadata.description`: one-line summary.
- `metadata.created_at`: ISO 8601 timestamp.
- `params`: parameter definitions; each param needs `description` and `required`, optional `default`.
- `settings`: replay defaults, usually `{ "default_delay_ms": 500, "default_retry_count": 1, "step_timeout_ms": 30000 }`.
- `steps`: ordered replay steps; each step needs `action`, `params`, and `description`.

### Optional Fields

- `metadata.url`: canonical entry URL.
- `metadata.requires_ai`: set `true` when some part still needs AI judgment.
- `condition`: skip a step unless an optional param exists.

```json
{
  "action": "browser_input_text",
  "params": { "index": "12_abcd_efgh", "text": "{{cc}}" },
  "condition": { "param": "cc" },
  "description": "填写抄送人"
}
```

When an optional param controls a sub-flow, add the same `condition` to **all** dependent steps.

---

## Parameter Extraction

**Parameterize:**

- User-entered text.
- Emails, usernames, addresses, phone numbers.
- Search keywords and query params.
- Quantities such as `count`.
- File paths and user-specific URL segments.
- `actionValue` for `browser_find_and_act` fill/type operations.

**Never parameterize:**

- `action`.
- Element `index`.
- Fixed workflow URLs and fixed UI buttons.
- `settings`.
- Internal control structure unless explicitly supported, such as `loop.params.count`.

**Naming:** use descriptive `snake_case`, for example `notes_title` instead of `title`.

---

## `requires_ai` Tasks

Set `metadata.requires_ai: true` when the task contains AI-dependent operations that cannot be replayed deterministically, such as:

- Summarization.
- Comparison or subjective judgment.
- Conditional decisions based on page meaning.
- Rewriting content for another platform.

In that case, include only the deterministic browser portions as steps and leave the AI-dependent part outside the pure replay path.

---

## Selector Extraction for Loops

### Primary Source: `__list_probe__`

Look for `browser_eval_content_js` calls whose output contains `__list_probe__: true`.

```text
browser_eval_content_js → output:
{"__list_probe__": true, "selector": ".SearchResult-Card .ContentItem h2 a", "count": 10, "samples": ["文章A", "文章B", "文章C"]}
```

Extract the `selector` value and use it directly in loop `browser_find_and_act` steps.

### Fallback Order

If there is no `__list_probe__`:

1. If the recording already uses `browser_find_and_act --by css`, reuse that selector.
2. If the recording only uses `by: "text"` or `browser_click_element(index)`, the selector is unknown.
3. Use `browser_get_info --type list_selector --index <any_list_item_index>` to auto-detect a selector before generating the playbook.
4. If `list_selector` fails, run a focused `browser_eval_content_js` probe to discover a stable selector.
5. If all selector discovery fails, do not guess; set `metadata.requires_ai: true`.

---

## Loop Steps

Use `loop` when the recording shows **2+ repetitions** of the same action sequence differing only in target item, and the count is user-controlled or naturally dynamic.

Do **not** use `loop` for fixed form fields or when a single `browser_eval_content_js` can extract all data at once.

### Loop JSON

```json
{
  "action": "loop",
  "params": { "count": "{{count}}", "variable": "i", "start": 1 },
  "description": "逐个访问前N篇文章",
  "steps": [ ... ]
}
```

Fields:

- `count`: string or number; supports `{{param}}`.
- `variable`: loop variable name, usually `i`.
- `start`: default `1`; aligns with `nth` because `nth=1` is the first match.
- `on_error`: optional; default `"fail"`.

### `on_error` for Dynamic Lists

When the list length is unknown, use `on_error: "break"` with a large upper bound.

```json
{
  "action": "loop",
  "params": { "count": "100", "variable": "i", "start": 1, "on_error": "break" },
  "description": "处理所有列表项（自动检测结束）",
  "steps": [ ... ]
}
```

| `on_error` | Behavior |
|---|---|
| `"fail"` | Sub-step failure fails the whole replay |
| `"break"` | Sub-step failure exits the loop gracefully and replay continues |

Use `on_error: "break"` when the user asks to process all available items or when the count cannot be known at generation time.

### Loop Conversion Rules

1. Use `browser_find_and_act` with `by: "css"` + `nth: "{{i}}"` inside loops.
2. `by` must be `"css"` when `nth` is used. Do not use `by: "text"` or `by: "label"` for list iteration.
3. `value` must be a list-level CSS selector matching all items, not a specific title or keyword.
4. The selector must come from actual DOM: `__list_probe__`, existing `find_and_act(css)`, `list_selector`, or a live probe.
5. Convert repeated `browser_click_element(index=...)` on different list items into one `browser_find_and_act(css, nth="{{i}}")` step.
6. Convert repeated `find_and_act(by="text", value="标题A/B/C")` into `find_and_act(by="css", nth="{{i}}")`.
7. Include `browser_wait` between iterations for stability.

### Loop Decision Table

| Scenario | Method |
|---|---|
| List page data only | Single `browser_eval_content_js` |
| Need detail page content | `loop` |
| Pagination + extraction | `loop` |
| Fixed different form fields | Linear steps |
| Process all unknown-length items | `loop` with `on_error: "break"` and large `count` |

---

## Tab Management

Playbooks must use **semantic tab references**. Physical `tabId` values change across sessions and must not be hardcoded.

| Reference | Meaning |
|---|---|
| `"origin"` | Tab active when replay started |
| `"current"` | Currently active tab |
| `"latest"` | Most recently opened tab |
| Custom alias | Named via `"as"` in `browser_tab_open` |

Examples:

```json
{ "action": "browser_tab_open", "params": { "url": "https://example.com", "as": "detail" }, "description": "打开详情页" }
{ "action": "browser_tab_switch", "params": { "tab": "origin" }, "description": "切回原始Tab" }
{ "action": "browser_tab_close", "params": { "tab": "current" }, "description": "关闭当前Tab" }
```

Rules:

1. Never use physical `tabId` in playbook JSON.
2. `browser_go_back` does not work across tabs.
3. After `browser_tab_close`, explicitly `browser_tab_switch`; do not assume Chrome's active tab.
4. If a loop iteration opens a new tab, use `tab_switch("latest")` → operate/extract → `tab_close("current")` → `tab_switch("origin")`.
5. Use `browser_go_back` only if iteration stays in the same tab.

### `go_back` vs Tab Close/Switch

| Scenario | Method |
|---|---|
| Link opens in same tab | `browser_go_back` |
| Link opens in new tab | `browser_tab_close` + `browser_tab_switch` |
| Unsure, especially in loops | `openInNewTab: true` + `browser_tab_close` + `browser_tab_switch` |

---

## `browser_find_and_act` Usage

For single-element targeting, use stable semantic locators:

```json
{ "action": "browser_find_and_act", "params": { "by": "text", "value": "提交", "action": "click" }, "description": "点击提交" }
```

For list iteration, use CSS + `nth`:

```json
{ "action": "browser_find_and_act", "params": { "by": "css", "value": ".List-item a", "nth": "{{i}}", "action": "click" }, "description": "点击第{{i}}个结果" }
```

### `openInNewTab`

When `action: "click"` and the workflow requires a new tab, add `"openInNewTab": true`.

```json
{
  "action": "browser_find_and_act",
  "params": {
    "by": "css",
    "value": ".List-item a",
    "nth": "{{i}}",
    "action": "click",
    "openInNewTab": true
  },
  "description": "在新Tab打开第{{i}}篇文章"
}
```

Use it when:

- Loop pattern requires `tab_switch("latest")` → extract → `tab_close("current")` → `tab_switch("origin")`.
- Link behavior varies by site or context.
- Navigating away from the current page would break the workflow.

Behavior: the engine extracts the element's `href` and opens it via browser tab creation. If no `href` is found, it falls back to modifier-click behavior.

---

## `browser_eval_content_js` Usage

Use `browser_eval_content_js` as the primary data extraction method for playbooks.

- Return JSON strings for structured data.
- Support `{{param}}` in scripts for selectors, keywords, counts, and user data.
- Prefer stable selectors: `id`, `data-*`, ARIA, semantic class, structural path.
- Avoid dynamic or hashed classes.

Example:

```json
{
  "action": "browser_eval_content_js",
  "params": {
    "script": "JSON.stringify(Array.from(document.querySelectorAll('.product-item')).slice(0, Number('{{count}}')).map(el => ({ name: el.querySelector('.name')?.textContent?.trim(), price: el.querySelector('.price')?.textContent?.trim() })))"
  },
  "description": "提取商品列表"
}
```

---

## Complete Example: Loop + New Tab

This example demonstrates key conversions: text target to CSS selector, physical tab ID to semantic tab refs, and repeated linear steps to `loop`.

Raw recording pattern:

```text
browser_eval_content_js → {"__list_probe__": true, "selector": ".ContentItem h2 a", "count": 10, "samples": ["文章标题A", "文章标题B", "文章标题C"]}
browser_find_and_act(by="text", value="文章标题A", action="click")
browser_click_element(index="197_3i4c_uv7n")
browser_tab_switch(tabId=1412776911)
browser_eval_content_js(script="...")
browser_tab_close(tabId=1412776911)
browser_find_and_act(by="text", value="文章标题B", action="click")
browser_click_element(index="206_90r2_rddo")
browser_tab_switch(tabId=1412776913)
browser_eval_content_js(script="...")
browser_tab_close(tabId=1412776913)
```

Generated playbook:

```json
{
  "version": "1.0",
  "metadata": {
    "name": "搜索并提取文章(新Tab场景)",
    "description": "搜索主题，逐个在新Tab打开文章提取内容",
    "created_at": "2026-06-02T15:00:00Z",
    "requires_ai": false
  },
  "params": {
    "topic": { "description": "搜索关键词", "required": true },
    "count": { "description": "提取数量", "required": false, "default": "3" }
  },
  "settings": {
    "default_delay_ms": 500,
    "default_retry_count": 1,
    "step_timeout_ms": 30000
  },
  "steps": [
    {
      "action": "browser_go_to_url",
      "params": { "url": "https://example.com/search?q={{topic}}" },
      "description": "搜索主题"
    },
    {
      "action": "browser_wait",
      "params": { "seconds": 3 },
      "description": "等待搜索结果"
    },
    {
      "action": "loop",
      "params": { "count": "{{count}}", "variable": "i", "start": 1 },
      "description": "逐个在新Tab打开文章并提取",
      "steps": [
        {
          "action": "browser_find_and_act",
          "params": { "by": "css", "value": ".ContentItem h2 a", "nth": "{{i}}", "action": "click", "openInNewTab": true },
          "description": "在新Tab打开第{{i}}篇文章"
        },
        {
          "action": "browser_tab_switch",
          "params": { "tab": "latest" },
          "description": "切到文章Tab"
        },
        {
          "action": "browser_wait",
          "params": { "seconds": 2 },
          "description": "等待加载"
        },
        {
          "action": "browser_eval_content_js",
          "params": { "script": "JSON.stringify({title:document.querySelector('h1')?.textContent?.trim(),content:document.querySelector('.RichText')?.textContent?.substring(0,2000)})" },
          "description": "提取内容"
        },
        {
          "action": "browser_tab_close",
          "params": { "tab": "current" },
          "description": "关闭文章Tab"
        },
        {
          "action": "browser_tab_switch",
          "params": { "tab": "origin" },
          "description": "切回列表页"
        },
        {
          "action": "browser_wait",
          "params": { "seconds": 1 },
          "description": "等待恢复"
        }
      ]
    }
  ]
}
```

Key conversions:

- `by: "text"` + specific title → `by: "css"` + `nth: "{{i}}"`.
- `browser_click_element(index=...)` on repeated list items → merged into `browser_find_and_act`.
- `tabId: N` → `"latest"`, `"current"`, `"origin"`.
- 2+ repeated linear sequences → one `loop`.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Generating a playbook without `task_latest` | Always base playbook on an actual recording |
| Including `browser_snapshot` or `browser_get_info` in final steps | Filter them out; they are AI-decision/probe commands |
| Parameterizing `index` or `action` | Only parameterize user-controlled values |
| Using `parameters` instead of `params` | Schema key is `params` |
| Expanding N repetitions as linear steps | Use `loop` with `{{count}}` or `on_error: "break"` |
| Using `click_element` + hardcoded index in loops | Use `find_and_act` + CSS selector + `nth` |
| Using `by: "text"` or `by: "label"` with `nth` | `nth` requires `by: "css"` |
| Keeping specific titles in loop locators | Convert title-specific actions to CSS + `nth` |
| Guessing CSS selectors | Use `__list_probe__`, existing CSS locator, `list_selector`, or live probe |
| Using search keyword as loop `value` | `value` must be a CSS selector, not the keyword |
| Hardcoding physical `tabId` | Use semantic refs: `origin`, `current`, `latest`, or custom alias |
| Using `browser_go_back` after a new tab opens | Use `browser_tab_close` + `browser_tab_switch` |
| Dropping tab operations from a recording | Preserve tab behavior with semantic refs |
| Replaying a side-effecting playbook blindly | Use test data, draft mode, or explicit user approval |
