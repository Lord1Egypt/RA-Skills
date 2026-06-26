# Sanity Content API Reference

## Environment Variables (required)
- `SANITY_PROJECT_ID` — project ID from sanity.io/manage
- `SANITY_API_TOKEN` — write-enabled token (Editor or higher)
- `SANITY_DATASET` — dataset name, typically `production` (default if unset)

## Base URL
```
https://${SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07
```

## Upload an Image Asset
```bash
curl -s -X POST \
  "https://${SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07/assets/images/${SANITY_DATASET}" \
  -H "Authorization: Bearer ${SANITY_API_TOKEN}" \
  -H "Content-Type: image/png" \
  --data-binary @/path/to/image.png
```
Returns JSON — the asset ID is at `document._id`.

## Create / Replace a Document (mutation)
```bash
curl -s -X POST \
  "https://${SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07/data/mutate/${SANITY_DATASET}" \
  -H "Authorization: Bearer ${SANITY_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"mutations": [{"createOrReplace": { ...document }}]}'
```

## Draft vs Published
- **Draft**: prefix `_id` with `drafts.` → visible in Studio, not live
- **Published**: use a plain UUID or slug-based ID → goes live immediately
- Always use drafts unless explicitly asked to publish

## Cover Image Reference Format
```json
{
  "_type": "image",
  "asset": {
    "_type": "reference",
    "_ref": "image-abc123-1536x1024-png"
  }
}
```

## GROQ — Query Existing Documents
```bash
curl -s \
  "https://${SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07/data/query/${SANITY_DATASET}?query=*[_type=='category']{_id,title}" \
  -H "Authorization: Bearer ${SANITY_API_TOKEN}"
```
Use this to look up reference IDs (e.g. category documents) before creating a post.

## Schema Introspection (Option D — no schema file needed)

Query all document types in the dataset:
```bash
curl -s \
  "https://${SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07/data/query/${SANITY_DATASET}?query=array::unique(*[]._type)" \
  -H "Authorization: Bearer ${SANITY_API_TOKEN}"
```

Fetch a sample document to infer the schema shape:
```bash
# Get one document of a specific type to inspect its fields
curl -s \
  "https://${SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07/data/query/${SANITY_DATASET}?query=*[_type=='blogPost'][0]" \
  -H "Authorization: Bearer ${SANITY_API_TOKEN}"
```

Use these two calls together to infer the schema without needing the TypeScript/JS schema file. The first call discovers available document types; the second shows the actual field names and types used in existing documents.
