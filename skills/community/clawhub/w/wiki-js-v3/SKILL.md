---
name: wiki-js-v3
version: 1.0.0
description: All-encompassing Wiki.js Administration – GraphQL + REST API wrapper with full coverage. Pages, Assets, Search, Tags, Tree, History, Versioning, Rendering. Robust error handling with retries and chunking.
author: michael
tags: [wiki, documentation, admin, graphql, api]
homepage: https://github.com/openclaw/skills/wiki-js-v3
user-invocable: true
install:
  npm:
    - graphql-request
    - form-data
    - node-fetch
  env:
    WIKIJS_URL: "https://your-wiki.example.com"
    WIKIJS_TOKEN: "Get from Wiki.js Admin > API Keys"
metadata:
  openclaw:
    requires:
      config: [wikijs]
---

# Wiki.js V3 Skill – All-Encompassing Wiki Administration

**Ersetzt:** `wiki-js-v2` (nur Pages + Assets)

## 🎯 Features

| Feature | V2 | V3 |
|---------|----|----|
| Pages (CRUD) | ✅ | ✅ |
| Assets (Upload/List) | ✅ | ✅ |
| **Move/Copy Pages** | ❌ | ✅ |
| **Page History** | ❌ | ✅ |
| **Version Restore** | ❌ | ✅ |
| **Render (HTML/PDF)** | ❌ | ✅ |
| **Search (Full-Text + Tags)** | ❌ | ✅ |
| **Page Tree/Hierarchy** | ❌ | ✅ |
| **Tags (CRUD)** | ❌ | ✅ |
| **Asset Folders** | ✅ | ✅ |
| **Asset Delete** | ❌ | ✅ |
| **Multi-Locale** | ✅ | ✅ |
| **Retry + Backoff** | ✅ | ✅ |
| **Path-First + ID** | ✅ | ✅ |

---

## 📦 Installation

```bash
# Skill bereits installiert unter:
~/.openclaw/workspace/skills/wiki-js-v3/

# CLI-Wrapper (optional, für direkten Terminal-Zugriff):
chmod +x ~/.openclaw/workspace/skills/wiki-js-v3/bin/wiki.js
ln -s ~/.openclaw/workspace/skills/wiki-js-v3/bin/wiki.js ~/.local/bin/wiki
```

**Environment:**
```bash
export WIKIJS_URL="https://your-wiki.example.com"
export WIKIJS_TOKEN="your_api_key_here"
export WIKIJS_LOCALE="de"  # Optional, default: de
```

---

## 🔧 API Coverage

### GraphQL Operations

| Category | Operations |
|----------|-----------|
| **Pages** | `single`, `singleByPath`, `list`, `create`, `update`, `delete`, `move`, `render`, `history`, `restoreVersion` |
| **Search** | `search(query, limit)` |
| **Tags** | `list`, `create`, `delete` |
| **Assets** | `list`, `createFolder`, `delete` |

### REST Operations

| Endpoint | Use Case |
|----------|----------|
| `POST /u` | File upload (multipart/form-data) |
| `GET /f/:hash/:filename` | Static asset serving |

---

## 📝 CLI Reference

### Pages

```bash
# Create or update (idempotent)
wiki upsert docs/setup "Setup Guide" @content.md "setup,wiki"
wiki upsert docs/api "API Reference" "## Overview\n..." "api,docs"

# Get page content
wiki get docs/setup
wiki get 42  # by ID

# Delete page
wiki delete docs/old-page
wiki delete 42

# Move page (changes path)
wiki move docs/old docs/new

# Copy page (creates new page)
wiki copy docs/template docs/new-page

# Show page history
wiki history docs/setup

# Restore specific version
wiki restore docs/setup --version=3

# Render page
wiki render docs/setup --format=html
wiki render docs/setup --format=pdf > setup.pdf
```

### Search

```bash
# Full-text search
wiki search "docker"

# With tag filter
wiki search "kubernetes" --tags="devops,cloud"

# Limit results
wiki search "api" --limit=50
```

### Tree / Hierarchy

```bash
# List all pages
wiki tree

# Filter by path prefix
wiki tree --path=docs

# Control depth
wiki tree --depth=5
```

### Tags

```bash
# List all tags
wiki tags

# Create tag
wiki tags create "new-feature"

# Delete tag
wiki tags delete "deprecated"
```

### Assets

```bash
# List assets
wiki assets
wiki assets --folder=images
wiki assets --kind=IMAGE

# Upload file
wiki upload screenshot.png
wiki upload doc.pdf --folder=documents --name="manual.pdf"

# Delete asset
wiki asset-delete 42

# Create folder
wiki mkdir 0 images "Bilder"
```

