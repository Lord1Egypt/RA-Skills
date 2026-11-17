---
name: traecnclaw-mcp
description: Operate TraeCN through TRAECNclaw's focused stdio MCP tools. Use when an MCP-capable agent must send or stop work, choose a workspace/model/mode/conversation, inspect or change Trae settings through its UI, manage conversations, or resolve an exceptional question or command approval. Queueing, waiting, recovery, notifications, routine non-command questions, and keep/revert gates are gateway-managed.
license: MIT-0
metadata:
  author: TRAECNclaw
  version: "0.6.0"
  openclaw:
    requires:
      bins:
        - node
    primaryEnv: TRAECN_GATEWAY_TOKEN
    envVars:
      - name: TRAECN_GATEWAY_HOST
        required: false
        description: Optional gateway host override; keep loopback unless remote access is secured.
      - name: TRAECN_GATEWAY_PORT
        required: false
        description: Optional gateway port override.
      - name: TRAECN_GATEWAY_TOKEN
        required: false
        description: Optional gateway secret; never print, log, or persist it.
      - name: TRAECN_MCP_CLIENT_ID
        required: false
        description: Stable client identifier for legacy MCP task notifications.
---

# TRAECNclaw MCP

Compose focused tools around user intent. Do not call preflight, wait, poll,
event acknowledgement, recovery, cleanup, proof, process, or generic command
operations from the agent loop; the gateway owns those mechanics.

## Setup

1. Install the matching TRAECNclaw server from its source checkout or release server archive. The launcher checks the repository, an installed `traecnclaw` package, then `traecnclaw-mcp` on `PATH`; it never executes a JavaScript path selected by an environment variable.
2. Run `npm run doctor` in a source checkout. Then run `npm run --silent setup:mcp` from the checkout, or `node scripts/setup-mcp.js` from this Skill directory, to validate the server and print a resolved client entry. Use `--output FILE` to create a new mode-0600 file atomically; the command never overwrites an existing file. The JSON templates under [assets](assets) remain manual fallbacks.
3. Start the gateway with `npm run start:gateway`, then reconnect the MCP client.
4. Use mock mode only for development; never cite mock output as live TraeCN evidence.

## Choose only necessary context

- Call `traecn_open_workspace` only when the requested folder is not already open.
- Call `traecn_list_models` when the available choices matter; then call `traecn_select_model` once.
- Call `traecn_select_mode` only when the task requires a different Solo/IDE mode.
- Call `traecn_list_conversations` to read the current mode and stable conversation IDs.
- Use `traecn_create_conversation`, `traecn_select_conversation`, or `traecn_delete_conversation` for exactly one conversation operation.

These tools change TraeCN context. Never repeat workspace paths in the model
message.

## Send and track work

Call `traecn_send_message` with the exact message and, when concurrency makes
the target ambiguous, an explicit `conversationId`. Clients without the Tasks
extension receive the accepted `taskId` and status. When the host declares
`io.modelcontextprotocol/tasks` on the request, the same call returns that
durable gateway identity as `resultType: "task"`.

Do not wait or busy-poll after sending. Legacy initialization-based clients
receive compact task notifications that the stdio server acknowledges
internally. Modern hosts can open `subscriptions/listen` for the returned task
ID and receive a complete `notifications/tasks` snapshot; hosts without that
extension call `traecn_get_task` only for an intentional later status/result
read. If a modern task reports `input_required`, its elicitation and
`tasks/update` response carry the same approval safeguards documented below.
The first legacy connection for a client ID baselines retained history before
notifications start. Reusing that stable ID later resumes only durably
unacknowledged events; configure a distinct `TRAECN_MCP_CLIENT_ID` when the
host-derived name is not unique.
Use `traecn_cancel_task` for one known gateway task. Use
`traecn_stop_generation` only when the user wants the
generation currently visible in TraeCN stopped. First list conversations and
pass the active `conversationId`; the gateway rejects a stale or different
conversation. Because visible work may belong to the user or another agent,
set `acknowledgeUntrackedWork:true` and include a short audit `reason`. Use
`traecn_cancel_task` instead when the work has a gateway task ID.

For a completed task, omit `detailLevel` or pass `"result"` to retrieve only
the final answer. Pass `detailLevel: "trace"` only when the detailed visible
execution process is needed to diagnose or trace an unexpected outcome.

## Inspect or change Trae settings

Treat settings as a second-level capability. Call
`traecn_list_setting_sections`, then `traecn_list_settings` for only the needed
section. For dropdowns, call `traecn_list_setting_options` instead of guessing.
Use exactly one matching mutation tool:

- `traecn_set_setting_toggle` for a boolean switch.
- `traecn_select_setting_option` for a dropdown choice.
- `traecn_set_setting_text` for a text or numeric input.

These commands make the change through Trae's visible settings UI. The gateway
serializes UI access and returns to chat automatically; do not navigate back
manually or repeat reads after a successful write.

## Resolve exceptional interactions

The gateway never approves shell commands automatically, including commands
classified as read-only. Command text alone cannot establish workspace scope,
exclude sensitive-file reads, or account for Git configuration and external
hooks. Every command is returned to the Agent with its risk classification.

If a task reports an unresolved interaction:

- Use `traecn_answer_question` for a returned question and one of its offered answers.
- Use `traecn_decide_approval` only after checking the returned command and risk. Approval requires the exact `expectedCommand`, `acknowledgeRisk:true`, and a short audit `reason`; the gateway re-reads the visible card and rejects stale or changed commands. Denial needs no risk acknowledgement.

Conversation deletion is permanent. Delete only an inactive conversation and
only when the current user request explicitly names or unambiguously identifies
it for deletion. Re-read its listed ID and exact title, then pass the title with
`acknowledgePermanentDeletion:true`; the gateway rejects title mismatches and
the active conversation, records the attempt, and cannot restore a successful
deletion. This uses the user's existing instruction and does not add a separate
confirmation round trip.

## Safety

- Keep the gateway on `127.0.0.1` unless remote access is secured.
- Never expose `.env`, tokens, authorization headers, or TraeCN profile data.
- Keep the default security audit log enabled; high-impact approvals, stops,
  and deletions are written to date-based JSONL files with sensitive fields
  redacted and a default 30-day retention.
- Treat mock results and non-terminal task states as incomplete.
- Do not recreate removed low-level tools through shell, generic commands, or GUI control.

Read [references/mcp-surface.md](references/mcp-surface.md) only for exact
schemas, protocol compatibility, notification behavior, and gateway ownership
boundaries.
