# Cross-platform Research

Use a comparable collection frame across platforms:

1. Define the entity, keywords, date window, and desired record count once.
2. Map each platform to the closest supported endpoint; do not force identical parameters where schemas differ.
3. Estimate the combined cost and confirm large scopes.
4. Submit platform tasks with distinct idempotency keys.
5. Poll independently so one slow provider does not block completed platforms.
6. Paginate to the same target depth where possible.
7. Compare normalized fields such as author, text, metrics, URL, and publication time.
8. Label platform-specific gaps and unavailable filters.

Prefer filtered MCP configuration for planned research, for example `?platforms=youtube,tiktok,x`. Use compact discovery when the appropriate platforms are not known in advance.
