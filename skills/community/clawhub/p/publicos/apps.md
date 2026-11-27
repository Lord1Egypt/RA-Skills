# Apps

*Last verified against the live network: 2026-11-11.*

The **App Registry** is an on-chain name service for apps: each app has a unique **slug**, a **title**, an **owner** account, and free-form **pointers** (its URL, icon, description…). Registering an app does not advertise it anywhere; the registry only lets you find it by name.

## Find the registry

Module `APP_REGISTRY_MANAGER` in the ModuleRegistry ([Endpoints](endpoints.md)). Pre-built lookup `data`:

```
0x22dbefbb4d046837193e6dc2b46b378ad1cb9f434835c12f86db3fea6328239ff1ac6a3d
```

## Reads (all `eth_call` on the AppRegistryManager)

| Call | Selector | Returns |
|---|---|---|
| `getAppBySlug(string slug)` | `0x119f6b81` | **one struct**, `tuple(bool exists, string slug, string title, address owner)`: decode it as a single tuple |
| `getAllAppPointers(string slug)` | `0x5df703db` | `(string[] pointerTypes, string[] values)` |
| `getAppPointer(string slug, string pointerType)` | via ABI | one value |
| `getAppsByOwner(address owner)` | `0x849a7ebf` | `string[]` slugs |
| `searchByTitle(string title)` | `0x5bab3ba1` | `string[]` slugs. **Whole title only**, case-insensitive: `Manual` and `MANUAL` match, `Man` does not |
| `getTotalAppCount()` | `0x43429ec2` | how many apps exist |

Example, all pointers of the app `manual`:

```bash
curl -s -A 'PublicOS-Agent/1.0' -X POST https://rpc.publicos.dev -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_call","id":1,"params":[{"to":"<APP_REGISTRY_MANAGER>","data":"0x5df703db000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000066d616e75616c0000000000000000000000000000000000000000000000000000"},"latest"]}'
# decodes to: url, icon, description, category_one
#   url = https://publicos.dev/manual/   category_one = Education   (verified 2026-11-11)
```

## Pointers

The contract accepts any pointer name. These are the ones apps use and clients show:

| Pointer | Meaning |
|---|---|
| `url` | where the app lives (open this) |
| `icon` | icon image URL |
| `description` | one-line description |
| `category_one` · `category_two` | category labels |
| `appstore_link` · `playstore_link` · `apk_download` · `ipa_download` | native downloads |
| `skill` | the URL of a `SKILL.md`: instructions this app publishes for AI agents |
| `card_origin` | the app can put **cards** on profiles; card artwork is served from under this URL |
| `warnings` | publisher warnings |

## List every app

There is no "list all" call. Replay the registration events, then read each owner's apps:

1. `eth_getLogs` on the `APP_REGISTRY_MEMORY` module with topic0 `0xe2b0a51cbb811a588cd00131a9477805b8cf16c6931cc8fadb3a47cf3878093e` (`AppRegistered(string,address,string)`). **The RPC refuses a range wider than 10,000 blocks** (error `-32602`), so walk the chain in windows: `fromBlock` 0 → 9,999, then 10,000 → 19,999, and so on up to the current block (`eth_blockNumber`), and keep the last block you read as a cursor for next time. `getTotalAppCount()` tells you how many apps to expect (4 on 2026-11-11). The owner is in `topics[2]`. The slug is hashed in the log, so it can't be read from there.
2. For each distinct owner, `getAppsByOwner(owner)`, then `getAppBySlug` for the current title. A title in the log may since have been changed.

## App cards on profiles

A profile record `card.<id>` whose value is JSON with an `"app"` field is an **app card**: `{"v":1,"app":"<slug>","image":"<url>","live":"<url>"?}`. `image` is the artwork; `live`, when present, is an interactive page. Check them against the app's `card_origin` pointer the way PublicOS clients do:

- `image` **outside** `card_origin` → the card is broken; show nothing.
- app not registered, no `card_origin`, or `live` missing or outside it → show the image only.
- both under `card_origin` → the image, and `live` may be opened.
