# Jira Field Reference

## Standard Fields

| Field | API Name | Type | Notes |
|-------|----------|------|-------|
| Summary | `summary` | string | Required for create |
| Description | `description` | ADF | Rich text format |
| Issue Type | `issuetype` | `{name: "Task"}` | Task, Bug, Story, Epic, Sub-task |
| Priority | `priority` | `{name: "High"}` | Highest, High, Medium, Low, Lowest |
| Status | `status` | read-only | Use transitions to change |
| Assignee | `assignee` | `{accountId: "..."}` | Use account ID, not email |
| Reporter | `reporter` | `{accountId: "..."}` | Usually auto-set |
| Labels | `labels` | `["label1", "label2"]` | Array of strings |
| Components | `components` | `[{name: "Web"}]` | Array of objects |
| Fix Versions | `fixVersions` | `[{name: "1.0"}]` | Array of objects |
| Affects Versions | `versions` | `[{name: "0.9"}]` | Array of objects |
| Due Date | `duedate` | `"2024-03-15"` | YYYY-MM-DD format |
| Parent | `parent` | `{key: "PROJ-100"}` | For subtasks |
| Sprint | `customfield_*` | varies | Board-specific |

## Finding Account IDs

Assignees require account IDs, not emails. Find them via:

```bash
# Search users by email or name
curl -s -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/user/search?query=john@company.com" | jq .
```

## Custom Fields

Custom fields use `customfield_XXXXX` format. List all fields:

```bash
curl -s -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/field" | jq '.[] | {id, name, custom}'
```

Common custom field types:

| Type | Set Value |
|------|-----------|
| Text | `"value"` |
| Number | `123` |
| Select | `{value: "Option Name"}` |
| Multi-select | `[{value: "Opt1"}, {value: "Opt2"}]` |
| User picker | `{accountId: "..."}` |
| Date | `"2024-03-15"` |
| Datetime | `"2024-03-15T10:30:00.000+0000"` |

## Atlassian Document Format (ADF)

Description and comment fields use ADF for rich text:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Regular text "},
        {"type": "text", "text": "bold", "marks": [{"type": "strong"}]},
        {"type": "text", "text": " and "},
        {"type": "text", "text": "italic", "marks": [{"type": "em"}]}
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": "Item 1"}]}
          ]
        }
      ]
    },
    {
      "type": "codeBlock",
      "attrs": {"language": "python"},
      "content": [
        {"type": "text", "text": "print('hello')"}
      ]
    }
  ]
}
```

### ADF Node Types

- `paragraph` - Basic text block
- `heading` - `attrs: {level: 1-6}`
- `bulletList` / `orderedList` - Lists
- `listItem` - List items (wrap content in paragraph)
- `codeBlock` - Code with optional `language` attr
- `blockquote` - Quote blocks
- `rule` - Horizontal rule
- `table`, `tableRow`, `tableHeader`, `tableCell` - Tables

### Text Marks

- `strong` - Bold
- `em` - Italic
- `underline` - Underline
- `strike` - Strikethrough
- `code` - Inline code
- `link` - `attrs: {href: "url"}`

## Issue Links

Link issues together:

```bash
# Create link
curl -X POST -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": {"name": "Blocks"},
    "inwardIssue": {"key": "PROJ-123"},
    "outwardIssue": {"key": "PROJ-456"}
  }' \
  "$JIRA_BASE_URL/rest/api/3/issueLink"
```

Link types: Blocks, Clones, Duplicate, Relates

## Attachments

```bash
# Add attachment
curl -X POST -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/file.png" \
  "$JIRA_BASE_URL/rest/api/3/issue/PROJ-123/attachments"
```
