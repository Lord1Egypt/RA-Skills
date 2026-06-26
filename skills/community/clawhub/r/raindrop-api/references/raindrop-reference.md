# Raindrop.io Reference

## Quick Start

- Developer docs: `https://developer.raindrop.io/`
- REST API base: `https://api.raindrop.io/rest/v1`
- MCP endpoint: `https://api.raindrop.io/rest/v2/ai/mcp`
- Request format:
  - Non-POST requests accept URL-encoded parameters.
  - POST requests use JSON with `Content-Type: application/json`.
- Response format: JSON
- Timestamp format: `YYYY-MM-DDTHH:MM:SSZ`
- OAuth request limit: `120 requests per minute per authenticated user`

## Terms And Constraints

- The docs allow commercial use, but explicitly forbid building an application, website, product, or business that harms, competes with, or replaces Raindrop.io.
- Do not propose abusive polling or multi-account rate-limit evasion.
- Respect live rate-limit headers:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Authentication

### Personal testing

- If the user only needs access to their own account for testing, the docs say they can use the app console's test token instead of completing the full OAuth flow.

### OAuth 2 authorization code flow

1. Register an app in the Raindrop.io app management console.
2. Send the user to:
   - `GET https://raindrop.io/oauth/authorize`
3. Include standard params:
   - `response_type=code`
   - `client_id`
   - `redirect_uri`
4. Exchange the code at:
   - `POST https://raindrop.io/oauth/access_token`
5. Send JSON with:
   - `code`
   - `client_id`
   - `client_secret`
   - `redirect_uri`
   - `grant_type=authorization_code`
6. Use the returned bearer token:
   - `Authorization: Bearer <access_token>`

### Authenticated calls

- Header format:

```http
Authorization: Bearer <access_token>
```

## MCP Server

- Endpoint: `https://api.raindrop.io/rest/v2/ai/mcp`
- Transport: Streamable HTTP only
- Availability: beta, Pro users only according to the docs
- Auth:
  - Prefer OAuth 2.1 interactive auth in compatible MCP clients
  - Bearer token auth also works
- Good fit:
  - Claude, ChatGPT, Cursor, VS Code, or another MCP-capable client that should browse and manage bookmarks directly

## Endpoint Map

### Collections

- Main docs:
  - `/v1/collections`
  - `/v1/collections/methods`
  - `/v1/collections/nested-structure`
  - `/v1/collections/sharing`
  - `/v1/collections/covers-icons`
- Use for:
  - Listing root collections
  - Listing nested collections
  - Fetching one collection
  - Creating, updating, deleting, expanding, emptying, merging, and bulk-removing collections
  - Sharing collections and managing collaborators
  - Searching covers and icons
- Important nuance:
  - Recreating the sidebar tree requires multiple calls. The docs say the group order and the child collections are not returned as a single ready-made tree.

### Raindrops

- Main docs:
  - `/v1/raindrops`
  - `/v1/raindrops/single`
  - `/v1/raindrops/multiple`
- Use for:
  - Getting one bookmark
  - Creating one bookmark
  - Updating or deleting one bookmark
  - Searching and paginating many bookmarks
  - Bulk updates or deletes
  - Moving bookmarks between collections
- Notable route patterns from the docs:
  - `GET /raindrop/{id}`
  - `POST /raindrop`
  - Bulk operations under the multiple-raindrops section

### Highlights

- Main docs: `/v1/highlights`
- Use for:
  - Get all highlights
  - Get highlights in a collection
  - Get highlights for a raindrop
  - Add, update, or remove a highlight

### User

- Main docs:
  - `/v1/user`
  - `/v1/user/authenticated`
- Use for:
  - Current authenticated user profile
  - Public user profile by name

### Tags

- Main docs: `/v1/tags`
- Use for:
  - Get tags for a collection or all collections
  - Rename a tag
  - Merge tags
  - Remove one or more tags

### Filters

- Main docs: `/v1/filters`
- Use for:
  - Broken links count
  - Duplicates count
  - Important count
  - Untagged count
  - Aggregated tag and content-type counts

### Import

- Main docs: `/v1/import`
- Use for:
  - Parse a URL and extract bookmark metadata
  - Check whether one or more URLs already exist
  - Parse an HTML bookmarks export file

### Export

- Main docs: `/v1/export`
- Route pattern:
  - `GET /raindrops/{collectionId}/export.{format}`
- Formats:
  - `csv`
  - `html`
  - `zip`
- Note:
  - Use collection ID `0` for all raindrops

### Backups

- Main docs: `/v1/backups`
- Use for:
  - Listing existing backup IDs
  - Downloading a backup file by ID and format
  - Triggering a new backup generation
- Notable behavior:
  - The docs mention email delivery for generated HTML exports

## Implementation Notes

- Use `GET`, `POST`, `PUT`, and `DELETE` per the docs' normal HTTP verb semantics.
- Treat `4xx` responses as caller or payload problems unless the docs indicate otherwise.
- Treat `5xx` as retryable server failures.
- Use `429` handling with backoff and reset timing from response headers.
- For browser-based integrations, the docs state that the API supports CORS.

## Useful User Requests

- "Build OAuth login for a Raindrop.io integration."
- "List collections and bookmark counts from Raindrop."
- "Search my raindrops by tag and update them in bulk."
- "Import bookmarks from an HTML export."
- "Export a collection as CSV."
- "Set up the Raindrop MCP server in an AI client."
