# Atlassian (Jira + Confluence) OAuth Provider

## Overview

Atlassian uses OAuth 2.0 (3LO) with authorization code flow and PKCE. Tokens are scoped to Atlassian cloud sites. After obtaining a token, you must call the accessible-resources endpoint to get the cloud ID for your Jira/Confluence site before making API calls.

## Key Gotchas

### Cloud ID Required
After obtaining a token, call `GET https://api.atlassian.com/oauth/token/accessible-resources` to get the cloud ID(s) for the user's Atlassian sites. API calls use the format:
- Jira: `https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/...`
- Confluence: `https://api.atlassian.com/wiki/rest/api/...` (via `https://api.atlassian.com/ex/confluence/{cloudId}/wiki/rest/api/...`)

### Audience Parameter
The OAuth authorization URL requires `audience=api.atlassian.com`. TapAuth handles this automatically.

### Refresh Tokens Require offline_access
To get refresh tokens, the `offline_access` scope must be included. TapAuth includes this by default.

### Token Expiry
Access tokens expire in 1 hour. Refresh tokens are long-lived but may be rotated — always persist the latest refresh token from the response.

### Scope Format
Atlassian scopes use `action:resource` format (e.g., `read:jira-work`, `write:confluence-content`). Scopes are space-separated.

## Scopes

### Jira API (5 scopes)
- `read:jira-work` — Read Jira issues, projects, boards, and sprints
- `write:jira-work` — Create and edit Jira issues, comments, and worklogs
- `read:jira-user` — Read Jira user profiles
- `manage:jira-project` — Manage Jira project settings
- `manage:jira-configuration` — Manage Jira settings and configuration

### Confluence API (15 scopes)
- `read:confluence-content.all` — Read all Confluence content
- `read:confluence-content.summary` — Read Confluence content summaries
- `write:confluence-content` — Create and edit Confluence content
- `read:confluence-space.summary` — Read Confluence space summaries
- `write:confluence-space` — Create and edit Confluence spaces
- `write:confluence-file` — Upload files to Confluence
- `read:confluence-props` — Read Confluence content properties
- `write:confluence-props` — Edit Confluence content properties
- `manage:confluence-project` — Manage Confluence projects
- `manage:confluence-configuration` — Manage Confluence settings
- `read:confluence-user` — Read Confluence user profiles
- `read:confluence-groups` — Read Confluence groups
- `write:confluence-groups` — Manage Confluence groups
- `search:confluence` — Search Confluence
- `readonly:content.attachment:confluence` — Read Confluence attachments

### User Identity API (2 scopes)
- `read:me` — Read your Atlassian profile
- `read:account` — Read your Atlassian account details

### Personal Data Reporting API (1 scope)
- `report:personal-data` — Report personal data usage

### Auth (1 scope)
- `offline_access` — Maintain access when offline (refresh tokens)

## Example Usage

```bash
# Step 1: Get accessible resources (cloud IDs)
curl -H "Authorization: Bearer {access_token}" \
  "https://api.atlassian.com/oauth/token/accessible-resources"
# Returns: [{"id": "cloud-id-here", "name": "My Site", ...}]

# Step 2: Search Jira issues
curl -H "Authorization: Bearer {access_token}" \
  "https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/search?jql=project=PROJ&maxResults=10"

# Create a Jira issue
curl -X POST \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"project": {"key": "PROJ"}, "summary": "Bug report", "issuetype": {"name": "Bug"}}}' \
  "https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/issue"

# Search Confluence content
curl -H "Authorization: Bearer {access_token}" \
  "https://api.atlassian.com/ex/confluence/{cloudId}/wiki/rest/api/content?title=My+Page&spaceKey=SPACE"

# Get user info
curl -H "Authorization: Bearer {access_token}" \
  "https://api.atlassian.com/me"
```

## API Reference
- Jira base URL: `https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/`
- Confluence base URL: `https://api.atlassian.com/ex/confluence/{cloudId}/wiki/rest/api/`
- User info: `https://api.atlassian.com/me`
- Accessible resources: `https://api.atlassian.com/oauth/token/accessible-resources`
- Jira docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- Confluence docs: https://developer.atlassian.com/cloud/confluence/rest/v2/
