# Yunxiao Skill

OpenClaw skill for [Yunxiao (阿里云云效)](https://devops.aliyun.com) integration.

This public README intentionally uses placeholder IDs and synthetic examples only.
Keep organization-specific mappings, internal project IDs, and private conventions in a local `AGENTS.md` or equivalent private workspace note.

## Features

- Get work item details
- Search work items
- Search projects
- List comments
- Create comments
- Search organization members
- List organizations

## Prerequisites

1. A Yunxiao Personal Access Token
2. Node.js 18+

## Installation

### As an OpenClaw Skill

```bash
cp -r yunxiao ~/.openclaw/skills/
```

### Standalone Usage

```bash
export YUNXIAO_ACCESS_TOKEN="your-token"
export YUNXIAO_ORG_ID="your-org-id" # optional

node scripts/yunxiao-mcp.cjs get_work_item PROJ-12345
```

## Organization Resolution

The CLI resolves organization ID in this order:

1. Explicit `[orgId]` command argument
2. `YUNXIAO_ORG_ID` environment variable
3. First organization returned by `get_organizations`

## Commands

```bash
node scripts/yunxiao-mcp.cjs get_organizations
node scripts/yunxiao-mcp.cjs get_current_user [orgId]
node scripts/yunxiao-mcp.cjs search_projects [keyword] [orgId]
node scripts/yunxiao-mcp.cjs get_work_item <workItemId> [orgId]
node scripts/yunxiao-mcp.cjs search_workitems <spaceId> [optionsJson] [orgId]
node scripts/yunxiao-mcp.cjs get_comments <workItemId> [orgId] [page] [perPage]
node scripts/yunxiao-mcp.cjs create_comment <workItemId> "Comment content" [orgId]
node scripts/yunxiao-mcp.cjs search_members <keyword> [orgId]
```

## Example Output

### Get Work Item

```bash
$ node scripts/yunxiao-mcp.cjs get_work_item PROJ-12345
```

```json
{
  "id": "work-item-id",
  "serialNumber": "PROJ-12345",
  "subject": "Example requirement title",
  "status": { "name": "处理中", "nameEn": "In Progress" },
  "assignedTo": { "name": "Owner A", "id": "user-id-1" },
  "creator": { "name": "Creator A", "id": "user-id-2" },
  "customFieldValues": [
    { "fieldName": "Priority", "values": [{ "displayValue": "High" }] }
  ]
}
```

### Get Comments

```bash
$ node scripts/yunxiao-mcp.cjs get_comments PROJ-12345
```

```json
[
  {
    "id": "comment-id",
    "content": "Example comment content",
    "user": { "name": "Reviewer A", "id": "user-id-3" },
    "gmtCreate": 1767843788000
  }
]
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `YUNXIAO_ACCESS_TOKEN` | Yes | Yunxiao Personal Access Token |
| `YUNXIAO_ORG_ID` | No | Default organization ID |

## Testing

```bash
npm test
```

## API Reference

This skill uses the [alibabacloud-devops-mcp-server](https://www.npmjs.com/package/alibabacloud-devops-mcp-server), which wraps the [Yunxiao OpenAPI](https://help.aliyun.com/document_detail/261300.html).

## License

MIT