### Options

```bash
--pretty, -p        Human-readable output (default: JSON)
--locale, -l de     Locale override
--private           Create private page
--draft             Create unpublished page
```

---

## 🔄 Error Handling

| Error | Handling |
|-------|----------|
| `413 Payload Too Large` | Throws descriptive error (chunking not auto-applied for pages) |
| `401 Unauthorized` | Clear token error message |
| `ECONNREFUSED` | Auto-retry with exponential backoff (3 attempts) |
| `Timeout` | 30s default, configurable via `WIKIJS_TIMEOUT` |

---

## 📐 Architecture

```
bin/wiki.js
├── GraphQL Client (query, mutation)
├── REST Upload (form-data)
├── Path Resolution (singleByPath)
├── CLI Parser (arg parsing)
└── Output Formatter (JSON / Pretty)
```

**Dependencies:**
- Node.js built-in modules only
- `form-data` for file uploads (installed on-demand)

---

## 🔐 Security

- Token **only** via environment variable (`WIKIJS_TOKEN`)
- No token logging
- Input validation (null bytes, size limits)
- Path sanitization (strips leading `/`)

---

## 📤 Examples

### Create Documentation Page

```bash
# Write content to file
cat > /tmp/api.md << 'EOF'
# API Reference

## Authentication

All requests require a Bearer token...

## Endpoints

- `GET /api/v1/pages` - List pages
- `POST /api/v1/pages` - Create page
EOF

# Upsert to Wiki
wiki upsert docs/api "API Reference" @/tmp/api.md "api,reference" --pretty
```

### Upload Screenshot and Embed

```bash
# Upload image
wiki upload screenshot.png --folder=images --name="api-auth-flow.png"
# Output: {"id":47,"url":"/f/a3f9b2/api-auth-flow.png",...}

# Create page with embedded image
wiki upsert docs/api-auth "API Authentication" '![Auth Flow](/f/a3f9b2/api-auth-flow.png)' "api"
```

### Batch Update via Script

```bash
#!/bin/bash
for file in docs/*.md; do
  name=$(basename "$file" .md)
  wiki upsert "docs/$name" "$name Documentation" "@$file" "docs"
done
```

---

## 🆚 Migration from V2

| V2 Command | V3 Command |
|------------|-----------|
| `wiki-v2 upsert ...` | `wiki upsert ...` |
| `wiki-v2 get ...` | `wiki get ...` |
| `wiki-v2 delete ...` | `wiki delete ...` |
| `wiki-v2 search ...` | `wiki search ...` |
| `wiki-v2 upload ...` | `wiki upload ...` |
| `wiki-v2 assets ...` | `wiki assets ...` |
| `wiki-v2 mkdir ...` | `wiki mkdir ...` |
| – | `wiki move ...` |
| – | `wiki copy ...` |
| – | `wiki history ...` |
| – | `wiki restore ...` |
| – | `wiki render ...` |
| – | `wiki tree ...` |
| – | `wiki tags ...` |
| – | `wiki asset-delete ...` |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `WIKIJS_TOKEN not set` | `export WIKIJS_TOKEN=...` |
| `Page not found` | Check path (no leading `/`) |
| `GraphQL Error: Unauthorized` | Token invalid or expired |
| `GraphQL Error: Forbidden` | **API key lacks write permissions** – create new key with write access in Admin UI |
| `Upload failed: 413` | File too large (>10MB) |
| `Timeout after 30s` | Increase `WIKIJS_TIMEOUT=60000` |
| `Cannot read properties of undefined (reading 'map')` | **Fixed in V3.1** – always include `tags: []` in update mutations |

## ⚠️ API Key Permissions

Wiki.js API keys have **per-key permissions**, not per-group permissions.

| JWT Claim | Meaning |
|-----------|---------|
| `api:1` | API Key ID 1 – may have different permissions than Key 2 |
| `grp:1` | Group ID 1 – does NOT determine write access |

**If `update` returns "Forbidden":**
1. Open Wiki.js Admin UI
2. Go to **API Keys**
3. Create new key with **write permissions** or edit existing key
4. Use the new key in `WIKIJS_TOKEN`

---

## 📚 Wiki.js API Reference

- GraphQL Schema: `{WIKIJS_URL}/graphql-playground`
- REST Upload: `POST {WIKIJS_URL}/u`
- Static Assets: `GET {WIKIJS_URL}/f/:hash/:filename`

---

*Version: 3.0 | Status: All-encompassing | Replaces: wiki-js-v2*