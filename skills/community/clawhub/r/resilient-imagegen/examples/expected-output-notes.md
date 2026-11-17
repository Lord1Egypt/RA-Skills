# Expected Output Notes

A good run output should include:

- one queue table with all jobs and attempt counts
- one failure table, even when empty
- a manifest path or planned manifest path
- inspected capability states, selected backend, and a readable selection reason
- generated file paths for completed jobs
- clear status for queued, failed, or skipped jobs
- a `chatgpt-image-handoff` pack when Computer Use or manual ChatGPT is selected
- a paid fallback recommendation only after retry limits or repeated network-like failures, with no automatic paid execution
- a downstream handoff to `cards-to-images` or `article-to-illustrations`

Do not mark the batch complete when any job remains `queued`, `running`, or `failed`.
