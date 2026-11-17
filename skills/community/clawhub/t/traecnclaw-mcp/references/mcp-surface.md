# MCP surface

TRAECNclaw exposes one focused Agent surface. There are no tool profiles.

## Protocol and transport

- MCP `2026-07-28`: stateless per-request `_meta`, `server/discover`, typed
  results, structured tool content, server identity metadata, and cache hints.
- MCP `2025-11-25` and `2024-11-05`: legacy `initialize` compatibility.
- stdio: one compact JSON-RPC object per line. `Content-Length` framing is
  accepted only as a migration compatibility path.

MCP contract version 5 below identifies this Skill's frozen 20-tool surface;
it is not an MCP protocol revision. Legacy clients receive compact
`notifications/message` task events. For MCP `2026-07-28`, the server advertises
the separately negotiated `io.modelcontextprotocol/tasks` extension. An
opted-in `traecn_send_message` returns the durable gateway ID as a Task;
`tasks/get`, `tasks/update`, and `tasks/cancel` operate that same identity, and
`subscriptions/listen` can stream exact-ID `notifications/tasks` snapshots.
For a legacy client ID's first connection, already-retained events are
baselined without delivery; a returning ID resumes only events newer than its
durable acknowledgement. Unrelated request metadata such as `progressToken`
does not change the negotiated legacy protocol era.
Modern retries derive a stable idempotency key from the request identity and
arguments. The gateway retains the corresponding terminal fingerprint and
response across restart for a configurable 24-hour default TTL, so the same
request reuses the original task while different work cannot collide.
Clients that do not opt in retain the ordinary complete result and use
`traecn_get_task` only for an intentional read. The extension is upstream-draft
and does not change the 20-tool contract.

| Tool | Required input | Gateway route |
| --- | --- | --- |
| `traecn_send_message` | `message` | `POST /api/tasks/submit` |
| `traecn_get_task` | `taskId`; optional `detailLevel` (`result` or `trace`) | `GET /api/task/{taskId}` |
| `traecn_cancel_task` | `taskId` | `POST /api/task/{taskId}/cancel` |
| `traecn_stop_generation` | `conversationId`, `acknowledgeUntrackedWork`, `reason` | `POST /api/trae/stop-generation` |
| `traecn_open_workspace` | `path` | `POST /api/open-project` |
| `traecn_list_models` | none | `GET /api/models` |
| `traecn_select_model` | `model` | `POST /api/switch-model` |
| `traecn_select_mode` | `mode` | `POST /api/switch-mode` |
| `traecn_list_setting_sections` | none | `GET /api/settings/sections` |
| `traecn_list_settings` | `section` | `GET /api/settings/read` |
| `traecn_list_setting_options` | `section`, `label` | `GET /api/settings/options` |
| `traecn_set_setting_toggle` | `section`, `label`, `enabled` | `POST /api/settings/set` |
| `traecn_select_setting_option` | `section`, `label`, `value` | `POST /api/settings/set` |
| `traecn_set_setting_text` | `section`, `label`, `text` | `POST /api/settings/set` |
| `traecn_list_conversations` | none | `GET /api/conversations` |
| `traecn_create_conversation` | none | `POST /api/conversations/manage` |
| `traecn_select_conversation` | `conversationId` | `POST /api/conversations/manage` |
| `traecn_delete_conversation` | `conversationId`, `expectedTitle`, `acknowledgePermanentDeletion` | `POST /api/conversations/manage` |
| `traecn_answer_question` | `answer` | `POST /api/interactions/resolve` |
| `traecn_decide_approval` | `decision`; approve also needs `expectedCommand`, `acknowledgeRisk`, `reason` | `POST /api/interactions/resolve` |

`traecn_send_message` accepts only `message` and optional `conversationId`.
Set workspace, model, mode, and conversation through their focused tools. New
conversations are explicit and messages otherwise stay in the selected chat.

After message acceptance the gateway owns persistence, external and local
queues, recovery, completion checks, notifications, routine non-command
questions, and keep/revert gates. Agents do not wait, poll, acknowledge
events, run preflight, or recover work. A supporting host owns the Tasks
subscription; `traecn_get_task` is an optional explicit fallback read, not a
polling instruction. Its default `detailLevel: "result"`
returns only the final answer; use `detailLevel: "trace"` when a failure or
unexpected result requires the visible execution process for diagnosis.

Settings tools form a second level: list visible sections, then list only one
section's items and their `controlType`. List dropdown options before selecting
one. Each write tool maps to one exact UI control operation, while the gateway
opens settings and restores chat automatically.

No shell command is approved automatically, including commands classified as
read-only. Command text alone cannot establish workspace scope, exclude
sensitive-file reads, or account for Git configuration and external hooks.
Every command goes to Agent review. Approval requires the exact visible
command, `acknowledgeRisk:true`, and a short audit reason; the gateway rejects
stale command cards. Every high-impact Agent decision is written to the local
append-only security audit log.

The direct stop action works only in Solo mode and only when its supplied ID
still matches the active conversation. It requires an acknowledgement that the
visible generation may be untracked plus an audit reason. Conversation delete
requires an inactive target, exact listed title, and permanent-deletion
acknowledgement; it has no recovery path. Unsafe-command approval revalidates
the exact currently visible command and records the risk acknowledgement and
reason before clicking.
