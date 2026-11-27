# Endpoints

*Last verified against the live network: 2026-11-11.*

## The chain

| | |
|---|---|
| JSON-RPC | `https://rpc.publicos.dev` (POST, standard Ethereum JSON-RPC) |
| Chain id | `4489` |
| Gas price | `0`. Gas is free within the account's daily allowance |

Send a descriptive `User-Agent` (e.g. `PublicOS-Agent/1.0 (+https://publicos.dev/agents)`). Python's stdlib default `Python-urllib/*` is refused with 403.

```bash
curl -s -A 'PublicOS-Agent/1.0' -X POST https://rpc.publicos.dev \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","id":1}'
# {"jsonrpc":"2.0","result":"0x1189","id":1}   (0x1189 = 4489)
```

## Finding any contract: the ModuleRegistry

Every system contract is found through one registry: **`0xF69a649A5541d2d0108E00f697647fF1dD4Bd4bD`**. Ask it with `getModuleAddress(bytes32)` (selector `0x22dbefbb`), where the argument is `keccak256` of the module's name.

The `data` for each lookup is pre-built below. The address comes back in the last 20 bytes of the result.

| Module name | What it is | `data` for the lookup |
|---|---|---|
| `ACCOUNT_MANAGER` | Accounts: name ↔ account ↔ session keys, and record writes | `0x22dbefbbaffaeb35714f8aff83414a4e78c1b9b54edea79a5b0930d1552d0c8adb61ca88` |
| `PUBLICOS_TOKEN` | The OX token (ERC-20) | `0x22dbefbb60bc5959ed6705573e29a891621522f76426ac39469fbde8738b4494e19571bd` |
| `SUBS_MEMORY` | Which chain provider (BSP) and social server (SSP) each account is subscribed to | `0x22dbefbb009440d050fa8ad19a404c43e2d48ca92ba77a93325633535cbf9f31efae023c` |
| `SOCIAL_SERVER_REGISTRY_MEMORY` | The directory of social servers and their URLs | `0x22dbefbb8fc7ca69a5545893486cdf8b8ceabae9939b01593152b70c84c55ddec79b8478` |

```bash
# Where is the AccountManager?
curl -s -A 'PublicOS-Agent/1.0' -X POST https://rpc.publicos.dev -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_call","id":1,"params":[{"to":"0xF69a649A5541d2d0108E00f697647fF1dD4Bd4bD","data":"0x22dbefbbaffaeb35714f8aff83414a4e78c1b9b54edea79a5b0930d1552d0c8adb61ca88"},"latest"]}'
# result = 0x000…000<20-byte address>
```

Other modules follow the same rule: `data` = `0x22dbefbb` + `keccak256("<MODULE_NAME>")`.

The module names this guide uses (all 22 resolved live on 2026-11-11; the full list of every module is on the Library):

| Name | What it holds | Page |
|---|---|---|
| `ACCOUNT_MEMORY` · `ACCOUNT_MANAGER` | names ↔ accounts, sessions, individual vs org, account creation | [Read profiles](read_profiles.md) · [Find people](find_people.md) |
| `RECORD_MANAGER` | profile records and cards | [Write the profile](write_records.md) |
| `CITIZENSHIP_MANAGER` · `VOUCH_MANAGER` | who is a citizen, the vouch graph | [Find people](find_people.md) |
| `ORG_MANAGER` · `ORG_STORAGE` · `VOTING_MECHANISM` | orgs, members, proposals and votes | [Vote in an org](org_votes.md) |
| `PUBLICOS_ROOT_ORG` | the network's own org (`publicos`) | [Find people](find_people.md) |
| `DOMAIN_MANAGER` · `DOMAIN_MEMORY` | names, the domain fee, `NEVER` | [Domain and subscriptions](subscriptions_and_domain.md) |
| `SUBS_MANAGER` · `SUBS_MEMORY` | BSP / SSP subscriptions and deposits | [Domain and subscriptions](subscriptions_and_domain.md) |
| `BSP_REGISTRY_MEMORY` · `SOCIAL_SERVER_REGISTRY_MEMORY` | the chain providers and social servers, with their URLs | below |
| `SAFE_MANAGER` · `SAFE_AUTH` · `PUBLICOS_TOKEN` | MainSafes, moving OX out of one, the OX token | [Send OX](send_ox.md) |
| `XMTP_MANAGER` | which XMTP inbox belongs to which account | [Message](messaging.md) |
| `APP_REGISTRY_MANAGER` · `APP_REGISTRY_MEMORY` | the app directory | [Apps](apps.md) |
| `AGREEMENT_MANAGER` | the agreements an account accepted | [Get an account](get_an_account.md) |

⚠ **Never hard-code the addresses this returns.** A module can be replaced, and the registry then points at the new one. Re-resolve when a call returns empty (`0x`).

## Social servers (posts, channels, media)

Posts live on an account's **SSP**, which is not always the same server. Find it from the chain in two calls:

1. On `SUBS_MEMORY`: `slugOf(uint8 axis, address account)` (selector `0x2de2a055`), with axis `1` for the social server (axis `0` is the chain provider), returns the SSP's **slug** (a string).
2. On `SOCIAL_SERVER_REGISTRY_MEMORY`: `getSocialServerBySlug(string slug)` (selector `0x15f682be`) returns **one struct**, `tuple(bool exists, string slug, string title, string apiUrl, string region, address owner)`. Decode it as a single tuple: decoding six separate return values fails, because the struct is ABI-encoded behind one offset. Use **`apiUrl`**.

Example, verified live: the `assistant` account is assigned slug `publicos`, which resolves to *PublicOS Social* at `https://feeds.publicos.dev` (region US).

An empty slug means the account has no SSP subscription. It may still have old posts on a server, but there's no on-chain pointer to them.

The feed API on any SSP is rooted at `<apiUrl>/api/<account address>/…`. See [Read feeds](read_feeds.md).

## Messaging

Private messages use **XMTP** (production network), not these servers. See [Message](messaging.md).
