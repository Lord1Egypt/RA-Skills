---
name: snowsand-confluence
version: 1.0.0
description: Interact with Confluence Cloud via REST API. Use for space management, page operations (list, view, create, update, delete), content search (CQL queries), page tree navigation (parent/child), attachments, comments, and labels. Triggers on Confluence operations, wiki pages, documentation tasks, or any Atlassian Confluence Cloud task.
---

# Confluence Cloud Integration

Confluence Cloud REST API v2 integration for wiki/documentation management, including spaces, pages, attachments, comments, and labels.

## Authentication

Confluence Cloud uses API token authentication. Required environment variables:

- `CONFLUENCE_BASE_URL` - Your Confluence instance (e.g., `https://yourcompany.atlassian.net`)
- `CONFLUENCE_USER_EMAIL` - Atlassian account email
- `CONFLUENCE_API_TOKEN` - API token from https://id.atlassian.com/manage-profile/security/api-tokens

Test connection:
```bash
curl -s -u "$CONFLUENCE_USER_EMAIL:$CONFLUENCE_API_TOKEN" "$CONFLUENCE_BASE_URL/wiki/api/v2/spaces?limit=1" | jq .
```

## Quick Reference

All operations use the `scripts/confluence.py` script:

| Operation | Command |
|-----------|---------|
| **Spaces** | |
| List spaces | `confluence.py spaces` |
| Get space by ID | `confluence.py space SPACE_ID` |
| Get space by key | `confluence.py space-by-key PROJ` |
| Create space | `confluence.py create-space --name "My Space" --key MYSP` |
| **Pages** | |
| List pages | `confluence.py pages --space-id SPACE_ID` |
| Get page | `confluence.py page PAGE_ID` |
| Create page | `confluence.py create-page --space-id ID --title "Title" --body "<p>Content</p>"` |
| Update page | `confluence.py update-page PAGE_ID --body "<p>New content</p>"` |
| Delete page | `confluence.py delete-page PAGE_ID` |
| **Page Tree** | |
| Get children | `confluence.py children PAGE_ID` |
| Get ancestors | `confluence.py ancestors PAGE_ID` |
| **Search** | |
| CQL search | `confluence.py search "type=page AND space=PROJ"` |
| **Attachments** | |
| List attachments | `confluence.py attachments PAGE_ID` |
| Get attachment | `confluence.py attachment ATT_ID` |
| Upload file | `confluence.py upload PAGE_ID /path/to/file.pdf` |
| Download | `confluence.py download ATT_ID -o output.pdf` |
| Delete attachment | `confluence.py delete-attachment ATT_ID` |
| **Comments** | |
| List comments | `confluence.py comments PAGE_ID` |
| Get comment | `confluence.py comment COMMENT_ID` |
| Create comment | `confluence.py create-comment PAGE_ID "Comment text"` |
| Update comment | `confluence.py update-comment COMMENT_ID "New text"` |
| Delete comment | `confluence.py delete-comment COMMENT_ID` |
| **Labels** | |
| Get labels | `confluence.py labels PAGE_ID` |
| Add labels | `confluence.py add-labels PAGE_ID "label1,label2"` |
| Remove label | `confluence.py remove-label PAGE_ID labelname` |
| **User** | |
| Current user | `confluence.py me` |

## Common Workflows

### Space Management

```bash
# List all spaces
confluence.py spaces

# List global spaces only
confluence.py spaces --type global

# Get space by key
confluence.py space-by-key PROJ

# Create a new space
confluence.py create-space --name "Project Documentation" --key DOCS --description "Team docs"

# Create a private space
confluence.py create-space --name "Private Notes" --key PRIV --private
```

### Page Operations

```bash
# List pages in a space (need space ID, not key)
# First get the space ID:
confluence.py space-by-key PROJ
# Then list pages:
confluence.py pages --space-id 12345678

# Filter pages by title
confluence.py pages --title "Meeting Notes"

# Get page with body content
confluence.py page 98765432 --body-format storage

# Get page with labels
confluence.py page 98765432 --include-labels

# Get specific version
confluence.py page 98765432 --version 5
```

### Creating Pages

Pages use Confluence Storage Format (XHTML-based):

```bash
# Simple page
confluence.py create-page --space-id 12345678 --title "New Page" \
  --body "<p>Hello World</p>"

# Page with formatting
confluence.py create-page --space-id 12345678 --title "Formatted Page" \
  --body "<h1>Heading</h1><p>Paragraph with <strong>bold</strong> text.</p><ul><li>Item 1</li><li>Item 2</li></ul>"

# Child page (under a parent)
confluence.py create-page --space-id 12345678 --title "Child Page" \
  --parent-id 98765432 --body "<p>This is a child page</p>"

# Draft page
confluence.py create-page --space-id 12345678 --title "Draft" \
  --status draft --body "<p>Work in progress</p>"
```

### Updating Pages

```bash
# Update page content
confluence.py update-page 98765432 --body "<p>Updated content</p>"

# Update with new title
confluence.py update-page 98765432 --title "New Title" --body "<p>Content</p>"

# Update with version message
confluence.py update-page 98765432 --body "<p>Fixed typo</p>" \
  --message "Corrected spelling errors"
```

