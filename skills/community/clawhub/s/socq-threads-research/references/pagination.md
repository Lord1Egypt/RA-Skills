# Pagination and Files

Successful task responses include normalized results:

```json
{
  "results": {
    "items": [],
    "has_more": true,
    "next_cursor": "..."
  }
}
```

Pass `next_cursor` back unchanged. Stop when `has_more` is false, `next_cursor` is null, or the user-requested cap is reached. MCP accepts up to 100 results per page; REST may support a larger page but portable workflows should use 100 or fewer.

Use `socq_get_files` or `socq task files TASK_ID` when the task exposes a raw JSONL export. File URLs can expire, so retrieve them promptly. Do not treat a raw provider file as normalized data unless the task documentation says so.
