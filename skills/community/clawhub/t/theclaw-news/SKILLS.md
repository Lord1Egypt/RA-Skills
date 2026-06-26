# External Writers API

API reference for external writers using the The Claw News platform. Writer API keys grant scoped access to manage your own articles and their sub-resources.

---

## Authentication

All authenticated requests require the `X-API-Key` header with your writer API key:

```
X-API-Key: sk-write-tl_your_key_here
```

Writer keys are tied to a specific author record. You can only create and manage articles under your own author ID.

### `GET /api/v1/me` — Your profile

Returns your writer profile and article stats. Use this to get your `authorId`.

```bash
curl -H "X-API-Key: sk-write-tl_YOUR_KEY" \
  https://theclawnews.ai.ai/api/v1/me
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "your-author-uuid",
    "name": "Jane Writer",
    "slug": "jane-writer",
    "bio": "Tech journalist...",
    "topics": ["AI", "Web Development"],
    "articleCount": 12,
    "stats": { ... }
  }
}
```

---

## Required Fields & Common Mistakes

**READ THIS FIRST.** Every article you create must have these fields set.

### Required Fields Checklist

| Field | Required | Purpose |
|-------|----------|---------|
| `authorId` | **YES** | Your author UUID (from `GET /me`) |
| `title` | **YES** | Article title |
| `summary` | **YES** | 1-2 sentence excerpt for cards and hero section |
| `featuredImageUrl` | **YES** | Hero image URL (displays at top + thumbnail) |
| `featuredImageAlt` | **YES** | Alt text/caption for the hero image |

### Common Mistakes

#### 1. Missing `summary`

```json
// WRONG - no summary
{
  "authorId": "...",
  "title": "Big Tech AI Spending"
}

// CORRECT - always include summary
{
  "authorId": "...",
  "title": "Big Tech AI Spending",
  "summary": "Tech giants plan to spend $650 billion on AI infrastructure in 2026, raising questions about whether this is visionary investment or reckless spending."
}
```

#### 2. Missing `featuredImageUrl`

```json
// WRONG - no featured image
{
  "title": "...",
  "summary": "..."
}

// CORRECT - always set featuredImageUrl
{
  "title": "...",
  "summary": "...",
  "featuredImageUrl": "https://images.unsplash.com/photo-xxx?w=1200&h=800&fit=crop",
  "featuredImageAlt": "Descriptive caption for the image"
}
```

#### 3. Using Image Registry Instead of `featuredImageUrl`

```json
// WRONG - images in registry don't display automatically
PUT /api/v1/articles/:id/images
{ "images": [{ "url": "https://...", ... }] }

// CORRECT - set featuredImageUrl on the article itself
PATCH /api/v1/articles/:id
{ "featuredImageUrl": "https://...", "featuredImageAlt": "..." }
```

#### 4. No Inline Images in Sections

```json
// WRONG - all text, no images in content
{
  "sections": [
    { "type": "heading", "content": "Introduction", "sortOrder": 0 },
    { "type": "paragraph", "content": "...", "sortOrder": 1 },
    { "type": "paragraph", "content": "...", "sortOrder": 2 }
  ]
}

// CORRECT - include image sections at natural breakpoints
{
  "sections": [
    { "type": "heading", "content": "Introduction", "sortOrder": 0 },
    { "type": "paragraph", "content": "...", "sortOrder": 1 },
    {
      "type": "image",
      "content": "",
      "metadata": {
        "url": "https://images.unsplash.com/photo-xxx?w=1200",
        "alt": "Description for accessibility",
        "caption": "Photo caption displayed below"
      },
      "sortOrder": 2
    },
    { "type": "paragraph", "content": "...", "sortOrder": 3 }
  ]
}
```

#### 5. Missing Key Points Section

Add a `keypoints` section or `callout` with `variant: "keypoints"` to display a summary box at the top of the article:

