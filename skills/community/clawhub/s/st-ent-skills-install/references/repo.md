# st-ent-mcp repository notes

Repo:

- https://github.com/st699pic/st-ent-mcp

README-derived basics:

- Node.js 22+
- Required env:
  - `SERVICE_API_BASE_URL`
  - `SERVICE_API_KEY`
- Use a least-privilege `SERVICE_API_KEY`
- Start command:
  - `node mcp/server.js`

Review before execution:

- Verify the GitHub repository URL and homepage/source identity before cloning or pulling.
- Inspect `mcp/server.js` before starting the server.
- If audit is incomplete, run install and smoke tests in an isolated container or VM.

Available tools mentioned in the repo README:

- `search_photos`
- `search_videos`
- `download_asset`
- `get_download_records`
- `check_downloaded`

Example stdio MCP client shape:

```json
{
  "command": "node",
  "args": ["/absolute/path/to/mcp/server.js"],
  "env": {
    "SERVICE_API_BASE_URL": "https://co-api.699pic.com",
    "SERVICE_API_KEY": "st_ent_xxx"
  }
}
```

OpenClaw-specific recommendation:

- Prefer project-scoped `mcporter` registration when the request is about local OpenClaw integration.
- After install, verify both `mcporter list <name> --schema` and one real `mcporter call ...`.
