# Semantic Search & Similar Resources

Search MSW resources by natural language, and find resources similar to a given one.

> **All examples in this file go through the Node.js wrapper
> `scripts/msw_resource_api.cjs`.** Use it either as a CLI from a
> shell or via `require(...)` inside Node.js — never assemble curl commands
> by hand. The wrapper sends UTF-8 JSON bodies directly, so non-ASCII queries
> (Korean / Japanese / Chinese / emoji) are safe and the
> `{"detail":"There was an error parsing the body"}` failure mode is
> impossible to trigger.

## POST /v3/search/resources

Natural-language semantic search. Supports queries in Korean, English, Japanese, and Chinese.

### Usage

```bash
# CLI — defaults: topK=3, --resource-type / --category optional
node scripts/msw_resource_api.cjs \
    search "orange mushroom" --resource-type resource_pack --category npc --topK 3
```

```js
// Node.js — require and call
const { searchResources } = require('./scripts/msw_resource_api.cjs');

const result = await searchResources("orange mushroom", {
  resourceTypeFilter: ["resource_pack"],
  categoryFilter: ["npc"],
  topK: 3,
});
```

> Use `require(...)` with a relative path (e.g.
> `require('./scripts/msw_resource_api.cjs')`) when calling from a sibling file —
> the wrapper is a single-file CommonJS drop-in with zero dependencies.

