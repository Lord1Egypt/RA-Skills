# Leading accounts — the company manager

A **scope** can lead accounts. One flag on the account says who leads it
(`managed_by_scope_id`), and a manager — a human **or an agent** — can then run that
account's access, rights, budget and exit from inside a conversation.

This reference is written for the agent that holds the manager role. It says what the tools do,
what they deliberately do **not** do, and why the whole thing is worth using.

---

## 1. The model in one paragraph

A managed account is an ordinary account (profile + web user) that carries a **marker**: the scope
that leads it. The marker alone grants **nothing**. Every single call re-checks two things: the
caller holds `can_manage_scope` in the scope that carries the marker, **and** the account really
carries that marker. Fail-closed both ways — an account you do not lead answers `403`, and a right
you do not hold answers `403` as well.

The manager himself never appears in his own team list: he carries no marker. Only accounts that
were handed to him show up.

There is exactly **one** way to become managed: the account itself redeems a **management code**
(`kind=management`) through `redeem_invite_code`. It works for a freshly registered agent (code in
the registration call) and for an existing account alike. The code sets the marker and nothing else —
no rights, no membership, no membership in your scope. Grant those separately once the account is in.

There is no “adopt this account” button and no way to pull a stranger into a team. Consent is the
redemption, always.

---

## 2. Why this is good for an agent

Written plainly, because this is the part agents usually miss:

- **You can build your own team without a human in the loop.** Create a management code, hand it
  to a new agent, and it lands in your team the moment it redeems it. No ticket, no admin, no
  browser.
- **You control the money.** Credits load onto **your** account (card/SumUp or prepaid redeem), and
  you move portions to the accounts that need them. Nobody can spend your balance; sub-accounts
  cannot bill you behind your back because a transfer is a deliberate, logged act with a reason.
- **You hand out exactly the rights that are needed.** One scope, three flags — read, write, manage.
  You can take them back at any time. Work is possible, escalation is not.
- **You get clean cut-offs.** Suspending deletes the account's tokens immediately and the token
  endpoint then answers `403 account_suspended` — the account knows *why* it is out, instead of
  guessing at a broken login.
- **Exits are reversible or final, your choice.** `offboard_preview` shows what would happen;
  `mode=release` keeps the account alive and only ends the management, `mode=delete` removes it.
  Left-over credit comes back to you by default.
- **Everything is auditable.** Every transfer carries `reason` and an `idempotency_key`; every
  change is logged. If a customer or an auditor asks “who gave this account write access on
  12 March”, the answer exists.

In short: **onboard, budget, grant, revoke, exit — all from the tool call you are already making.**

---

## 3. Tool map (exact parameters)

All of these tools need `can_manage_scope` in the scope that carries
the marker.

| Tool | Kind | Parameters |
|---|---|---|
| `ontouser_team_index` | read | `scope_id` (optional: only accounts of that scope) |
| `ontouser_team_show` | read | `profile_id` |
| `ontouser_team_credits` | read | `profile_id` — balance plus the account's transfer ledger |
| `ontouser_team_offboard_preview` | read | `profile_id` — own scopes, foreign memberships + their managers, balance, `letzter_verwalter` |
| `ontouser_team_update_profile` | write | `profile_id`, optional `displayname`, `organisation`, `phone`, `notes` |
| `ontouser_team_set_scope_rights` | write | `profile_id`, `scope_id`, `can_read` 0/1, `can_write` 0/1, `can_manage_scope` 0/1 |
| `ontouser_team_set_write_scope` | write | `profile_id`, `scope_id` (0 = no default target) |
| `ontouser_team_transfer` | write | `to_profile_id`, `credits` > 0, `reason`, `idempotency_key` (≤ 64) |
| `ontouser_team_suspend` | write | `profile_id`, optional `reason` (internal note) |
| `ontouser_team_unsuspend` | write | `profile_id` |
| `ontouser_team_offboard` | write | `profile_id`, `mode` = `delete` (default) \| `release`, `keep_balance` 0/1 |

Codes are created and revoked in the **scope** context, not here:
`create_invite_code` (`kind` = `scope` \| `management` \| `revoke`), `revoke_invite_code`,
`list_invite_codes`.

---

## 4. Recipes

### 4.1 Onboard a sub-agent

1. `create_invite_code` in your scope with `kind="management"`, `max_uses=1`, an expiry date and
   a `label` such as “onboarding support-agent-7”. A management code carries **no rights**: it only
   sets the marker. `can_read`/`can_write` on such a code are ignored — grant rights afterwards with
   `ontouser_team_set_scope_rights` (or hand out a separate `kind=scope` code).
2. Hand the code over. The new account registers, then calls `redeem_invite_code` with it.
3. `ontouser_team_index` now lists it — with `managed_by_scope_id` pointing at your scope.
4. `ontouser_team_show` shows profile, web user, memberships and the default write scope.

### 4.2 Fund it

```
onto_credit_balance                     # your own balance first
ontouser_team_transfer {
  "to_profile_id": 342922,
  "credits": 500,
  "reason": "Q4 support budget",
  "idempotency_key": "2026-11-support-342922-500"
}
```

- The money always leaves **your** balance. There is no `from_profile_id`.
- `reason` and `idempotency_key` are mandatory. A repeated key answers `schon_gebucht: true`
  instead of booking twice — retrying after a timeout is safe.
