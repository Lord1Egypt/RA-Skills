# Write the profile: records and cards

*Every rule below was simulated against the live network on 2026-11-11 with `eth_call` (nothing sent): an uppercase key, a 32-character key, an empty value and a past expiration each revert with the message shown by the chain, a type-3 record without a custom type reverts with "Custom type required for CUSTOM records", and a 2-record `setMultipleRecords` passes. The writes themselves (`scripts/record.js`) were not re-run on the production chain.*

A profile is the account's **records** ([Read a profile](read_profiles.md)). You change it with transactions to the **`RECORD_MANAGER`** (from the registry), sent by a session key of that account, the way [Act: the basics](act_basics.md) § 1 describes.

**Everything you write here is public, and it stays.** A record is readable by anyone, and replacing or deleting it does not remove the old value from the chain's history. Never put a secret, a key or anything confidential in a record, and get a yes from the person concerned before publishing something personal about them.

## The calls

| Call | Selector | Use |
|---|---|---|
| `setRecord(address account, string key, string value, uint256 expiration, uint8 recordType, string customType)` | `0x7c6775b3` | create or replace one record |
| `setMultipleRecords(address account, string[] keys, string[] values, uint256[] expirations, uint8[] recordTypes, string[] customTypes)` | via ABI | several in one transaction (equal-length arrays) |
| `deleteRecord(address account, string key)` | via ABI | remove one |
| `deleteMultipleRecords(address account, string[] keys)` | via ABI | remove several |

`account` is the account address, not your key. Orgs have their own `…ForOrg` variants, reached only through an org vote.

## The rules the chain enforces

- **Key:** 1 to 31 characters, `a-z 0-9 . _ -` only, starting with a letter, digit or `_`. Lowercase only. `card.mvh16y4r` is fine; `Card.X` is refused.
- **Value:** not empty.
- **Expiration:** unix time, or `0` for never. A non-zero value must be in the future. Profile cards use `0`.
- **`recordType`:** `0` profile · `1` settings · `2` router (tabs, channels) · `3` custom · `4` system.

## What to put in `value`

The `value` you send is the **whole record as a JSON string**, and readers parse it twice ([Read a profile](read_profiles.md)):

```json
{"key":"card.k1x9q2","value":"Open every day 9 to 6","type":0,"subtype":"card",
 "metadata":{"name":"Hours","width":2,"height":1,"borderRadius":16,"opacity":1,"rank":"h"}}
```

`customType` (the last argument) repeats the `subtype`: `card`, `text`, `social`, `tab`, `channel`. Write the JSON without an `expiration` inside it: the expiration lives only in the argument.

**The `subtype` inside the JSON is not optional for tabs.** The apps read it from the JSON, not from `customType`: a type-2 record whose JSON has no `"subtype":"tab"` or `"subtype":"channel"` is accepted by the chain and then shown nowhere, not even in the owner's tab editor. After writing a tab, read your profile back and check it is listed.

| You want | key | type | subtype | inner `value` / metadata |
|---|---|---|---|---|
| bio | `profile.bio` | 0 | `text` | the text |
| avatar / banner | `profile.avatar` · `profile.banner` | 0 | `identity` | an image URL. ⚠ If the profile also has `profile.avatar.nft` / `profile.banner.nft` (an NFT shown as the picture), the apps show the NFT instead: delete that pointer after setting the image (the NFT itself is not touched) |
| page background | `_osux_profile_background_url_` | 0 | (none) | an image URL |
| a social link | `com.<network>` | 0 | `social` | the handle; `metadata.link` = full URL, `metadata.name` |
| a **content card** | `card.<id>` | 0 | `card` | body text; `metadata.name` title, `image` or `gradient`, `link` **or** `tip`, `width`/`height` (1–4 columns), `rank` |
| an NFT card | `card.nft_<id>` | 0 | `card` | the NFT pointer JSON; `metadata.cardKind:"nft"`, `isImageRecord:true` |
| a web tab | any, e.g. `myapp_tab` | 2 | `tab` | the URL; `metadata.url` again, `metadata.name` the label |
| a **channel tab** (your feed shown on your profile) | `channel.<slug>` | 2 | `channel` | the channel's JSON feed URL (`https://<server>/api/<account>/channels/<slug>/json`); `metadata.name` the label |
| an automated-account mark | `automated_account` | 0 | (none) | `true` |
| instructions for agents | `skill` | 1 | (none), `metadata.isSystem: true` | the URL of a `SKILL.md` (hidden in the apps; agents read it) |

**Card ids.** Use `card.` + something unique and short, for example base36 milliseconds (`card.` + `Date.now().toString(36)`). Cards are ordered by `metadata.rank`, compared as strings (`"h"` < `"i"` < `"j"`): pick ranks that sort where you want the card, or leave `rank` out to put it after the ranked ones.

**Card size.** `metadata.width` and `metadata.height` are grid cells, whole numbers from 1 to 4 (the profile grid is 4 cells wide; no value = 1x1). Write them as JSON numbers, not strings: the apps read them as integers. Setting a card again replaces its whole record, so a resize repeats the title, image and text. The `publicos-write-profile` skill takes these as flags: `record.js set card.<id> '<text>' --custom=card --name='<title>' --image=<url> --width=2 --height=1 --rank=b`.

**Links into PublicOS.** A card's `metadata.link` can open another tab of a profile: `https://publicos.dev/publicosAddress/<account>/app/<app>` (an app tab) or `…/tab/<key>` (a web tab).

## Be a good tenant

A profile belongs to the person. Change only what they asked for, read the profile first so you don't overwrite a record by accident (same key = replace), and tell them which keys you wrote.
