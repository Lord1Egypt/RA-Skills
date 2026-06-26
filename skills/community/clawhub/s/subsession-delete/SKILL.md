---
name: subsession-delete
description: Delete an OpenClaw child session cleanly by removing its transcript, trajectory files, and sessions.json index entry.
input: sessionKey or sessionId
output: deleted files, updated index status, verification result
---

# Subsession Delete

Use this skill when you need to remove a spawned child session cleanly so it disappears from both disk and the session index/UI.

## Scope
This skill removes a child session by:
- deleting the main transcript `.jsonl`
- deleting related `.trajectory.jsonl` and `.trajectory-path.json`
- removing matching entries from `sessions.json`
- verifying the session no longer appears in session listings

## Safety boundary
- Treat this as destructive local deletion.
- Confirm the exact target session before execution.
- Prefer deleting child/subagent test sessions, not active primary sessions.
- Default to dry-run first unless the user explicitly wants immediate deletion.

## Recommended command
```bash
python3 skills/subsession-delete/scripts/delete_subsession.py \
  --session-key 'agent:subtest2:subagent:EXAMPLE' \
  --execute
```

You can also target by session id:
```bash
python3 skills/subsession-delete/scripts/delete_subsession.py \
  --session-id '3e16bcb6-998c-45dd-9906-001792b8b706' \
  --agent-id subtest2 \
  --execute
```

## Behavior
1. Resolve the agent/session target from `sessionKey` or `sessionId`
2. Load the target agent's `sessions.json`
3. Identify all matching session files
4. Delete the files that exist
5. Remove matching `sessions.json` records
6. Verify the session id/key no longer appears in the index

## Report back
Return:
- target session key/id
- deleted file paths
- whether `sessions.json` changed
- verification result

## Guardrails
- Do not guess the target session.
- Do not delete unrelated sessions in the same folder.
- If the session is missing on disk but still indexed, clean the index too.
- If the session is active/running, stop and ask before forcing deletion.
