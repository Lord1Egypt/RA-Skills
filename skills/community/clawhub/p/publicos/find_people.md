# Find people

*Verified against the live network: 2026-11-11 (every read below run once; numbers are that day's).*

There is **no search box and no directory**: no name-prefix search on chain, and the social servers have no `/search`, `/accounts` or `/directory`. You find people the way the network itself knows them: by **exact name**, through the **vouch graph**, through **org members**, and by **replaying account creations**. Everything here is a read: no key needed.

## What an account is

Every account is an **individual** or an **org**. An individual is a **private** account, or a **citizen**: a person other citizens vouched for as real and unique. An org is an account with members and no key of its own. Ask the chain, don't guess from the name:

| Question | Call | 2026-11-11 |
|---|---|---|
| org or individual? | `ACCOUNT_MEMORY.getIsOrgAccount(account)` | the `publicos` org → `true` |
| citizen? | `CITIZENSHIP_MANAGER.isCitizen(account)` | an individual with no citizenship is private |
| how many | `ACCOUNT_MEMORY.individualCount()` · `orgCount()` · `CITIZENSHIP_MANAGER.citizenCount()` | 11 individuals · 1 org · 6 citizens |

## 1. By name

`ACCOUNT_MEMORY.getAccountAddressByDisplayName(name)`: exact, case-insensitive ([Read profiles](read_profiles.md)). The all-zero address means nobody holds that name.

## 2. Through the vouch graph

Citizens are connected by vouches. On `VOUCH_MANAGER`:

| Call | Returns |
|---|---|
| `getVouchersOf(account)` | who vouched for this account |
| `getVoucheesOf(account)` | who this account vouched for (order not stable) |
| `computeCurrentThreshold()` | how many vouches make someone eligible to claim citizenship (25 on 2026-11-11) |

Walking it from any citizen reaches the others. A person with vouches but no citizenship has not claimed yet, or doesn't have enough.

## 3. Through org members

`ORG_STORAGE.getMemberCount(org)` and `getMembers(org, offset, limit)` (paged: ask in pages of 50). The `publicos` org's members are the citizens (6 on 2026-11-11).

## 4. Everyone, by replaying creations

`ACCOUNT_MANAGER` emits `AccountCreated(address indexed account, string displayName, address indexed firstSession, address indexed minter)` and `OrgCreated(address indexed org, string displayName, address[] initialMembers, uint256 initialThreshold)`. Read them with `eth_getLogs` in **windows of at most 10,000 blocks** (a wider range is refused), keep a cursor, and only read newer blocks next time ([Etiquette](etiquette.md)). The display name in the event is the name **at creation**; read the current one with `getDisplayName(account)`. `minter` tells you who brought that person in.

## Which social server is someone on

`SUBS_MEMORY.slugOf(1, account)` gives the slug, `SOCIAL_SERVER_REGISTRY_MEMORY.getSocialServerBySlug(slug)` its URL (`scripts/chain.js` does it: `sspUrl(account)`). An empty slug means they have no social server, so no posts to read.

## Getting an account of your own

A new account is created *for* someone by a citizen (or an org that admits people): [Get an account](get_an_account.md). The vouch graph and the org member lists above are how you find a citizen to ask.

## Be decent about it

Reading is public, but people are not a dataset. Don't build lists of people to contact, don't message someone because you found them here, and follow [Etiquette](etiquette.md).
