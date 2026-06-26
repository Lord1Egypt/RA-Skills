---
name: sanity
description: Query and manage Sanity CMS content via GROQ queries and the Sanity HTTP API. Use when asked to fetch content from a Sanity dataset, create or update documents, upload assets, run GROQ queries, manage drafts, or interact with Sanity Content Lake. Requires SANITY_PROJECT_ID, SANITY_DATASET, and SANITY_API_TOKEN env vars.
---

# Sanity CMS Skill

Sanity API base: `https://<projectId>.api.sanity.io/v2021-10-21`

## Env Vars
```bash
SANITY_PROJECT_ID=abc123
SANITY_DATASET=production   # or staging
SANITY_API_TOKEN=sk...      # from sanity.io/manage > API > Tokens
SANITY_BASE="https://$SANITY_PROJECT_ID.api.sanity.io/v2021-10-21"
```

## GROQ Queries (Read)

### Fetch All Documents of a Type
```bash
curl -G "$SANITY_BASE/data/query/$SANITY_DATASET" \
  -H "Authorization: Bearer $SANITY_API_TOKEN" \
  --data-urlencode 'query=*[_type == "post"]{_id, title, slug, publishedAt}'
```

### Fetch Single Document by Slug
```bash
curl -G "$SANITY_BASE/data/query/$SANITY_DATASET" \
  -H "Authorization: Bearer $SANITY_API_TOKEN" \
  --data-urlencode 'query=*[_type == "post" && slug.current == $slug][0]' \
  --data-urlencode '$slug="my-blog-post"'
```

### Complex Query with References
```bash
# Posts with author name resolved
*[_type == "post"]{title, "author": author->name, "category": category->title, body}
```

### Count Documents
```groq
count(*[_type == "post"])
```

## Mutations (Create/Update/Delete)

### Create Document
```bash
curl -X POST "$SANITY_BASE/data/mutate/$SANITY_DATASET" \
  -H "Authorization: Bearer $SANITY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mutations": [{
      "create": {
        "_type": "post",
        "_id": "drafts.new-post-id",
        "title": "New Blog Post",
        "slug": {"_type": "slug", "current": "new-blog-post"},
        "publishedAt": "2026-03-27T00:00:00Z"
      }
    }]
  }'
```

### Update Document (Patch)
```bash
curl -X POST "$SANITY_BASE/data/mutate/$SANITY_DATASET" \
  -H "Authorization: Bearer $SANITY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mutations": [{
      "patch": {
        "id": "<document_id>",
        "set": {"title": "Updated Title", "status": "published"}
      }
    }]
  }'
```

### Delete Document
```bash
-d '{"mutations": [{"delete": {"id": "<document_id>"}}]}'
```

### Publish Draft
```bash
# Move draft to published: delete draft, create published version
-d '{
  "mutations": [
    {"delete": {"id": "drafts.<doc_id>"}},
    {"createOrReplace": {"_id": "<doc_id>", "_type": "post", ...fields}}
  ]
}'
```

## GROQ Syntax Reference
- Filter: `*[_type == "post" && status == "published"]`
- Sort: `| order(publishedAt desc)`
- Slice: `[0...10]`
- Projection: `{title, "authorName": author->name}`
- References: `->` dereferences a reference field
- `$param` for query parameters (pass as `$paramName=value`)

## Tips
- IDs starting with `drafts.` are unpublished drafts
- Use `_rev` field to detect conflicts on concurrent edits
- Token needs "Editor" role minimum for mutations; "Viewer" for queries only
- GROQ playground: sanity.io/manage > your project > Vision tab
