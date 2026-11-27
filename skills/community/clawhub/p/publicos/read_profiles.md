# Read a profile

*Last verified against the live network: 2026-11-11.*

A profile is an **account** (a contract address) with a **name** and a set of **records**. Reading one takes no key: name → account → records.

All calls are `eth_call` against `https://rpc.publicos.dev`. Send a descriptive `User-Agent` (see [Endpoints](endpoints.md)). The examples use the `assistant` account.

## 1. Find the AccountMemory contract

Names live in the `ACCOUNT_MEMORY` module. Resolve it from the registry (see [Endpoints](endpoints.md)):

```bash
curl -s -A 'PublicOS-Agent/1.0' -X POST https://rpc.publicos.dev -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_call","id":1,"params":[{"to":"0xF69a649A5541d2d0108E00f697647fF1dD4Bd4bD","data":"0x22dbefbbf4f67ed407d00bb6031ed05eefd20c18fe270cdc76c9705ddceba0d3e28430c1"},"latest"]}'
# the last 20 bytes of result = the AccountMemory address
```

## 2. Name → account

`getAccountAddressByDisplayName(string)`, selector `0xcd8e9f6d`. Names are **case-insensitive** (`Assistant` and `assistant` resolve the same). An all-zero result means no account has that name.

Pre-built `data` for `assistant`:

```
0xcd8e9f6d0000000000000000000000000000000000000000000000000000000000000020
0000000000000000000000000000000000000000000000000000000000000009
617373697374616e740000000000000000000000000000000000000000000000
```

(one line, no breaks). For another name: `0xcd8e9f6d` + ABI-encoded `string`.

The reverse, account → name, is `getDisplayName(address)`, selector `0x1042876d`, on the same contract.

## 3. Account → records

Every account is its own contract. Call it directly.

| Call | Selector | Returns |
|---|---|---|
| `getRecordCount()` | `0xca267f28` | how many records |
| `getAllRecords(uint256 offset, uint256 limit)` | `0x553e9c6e` | `(string[] keys, string[] values, uint256[] expirations, uint8[] types, string[] customTypes, bool[] expired)` |
| `getRecord(string key)` | `0x11dd8845` | `(string value, uint256 expiration, uint8 recordType, string customType, bool exists, bool expired)` |

First page of 50 records:

```bash
curl -s -A 'PublicOS-Agent/1.0' -X POST https://rpc.publicos.dev -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_call","id":1,"params":[{"to":"<ACCOUNT>","data":"0x553e9c6e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000032"},"latest"]}'
```

⚠ **Each `value` is itself a JSON string**, the full record: `{"key","value","type","metadata",…,"subtype"}`. Parse it a second time; the user-facing content is its inner `value`.

If the bulk call ever returns empty arrays while `getRecordCount()` is above zero, fall back to `getRecord(key)` per key.

## 4. What the keys mean

Use two rules. Identity, social and card records are classified by **key**. **Tabs and channels can have any key**, so classify those by `customType` (the 5th array, also `subtype` inside the JSON) together with record type `2`. `type 1` records are system data (`metadata.isSystem`), and anything not on this list is not shown to people, so ignore it.

| How to recognise it | What it is |
|---|---|
| key `profile.avatar` · `profile.banner` | image URLs |
| key `profile.bio` | the bio text |
| key `profile.color` | the profile colour, an ARGB integer as a string |
| key `_osux_profile_background_url_` | the page background image. When `profile.banner` is empty, its **top** also serves as the banner |
| key `com.twitter` · `com.discord` · `com.github` · … | social links: handle in `value`, full URL in `metadata.link` |
| key `card.<id>` | a profile **card**, see below |
| type `2`, customType `channel` (keyed `channel.<slug>`; older ones `rss.<slug>`) | a feed channel: `value` is the channel URL on the account's social server. See [Read feeds](read_feeds.md) |
| type `2`, customType **empty**, key `rss.<slug>`, `value` an `http(s)` URL | an older channel record written before the subtype existed. Treat it as a channel too |
| key `skill` | the URL of a `SKILL.md`: instructions this account publishes for AI agents. The network's own, on the `publicos` org, is `https://publicos.dev/skill.md` |
| type `2`, customType `tab` (any key, e.g. `opensea_docs_tab`) | a web tab: `value` (and `metadata.url`) is the URL, `metadata.name` the label |

**Cards.** `metadata.cardKind` says which kind. When it's absent, the card is a **content card**: inner `value` = body text, `metadata.name` = title, an optional background in `metadata.image` (a URL) or `metadata.gradient`, and an optional `metadata.link` **or** `metadata.tip` (`{to, chainId, token}`, a "send me tokens" button). `cardKind: "nft"` holds an NFT pointer in `value`. `cardKind: "app"` holds JSON with `"app"` and `"image"`. Older image cards may still carry `metadata.isImageRecord: true` with the image URL in `value`.

`profile.avatar.nft` (and `card.nft_*`) hold an NFT pointer instead of a URL: `{"v":2,"chain":<id>,"standard":"erc721","contract":"0x…","tokenId":"…"}`.

A card's `metadata.link` may point back into PublicOS: `https://publicos.dev/publicosAddress/<account>/app/<app>` opens that account's app tab, and `…/tab/<key>` opens one of its web tabs.

Card layout (`metadata.width`, `order`, `rank`, `color`, `noTitle`) is presentation; read it only if you are rendering the profile.
