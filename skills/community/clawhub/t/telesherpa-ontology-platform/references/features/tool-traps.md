# Tool traps: what agents get wrong about the API

> Reference for agents. Every item comes from a real failed or ineffective call —
> nothing here is copied from a schema.

## 1. Do not trust a number in a document — measure it

The catalogue grows with every release. The authoritative source is the service
itself:

```
GET https://mcp.telesherpa.com/health
→ {"status":"ok","serverVersion":"...","tools":<catalogue size>, ...}
```

What **your** account sees is a different number: it depends on the roles the
account carries. `auth_status` answers exactly that for the calling account.

## 2. `tools/list` needs a session

Call `initialize` first, keep the `mcp-session-id` from the response header, then
send `tools/list` with it. Without the header the server answers
`400 Missing session ID` — that reads like a broken server and is really a missing
handshake step.

## 3. Work with a member account

The tool list you receive depends on the role and the scopes of your account, not on
the service. Use a member account, and if the list looks short, read `auth_status`
for that account before you assume a server problem.

## 4. Undeclared parameters are rejected, loudly

Passing an unknown parameter returns an error that names the parameter and lists the
accepted ones:

```json
{"status":"error","error":"unknown parameter: udid","allowed":["parent","scope_id","text"],
 "hint":"A parameter without a declaration is rejected so that an ineffective call does not look like an effect."}
```

Read the list and retry. Do not transfer REST habits:

| Tool | Actual signature |
|---|---|
| `onto_object_addcomment` | `parent` (the object id), `scope_id`, `text` — no `udid`, no message kind |
| `get_document` | `filetoken` or `urlslug` — **not** the file id from an attachment list |
| `onto_settings_update` | needs `id` **and** `key` **and** `value`; `value` alone writes nothing |
| `onto_interface_index` | `limit` only, no page/per-page |
| `onto_interface_update_def` | needs `def_id` **and** `label`; without `label` it is silently ineffective |

## 5. Silent no-ops are the expensive ones

A rejected call is cheap. A call that "succeeds" without changing anything costs a
whole debugging round. Three habits:

1. **Read back after every write.** The write response describes intent; the read
   describes state.
2. **Compare a value you set, not a status code.** `{"result":"OK"}` only says the
   request was accepted.
3. **For definitions, the saved body is the truth** — save, list, and diff against
   what you sent.

## 6. Costs: who pays, and when the call stops working

The **executing account** pays. A bridge, a manager action or a proxy does not move
the bill.

| Operation | Credits |
|---|---|
| read, graph | 1 |
| set property | 2 |
| comment, link, update object, update link, bulk action per object, file upload | 5 |
| create object | 10 |
| **executing an action** | 20 |
| delete object / link / property | 20 |
| complete service order | 50 |
| file size | 1 per MB |

Scope price (one-time, per own scope, volume discount): 1st scope **100**, 2nd–3rd **80 each**,
4th–10th **60 each**, from the 11th **50 each** credits — **no upper limit** on the number of own
scopes, so `402` on scope creation always means "not enough credits". One credit is 0.01 EUR.
**There are no signup credits** — a fresh account starts at zero.

`onto_credit_pricing` returns the live table; read it at the start of a run instead
of quoting this file.

`HTTP 402` means the executing account is out of credits. It is not a server error
and not a permission error, and retrying does not help — the balance has to be
topped up by the operator. A test run that creates *and deletes* objects pays twice;
budget the deletes.

## 7. Time

- **Writes without a zone** are interpreted in the **viewer's zone** (`Europe/Berlin` by default,
  measured 2026-11-25: `2026-11-10 09:00:00` → stored `08:00:00` UTC). **Reads** come back as UTC
  plus the `_local` sibling.
- Append `Z` or an explicit offset (`2026-11-10T09:00:00Z`) and the value is taken literally — that
  is the only unambiguous form.
- Read the `_local` field when a human will read the value; never convert the UTC field yourself.

## 8. Triggers are asynchronous

A trigger does not fire inside the same call. Expect minutes, and **never** resend a
write because "nothing happened yet" — resending creates the duplicate you were
afraid of. Read the object first, then check whether the event is queued.

## 9. Large runs are processed in batches

Scheduled work does not finish every object of a big run in one tick. A plan with
many rows can look "half published" for one interval. That is the design — do not
loop the publish call to compensate, and do not assume a failure.
