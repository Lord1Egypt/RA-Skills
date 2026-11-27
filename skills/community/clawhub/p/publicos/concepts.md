# Concepts

*Last checked against the live network: 2026-11-11 (the reads behind these definitions; the rules for writes were not re-run on the production chain).*

PublicOS uses a small, exact vocabulary. Use these words the way they're defined here; several of them don't mean what they mean elsewhere.

## Who is on the network

- **Account**: the permanent on-chain identity of a person or organization. It's a smart contract that others look up by name. **An account holds no money and has no key of its own.**
- Every account is either an **individual** or an **org**. There is no third kind.
  - An **individual** is controlled by one or more **session keys** (below).
  - An **org** has **no key at all**. It acts only by a vote of its members.
- Individuals are either **private** or **citizen**.
  - A **private** account can do everything ordinary: post, message, pay. It pays the domain fee for its name, and it can't create accounts for others, register a provider, or vote in the network's own org.
  - A **citizen** is an individual that other citizens have vouched for. Once its vouches reach the current threshold it becomes *eligible*, and it then **claims** citizenship itself, signing the citizen agreement. Citizenship is a flag on chain that does not lapse on its own: a later rise of the threshold does not undo it, though the network's own org can remove it. Read it straight from the chain (`isCitizen`, see [Find people](find_people.md)). Never infer it from other data.
  - An org is **public** or **private** by a flag set **once, when it is created**. A public org can only ever add citizens as members; a private org can add anyone.
- A **subdomain** (written `name.sub`) is a named persona of an individual, with its own records and funds but no identity of its own: everything it does resolves back to its parent account.

## Keys and addresses

One person touches four kinds of address. Mixing them up is the most common mistake.

| Address | What it is |
|---|---|
| **Account** | The identity contract. This is what you look up, follow, mention, and pay *to*. |
| **Session key** | A normal keypair (EOA) that signs transactions *for* an account, one per device. A key belongs to exactly one account. Called a *client key* before 2026-10-14; the chain and the servers now say `session`. |
| **MainSafe** | A Safe smart wallet created with each account. **It holds the account's funds. The Safe pays; the account is credited.** |
| **XMTP key** | A separate keypair for messaging, which derives an XMTP **inbox ID**. It's unrelated to the session keys. |

## What an account publishes

- **Records**: key → value entries in the account's own storage: name, avatar, banner, bio, social links, cards. Anyone can read them. They carry no authority; they're what the account says about itself.
- **Cards**: records shown as tiles on the profile: text, an image, a link, an NFT, or a small embedded app.
- **Inbox directory**: an account can publish its XMTP inbox IDs on chain, each with a label. People write an inbox as `name/label` (e.g. `publicos/support`, the network org's support inbox).
- **Apps**: an on-chain **App Registry** lists apps (slug, title, URL, icon) owned by accounts or orgs.

## Where things live

| Thing | Where |
|---|---|
| Identity, records, citizenship, payments | The PublicOS chain (chain id **4489**), over JSON-RPC |
| Posts, channels, media | An **SSP** (social server provider) that serves **JSON Feed 1.1**. Each post is signed by its author |
| Private messages | **XMTP**, an end-to-end encrypted messaging network |

- **BSP** (blockchain service provider): a node operator that gives users RPC access to the chain.
- **SSP** (social server provider): hosts channels, posts and media. Accounts subscribe to one, and anyone can read from it.
- A **channel** is a feed on an SSP, always owned by an **individual** account. Orgs can't own channels.

## Money

- **OX** is the network's token. Fees on PublicOS are paid in OX. Gas has no price: every account has a free gas allowance that renews each day, set by the publicos org, and an account that wants more can get extra gas by burning OX.
- A **domain** is an account's name plus the right to transact. It's renewed by paying a fee priced by name length; citizens with names of 5+ characters don't pay it.
- To send OX you act through the sender's **MainSafe**, not the session key. See [Send OX](send_ox.md).

## What you can do without a key

Everything public: look up any account, read its records and cards, check whether it's a citizen, list its apps and inboxes, and read its channels and posts. Writing anything (a post, a message, a payment) needs a session key of an account, or an XMTP key for messages.
