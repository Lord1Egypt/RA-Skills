# Error recovery

Error patterns the daemon emits and what to do about each. Quota and
upgrade-required errors live in `references/free-tier.md` since they're
inseparable from free-tier handling. 

## Quick reference

| Symptom | What to do |
|---|---|
| `accepted: false` on `connect` or `disconnect` | An earlier op is still in flight. One retry after one `xvpn_get_status` read. See "Lock conflict" below. |
| Long-running `connect` that never resolves | `xvpn_cancel_operation(operation_id)` from the last status. |
| Tool returns a shape you don't recognize | Don't guess. Surface the raw response and ask the user how to proceed. |
| `connect` fails with `location not found: <slug>` | Either a typo (see `references/locations.md`) or a tier mismatch — free accounts on non-free slugs get an upgrade message instead, but premium accounts on `free/...` slugs get exactly this. See `references/free-tier.md`. |
| Connect failed with quota or upgrade message | See `references/free-tier.md`. |

## Lock conflict (`accepted: false`)

The daemon serializes write operations through an IPC lock. If another
tool call is in flight when you issue `connect` or `disconnect`, you get
`accepted: false` immediately.

Recovery:

1. Call `xvpn_get_status` once.
2. Read `operation_inflight`. If true, the previous op is still running —
   wait one beat (don't tight-poll), then retry your call once.
3. If the second call also returns `accepted: false`, surface the error
   to the user. Don't loop.

This usually resolves in well under a second; the lock is short-lived.

## Cancellable operations

Some operations carry an `operation_id` (visible in `xvpn_get_status`
under `active_operation`). If `connect` is taking too long or the user
changed their mind:

```
xvpn_cancel_operation(operation_id="<id from xvpn_get_status>")
```

Returned shape:

- `cancelled: true` — successfully aborted.
- `cancelled: false` — the op already finished or wasn't cancellable.
- `strategy` — describes how the cancel was applied.

After a cancel, call `xvpn_get_status` once to confirm state before
issuing a new `connect`.

## Unknown response shapes

The daemon evolves; new fields can appear in responses. Two rules:

1. **Read what you understand, ignore what you don't.** Extra keys are
   not errors.
2. **Don't fabricate.** If a response is missing a field you need (like
   `accepted` or `status`), surface the raw response to the user instead
   of guessing what it might mean.

## Don't loop

Across all error paths, the rule is the same: **one retry, then surface**.
The user benefits more from a clear error message than from a tool-call
storm. Looping also burns tokens fast and can hold the IPC lock open
longer than it needs to be.
