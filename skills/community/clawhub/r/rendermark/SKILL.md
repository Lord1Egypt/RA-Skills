---
name: rendermark
description: Professional markdown rendering, export, and publishing via MCP. Use when user asks to "render markdown", "export to PDF", "convert to DOCX", "create a document", "publish a document", "share a link", "make a slide deck", "diff two markdown files", "export to HTML", "create a shareable document", "sync docs from GitHub", or "generate an image of this markdown". Do NOT use for simple markdown editing, code generation, or general writing that doesn't need styled output.
license: MIT-0
compatibility: Requires Node.js 18+ and npx. PDF/image export requires Chrome or Browserless API. Google Docs requires OAuth setup.
metadata:
  author: RenderMark
  version: 0.1.8
  mcp-server: rendermark
  category: document-creation
  tags: [markdown, pdf, docx, html, export, publishing, mermaid, slides, github-sync, google-docs]
  openclaw:
    requires:
      bins:
        - npx
      config:
        - ~/.rendermark/config.json
    primaryEnv: RENDERMARK_API_KEY
    install:
      - kind: node
        package: "@rendermark/mcp-server"
        bins: [rendermark-mcp]
    homepage: https://rendermark.app
---

# RenderMark

Convert markdown into beautiful, shareable documents — PDF, DOCX, HTML, images, and hosted web pages.

## When to use RenderMark

Use these tools when the user needs **styled output** from markdown — not when they're just writing or editing markdown content.

**Use RenderMark when:**
- User wants to export, publish, or share a document
- User needs a visual preview (HTML, PDF, image) of markdown
- User wants to compare two document versions visually
- User asks to sync documentation from GitHub
- User needs batch export of multiple markdown files

**Do NOT use RenderMark when:**
- User is just writing or editing markdown (use normal text editing)
- User wants to run code or generate non-document output
- User needs general file format conversion unrelated to markdown
- Simple markdown preview without styling is sufficient

## Instructions

### Step 1: Choose the right tool for the task

| User wants to... | Tool to use |
|---|---|
| Preview styled markdown | `render_markdown` |
| Export a file (PDF, DOCX, HTML) | `export_markdown` |
| Export multiple files at once | `export_batch` |
| Create a PNG/JPEG image | `render_to_image` |
| Publish to the web with a shareable link | `publish_to_rendermark` |
| Publish as a Google Doc | `publish_to_google_docs` |
| Share with specific people | `share_document` |
| Compare two versions | `render_diff` |
| Check markdown quality | `validate_markdown` |
| Import from GitHub | `sync_from_github` |

### Step 2: Apply themes and options

Four built-in themes are available: `default` (light, clean sans-serif), `dark` (dark background), `serif` (Georgia, academic), `minimal` (stripped-down).

Pass the `theme` parameter to any render/export tool. If the user doesn't specify a theme, use `default`.

Table of contents is included by default. Set `showToc: false` to disable.

### Step 3: Verify output

- For `export_markdown`: Returns a file path. Confirm the file was saved.
- For `publish_to_rendermark`: Returns a URL. Share the link with the user.
- For `render_to_image`: Returns image data. Show or save as needed.

### Step 4: Use markdown features effectively

RenderMark supports GitHub-flavored markdown plus these extensions:
- **Mermaid diagrams**: Fenced code blocks with language `mermaid` render as interactive diagrams
- **KaTeX math**: Inline `$...$` and display `$$...$$` for mathematical notation
- **Syntax highlighting**: All common programming languages
- **Frontmatter**: YAML frontmatter (`title`, `theme`, `template`, `toc`) is parsed and applied automatically
- **Templates**: `report`, `meeting-notes`, `memo`, `letter`, `slides`, `changelog`
- **Task lists**, **footnotes**, **tables** with alignment, and **collapsible sections** (`<details>`)

### Step 5: Apply best practices

- **Always include a title** when publishing or exporting — extract from frontmatter, first `# heading`, or filename
- **Default to `showToc: true`** for documents longer than a few paragraphs
- **Choose themes contextually**: `serif` for formal documents, `dark` for technical docs, `default` for general use
- **For GitHub READMEs**, always pass the `github` context object (`{ owner, repo, branch, path }`) so relative image paths resolve correctly
- **Prefer `publish_to_rendermark` over `export_markdown`** when the user says "share" — a link is usually more convenient than a file
- **Run `validate_markdown` first** on important documents to catch broken links and structural issues before publishing

