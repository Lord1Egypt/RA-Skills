# Resource Details & Tags

Fetch details for a single or multiple resources, and inspect AI-generated multilingual tags.

> **All examples in this file go through the Node.js wrapper
> `scripts/msw_resource_api.cjs`.** Use it either as a CLI from a
> shell or via `require(...)` inside Node.js — never assemble curl commands
> by hand.

## GET /v3/resources/{ruid}

Fetch detail for a single resource.

### Usage

```bash
# CLI
node scripts/msw_resource_api.cjs \
    get 0017da7385e04bc4b2ddbe5949b4b462
```

```js
// Node.js
const { getResource } = require('./scripts/msw_resource_api.cjs');

const detail = await getResource("0017da7385e04bc4b2ddbe5949b4b462");
```

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| ruid | path | string | O | Resource RUID (32-char hex) |

### Response

```json
{
  "id": "0017da7385e04bc4b2ddbe5949b4b462",
  "type": "sprite",
  "category": "mob",
  "names": {
    "ko": ["초록버섯"],
    "en": ["Green Mushroom"]
  },
  "assetGuid": "304aba4bea874f948a7548c0d8e393f5",
  "payload": {
    "width": 64,
    "height": 64,
    "pivot": {"x": 32, "y": 50},
    "thumbnail": "https://...",
    "frames": [
      {"filename": "frame0.png", "delay": 100}
    ],
    "elements": [
      {
        "resource_type": "animationclip",
        "rel_path": "mob/stand",
        "ruid": "element_ruid"
      }
    ]
  }
}
```

### Key `payload` Fields

| Field | Type | Description |
|-------|------|-------------|
| `width`, `height` | int | Image size (pixels) |
| `pivot` | {x, y} | Sprite anchor coordinates |
| `thumbnail` | string | Thumbnail image URL |
| `frames` | array | Animation frame list (animationclip) |
| `elements` | array | Resource pack components (resource_pack) |

- `frames` exists only on `animationclip`
- `elements` exists only on `resource_pack`
- `pivot` exists on `sprite`

---

## POST /v3/resources/batch

Fetch multiple RUIDs in a single request.

### Usage

```bash
# CLI — pass RUIDs as space-separated positional arguments
node scripts/msw_resource_api.cjs \
    batch 0017da7385e04bc4b2ddbe5949b4b462 abc123def456789012345678abcdef01
```

```js
// Node.js
const { getResourcesBatch } = require('./scripts/msw_resource_api.cjs');

const resources = await getResourcesBatch([
  "0017da7385e04bc4b2ddbe5949b4b462",
  "abc123def456789012345678abcdef01",
]);
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ids | string[] | O | Array of RUIDs |

### Response

An array of resource objects. Each element has the same structure as the single-resource response.

---

## GET /v3/resources/tags/{ruid}

Fetch AI-generated multilingual tags for a resource — including description, keywords, and per-language tags.

### Usage

```bash
# CLI
node scripts/msw_resource_api.cjs \
    tags 0017da7385e04bc4b2ddbe5949b4b462
```

```js
// Node.js
const { getResourceTags } = require('./scripts/msw_resource_api.cjs');

const tags = await getResourceTags("0017da7385e04bc4b2ddbe5949b4b462");
```

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| ruid | path | string | O | Resource RUID (32-char hex) |

### Response

```json
{
  "tags": {
    "ko": ["초록", "버섯", "몬스터", "슬라임"],
    "en": ["green", "mushroom", "monster", "slime"],
    "ja": ["緑", "キノコ", "モンスター"],
    "zh": ["绿色", "蘑菇", "怪物"],
    "description": "A green mushroom monster from MapleStory",
    "keywords": ["green_mushroom", "mob", "monster"]
  }
}
```

| Field | Description |
|-------|-------------|
| `tags.ko/en/ja/zh` | Tag array per language |
| `tags.description` | Resource description (English) |
| `tags.keywords` | Search keywords |

Tags are generated automatically by AI and describe the resource's visual traits and intended use.
They are useful for similar-resource search and for filtering.
