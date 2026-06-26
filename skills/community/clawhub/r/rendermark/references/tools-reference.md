# RenderMark Tools Reference

## Rendering Tools

### render_markdown
Convert markdown to styled HTML with syntax highlighting, TOC, themes, Mermaid diagrams, and KaTeX math.

**Parameters:**
- `markdown` (string, required): Markdown content
- `title` (string): Document title
- `showToc` (boolean): Include table of contents (default: true)
- `theme` (string): `default`, `dark`, `serif`, or `minimal`
- `template` (string): `report`, `meeting-notes`, `memo`, `letter`, `slides`, or `changelog`
- `github` (object): `{ owner, repo, branch?, path }` — resolves relative image paths to GitHub raw URLs
- `unsanitized` (boolean): Return unsanitized HTML (default: false)

### render_to_image
Render markdown as PNG or JPEG. Ideal for sharing visual previews in chat (Slack, Discord, Telegram).

**Parameters:**
- `markdown` (string, required): Markdown content
- `title` (string): Document title
- `format` (enum): `png` or `jpeg` (default: png)
- `width` (number): Viewport width in pixels (default: 1200)
- `quality` (number): JPEG quality 0–100 (default: 90)
- `theme` (string): Theme name
- `section` (string): Render only a specific heading section by name

### render_diff
Visual redline diff between two markdown versions. Green = additions, red strikethrough = deletions.

**Parameters:**
- `before` (string, required): Original markdown
- `after` (string, required): Revised markdown
- `title` (string): Document title
- `mode` (enum): `inline` or `side-by-side` (default: inline)
- `outputFormat` (enum): `html` or `image` (default: html)

## Export Tools

### export_markdown
Export markdown to a file on disk.

**Parameters:**
- `markdown` (string, required): Markdown content
- `title` (string, required): Document title (used for filename and header)
- `format` (enum, required): `pdf`, `docx`, or `html`
- `outputPath` (string): Where to save (defaults to current directory)
- `showToc` (boolean): Include TOC (default: true)
- `theme` (string): Theme name
- `github` (object): GitHub context for image resolution

### export_batch
Export multiple markdown files as a merged document or individual zip.

**Parameters:**
- `files` (array): `[{ path, title? }]` — list of markdown files
- `glob` (string): Glob pattern (e.g., `docs/**/*.md`)
- `format` (enum, required): `pdf`, `docx`, or `html`
- `mode` (enum): `merged` (one document) or `zip` (individual exports)
- `outputPath` (string): Where to save
- `title` (string): Title for merged document
- `theme` (string): Theme name

### validate_markdown
Check markdown for common issues.

**Parameters:**
- `markdown` (string, required): Markdown content
- `filePath` (string): File path for resolving relative links
- `checks` (array): Any of: `broken-links`, `missing-images`, `malformed-tables`, `unclosed-formatting`, `heading-structure`, `all` (default: all)

## Publishing Tools

### publish_to_rendermark
Publish markdown to rendermark.app and get a shareable link. Requires API key.

**Parameters:**
- `markdown` (string, required): Markdown content
- `title` (string, required): Document title
- `options` (object): `{ showToc?, showByLine? }`

### publish_to_google_docs
Publish markdown as a Google Doc. Requires Google OAuth setup.

**Parameters:**
- `markdown` (string, required): Markdown content
- `title` (string, required): Document title

### share_live_preview
Create a temporary shareable preview URL.

**Parameters:**
- `markdown` (string, required): Markdown content
- `title` (string): Document title
- `theme` (string): Theme name
- `expiresIn` (enum): `1h`, `4h`, `24h`, or `7d` (default: 24h)

## Document Management Tools

### read_document
Retrieve a document's raw markdown and metadata from RenderMark.

**Parameters:**
- `identifier` (string, required): Document slug, ID, or full rendermark.app URL

### update_document
Update an existing document on RenderMark.

**Parameters:**
- `identifier` (string, required): Document slug, ID, or URL
- `markdown` (string): New markdown content (replaces entire document)
- `title` (string): New title
- `publish` (boolean): Set publish state
- `options` (object): `{ showToc?, showByLine?, showDatePublished?, showDateUpdated?, protection? }`
  - `protection`: `none`, `password`, or `email`

### list_documents
List the user's documents. Supports search, filtering, and pagination.

**Parameters:**
- `search` (string): Search by title (fuzzy match)
- `published` (boolean): Filter by publish status
- `limit` (number): Max results (default: 20, max: 100)
- `offset` (number): Pagination offset
- `sortBy` (enum): `updated`, `created`, or `title` (default: updated)

### share_document
Share a document with specific people via email. Sets email-restricted protection.

**Parameters:**
- `identifier` (string, required): Document slug, ID, or URL
- `emails` (array of strings, required): Email addresses to grant access
- `message` (string): Optional message in share notification
- `notify` (boolean): Send email notification (default: true)

### delete_document
Permanently delete a document. Cannot be undone.

**Parameters:**
- `identifier` (string, required): Document slug, ID, or URL
- `confirm` (boolean, required): Must be `true`

## Sync Tools

### sync_from_github
Sync a markdown file from GitHub to RenderMark. Creates or updates a linked document.

**Parameters:**
- `owner` (string, required): Repository owner
- `repo` (string, required): Repository name
- `path` (string, required): Path to markdown file (e.g., `docs/README.md`)
- `branch` (string): Branch name (default: main)
- `autoSync` (boolean): Enable automatic sync via webhook (default: false)
- `publish` (boolean): Publish immediately (default: true)
- `title` (string): Override title

## Setup Tools

### setup_api_key
Opens the user's browser to sign in and generate an API key. Automatically saves to `~/.rendermark/config.json`.

**Parameters:** None
