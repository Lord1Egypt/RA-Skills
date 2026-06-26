---
name: workos
description: Manage enterprise SSO, Directory Sync (SCIM), Admin Portal, and user management via WorkOS API. Use when asked to set up SSO for an organization, provision users via SCIM, list directory users or groups, generate an Admin Portal link, or check SSO connection status. Requires WORKOS_API_KEY env var.
---

# WorkOS Skill

WorkOS REST API base: `https://api.workos.com`

## Auth
```bash
curl -H "Authorization: Bearer $WORKOS_API_KEY" https://api.workos.com/...
```

## Organizations

### List Organizations
```bash
curl "https://api.workos.com/organizations?limit=10" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

### Create Organization
```bash
curl -X POST "https://api.workos.com/organizations" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corp", "domains": [{"domain": "acme.com"}]}'
```

## SSO

### List SSO Connections
```bash
curl "https://api.workos.com/connections?organization_id=<org_id>" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

### Get SSO Authorization URL
```bash
curl -X POST "https://api.workos.com/sso/authorize" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "<WORKOS_CLIENT_ID>",
    "redirect_uri": "https://yourapp.com/auth/callback",
    "connection": "<connection_id>",
    "state": "<random_state>"
  }'
```

### Get Profile After SSO Callback
```bash
curl -X POST "https://api.workos.com/sso/token" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "<auth_code>", "client_id": "<WORKOS_CLIENT_ID>"}'
```

## Directory Sync (SCIM)

### List Directories
```bash
curl "https://api.workos.com/directories?organization_id=<org_id>" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

### List Directory Users
```bash
curl "https://api.workos.com/directory_users?directory=<dir_id>&limit=25" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

### List Directory Groups
```bash
curl "https://api.workos.com/directory_groups?directory=<dir_id>" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

### Get Directory User
```bash
curl "https://api.workos.com/directory_users/<user_id>" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

## Admin Portal

### Generate Admin Portal Link
```bash
curl -X POST "https://api.workos.com/portal/generate_link" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"intent": "sso", "organization": "<org_id>", "return_url": "https://yourapp.com/settings"}'
# Returns: { link: "https://..." } — share with customer's IT admin
```
`intent` options: `sso`, `dsync`, `log_streams`, `audit_logs`

## User Management (WorkOS AuthKit)

### List Users
```bash
curl "https://api.workos.com/user_management/users?limit=25" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

### Get User
```bash
curl "https://api.workos.com/user_management/users/<user_id>" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

### Delete User
```bash
curl -X DELETE "https://api.workos.com/user_management/users/<user_id>" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

## Connection Types
`OktaSAML`, `AzureSAML`, `GoogleSAML`, `OneLoginSAML`, `GenericSAML`, `ADFSSAML`, `PingFederateSAML`, `OktaOIDC`, `MicrosoftOIDC`, `GoogleOIDC`
