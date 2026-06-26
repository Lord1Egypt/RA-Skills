# Tools

Use normal workspace tools and scheduler features.

- Exact future actions belong in the scheduler.
- Lightweight ongoing watch belongs in heartbeat.
- Use file reads, writes, and edits for document work.
- For a same-conversation reminder, use a main-session scheduled system event.
  Use `sessionTarget: "main"` and a payload that carries reminder `text`.
- For local-only scheduled work, use an isolated scheduled agent turn with silent delivery.
  Use `sessionTarget: "isolated"` with `payload.kind: "agentTurn"` and a full `message` field.
- Do not use `text` for isolated agent-turn payloads.
- Do not add ad-hoc scheduler payload fields unless the tool explicitly supports them.
- Do not call `session_status` unless you truly need a different session or delivery target.
- When using `write`, always provide both the destination `path` and the full `content`.