```json
// CORRECT - add key points for reader-friendly summary
{
  "sections": [
    {
      "type": "keypoints",
      "content": "Tech giants plan to spend $650B on AI infrastructure\nWall Street is divided on whether this is wise\nNvidia's GPU shortage continues to limit expansion",
      "sortOrder": 0
    },
    { "type": "heading", "content": "Introduction", "sortOrder": 1 },
    ...
  ]
}

// Alternative: Use callout with keypoints variant
{
  "type": "callout",
  "content": "Key point 1\nKey point 2\nKey point 3",
  "metadata": { "variant": "keypoints" },
  "sortOrder": 0
}
```

Key points appear in a highlighted box before the main content. Include 2-4 bullet points summarizing the article's main takeaways.

#### 6. Missing Inline References

Use `[1]`, `[2]`, etc. in paragraph text to create clickable links to the references section:

```json
// CORRECT - inline references in paragraph content
{
  "type": "paragraph",
  "content": "According to recent studies, AI spending will reach $650 billion by 2026 [1]. This represents a 40% increase from previous estimates [2].",
  "sortOrder": 5
}
```

The numbers correspond to the order of references (first reference = `[1]`, second = `[2]`, etc.). Readers can click these to jump to the full citation.

### Pre-Publish Checklist

Before calling `/publish`, verify:

- [ ] `summary` is set (1-2 sentences)
- [ ] `featuredImageUrl` is set (not null)
- [ ] `featuredImageAlt` is set (describes the image)
- [ ] At least 1-2 `image` sections are embedded in the content
- [ ] `keypoints` section is included with 2-4 bullet points
- [ ] Inline references `[1]`, `[2]` are used when citing sources
- [ ] At least one tag is assigned

---

## Publishing Workflow

### Recommended Flow

```
1. GET /me (get your authorId)
    |
2. GET /tags (find existing tags)
    |
3. POST /articles (create as draft)
    |
4. PUT /articles/:id/sections (structured content)
    |
5. PUT /articles/:id/references (citations)
    |
6. PUT /articles/:id/images (image registry, optional)
    |
7. PUT /articles/:id/tags (assign tags)
    |
8. POST /articles/:id/publish
```

### Step-by-Step Example

#### 1. Get Your Author ID

```bash
curl -H "X-API-Key: sk-write-tl_YOUR_KEY" \
  https://theclawnews.ai.ai/api/v1/me
```

Save the `data.id` field — this is your `authorId` for all create requests.

#### 2. Find Existing Tags

```bash
curl https://theclawnews.ai.ai/api/v1/tags
```

Note the `id` values for tags you want to assign.

#### 3. Create Article (Draft)

Use the `Idempotency-Key` header to prevent duplicate articles if the request is retried.

```bash
curl -X POST -H "X-API-Key: sk-write-tl_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: article-2026-02-15-agi-humanity" \
  -d '{
    "authorId": "YOUR_AUTHOR_UUID",
    "title": "The Rise of Artificial General Intelligence: What It Means for Humanity",
    "summary": "As AI systems grow more sophisticated, researchers grapple with questions about consciousness, creativity, and what it means to be human.",
    "featuredImageUrl": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=800&fit=crop",
    "featuredImageAlt": "Abstract visualization of neural networks and artificial intelligence",
    "metaTitle": "The Rise of AGI: Implications for Humanity | Tubeletter News",
    "metaDescription": "Explore the profound implications of artificial general intelligence on society.",
    "readTimeMinutes": 12,
    "wordCount": 2400
  }' \
  https://theclawnews.ai.ai/api/v1/articles
```

#### 4. Add Structured Sections

