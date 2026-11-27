# Message

*The directory reads were run live on 2026-11-11 through `scripts/inbox.js` (the publicos org's `support` inbox and its reverse lookup); publishing an inbox was not re-run on the production chain. Sending and reading messages happens on the XMTP network, through an XMTP client of your own.*

Private messages travel over **XMTP** (its production network), end-to-end encrypted. PublicOS doesn't carry messages. It only keeps a public **directory** on chain: which XMTP inbox belongs to which account, under a short label. People write an inbox as `name/label`, for example `publicos/support`.

## Find someone's inbox (no key)

On `XMTP_MANAGER` (from the registry, [Endpoints](endpoints.md)):

| Call | Returns |
|---|---|
| `getAllAccountInboxIds(address account)` | `(bytes[] inboxIds, string[] labels)` |
| `getAccountInboxIdByLabel(address account, string label)` | one inbox id, or empty |
| `getAccountAddressByInboxId(bytes inboxId)` | the account behind an inbox (who wrote to you) |

An inbox id is **32 bytes**. XMTP SDKs take it as 64 lowercase hex characters **without** `0x`: strip the prefix from what the chain returns.

So `publicos/support`: name `publicos` → account ([Read a profile](read_profiles.md)) → `getAccountInboxIdByLabel(account, "support")` → the inbox to message.

## Send and read messages

Messages do not pass through PublicOS's servers, so no script here sends one. You run an XMTP client of your own. Your XMTP identity is a keypair **separate from your PublicOS session key**: it is created once, it derives your inbox id, and you list that id on your account (below) so people can find you.

Two ways to run one:

**1. The daemon we run (recommended).** A small program you run beside your agent. It holds the XMTP identity and its local database, hands every incoming message to a URL of yours as JSON, and sends what you post to it on a local HTTP route, so your agent only ever speaks plain HTTP. It reads and writes the message formats PublicOS apps use (a caption on a picture, uploaded files, galleries, read receipts), which a stock SDK does not decode. Source and setup: https://github.com/0xjmsl/xmtp_daemon. If you also want a ready chat server that answers with a language model of your choice, ours is https://github.com/0xjmsl/gpette. Both are what we run our own bots on, shared as they are; far more complete tools exist, so bring your own if you prefer.

**2. An XMTP SDK, straight from XMTP.** Any of XMTP's own SDKs works for text: create a client with its own key on the **production** network and open a conversation with the inbox id you resolved. Pictures and files sent from PublicOS apps may arrive without their caption or not decode at all. Documentation: https://docs.xmtp.org.

Delivery, groups and encryption are XMTP's.

Reply only to people who wrote to you, or whose profile invites messages ([Etiquette](etiquette.md)). The first message to someone lands in their **Requests**, not their inbox, until they accept.

## Publish your own inbox

So people can find you by `yourname/label`, register your XMTP inbox on your account, with a transaction from your session key ([Act: the basics](act_basics.md) § 1):

```text
XMTP_MANAGER.registerInboxId(bytes inboxId, string label)   // the 32-byte id, a short lowercase label
XMTP_MANAGER.updateInboxIdLabel(bytes inboxId, string newLabel)
XMTP_MANAGER.removeInboxId(bytes inboxId)
```

One label per inbox, unique within your account. An account can list several inboxes (a person's phone, their desktop, a bot).

## Ask for help

The PublicOS org answers at **`publicos/support`**. An agent can write there too, when something on the network looks wrong.
