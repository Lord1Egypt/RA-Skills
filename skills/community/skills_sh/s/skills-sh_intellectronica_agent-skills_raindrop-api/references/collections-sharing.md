# Collection Sharing and Collaborators

Raindrop.io allows sharing collections with other users for collaboration. This reference covers the sharing API endpoints.

Docs: https://developer.raindrop.io/v1/collections/sharing

## Collaborator Object

Each collaborator record contains:

| Field | Type | Description |
|-------|------|-------------|
| `_id` | number | User ID |
| `email` | string | Email address (empty for read-only users) |
| `email_MD5` | string | MD5 hash of email (for Gravatar) |
| `fullName` | string | Full name |
| `role` | string | `member` (write + invite) or `viewer` (read-only) |

## Endpoints

### Share Collection (Invite)

Send invitations to collaborate on a collection.

```bash
curl -s -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "member",
    "emails": ["user1@example.com", "user2@example.com"]
  }' \
  "https://api.raindrop.io/rest/v1/collection/{id}/sharing" | jq '.'
```

**Fields:**
- `role` (string, required) - `member` or `viewer`
- `emails` (array, required) - Up to 10 email addresses

### Get Collaborators

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/collection/{id}/sharing" | jq '.'
```

Returns array of collaborator objects.

### Unshare / Leave Collection

- **Owner**: Removes all collaborators
- **Member/Viewer**: Removes self from the collection

```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/collection/{id}/sharing" | jq '.'
```

### Change Collaborator Role

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "viewer"}' \
  "https://api.raindrop.io/rest/v1/collection/{id}/sharing/{userId}" | jq '.'
```

### Remove Specific Collaborator

```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/collection/{id}/sharing/{userId}" | jq '.'
```

### Accept Invitation

```bash
curl -s -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"token": "INVITATION_TOKEN"}' \
  "https://api.raindrop.io/rest/v1/collection/{id}/join" | jq '.'
```

The `token` is provided in the email invitation.

## Error Cases

- Empty emails array
- More than 10 recipients
- Too many pending invitations
- Insufficient permissions (not an owner)
- Invalid/expired invitation token
- Collection no longer exists
- User already owns the collection