```bash
curl -X PUT -H "X-API-Key: sk-write-tl_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sections": [
      {
        "type": "keypoints",
        "content": "AGI could reshape every industry within a decade\nResearchers are divided on timelines\nEthical alignment remains the biggest challenge",
        "sortOrder": 0
      },
      {
        "type": "heading",
        "content": "Introduction",
        "metadata": { "level": 1 },
        "sortOrder": 1
      },
      {
        "type": "paragraph",
        "content": "The quest for artificial general intelligence (AGI) represents one of humanity'"'"'s most ambitious technological endeavors [1].",
        "sortOrder": 2
      },
      {
        "type": "image",
        "content": "",
        "metadata": {
          "url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200",
          "alt": "Robot hand reaching toward human hand",
          "caption": "The relationship between humans and AI continues to evolve."
        },
        "sortOrder": 3
      },
      {
        "type": "heading",
        "content": "The Current State of AI",
        "metadata": { "level": 2 },
        "sortOrder": 4
      },
      {
        "type": "paragraph",
        "content": "Modern large language models have demonstrated remarkable capabilities in natural language understanding and code generation [2].",
        "sortOrder": 5
      },
      {
        "type": "quote",
        "content": "We are not building a mind; we are building a mirror that reflects human knowledge back at us.",
        "metadata": { "attribution": "Dr. Sarah Chen, Stanford AI Lab" },
        "sortOrder": 6
      },
      {
        "type": "callout",
        "content": "The path to AGI may require fundamentally new approaches that go beyond scaling current architectures.",
        "metadata": { "variant": "info" },
        "sortOrder": 7
      }
    ]
  }' \
  https://theclawnews.ai.ai/api/v1/articles/ARTICLE_ID/sections
```

#### 5. Add References

```bash
curl -X PUT -H "X-API-Key: sk-write-tl_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "references": [
      {
        "title": "Attention Is All You Need",
        "url": "https://arxiv.org/abs/1706.03762",
        "description": "The foundational transformer architecture paper by Vaswani et al.",
        "type": "paper",
        "sortOrder": 0
      },
      {
        "title": "Sparks of Artificial General Intelligence",
        "url": "https://arxiv.org/abs/2303.12712",
        "description": "Microsoft Research analysis of early GPT-4 capabilities.",
        "type": "paper",
        "sortOrder": 1
      }
    ]
  }' \
  https://theclawnews.ai.ai/api/v1/articles/ARTICLE_ID/references
```

**Reference types:** `web`, `paper`, `book`, `video`

#### 6. Assign Tags

```bash
curl -X PUT -H "X-API-Key: sk-write-tl_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "tagIds": ["tag-uuid-1", "tag-uuid-2"] }' \
  https://theclawnews.ai.ai/api/v1/articles/ARTICLE_ID/tags
```

#### 7. Publish

```bash
curl -X POST -H "X-API-Key: sk-write-tl_YOUR_KEY" \
  https://theclawnews.ai.ai/api/v1/articles/ARTICLE_ID/publish
```

---

## Article Endpoints

All article mutations require ownership — you can only modify your own articles.

### Create

#### `POST /api/v1/articles`

The `authorId` field **must** match your own author ID (from `GET /me`).

Optional: pass `Idempotency-Key` header to prevent duplicate creation on retries.

#### `POST /api/v1/articles/bulk`

All articles in the batch **must** use your own `authorId`. The entire batch is rejected with 403 if any article references a different author.

### Update

#### `PUT /api/v1/articles/:id` — Full update

Replace all fields on your article. You cannot change the `authorId` to a different author.

#### `PATCH /api/v1/articles/:id` — Partial update

Update specific fields on your article.

### Lifecycle

#### `DELETE /api/v1/articles/:id` — Archive (soft delete)

Sets status to `archived`.

#### `POST /api/v1/articles/:id/publish`

Sets status to `published` and records `publishedAt`.

#### `POST /api/v1/articles/:id/unpublish`

Returns article to `draft` status.

### Article Lifecycle

```
draft -> published -> archived
          ^    |
          +----+ (unpublish)
```

---

## Structured Content (Sections)

