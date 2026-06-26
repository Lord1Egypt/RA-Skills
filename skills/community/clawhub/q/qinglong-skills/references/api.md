# QingLong API Reference

Base URL: `{{QINGLONG_URL}}/api`

Authentication: `Authorization: Bearer {{token}}`

Token is obtained via: `GET {{QINGLONG_URL}}/open/auth/token?client_id={{id}}&client_secret={{secret}}`

---

## Cron Jobs `/crons`

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/crons` | List all cron jobs | — |
| GET | `/crons/detail?id=<id>` | Get cron detail | — |
| GET | `/crons/<id>` | Get cron by ID | — |
| POST | `/crons` | Create cron(s) | `{command, schedule, name?, labels?}` |
| PUT | `/crons` | Update cron | `{id, command?, schedule?, name?}` |
| DELETE | `/crons` | Delete crons | `[id, ...]` |
| PUT | `/crons/run` | Run crons | `[id, ...]` |
| PUT | `/crons/stop` | Stop running crons | `[id, ...]` |
| PUT | `/crons/enable` | Enable crons | `[id, ...]` |
| PUT | `/crons/disable` | Disable crons | `[id, ...]` |
| PUT | `/crons/pin` | Pin crons | `[id, ...]` |
| PUT | `/crons/unpin` | Unpin crons | `[id, ...]` |
| GET | `/crons/<id>/log` | Get cron log file content | — |
| GET | `/crons/<id>/logs` | List cron log files | — |
| PUT | `/crons/status` | Update cron status | `{ids, status, pid?, log_path?}` |

### Cron Object

```json
{
  "id": 1,
  "name": "Task Name",
  "command": "task test.js",
  "schedule": "0 0 * * *",
  "isDisabled": 0,
  "isPinned": 0,
  "labels": ["label1"],
  "status": 0,
  "pid": null,
  "last_running_time": null,
  "last_execution_time": null,
  "log_path": null,
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

---

## Environment Variables `/envs`

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/envs` | List all envs | — |
| GET | `/envs?searchValue=<q>` | Search envs | — |
| GET | `/envs/<id>` | Get env by ID | — |
| POST | `/envs` | Create env(s) | `[{name, value, remarks?}, ...]` |
| PUT | `/envs` | Update env | `{id, name, value, remarks?}` |
| DELETE | `/envs` | Delete envs | `[id, ...]` |
| PUT | `/envs/enable` | Enable envs | `[id, ...]` |
| PUT | `/envs/disable` | Disable envs | `[id, ...]` |
| PUT | `/envs/<id>/move` | Move env position | `{fromIndex, toIndex}` |
| PUT | `/envs/pin` | Pin envs | `[id, ...]` |
| PUT | `/envs/unpin` | Unpin envs | `[id, ...]` |
| PUT | `/envs/name` | Update env name | `{ids: [...], name}` |
| POST | `/envs/upload` | Upload env file | multipart/form-data |

### Env Object

```json
{
  "id": 1,
  "name": "JD_COOKIE",
  "value": "pt_key=xxx;pt_pin=xxx",
  "remarks": "备注",
  "timestamp": 1704067200000,
  "status": 0,
  "position": 1
}
```

---

## Scripts `/scripts`

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/scripts` | List scripts | — |
| GET | `/scripts?path=<path>` | List scripts in path | — |
| GET | `/scripts/detail?file=<name>` | Get script content | — |
| GET | `/scripts/<file>` | Get script by filename | — |
| POST | `/scripts` | Upload/create script | `{filename, content?, path?}` or multipart |
| PUT | `/scripts` | Update script | `{filename, content, path?}` |
| DELETE | `/scripts` | Delete script | `{filename, path?}` |
| PUT | `/scripts/run` | Run script | `{filename, content?, path?}` |
| PUT | `/scripts/stop` | Stop script | `{filename, path?, pid?}` |
| PUT | `/scripts/rename` | Rename script | `{filename, newFilename, path?}` |
| POST | `/scripts/download` | Download script | `{filename, path?}` |

---

## Dependencies `/dependencies`

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/dependencies` | List dependencies | — |
| GET | `/dependencies/<id>` | Get dependency by ID | — |
| POST | `/dependencies` | Install dependency | `[{name, type, remark?}]` |
| PUT | `/dependencies` | Update dependency | `{id, name, type, remark?}` |
| DELETE | `/dependencies` | Delete dependencies | `[id, ...]` |
| PUT | `/dependencies/reinstall` | Reinstall | `[id, ...]` |
| PUT | `/dependencies/cancel` | Cancel install | `[id, ...]` |

### Dependency Types

| Type | Value | Description |
|------|-------|-------------|
| node | 0 | Node.js packages |
| linux | 1 | Linux packages |
| python3 | 2 | Python3 packages |

---

## Subscriptions `/subscriptions`

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/subscriptions` | List subscriptions | — |
| GET | `/subscriptions/<id>` | Get subscription by ID | — |
| POST | `/subscriptions` | Create subscription | `{type, url, alias, schedule_type, ...}` |
| PUT | `/subscriptions` | Update subscription | `{id, ...}` |
| DELETE | `/subscriptions` | Delete subscriptions | `[id, ...]` |
| PUT | `/subscriptions/run` | Run subscriptions | `[id, ...]` |
| PUT | `/subscriptions/stop` | Stop subscriptions | `[id, ...]` |
| PUT | `/subscriptions/enable` | Enable subscriptions | `[id, ...]` |
| PUT | `/subscriptions/disable` | Disable subscriptions | `[id, ...]` |
| GET | `/subscriptions/<id>/log` | Get subscription log | — |
| GET | `/subscriptions/<id>/logs` | List subscription logs | — |
| PUT | `/subscriptions/status` | Update status | `{ids, status, pid?}` |

---

## Logs `/logs`

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/logs` | List log files | — |
| GET | `/logs/<file>` | Get log content | — |
| GET | `/logs/detail?file=<name>` | Get log content (clean) | — |
| DELETE | `/logs` | Delete log | `{filename, path?}` |
| POST | `/logs/download` | Download log | `{filename, path?}` |

---

## System `/system`

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/system` | Get system info | — |
| GET | `/system/config` | Get system config | — |
| PUT | `/system/update-check` | Check for updates | — |
| PUT | `/system/update` | Update system | — |
| PUT | `/system/reload` | Reload system | `{type?}` |
| PUT | `/system/notify` | Send notification | `{title, content}` |
| PUT | `/system/command-run` | Run command (streaming) | `{command}` |
| PUT | `/system/command-stop` | Stop command | `{command?, pid?}` |
| PUT | `/system/data/export` | Export data | `{type?}` |
| PUT | `/system/data/import` | Import data | multipart |
| GET | `/system/log` | Get system log | — |
| PUT | `/system/auth/reset` | Reset auth | `{username?, password?}` |
| PUT | `/system/config/timezone` | Set timezone | `{timezone}` |
| PUT | `/system/config/log-remove-frequency` | Set log cleanup | `{logRemoveFrequency}` |
| PUT | `/system/config/cron-concurrency` | Set cron concurrency | `{cronConcurrency}` |

---

## Config Files `/configs`

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/configs/files` | List config files | — |
| GET | `/configs/<file>` | Get config file | — |
| GET | `/configs/detail?path=<name>` | Get config detail | — |
| POST | `/configs/save` | Save config file | `{name, content}` |
| GET | `/configs/sample` | Get sample files | — |

---

## Open API `/open` (for external apps)

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/open/apps` | List applications | — |
| POST | `/open/apps` | Create application | `{name, scopes}` |
| PUT | `/open/apps` | Update application | `{id, name, scopes}` |
| DELETE | `/open/apps` | Delete applications | `[id, ...]` |
| PUT | `/open/apps/<id>/reset-secret` | Reset client secret | — |
| GET | `/open/auth/token` | Get auth token | `?client_id=xxx&client_secret=xxx` |

### Available Scopes

- `crons` — Cron job management
- `envs` — Environment variable management
- `scripts` — Script management
- `logs` — Log access
- `system` — System operations
- `dependencies` — Dependency management
- `subscriptions` — Subscription management
- `configs` — Config file management

---

## Response Format

All API responses follow this format:

```json
{
  "code": 200,
  "data": { ... }
}
```

Error responses:

```json
{
  "code": 400,
  "message": "Error description"
}
```
