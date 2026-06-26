---
name: session-rename
description: Rename OpenClaw chat sessions by updating the session history store or calling the built-in `sessions.rename` backend path. Use when the user asks to rename, retitle, relabel, or rename the current or another OpenClaw session and no first-class chat tool exists for it.
---

# Session Rename

Rename sessions by targeting the correct `session_history.displayName` record.

## Quick rules

- Determine **which OpenClaw instance** owns the session before changing anything.
- Prefer the product path when available:
  - backend method: `sessions.rename`
  - storage field: `session_history.displayName`
- If the UI/browser path is unavailable, update the DB directly.
- Update only the intended row. Do not bulk-rename all rows for a `sessionKey` unless the user explicitly wants that.

## How rename works in OpenClaw

The canonical storage is the SQLite table:

- table: `session_history`
- key: `sessionId`
- display field: `displayName`

Backend implementation:

- `src/gateway/server-methods/sessions.ts` → `sessions.rename`
- `src/config/sessions/history-db.ts` → `updateSessionName(db, sessionId, name)`

The backend ultimately runs SQL equivalent to:

```sql
UPDATE session_history
SET displayName = ?, updatedAt = ?
WHERE sessionId = ?;
```

## Workflow

1. Identify which instance owns the session.
2. Find the active row in that instance's `history.db`.
3. Prefer the row with:
   - matching `sessionKey`
   - `status='active'`
   - most recent `updatedAt`
4. Set `displayName` to the requested title.
5. Confirm by reading the updated row back.
6. Tell the user to refresh the Sessions view if the UI does not update immediately.

## Direct DB rename pattern

Use a surgical SQLite update against the target instance's session history DB.

Typical query flow:

```bash
python3 - <<'PY'
import sqlite3, time
p='/path/to/history.db'
conn=sqlite3.connect(p)
cur=conn.cursor()
row=cur.execute("select sessionId from session_history where sessionKey=? and status='active' order by updatedAt desc limit 1", ('agent:main:main',)).fetchone()
if not row:
    row=cur.execute("select sessionId from session_history where sessionKey=? order by updatedAt desc limit 1", ('agent:main:main',)).fetchone()
if not row:
    raise SystemExit('No session row found')
cur.execute(
    "update session_history set displayName=?, updatedAt=? where sessionId=?",
    ('New Session Title', int(time.time()*1000), row[0]),
)
conn.commit()
print(cur.execute("select sessionId, sessionKey, displayName, status from session_history where sessionId=?", (row[0],)).fetchone())
conn.close()
PY
```

## Finding the right DB

Typical path shape:

```text
~/.openclaw/agents/<agent-id>/sessions/history.db
```

If the location is unknown, search for SQLite DBs containing a `session_history` table before writing.

## Safety notes

- Confirm the correct instance before writing.
- Do not overwrite labels in unrelated archived rows unless explicitly asked.
- Preserve `sessionId`; only change `displayName` and `updatedAt`.
- If multiple active candidates exist, inspect before writing.

## UI caveat

A successful DB write may still require a UI refresh to show the new title. If the rename does not appear immediately, refresh the Sessions view or reconnect the UI.