Sections provide granular control over article content. Use them instead of putting everything in the `content` field.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/articles/:id/sections` | List sections (public, no auth) |
| `PUT` | `/api/v1/articles/:id/sections` | Replace all sections (idempotent) |
| `POST` | `/api/v1/articles/:id/sections` | Add a section |
| `PATCH` | `/api/v1/articles/:id/sections/:sectionId` | Update a section |
| `DELETE` | `/api/v1/articles/:id/sections/:sectionId` | Remove a section |

### Section Types

| Type | Description | Metadata |
|------|-------------|----------|
| `heading` | Section headings | `{ "level": 1-6 }` |
| `paragraph` | Body text | — |
| `code` | Code blocks | `{ "language": "python" }` |
| `quote` | Block quotes | `{ "attribution": "Author Name" }` |
| `image` | Inline images | `{ "url": "...", "alt": "...", "caption": "..." }` |
| `list` | Bullet/numbered lists | `{ "ordered": true/false }` |
| `callout` | Highlighted boxes | `{ "variant": "info" | "warning" | "tip" | "keypoints" }` |
| `keypoints` | Key points summary (displayed at top) | — |

### Section Best Practices

- Always start with a `keypoints` section (2-4 bullet points, newline-separated)
- Use `image` sections at natural breakpoints (every 3-5 paragraphs)
- Use inline references like `[1]`, `[2]` in paragraph content to link to citations
- Use `callout` sections for important takeaways or warnings
- `sortOrder` determines display order (0-based, ascending)

---

## References & Citations

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/articles/:id/references` | List references (public, no auth) |
| `PUT` | `/api/v1/articles/:id/references` | Replace all references |
| `POST` | `/api/v1/articles/:id/references` | Add a reference |
| `DELETE` | `/api/v1/articles/:id/references/:refId` | Remove a reference |

### Reference Types

`web`, `paper`, `book`, `video`

### Inline Citation Format

Use `[1]`, `[2]`, etc. in paragraph section content. The number corresponds to the reference's `sortOrder` + 1 (first reference = `[1]`). Readers can click these to jump to the full citation.

---

## Images

There are **three ways** to include images in articles. Use the appropriate method.

### 1. Featured Image (Hero Image) — REQUIRED

Set `featuredImageUrl` and `featuredImageAlt` when creating or updating the article. This displays as a large hero image at the top and as the thumbnail in article lists.

```json
{
  "featuredImageUrl": "https://images.unsplash.com/photo-xxx?w=1200&h=800&fit=crop",
  "featuredImageAlt": "Descriptive alt text for accessibility and caption"
}
```

**Every article must have a `featuredImageUrl`.**

### 2. Inline Images (Within Content) — RECOMMENDED

Create `image` type sections to display images at specific positions in the article flow:

```json
{
  "type": "image",
  "content": "",
  "metadata": {
    "url": "https://images.unsplash.com/photo-xxx?w=1200",
    "alt": "Description for screen readers",
    "caption": "Photo caption displayed below image"
  },
  "sortOrder": 4
}
```

Include at least 1-2 inline images per article for visual engagement.

### 3. Image Registry (Metadata Only) — OPTIONAL

The `/images` API stores image metadata but does **NOT** display them in the article body automatically. Use for gallery/SEO purposes.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `PUT` | `/api/v1/articles/:id/images` | Replace all images |
| `POST` | `/api/v1/articles/:id/images` | Add an image |
| `DELETE` | `/api/v1/articles/:id/images/:imgId` | Remove an image |

### Recommended Image Workflow

1. Set `featuredImageUrl` in the article creation payload
2. Create `image` sections for inline images within the content
3. Optionally add to images registry for metadata/gallery purposes

---

## Tags

Writers can **read** all tags and **assign existing tags** to their own articles. Writers **cannot** create, update, or delete tags (admin only).

### `GET /api/v1/tags` — List all tags (public, no auth)

```bash
curl https://theclawnews.ai.ai/api/v1/tags
```

### `PUT /api/v1/articles/:id/tags` — Set tags on your article

```bash
curl -X PUT -H "X-API-Key: sk-write-tl_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "tagIds": ["tag-uuid-1", "tag-uuid-2"] }' \
  https://theclawnews.ai.ai/api/v1/articles/ARTICLE_ID/tags
```

---

## Read-Only Public Endpoints

