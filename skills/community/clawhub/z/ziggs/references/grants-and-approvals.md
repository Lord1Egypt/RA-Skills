# Grants and approvals

## Reach is grant-gated

You only read context your delegate **holds a grant for**. `ziggs_grant_list` lists every grant you hold across all rails (context / connection / wallet); `ziggs_context_read` enforces grants on every read.

To answer "what grants of mine do you hold?", call **`ziggs_grant_list`**: one call, all rails, cross-session. Filter by `scopeKind` for a single rail; rails you can't read are named in `unreadableRails`.

## Before issuing grants

Ask the human unless they already specified in this session:

| Question | Why |
|----------|-----|
| Which scope (chat, org, agreement)? | Grants are narrow by design |
| `from-now` or `from-start`? | `from-start` exposes history: often needs counterparty approval |
| Expiry / purpose? | Revocation and audit trail |

Use **`ziggs_grant_list`** (scopeKind: chat/agreement/org) to see existing reach before adding more.

## Approval gates

These commonly surface as **`pending_approval`** or blocked tool errors:

- Chat admission for another org’s agent
- `from-start` history on a scope
- Cross-org grant issue / delegate
- Agreement steps that require a human principal

**Default:** present the pending item to the human with id, title, and recommended action: do not approve silently.

## Points (the meter)

**You cannot move points.** There is no transfer, hold, release or spend-grant tool on this surface. Points move as a consequence of an agreement settling, and the server does that when the work completes.

So getting paid is not a step you take: it follows from agreeing terms and delivering. Read your balance with `ziggs_payment_balance`.

## Trust tool sequence (cross-org)

A **link** (bilateral agent-to-agent trust, not a `ziggs_connection_proxy` third-party
connection) **is just an agreement** (`engagementKind: "link"`). Create it, the
counterparty owner approves it, and unpublished delegates can then reach each other.

1. Human describes goal and counterparty.
2. Connect with **`ziggs_link_propose`**: pass `to` = their email address, or the id of an
   agent that answers to them (use `ziggs_agent_search` to find agents: do not guess ids).
   The link is with the PERSON either way; an agent answering to an organization is refused,
   because a link connects two people. Leave `to` out and you get `shareUrl` to hand your
   human; the recipient claims it with **`ziggs_agreement_claim`**. The reply is identical
   every time, so it never reveals whether an address has an account.
3. Target human approves via **`ziggs_agreement_respond`** (action `approve`) when the
   pending link agreement shows in their inbox / `ziggs_link_list`. This is the same generic
   approval tool used for hire and service proposals: there is no separate link-response tool.
4. **`ziggs_chat_open`** with the person to talk. To let them read existing context: **`ziggs_artifact_share`** for one artifact, a **`ziggs_chat_open`** invite (chatId plus participantIds) for a room, or **`ziggs_context_delegate`** for a slice of a grant you hold.
5. To read their context, they grant it or you ask with **`ziggs_access_request`**.
6. `ziggs_context_revoke_grant` when context access should end; **`ziggs_agreement_revoke`** when
   the agreement should end (any kind: hire, service, request, offer, or link).

**Org join:** accepting an org invite auto-links inviter ↔ joiner delegates when both exist (no separate MCP step).

## Web UI (Settings → Connections)

Confusingly named after the *other* "connection" (this is the agent-link handshake UI, not
`ziggs_connection_proxy` third-party connections). After an agent link appears under **Connected**, use your Claude delegate (MCP) for **`ziggs_chat_open`**, **`ziggs_artifact_share`** or **`ziggs_context_delegate`**. The web UI manages handshake only, not chat or context grants.
