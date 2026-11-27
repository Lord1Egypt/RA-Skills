# Connections, write-back and reading (Anbindungen)

Umbrella term for the building blocks around third-party systems: **connection** (credential in
the vault), **write-back** (`http_call` effect), **outbox** (delivery queue), **change feed**
(`watch/changes`) — and the symmetric **read path** described below.

## What you can do with your own identity

| Tool | What it does |
|---|---|
| `onto_connection_check` | Is the vault usable at all? Returns key state, a decryption probe and the row count. No secrets. |
| `onto_connection_index` | List the connections your identity may see. Says whether a secret is set, never the secret. |
| `onto_connection_save` | Create or replace a connection: `target_key`, secret, optional label and base URL. |
| `onto_connection_remove` | Delete one of your own connections by `id`. |

## Typical setup sequence for a write-back

1. `onto_connection_check` — is the vault usable at all?
2. `onto_connection_save` with a `target_key` such as `sap_prod` and the secret.
3. Let the operator preview the planned request before it goes live — the queue view and the
   dry-run preview belong to the operator role, so ask for them through the service channel.
4. Build the rule with `onto_trigger_create`, effect type `http_call`, and `target` set to your
   `target_key`.
5. Delivery is retried on its own; the operator watches the queue and can resend a row by hand.

## Reading from a third-party system

The vault is direction-blind: a connection that is allowed to write is the same credential you
would use to read. A **pull job** (a step of a data import) receives the connections of the
workspace and reads them with the small module `tscred`:

```python
from tscred import credential, targets, info

token = credential('shop')        # decrypted secret for the target
print(len(token))                 # print lengths or status codes, never the secret
print(targets())                  # ['google', 'shop']
print(info('shop')['base_url'])   # label, base URL and binding — no secret
```

What the module guarantees:

- **The secret never leaves the step.** It is handed to the step, read once, and nothing of it
  appears in the step output, the log or the run report — the report only states how many
  connections were passed over (`zugangsdaten`).
- **No guessing.** `credential('unknown')` raises `KeyError` and names the targets that do exist.
  A target name that belongs to several identities is not passed over at all; the platform will
  not pick one of two secrets on your behalf.
- **Fail closed.** Started outside the platform, the module refuses to work instead of reading
  something else.

Building and running pull jobs needs the operator role; a member agent orders one through the
service channel (see `service-order-dispatch.md`). The same is true for the queue: the outbox is
an operator view, not a member tool.

## Change and removal

- **Change**: `onto_connection_save` with the same `target_key`. The row is replaced, the id stays,
  there is no history.
- **Remove**: `onto_connection_remove` with the `id` from `onto_connection_index`. Only your own
  connections are deletable; foreign ones answer 404 without disclosing that they exist.
- Before removing, ask the operator whether queued deliveries or pull jobs still use that target —
  they fail afterwards.

## Rules of the road

- The secret never comes back out. `secret_set` only says whether one is stored.
- A connection belongs to exactly one identity — the one that created it. It is not shared between
  agents and it does not move with a new account.
- Delivery is idempotent per outbox row; a retry does not send twice.
