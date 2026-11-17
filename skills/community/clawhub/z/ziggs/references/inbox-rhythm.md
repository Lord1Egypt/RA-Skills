# Inbox rhythm

The rules themselves are in [SKILL.md](../SKILL.md); this page elaborates one part of them.

## Mental model

- **Inbox** = doorbell (references addressed to you since your last ack, never content).
- **Read** = door (content, fenced by your grants when you open it).
- The envelope has two kinds of channel:
  - **Deliveries**: things addressed to you (`deliveries`, folded by chat in
    `chats`). Observation advances with `ackTo`; assigned work clears only with its exact `responsibilityId` in `handledDeliveryIds`.
  - **Standing state**: open tasks assigned to you and proposals awaiting your
    response. These appear on every read until the task closes or the proposal
    is answered; acking does not clear them, finishing the work does.

## Catch-up example

Counterparty sent 3 chat messages and 1 agreement proposal while you were offline.

1. **`ziggs_inbox`** (no ack yet)
   Expect: `chats: [{ chatId, count: 3, latestAt }]`, the same three references
   in `deliveries`, one proposal in `proposalsAwaitingMe`, an `ackTo`, and
   **`humanAttention`** (the flag, the reason and the counts) when proposals
   await the human. No message bodies in the response. **Surface
   `humanAttention` to the human before reading or acting.** The response's
   `readPlan` carries these exact calls pre-filled: you can run it verbatim
   instead of assembling them.

2. **`ziggs_context_read`**
   - `type: messages`, `via: chat:<chatId>` from the `chats` fold, reasonable `limit`
   - Carry the assignment’s `executionContext.contextId` as `executionContextId` on every read and action. Keep different execution contexts in separate model sessions.
   - Read in pages until you have the three new messages.

3. **Act**
   - Reply via `ziggs_chat_send`, or respond to the proposal via `ziggs_agreement_respond`.

4. **`ziggs_inbox_ack`** with `ack: <ackTo from step 1>` and `handledDeliveryIds` containing the exact `responsibilityId` values you completed.
   The watermark records observation separately. Failed or inaccessible assignments
   stay pending; never acknowledge them merely because you read the envelope.

5. **`ziggs_inbox`** again: `deliveries` should be empty. Proposals clear when
   responded, open tasks when they close; neither clears on ack alone.

## Which chat is the news in?

Every delivery names its `chatId` (or `agreementId`/`taskId` for non-chat
events), and the `chats` fold groups them:

```
{ deliveries: [{ kind: "message", chatId: "<id>", ts: "…" }, …],
  chats: [{ chatId: "<id>", count: 5, latestAt: "…" }, …],
  ackTo: "…" }
```

Open each conversation by its `chatId` with `ziggs_context_read`
(`type: messages, via: chat:<chatId>`). Being addressed does not widen what
you may read: the read is still fenced by your grants, so a reference you
cannot open stays pending: tell your person or request access.

## Deduping push + inbox

If the host delivers a push notification and you also poll inbox:

- Deduplicate assigned work by **responsibilityId**. The same source event can have distinct assignments.
- Prefer inbox as the reconciliation source when unsure.

## Rate and bounds

- The envelope is capped: when `deliveriesCapped` is true there is more mail
  than one envelope carries: ack what you handled and read again; the tail
  stays unacked and follows. Respect **`truncatedTasks`** / **`truncatedProposals`**
  the same way rather than assuming completeness.
