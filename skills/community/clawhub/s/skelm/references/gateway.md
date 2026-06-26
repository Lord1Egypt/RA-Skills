# Gateway Reference

## What the gateway is

The gateway is a long-running process that is the **trust boundary** for all skelm security infrastructure. It owns:

- **Permission resolution** — intersects project defaults, profiles, and step-level policies into a `ResolvedPolicy`.
- **Permission enforcement** — `TrustEnforcer` is called before any privileged action (tool call, exec, MCP attach, network request, fs access).
- **Secret resolution** — resolves secret references before passing values to backends.
- **Audit log** — writes a tamper-evident, hash-chained audit trail for every privileged action.
- **Approval gating** — queues actions for human approval; the runtime calls `runtime.approvalGate.request(...)` at the start of every agent step whose policy declares `approval`.
- **Trigger dispatch** — receives cron, webhook, interval, and queue triggers; starts runs accordingly.
- **Registry management** — watches workflow, skill, and MCP server directories; hot-reloads on change.
- **ACP session persistence** — survives gateway restarts; sessions are re-attached on startup.

**Never write enforcement logic in pipeline or step code.** Pipelines are the user layer; the gateway is the trust layer.

## Starting the gateway

```bash
skelm gateway start               # foreground; SIGTERM/Ctrl-C drains and exits
skelm gateway status              # pid, URL, state
skelm gateway stop                # SIGTERM a running gateway
skelm gateway reload              # SIGHUP — hot-reloads skelm.config.ts
skelm gateway install --systemd   # install ~/.config/systemd/user/skelm-gateway.service
```

`skelm gateway start` always runs in the foreground; pass `--detach` and the CLI will tell you to spawn it via systemd or a shell wrapper instead. For long-running deployments, install the systemd unit.

The gateway is required for:
- Agent steps (permission enforcement, backend lifecycle)
- Trigger-based execution (cron, webhook, etc.)
- Approval gating
- History and audit storage via SQLite

`skelm run` works without the gateway for simple pipelines (no agent steps, in-memory run store).

## HTTP surface

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check |
| GET | `/registry/workflows` | List discovered workflows |
| POST | `/runs` | Start a run (sync or async) |
| GET | `/runs/:id` | Fetch run state |
| GET | `/runs/:id/events` | SSE event stream |
| POST | `/runs/:id/cancel` | Cancel a run |
| POST | `/runs/:id/resume` | Resume a `wait()` step |
| POST | `/approvals/:id/approve` | Approve a gated action |
| POST | `/approvals/:id/deny` | Deny a gated action |
| GET | `/audit` | Query audit log |

Default port: `14738`, default host: `127.0.0.1`. Configure via `server.port` and `server.host` in `skelm.config.ts`.

## Run events (SSE)

Connect to `GET /runs/:id/events` for a server-sent event stream. Events include:

- `run.started`, `run.completed`, `run.failed`, `run.cancelled`
- `step.started`, `step.completed`, `step.failed`, `step.skipped`
- `permission.denied` — emitted when enforcement blocks an action
- `tool.called`, `tool.result`

## Audit log

The gateway writes every privileged action to a hash-chained SQLite audit log. Query via:

```bash
skelm audit query --run <runId>
skelm audit query --action permission.denied --since 2025-01-01T00:00:00Z
```

## systemd integration

```bash
skelm gateway install --systemd    # writes ~/.config/systemd/user/skelm-gateway.service
systemctl --user enable skelm-gateway
systemctl --user start  skelm-gateway
```