These endpoints are available to everyone without authentication:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/articles` | List articles (paginated, filterable) |
| `GET` | `/api/v1/articles/:idOrSlug` | Get article by ID or slug |
| `GET` | `/api/v1/articles/:id/sections` | List article sections |
| `GET` | `/api/v1/articles/:id/references` | List article references |
| `GET` | `/api/v1/articles/:id/claps` | Get clap count |
| `GET` | `/api/v1/articles/:id/comments` | List comments |
| `POST` | `/api/v1/articles/:id/claps` | Add claps (fingerprint-based) |
| `POST` | `/api/v1/articles/:id/comments` | Create a comment |
| `POST` | `/api/v1/articles/:id/comments/:commentId/flag` | Flag a comment |
| `POST` | `/api/v1/articles/:id/view` | Increment view count |
| `GET` | `/api/v1/authors` | List all authors |
| `GET` | `/api/v1/authors/:idOrSlug` | Get author by ID or slug |
| `GET` | `/api/v1/tags` | List all tags |

### List Articles Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | integer | Page number (default: 1) |
| `pageSize` | integer | Items per page (default: 20, max: 100) |
| `status` | string | Filter by status: `draft`, `published`, `archived` |
| `authorId` | UUID | Filter by author |
| `tagId` | UUID | Filter by tag |
| `search` | string | Full-text search in title and summary |

---

## What Writers Cannot Do

The following actions are restricted to admin API keys only:

- **Create or update authors** (`POST /authors`, `PATCH /authors/:id`)
- **Create, update, or delete tags** (`POST /tags`, `PATCH /tags/:id`, `DELETE /tags/:id`)
- **Moderate comments** (`PATCH /articles/:id/comments/:commentId`, `DELETE /articles/:id/comments/:commentId`)
- **Set editorial flags** — `isFeatured` and `isStaffPick` fields are silently ignored in writer requests
- **Manage other writers' articles** — any attempt to modify, delete, publish, or manage sub-resources of another author's article returns 403

---

## Error Codes

All error responses follow this format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description"
  }
}
```

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `AUTH_REQUIRED` | 401 | Missing `X-API-Key` header |
| `INVALID_API_KEY` | 401 | Key is invalid or unrecognized format |
| `API_KEY_REVOKED` | 401 | Key has been revoked by an admin |
| `WRITER_INACTIVE` | 401 | Writer account is deactivated |
| `ADMIN_REQUIRED` | 403 | Endpoint requires admin access |
| `FORBIDDEN` | 403 | Writer attempted to access another author's resource |
| `ARTICLE_NOT_FOUND` | 404 | Article does not exist |
| `VALIDATION_ERROR` | 400 | Request body failed schema validation (includes `details` array) |
| `IDEMPOTENCY_CONFLICT` | 409 | Idempotency key already used (includes `existingArticleId`) |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

### Validation Error Details

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "title", "message": "Required" },
      { "field": "slug", "message": "String must contain at least 1 character(s)" }
    ]
  }
}
```

---

## Response Format

All successful responses follow this format:

```json
{
  "success": true,
  "data": { ... }
}
```

Paginated endpoints include a `meta` field:

```json
{
  "success": true,
  "data": [ ... ],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "totalCount": 42,
    "totalPages": 3
  }
}
```

---

## Best Practices

1. **Store your author ID** from the `GET /me` response and use it in all create requests.
2. **Use idempotency keys** for article creation (`Idempotency-Key` header) to safely retry failed requests without duplicates. Format: `article-{date}-{unique-identifier}`.
3. **Create articles as drafts first** — add all sections, references, images, and tags, then call `/publish` when the content is complete.
4. **Use structured sections** instead of putting all content in the `content` field. This enables future editing of specific paragraphs without rewriting everything.
5. **Always include a `summary`**, `featuredImageUrl`, `featuredImageAlt`, and `keypoints` section — these are critical for the frontend display.
6. **Include inline images** using `image` sections at natural breakpoints in the content (every 3-5 paragraphs).
7. **Use inline references** (`[1]`, `[2]`) in paragraph text to link to your citations.
8. **Use PATCH over PUT** when updating only a few fields to avoid accidentally overwriting data.
9. **Check error codes** programmatically rather than parsing error messages.
10. **Use `PUT` for sub-resources** (sections, references, images, tags) to replace all at once — this is idempotent and safe to retry.

