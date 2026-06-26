# Assets

Assets are static files (images, documents, media) that ship with your agent. Place files in the `assets/` directory at the project root, and they get synced to Botpress Cloud with permanent URLs accessible at runtime via the global `assets` object.

## Basic Concepts

### What are Assets?

- **Static file storage**: Ship images, PDFs, stylesheets, or any file alongside your agent
- **Permanent URLs**: Each asset gets a CDN-backed URL after sync
- **Auto-typed**: TypeScript paths are generated so `assets.get()` autocompletes
- **Sync-aware**: Runtime warns when assets are stale or never synced
- **Content-hashed**: Changes are detected via SHA-256 hashing

### File Location

- **Location**: `assets/` directory at the project root (not inside `src/`)
- **Subdirectories supported**: `assets/images/logo.png` → referenced as `"images/logo.png"`
- **Generated files**: `.adk/assets.d.ts` (types) and `.adk/assets-runtime.ts` (metadata)

### Supported File Types

Images, documents, media, and more — MIME type is auto-detected from the extension:

| Category  | Extensions                                       |
| --------- | ------------------------------------------------ |
| Images    | `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp` |
| Documents | `.pdf`, `.txt`, `.md`, `.html`                   |
| Styles    | `.css`                                           |
| Data      | `.js`, `.json`, `.xml`                           |
| Video     | `.mp4`, `.webm`                                  |
| Audio     | `.mp3`, `.wav`, `.ogg`                           |
| Archives  | `.zip`                                           |

Unrecognized extensions default to `application/octet-stream`.

## Project Structure

```
/                        # Project root
├── assets/              # ← Asset files live here
│   ├── logo.png
│   ├── onboarding.pdf
│   └── images/
│       └── header.webp
├── src/
│   └── ...
├── .adk/
│   ├── assets.d.ts          # Auto-generated types
│   ├── assets-runtime.ts    # Auto-generated metadata
│   └── assets-cache.json    # Sync state cache
└── agent.config.ts
```

## Using Assets at Runtime

The global `assets` object is available in any action, tool, workflow, or conversation handler.

### Get an Asset

`assets.get()` is async and throws an `Error` if the path does not match any known asset.

```typescript
const logo = await assets.get('logo.png')
console.log(logo.url) // CDN URL
console.log(logo.mime) // "image/png"
console.log(logo.size) // bytes
```

> `assets.get()` returns **metadata only** (URL, mime, size) — never the file's bytes. To ship a data table your code reads in-process (menu, catalog, rules), don't use assets — `import` the JSON statically instead. See [patterns-mistakes.md → Shipping a bundled data file](./patterns-mistakes.md#shipping-a-bundled-data-file).

### List All Assets

```typescript
const all = assets.list()
for (const asset of all) {
  console.log(`${asset.path}: ${asset.url}`)
}
```

### Check Sync Status

```typescript
const status = assets.getSyncStatus()
if (!status.synced) {
  console.warn('Unsynced assets:', status.neverSynced)
  console.warn('Stale assets:', status.stale)
}
```

### Asset Properties

Each `Asset` object has these fields:

| Field       | Type     | Description                        |
| ----------- | -------- | ---------------------------------- |
| `url`       | `string` | Permanent CDN URL                  |
| `path`      | `string` | Relative path (e.g., `"logo.png"`) |
| `name`      | `string` | Filename                           |
| `size`      | `number` | File size in bytes                 |
| `mime`      | `string` | MIME type                          |
| `hash`      | `string` | SHA-256 content hash               |
| `fileId`    | `string` | Unique file ID in Botpress         |
| `createdAt` | `string` | ISO timestamp                      |
| `updatedAt` | `string` | ISO timestamp                      |

## CLI Commands

```bash
# Sync local assets to Botpress Cloud
adk assets sync

# Dry run — see what would change without uploading
adk assets sync --dry-run

# Force re-upload all assets
adk assets sync --force

# Auto-confirm sync without prompts
adk assets sync --yes

# List assets (local, remote, or both)
adk assets list
adk assets list --local
adk assets list --remote
adk assets list --format json

# Check sync status
adk assets status
adk assets status --format json
```

Assets are also synced automatically during `adk deploy`.

## Sync Lifecycle

1. Local files in `assets/` are hashed (SHA-256)
2. Hashes are compared against the remote versions in Botpress Cloud
3. A sync plan is computed: create / update / delete
4. Files are uploaded with metadata tags (`type: "asset"`, `adk: "true"`, `path`, `hash`)
5. Cache is updated in `.adk/assets-cache.json`
6. TypeScript types and runtime metadata are regenerated

### Sync States

| State            | Meaning                                    |
| ---------------- | ------------------------------------------ |
| **Up to date**   | Local and remote hashes match              |
| **Stale**        | Local file changed since last sync         |
| **Never synced** | File exists locally but was never uploaded |

The runtime emits a console warning the first time you access a stale or never-synced asset.

## Practical Examples

### Send an Image in a Conversation

```typescript
import { Conversation } from '@botpress/runtime'

export default new Conversation({
  channel: 'webchat',
  async handler({ conversation }) {
    const logo = await assets.get('logo.png')
    await conversation.send({
      type: 'image',
      payload: { imageUrl: logo.url },
    })
  },
})
```

### Use an Asset URL in a Tool Response

```typescript
import { Autonomous } from '@botpress/runtime'

export const getBranding = new Autonomous.Tool({
  description: 'Returns branding assets',
  handler: async () => {
    const logo = await assets.get('logo.png')
    const header = await assets.get('images/header.webp')
    return {
      logoUrl: logo.url,
      headerUrl: header.url,
    }
  },
})
```

### Check Asset Health in an Action

```typescript
import { Action, z } from '@botpress/runtime'

export const checkAssets = new Action({
  name: 'checkAssets',
  input: {},
  output: { synced: z.boolean(), issues: z.array(z.string()) },
  async handler() {
    const status = assets.getSyncStatus()
    return {
      synced: status.synced,
      issues: [...status.neverSynced.map((p) => `Never synced: ${p}`), ...status.stale.map((p) => `Stale: ${p}`)],
    }
  },
})
```

## Common Mistakes

### Putting assets inside `src/`

```
# ❌ Wrong — assets/ must be at the project root
src/assets/logo.png

# ✅ Correct
assets/logo.png
```

### Forgetting to sync before deploy

Assets with placeholder URLs will not be accessible at runtime. Always run `adk assets sync` or `adk deploy` (which syncs automatically) before going live.

### Referencing assets by absolute path

```typescript
// ❌ Wrong
await assets.get('/assets/logo.png')
await assets.get('assets/logo.png')

// ✅ Correct — use the path relative to assets/
await assets.get('logo.png')
await assets.get('images/header.webp')
```
