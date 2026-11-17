# Command Extended Reference

> Load this file when you need the detailed usage guide for `browser_snapshot --markdown` or the `browser_replay` output format.
>
> For command syntax signatures, see the main [SKILL.md](../SKILL.md#commands).

---

## 📖 `browser_snapshot --markdown`: Usage Guide

`--markdown` returns clean, human-readable Markdown of the page (ads/nav/scripts stripped, **no element indices**). It is designed to feed page content **into the AI's context for reading**, not to drive further browser commands.

**✅ Use it when:**

- **Reading / summarizing** page content (articles, docs, search results, product detail pages)
- **One-off Q&A** about a page ("what does this article say?", "summarize this doc")
- Running in **non-recording mode (Branch C)** — the output is consumed by the AI once and discarded

**❌ Do NOT use it when:**

- Inside `task_begin` / `task_end` (**recording mode, Branch B**) — Markdown output is a text snapshot and cannot be reliably replayed
- You need **structured data** (JSON, specific fields, machine-consumable output) → use `browser_eval_content_js`
- You need to **iterate** over a list, paginate, or extract many items → use `browser_eval_content_js` + `browser_find_and_act`
- You need to **click / input / interact** with elements → use `browser_snapshot` (default mode, returns indices)

**Rule of thumb:** `--markdown` output goes to the **AI's eyes** (read once, then discarded). If the output needs to be consumed by **code, a playbook, or a later step**, use `browser_eval_content_js` instead.

---

## `browser_replay` Output Format

```json
{
  "success": true,
  "total_steps": 5,
  "completed_steps": 5,
  "step_results": [
    {
      "index": 0,
      "action": "browser_go_to_url",
      "description": "...",
      "success": true,
      "result": "Success! Navigated to ..."
    },
    {
      "index": 1,
      "action": "browser_eval_content_js",
      "description": "提取数据",
      "success": true,
      "result": "{\"title\":\"...\",\"content\":\"...\"}"
    }
  ],
  "duration_ms": 12345,
  "summary": "Replay completed successfully: 5/5 steps in 12345ms."
}
```

**How to use the output (especially for composite tasks):**

- `success`: Check overall success/failure. If `false`, check `failed_step` for error details.
- `step_results[N].result`: Contains the return value of each step. **For `browser_eval_content_js` steps, this is the extracted data (usually JSON string)** — parse it for use in subsequent AI processing or next playbook's variables.
- For composite pipelines: find all `eval_content_js` steps in `step_results`, parse their `result` field to get structured data for AI mediation.

---

## If `browser_replay` Returns Failure

When replay finishes with `success: false`:

- Inspect `failed_step`, `summary`, and the failed entry in `step_results` before deciding the next action.
- Do **not** immediately retry the same replay on a live target.
- Do **not** automatically fall back to manual execution for side-effecting tasks such as posting, submitting, messaging, purchasing, deleting, or publishing.
- For read-only tasks, manual fallback is acceptable only when the failure is clearly non-destructive.
- For side-effecting tasks, require user confirmation, draft mode, sandbox/test data, or another safer path before continuing.