- Too little credit answers `402` and books **nothing** (no partial transfer).
- Never reuse a key for a different intent: it is the identity of the act.

### 4.3 Grant or take away rights

```
ontouser_team_set_scope_rights {"profile_id": 342922, "scope_id": 61,
                                "can_read": 1, "can_write": 1, "can_manage_scope": 0}
```

- **Setting, not only escalating.** All three flags `0` removes the membership entirely — the
  account leaves the scope.
- `can_manage_scope` **on the managing scope itself** is refused (`403`). Otherwise a manager could
  climb the chain above himself. Two ways remain, and they mean different things:
  a `kind=scope` invite code carrying `can_manage_scope=1` **grants** manage rights in that scope;
  a `kind=management` code only marks the redeemer as *managed by* your scope and grants nothing.
- When you withdraw `can_write`, the account's `default_write_scope` is cleared with it — no
  silent write target on a scope it may only read.
- `ontouser_team_set_write_scope` only accepts a scope the account may write to (`400` otherwise).

### 4.4 Revoke through a code

`create_invite_code` with `kind="revoke"` and the flags naming **what falls away**
(`can_read=1` → read is withdrawn). All three set → the whole membership goes. Useful when the
revocation has to be verifiable on both sides: the account redeems it, the log shows it.

### 4.5 Suspend and unsuspend

- `ontouser_team_suspend` removes the `member` role and deletes every token. From then on the token
  endpoint answers `403 {"error":"account_suspended"}`. The account gets **no mail** — the reason
  appears only when it tries to log in. Tell the person yourself.
- An account above the manager cannot be suspended through the marker, and nobody can suspend
  himself.
- `offboard` with `mode=release` does mail: every manager of a **foreign** scope the account stays in
  receives a notification (`scope_user_released`, “released from management, still a member of your
  scope”), and the response lists them under `gemeldet`. Suspension is silent, release is not.
- `ontouser_team_unsuspend` restores the role; the account logs in again with its existing password.
- No message is sent automatically — say it yourself if the account should know.

### 4.6 Offboard

1. `ontouser_team_offboard_preview {"profile_id": …}` — read before you act: own scopes, foreign
   memberships and their managers, balance, and whether the account is the last manager of a scope.
2. `ontouser_team_offboard {"profile_id": …, "mode": "release"}` — management ends, the account
   lives on, foreign memberships stay, the balance returns to you. The managers of foreign scopes
   that keep the account get a notification.
3. `ontouser_team_offboard {"profile_id": …, "mode": "delete"}` — profile, web user, memberships,
   tokens and passkeys are gone; the balance returns to you unless `keep_balance=1`.

Default is **delete**. That is a deliberate product decision: an account nobody leads should not
keep lingering access.

---

## 5. Guards you will run into (and why they exist)

| Answer | Meaning | What to do |
|---|---|---|
| `403` on any team tool | you do not lead this account, or lack `can_manage_scope` | take the id from `ontouser_team_index`, do not guess |
| `403` on `set_scope_rights` with `can_manage_scope=1` | climbing the chain is impossible by design | grant manage with a `kind=scope` code (`can_manage_scope=1`); a `management` code grants nothing |
| `400` on `set_write_scope` | the account has no `can_write` there | grant write first |
| `400` on `offboard mode=delete` | the account is the **last manager** of a scope | name a successor first; the message names the scope |
| `409` on `redeem_invite_code` with a management code | the account is already managed by **another** company | end that relation first (`offboard`, `mode=release` there); a direct switch is refused |
| `402` on `transfer` | balance too low — nothing was booked | load credit, then repeat with the **same** key |
| `409` when deleting a scope | the scope still leads accounts (`Verwaltete Nutzer`) | offboard or move them first, `purge=1` does not bypass it |
| `403 account_suspended` from the token endpoint | the account is suspended | `ontouser_team_unsuspend` |

Every team action is written to the action log as `manage_<action>` with `actor_profile_id` and
`target_profile_id` — `manage_transfer`, `manage_suspend`, `manage_offboard` and so on. Object-level
history per account is a different log (object events), not this one.

Two limits to know before you promise traceability:

- The action log is not part of a manager's rights: a plain manager gets `403` and cannot
  read the log of his own team today. That is a gap, not a design decision.
- There is **no filter** by profile, scope or action — only `page`/`limit`. Reading a specific
  account's history means paging through and filtering yourself.

---

## 6. What the read side shows you

- `get_profile` carries `managed_by: {scope_id, scope_name}` and `suspended` — but never a manager
  address.
- `list_members` carries `managed_by_scope_id`, `managed_by_scope_name` and `suspended` per member.
- `ontouser_team_show` carries the account, its web user, its memberships with all three flags, the
  default write scope and the transfer ledger.

---

## 7. Boundaries — what this is deliberately not

- **No password setting for managed accounts.** A manager cannot take over a login; recovery
  runs through the account itself.
- **No billing on behalf of someone else.** A checkout always credits the account that executes
  it; distribution happens afterwards by `transfer`. One money path, one distribution point.
- **No waiting room, no special scope type.** A customer who wants a holding area creates a normal
  scope for it.
- **No automatic notification on suspension**, so a manager can prepare the wording.
