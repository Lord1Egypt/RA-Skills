---
name: sanity-cms
description: Publish content to any Sanity CMS instance. Use when asked to create a Sanity draft, push a document to Sanity, upload an image asset to Sanity, or convert content into a Sanity-formatted document. Works with any document type and schema — not limited to blog posts. Requires SANITY_PROJECT_ID and SANITY_API_TOKEN env vars.
---

# Sanity CMS Skill

Publishes documents to Sanity CMS via the Content API. Works with any schema.

## References
- **API patterns (upload, mutate, query)**: `references/api.md`
- **Portable Text body format**: `references/portable-text.md`

## Workflow

### 1. Understand the target schema

Four ways to get schema info — try in this order:

**A — File in workspace:** User drops schema at a known path (e.g. `sanity-schemas/blogPost.ts`). Read it directly.

**B — Pasted in chat:** User pastes the schema TypeScript/JS. Read it from the conversation.

**C — Remote URL:** User shares a GitHub raw URL or similar. Fetch with `web_fetch`.

**D — API introspection (no file needed):** Query the dataset directly — see `references/api.md` (Schema Introspection section). Use `array::unique(*[]._type)` to discover document types, then fetch one sample document to infer field names and shapes. Works without any schema file at all.

Once you have the schema (by any method):
- For `array` fields with `type: 'block'`, use Portable Text format — see `references/portable-text.md`
- For `reference` fields (categories, authors, tags), query existing documents via GROQ — see `references/api.md`

### 2. Format the document JSON
Build a JSON object matching the schema:
- Omit `_id` — the script generates a `drafts.` prefixed UUID automatically
- Omit the cover image field — the script injects it after uploading
- All required fields must be present and within any validation constraints
- Save to a logical path (e.g. `brain/projects/<slug>-sanity.json` or similar)

### 3. Run the publish script

The script is at `scripts/publish_draft.sh` within this skill directory. Resolve the path relative to where the skill is installed (e.g. `~/.openclaw/skills/sanity-cms/scripts/publish_draft.sh` or `<workspace>/skills/sanity-cms/scripts/publish_draft.sh`).

```bash
bash <skill-dir>/scripts/publish_draft.sh \
  path/to/document.json \
  path/to/cover-image.png   # optional
```

**Optional env overrides:**
| Var | Default | Purpose |
|-----|---------|---------|
| `SANITY_DATASET` | `production` | Target dataset |
| `COVER_IMAGE_FIELD` | `coverImage` | Field name for cover image |
| `DRAFT_PREFIX` | `true` | Set to `false` to publish immediately |

Example with overrides:
```bash
SANITY_DATASET=staging COVER_IMAGE_FIELD=mainImage \
  bash <skill-dir>/scripts/publish_draft.sh doc.json cover.jpg
```

### 4. Confirm and report
After the script prints a draft ID, report to the user:
- The draft document ID
- A link to Sanity Studio (ask if unsure of the Studio URL)
- Which fields, if any, still need manual attention in Studio (e.g. unpopulated references)

## Env Vars
| Var | Description |
|-----|-------------|
| `SANITY_PROJECT_ID` | Sanity project ID |
| `SANITY_API_TOKEN` | Write-enabled token (Editor or higher) |
| `SANITY_DATASET` | Dataset (optional, default: `production`) |

## Tips
- Always create drafts first (`DRAFT_PREFIX=true`) unless the user explicitly wants to publish live
- If a schema has `reference` fields, query for the referenced document IDs via GROQ before building the JSON — see `references/api.md`
- The script works with any document type: blog posts, pages, products, authors, etc.
- Cover image upload is optional — omit the second argument if the schema has no image field