| Body field (server) | Wrapper arg / CLI flag | Type | Required | Description |
|---------------------|------------------------|------|----------|-------------|
| `query` | `query` (positional) | string | O | Search term (natural language, RUID, or pack ID — exact-match patterns trigger ID lookup) |
| `resourceTypeFilter` | `resourceTypeFilter` / `--resource-type` | string[] | - | `sprite`, `animationclip`, `resource_pack`, `bgm`, `voice`, `effect` (all three are audio), `avataritem` |
| `categoryFilter` | `categoryFilter` / `--category` | string[] | - | `mob`, `npc`, `item`, `skill`, `object`, `background`, `foothold`, `rope`, `ladder`, `etc` (or avatar slot when `resourceTypeFilter=["avataritem"]`). **`map` / `effect` / `ui` are NOT valid** — see [`SKILL.md`](../../SKILL.md) "Categories" |
| `topK` | `topK` / `--topK` | int (1–100) | - | Number of results (server default 20 / **this skill's recommended default 3** — always send explicitly) |
| `offset` | `offset` / `--offset` | int (0–5000) | - | Result offset; default 0 |
| `canonicalOnly` | `canonicalOnly` / `--canonical-only` | bool | - | Server default `true` (sprite/animationclip/avataritem dedup) |
| `widthMin` / `widthMax` | `widthMin` / `widthMax` / `--width-min/max` | int | - | Sprite/animationclip width filter |
| `heightMin` / `heightMax` | `heightMin` / `heightMax` / `--height-min/max` | int | - | Sprite/animationclip height filter |
| `lengthMin` / `lengthMax` | `lengthMin` / `lengthMax` / `--length-min/max` | float | - | Sound length filter (seconds) |

> **The legacy field names `types` / `categories` / `limit` are silently
> ignored by the server.** Always use the canonical names above —
> the wrapper takes care of this for you.

> Avatar-item search uses the same endpoint with
> `resourceTypeFilter=["avataritem"]` already filled in. Use the
> `searchAvatarItems` wrapper (CLI: `search-avatar`) — see "Avatar
> Item Search" below.

### Response

```json
{
  "results": [
    {
      "id": "0017da7385e04bc4b2ddbe5949b4b462",
      "type": "resource_pack",
      "category": "mob",
      "names": {
        "ko": ["초록버섯"],
        "en": ["Green Mushroom"]
      },
      "dname": "Green Mushroom",
      "score": 0.9234,
      "assetGuid": "304aba4bea874f948a7548c0d8e393f5",
      "payload": {
        "width": 64,
        "height": 64,
        "thumbnail": "https://...",
        "elements": [
          {
            "resource_type": "animationclip",
            "rel_path": "mob/9833419.img/move",
            "ruid": "abc123..."
          }
        ]
      }
    }
  ],
  "nextOffset": 5
}
```

### Key Response Fields

| Field | Description |
|-------|-------------|
| `id` | RUID — 32-char hex resource identifier |
| `type` | Resource type |
| `category` | Category |
| `names` | Multilingual names (prefer ko > en) |
| `score` | Semantic similarity score (0–1) |
| `assetGuid` | Unity asset GUID (used in `spawn_preset`, may be missing) |
| `payload.thumbnail` | Thumbnail image URL |
| `payload.width/height` | Image dimensions |
| `payload.elements` | Resource pack components (sprite, animation, sound) |
| `nextOffset` | Next page offset (integer; pass it back as `offset` to paginate) |

### Choosing `resourceTypeFilter`

- **Default:** `resource_pack` — a finished asset bundling sprites + animations + sounds; suitable for most searches
- **Sound / audio:** `bgm` (background music) / `voice` (NPC voice) / `effect` (sound effect — **not visual**)
- **Individual sprite:** `sprite`
- **Individual animation:** `animationclip`
- **Visual effect / particle / hit FX:** `sprite` or `animationclip` + `categoryFilter: ["skill","mob","etc"]` — there is no visual `effect` resource_type or category
- **Avatar costume item:** `avataritem` (or just call `searchAvatarItems`)

### Using `categoryFilter`

| User phrase | category |
|-------------|----------|
| Monster, mob | `mob` |
| NPC | `npc` |
| Item | `item` |
| Skill resource / skill effect | `skill` |
| Tree / rock / map object / decoration | `object` |
| Background / map tile / scenery / BGM | `background` |
| Walkable platform | `foothold` |
| Rope | `rope` |
| Ladder | `ladder` |
| Uncategorized / misc | `etc` |
| Visual effect / particle | use `categoryFilter: ["skill","mob","etc"]` with `resourceTypeFilter: ["sprite","animationclip"]` — no dedicated `effect` category |
| Sound effect (audio) | use `resourceTypeFilter: ["effect"]` — `effect` is an audio **resource_type**, not a category |
| UI element | not indexed under a `ui` category — search `sprite` + `category: "etc"` or by direct name |

### Search Tips

- If you miss on the first try, retry with synonyms / English / Korean:
  - "tree" → "forest" → "forest background" → "plant"
  - "running monster" → "moving monster" → "moving enemy"
- You can also pass a RUID directly as `query`.

---

## Avatar Item Search (`resourceTypeFilter: ["avataritem"]`)

The same `POST /v3/search/resources` endpoint also covers **avatar costume items**
(hats, coats, shoes, weapons, etc.). This is the **only supported way to obtain
avatar item RUIDs by natural-language search** — the legacy full-list endpoint is
no longer used.

The wrapper hard-codes `resourceTypeFilter=["avataritem"]`. You can
narrow the search to a specific avatar slot by passing
`categoryFilter: ["cap", ...]` (CLI: `--category cap`).

### Usage

```bash
# CLI
node scripts/msw_resource_api.cjs \
    search-avatar "early dismissal" --topK 3 --category shoes
```

```js
// Node.js
const { searchAvatarItems } = require('./scripts/msw_resource_api.cjs');

const result = await searchAvatarItems("early dismissal", {
  topK: 3,
  categoryFilter: ["shoes"],
});
```

| Body field (server) | Wrapper arg / CLI flag | Type | Required | Description |
|---------------------|------------------------|------|----------|-------------|
| `query` | `query` (positional) | string | O | Search term (Korean / English / Japanese / Chinese) |
| `topK` | `topK` / `--topK` | int (1–100) | - | Page size (server default 20 / **this skill's recommended default 3**) |
| `offset` | `offset` / `--offset` | int (0–5000) | - | Pagination offset (default 0) |
| `categoryFilter` | `categoryFilter` / `--category` | string[] | - | Avatar slot: `cap`, `cape`, `coat`, `longcoat`, `pants`, `shoes`, `glove`, `hair`, `face`, `weapon`, `twohandweapon`, `subweapon`, `shield`, … |
| `canonicalOnly` | `canonicalOnly` / `--canonical-only` | bool | - | Server default `true` (color/shape variants deduped) |

> The wrapper hard-codes `resourceTypeFilter=["avataritem"]`, so you do not
> need to pass it explicitly.

### Response

```json
{
  "query": "early dismissal",
  "results": [
    {
      "id": "ac02d9eb84dc4c4197dfce6721c6543c",
      "type": "avataritem",
      "category": "shoes",
      "names": { "ko": ["이른 하교"] },
      "dname": "shoes-1141",
      "assetGuid": null,
      "score": 0.78686994,
      "hasEmbedding": true,
      "payload": {
        "color_hex": "#981125",
        "group_size": null,
        "group_canonical": null,
        "group_members": null,
        "group_id": null
      }
    }
  ],
  "nextOffset": 2,
  "exactMatch": false
}
```

### Avatar-Specific Response Fields

| Field | Description |
|-------|-------------|
| `id` | RUID — assign to the matching `Custom*Equip` slot (see slot mapping in the `msw-avatar` skill) |
| `type` | Always `avataritem` |
| `category` | Avatar slot / part category (`shoes`, `cap`, `coat`, `weapon`, …) — drives the slot mapping |
| `dname` | Internal display name (e.g. `shoes-1141`); useful as a stable secondary key |
| `assetGuid` | Usually `null` for avatar items — **do not depend on it for avatar items** |
| `score` | Semantic similarity (0–1) |
| `hasEmbedding` | Whether the item has a vector embedding indexed (filter out `false` if you want only well-indexed results) |
| `payload.color_hex` | Dominant color in `#RRGGBB` — handy for color-based filtering |
| `payload.group_*` | Variant grouping (e.g. recolor families). May be `null` when the item is standalone. |
| `nextOffset` | Pass back as `offset` to fetch the next page |
| `exactMatch` | `true` when the query exactly matches an item name |

### Tips

- The default `topK` is **3** (this skill's convention). Increase to 50–100 only when explicitly browsing widely.
- `category` in avatar item results aligns with avatar slots (`cap`, `coat`, `pants`, `shoes`, `weapon`, …) — use the slot mapping table in the `msw-avatar` skill to assign to the correct `Custom*Equip` property.
- `payload.color_hex` lets you filter results client-side, e.g. "red shoes" → search "shoes", then keep entries whose `color_hex` is reddish.

---

## GET /v3/search/resources/similar/{id}

Find resources that are visually or semantically similar to a given resource.

### Usage

```bash
# CLI
node scripts/msw_resource_api.cjs \
    similar 0017da7385e04bc4b2ddbe5949b4b462 --topK 3 --resource-type animationclip
```

```js
// Node.js
const { findSimilarResources } = require('./scripts/msw_resource_api.cjs');

const result = await findSimilarResources("0017da7385e04bc4b2ddbe5949b4b462", {
  topK: 3,
  resourceTypeFilter: ["animationclip"],
});
```

| Query param (server) | Wrapper arg / CLI flag | Type | Description |
|----------------------|------------------------|------|-------------|
| `id` (path) | `ruid` (positional) | string | Source resource RUID (32-char hex) |
| `topK` | `topK` / `--topK` | int (1–100) | Number of results (server default 20 / **this skill's recommended default 3**) |
| `resourceTypeFilter` | `resourceTypeFilter` / `--resource-type` | string[] | Optional type narrowing |
| `categoryFilter` | `categoryFilter` / `--category` | string[] | Optional category narrowing (incl. avatar slot for avataritem source) |
| `canonicalOnly` | `canonicalOnly` / `--canonical-only` | bool | Server default `true` |
| `widthMin` / `widthMax` / `heightMin` / `heightMax` | `widthMin/Max`, `heightMin/Max` | int | Sprite/animationclip size filter |

> Earlier wrapper sent `limit`; the server's parameter is **`topK`**.

### Response

An array with the same structure as search results. `score` represents similarity to the source resource.