### Deleting Pages

```bash
# Move to trash (recoverable)
confluence.py delete-page 98765432

# Permanently delete (purge)
confluence.py delete-page 98765432 --purge
```

### Page Tree Navigation

```bash
# Get child pages
confluence.py children 98765432

# Get parent chain (ancestors)
confluence.py ancestors 98765432
```

### Content Search (CQL)

Confluence Query Language (CQL) supports powerful filtering:

```bash
# Search by type
confluence.py search "type=page"

# Search in specific space
confluence.py search "type=page AND space=PROJ"

# Full-text search
confluence.py search "text ~ 'meeting notes'"

# Recently modified
confluence.py search "type=page AND lastModified > now('-7d')"

# By label
confluence.py search "type=page AND label=important"

# By creator
confluence.py search "type=page AND creator=currentUser()"

# Combined query
confluence.py search "type=page AND space=PROJ AND text ~ 'api' AND lastModified > now('-30d')"
```

### Attachments

```bash
# List attachments on a page
confluence.py attachments 98765432

# Filter by filename
confluence.py attachments 98765432 --filename "report.pdf"

# Filter by media type
confluence.py attachments 98765432 --media-type "image/png"

# Upload a file
confluence.py upload 98765432 /path/to/document.pdf

# Upload with comment
confluence.py upload 98765432 /path/to/file.pdf --comment "Q3 report"

# Download attachment
confluence.py download att123456 -o downloaded_file.pdf

# Delete attachment (move to trash)
confluence.py delete-attachment att123456

# Permanently delete
confluence.py delete-attachment att123456 --purge
```

### Comments

```bash
# List comments on a page
confluence.py comments 98765432

# Get comment with body
confluence.py comment comm123456 --body-format storage

# Add a comment
confluence.py create-comment 98765432 "<p>Great work!</p>"

# Update a comment
confluence.py update-comment comm123456 "<p>Updated comment</p>"

# Delete a comment
confluence.py delete-comment comm123456
```

### Labels

```bash
# Get labels for a page
confluence.py labels 98765432

# Add labels
confluence.py add-labels 98765432 "documentation,api,important"

# Remove a label
confluence.py remove-label 98765432 "draft"
```

## Storage Format Reference

Confluence uses Storage Format (XHTML-based) for page content. See `references/storage-format.md` for details.

### Common Elements

```html
<!-- Headings -->
<h1>Heading 1</h1>
<h2>Heading 2</h2>

<!-- Paragraphs -->
<p>Regular paragraph</p>
<p><strong>Bold</strong> and <em>italic</em> text</p>

<!-- Lists -->
<ul>
  <li>Unordered item</li>
</ul>
<ol>
  <li>Ordered item</li>
</ol>

<!-- Links -->
<a href="https://example.com">External link</a>
<ac:link><ri:page ri:content-title="Other Page" /></ac:link>

<!-- Code block -->
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">python</ac:parameter>
  <ac:plain-text-body><![CDATA[print("Hello")]]></ac:plain-text-body>
</ac:structured-macro>

<!-- Info panel -->
<ac:structured-macro ac:name="info">
  <ac:rich-text-body><p>Info message</p></ac:rich-text-body>
</ac:structured-macro>

<!-- Table -->
<table>
  <tr><th>Header</th></tr>
  <tr><td>Cell</td></tr>
</table>
```

## CQL Reference

See `references/cql.md` for the full CQL reference.

### Common CQL Patterns

| Query | Description |
|-------|-------------|
| `type=page` | All pages |
| `type=blogpost` | All blog posts |
| `space=KEY` | Content in space |
| `text ~ "keyword"` | Full-text search |
| `title ~ "keyword"` | Title search |
| `label=labelname` | Has label |
| `creator=currentUser()` | Created by me |
| `lastModified > now('-7d')` | Modified last week |

## Error Handling

Common errors:
- **401 Unauthorized**: Check CONFLUENCE_USER_EMAIL and CONFLUENCE_API_TOKEN
- **403 Forbidden**: User lacks permission for this operation
- **404 Not Found**: Space, page, or content doesn't exist
- **400 Bad Request**: Invalid parameters or malformed storage format

## Raw API Access

For operations not covered by the script:

```bash
# V2 API (preferred)
curl -s -u "$CONFLUENCE_USER_EMAIL:$CONFLUENCE_API_TOKEN" \
  "$CONFLUENCE_BASE_URL/wiki/api/v2/pages?limit=5" | jq .

# V1 API (legacy, some features)
curl -s -u "$CONFLUENCE_USER_EMAIL:$CONFLUENCE_API_TOKEN" \
  "$CONFLUENCE_BASE_URL/wiki/rest/api/content?type=page&limit=5" | jq .

# POST with body
curl -s -X POST -u "$CONFLUENCE_USER_EMAIL:$CONFLUENCE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"spaceId":"12345","title":"Test","body":{"representation":"storage","value":"<p>Hello</p>"}}' \
  "$CONFLUENCE_BASE_URL/wiki/api/v2/pages" | jq .
```

API docs: 
- V2: https://developer.atlassian.com/cloud/confluence/rest/v2/intro/
- V1: https://developer.atlassian.com/cloud/confluence/rest/v1/intro/