For full tool parameter details, see `references/tools-reference.md`.

## Available Tools (16)

| Tool | Description |
|------|-------------|
| `render_markdown` | Convert markdown to styled HTML with themes, TOC, syntax highlighting |
| `render_to_image` | Render markdown to PNG/JPEG — ideal for chat sharing (Slack, Discord) |
| `render_diff` | Visual redline diff between two markdown versions |
| `export_markdown` | Export to PDF, DOCX, or HTML file on disk |
| `export_batch` | Batch export multiple files (merged or individual zip) |
| `validate_markdown` | Check for broken links, malformed tables, structural issues |
| `publish_to_rendermark` | Publish to rendermark.app with a shareable URL |
| `publish_to_google_docs` | Publish as a Google Doc (requires OAuth setup) |
| `share_live_preview` | Generate a temporary preview link (1h to 7d expiry) |
| `share_document` | Share with specific emails via email-restricted access |
| `read_document` | Fetch document content and metadata by URL, slug, or ID |
| `update_document` | Update content, title, settings, or protection on a published document |
| `list_documents` | List documents with search, filtering, and pagination |
| `delete_document` | Permanently delete a document (requires explicit confirmation) |
| `sync_from_github` | Sync a markdown file from GitHub to RenderMark |
| `setup_api_key` | Authenticate via browser and save API key automatically |

## Examples

### Example 1: Export a README to PDF

User says: "Export my README to PDF with the serif theme"

Actions:
1. Call `export_markdown` with format `pdf`, theme `serif`, and the markdown content
2. Return the file path to the user

Result: PDF file saved locally with serif styling, table of contents, and syntax highlighting.

### Example 2: Publish and share a document

User says: "Publish this document and share it with my team"

Actions:
1. Call `publish_to_rendermark` with the markdown content and a title
2. Call `share_document` with the returned document ID and email addresses
3. Return the shareable URL

Result: Document published at a rendermark.app URL, sharing invites sent.

### Example 3: Compare two versions

User says: "Show me the diff between the old and new version"

Actions:
1. Call `render_diff` with the old and new markdown content
2. Return the visual diff HTML

Result: Side-by-side styled diff highlighting additions, deletions, and changes.

### Example 4: Batch export project docs

User says: "Export all the markdown files in this folder as PDFs"

Actions:
1. Gather all .md files and their contents
2. Call `export_batch` with the files array and format `pdf`
3. Return file paths

Result: All markdown files exported as individual PDFs in the same directory.

### Example 5: Sync and publish a GitHub README

User says: "Sync my project's README from GitHub and publish it"

Actions:
1. Call `sync_from_github` with the owner, repo, and path (`README.md`)
2. Return the published URL to the user

Result: README imported from GitHub, published at rendermark.app with relative images resolved.

### Example 6: Create a meeting notes document

User says: "Turn these notes into a proper meeting notes document and share it with the team"

Actions:
1. Call `render_markdown` with template `meeting-notes` to preview
2. Call `publish_to_rendermark` with the markdown and title
3. Call `share_document` with the document ID and team email addresses
4. Return the shareable URL

Result: Formatted meeting notes published and shared via email.

## Setup

Install via `npx -y @rendermark/mcp-server@latest`. Requires a RenderMark API key from https://rendermark.app/settings/keys.

For detailed setup including PDF export, Google Docs, and troubleshooting, see `references/setup-guide.md`.

## Troubleshooting

### API key errors
Run `setup_api_key` to authenticate via the browser, or manually set the key in `~/.rendermark/config.json`.

### PDF export fails
PDF/image export requires Chrome or a Browserless API key. All other tools work without it.

### Tool not found
Ensure you're running the latest version: `npx -y @rendermark/mcp-server@latest`

## Links

- Website: https://rendermark.app
- npm: https://www.npmjs.com/package/@rendermark/mcp-server
- GitHub: https://github.com/jmsaavedra/rendermark
