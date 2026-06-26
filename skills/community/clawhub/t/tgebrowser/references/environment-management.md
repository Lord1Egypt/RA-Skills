# Environment Management

**mcp__tgebrowser__open-browser** — Open a browser environment.

- **envId** (optional): Environment id to open.
- **userIndex** (optional): Environment index to open. One of envId or userIndex is required.
- **args** (optional): Extra browser launch args, e.g. `["--headless"]`.
- **port** (optional): Custom remote debugging port.

Returns: `envId`, `userIndex`, WebSocket URL (`ws`), `http`, `port`. Use the ws URL with mcp__tgebrowser__connect-browser-with-ws to enable automation.

**mcp__tgebrowser__close-browser** — Close a browser environment.

- **envId** (optional): Environment id to close.
- **userIndex** (optional): Environment index to close. One of envId or userIndex is required.

**mcp__tgebrowser__create-browser** — Create a browser environment.

- **browserName** (required): Environment name.
- **proxy** (required): Proxy config. Must include at minimum `protocol`. Use `{"protocol":"direct"}` for no proxy. See [proxy-config.md](proxy-config.md).
- **groupId** (optional): Group id (number). Omit for ungrouped.
- **remark** (optional): Remarks.
- **fingerprint** (optional): Fingerprint config. `os` is required when provided (e.g. `"Windows"`, `"macOS"`, `"Android"`, `"iOS"`). See [fingerprint.md](fingerprint.md).
- **startInfo** (optional): Startup config with `startPage` and `otherConfig`.
- **Cookie** (optional): Cookie data.

**mcp__tgebrowser__update-browser** — Update a browser environment.

- **envId** (required): Environment id to update.
- **browserName** (required): Environment name.
- **groupId**, **remark**, **proxy**, **fingerprint**, **startInfo**, **Cookie** (all optional).

**mcp__tgebrowser__delete-browser** — Delete a browser environment.

- **envId** (optional): Environment id to delete.
- **userIndex** (optional): Environment index to delete. One of envId or userIndex is required.

**mcp__tgebrowser__get-browser-list** — Get the list of browser environments.

- **current** (optional): Page number, default 1.
- **pageSize** (optional): Results per page.
- **keyword** (optional): Search keyword.
- **groupId** (optional): Filter by group id (number).

**mcp__tgebrowser__get-opened-browser** — Get the list of currently opened browser environments.

- No parameters.

**mcp__tgebrowser__get-profile-cookies** — Get cookies of a browser environment.

- **envId** (optional): Environment id.
- **userIndex** (optional): Environment index. One of envId or userIndex is required.

**mcp__tgebrowser__get-profile-ua** — Get User-Agent of a browser environment.

- **envId** (optional): Environment id.
- **userIndex** (optional): Environment index. One of envId or userIndex is required.

**mcp__tgebrowser__close-all-profiles** — Close all opened browser environments on the current device.

- No parameters.

**mcp__tgebrowser__new-fingerprint** — Generate a new random fingerprint for a browser environment.

- **envId** (optional): Environment id.
- **userIndex** (optional): Environment index. One of envId or userIndex is required.

**mcp__tgebrowser__delete-cache** — Clear local cache of a browser environment. Ensure the browser is closed before using.

- **envId** (optional): Environment id.
- **userIndex** (optional): Environment index. One of envId or userIndex is required.

**mcp__tgebrowser__get-browser-active** — Get active (opened) browser environment information.

- **profileId** (optional): Profile ID.
- **profileNo** (optional): Profile number.
