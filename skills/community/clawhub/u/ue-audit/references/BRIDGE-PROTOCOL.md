# Optional editor bridge protocol

Live checks are optional. `ue-audit` talks to a small local HTTP bridge. The bridge is not bundled; implement it in your editor plugin or use an existing compatible bridge.

## Transport

- Base URL: `http://127.0.0.1:8889` by default (`UE_AUDIT_BRIDGE_PORT`)
- Auth: `X-Skill-Token: <token>` or `Authorization: Bearer <token>`
- Token sources: `--token`, `UE_AUDIT_BRIDGE_TOKEN`, `UE_AUDIT_BRIDGE_TOKEN_FILE`, `%APPDATA%\ue-audit\bridge-token`

## Endpoints

### `GET /health`

```json
{
  "status": "ok",
  "bridge_version": "0.5.0",
  "ue_info": {
    "bridge_loaded": true,
    "engine_version": "5.1.1-...",
    "project_name": "MyGame",
    "project_dir": "C:/Projects/MyGame"
  }
}
```

Flat fields are also accepted.

### `POST /command`

Request:

```json
{ "command": "read_blueprint", "params": { "bp_path": "/Game/BP_Test", "level": "L2" } }
```

Response:

```json
{ "success": true, "command": "read_blueprint", "result": {}, "error": "" }
```

On failure: `{"success": false, "error": "..."}`.

## Read commands used by v0.4

| Command | Params | Used by |
|---|---|---|
| `health` | none | LIVE001 |
| `read_blueprint` | `bp_path`, `level=L1/L2`, `include_cdo`, `include_conn` | BP001 |
| `datatable_read` | `asset_path`, `limit`, `include_csv` | DT001 |
| `widget_read_tree` | `widget_path` | UMG001 |
| `material_read` | `material_path` | MAT001 |
| `animbp_probe` | `asset_path` | ANIM001 |
| `animbp_read` | `asset_path`, `include_nodes`, `limit` | ANIM001 |
| `pie_state` | none | PIE001 |
| `logs_read` | `lines`, `cursor` | PIE001 |
| `pie_start` | `mode` | PIE001 (opt-in) |
| `pie_stop` | none | PIE001 (opt-in) |

`pie_start`/`pie_stop` are the only stateful commands. They are only called when the user passes `--pie`, and `pie_stop` is called in a `finally` block.

## Read-only rule

The client allow-lists read commands. Any other command is rejected before it reaches the bridge. `--pie` adds only `pie_start`/`pie_stop` through a separate stateful entry point.

The bridge is responsible for its own authentication and for ensuring that the listed commands are read-only in its implementation.
