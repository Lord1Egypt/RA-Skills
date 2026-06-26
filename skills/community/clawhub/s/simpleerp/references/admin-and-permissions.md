## Admin and permissions

Admin endpoints manage users, API keys, and permissions.

All admin routes live under `/api/admin/...` and require appropriate admin-level permissions. In production, admin routes require the `admin_access` permission on the API key or user.

Base URL: `http://localhost:3000/api`.

---

### Users (`/api/admin/users`)

#### List system users

```bash
curl "http://localhost:3000/api/admin/users?status=&limit=100&offset=0"
```

---

### API keys (`/api/admin/api-keys`)

#### Create an API key

```bash
curl "http://localhost:3000/api/admin/api-keys" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "keyName": "My key",
    "expiresDt": null
  }'
# Response includes rawKey once; store it securely.
```

#### Rotate an API key

```bash
curl "http://localhost:3000/api/admin/api-keys/1/rotate"
```

---

### Permissions

The following non-admin endpoints manage permission definitions and assignments:

- `/api/permissions` — define permission IDs and functions.
- `/api/user-permissions` — assign permissions to users.
- `/api/api-key-permissions` — assign permissions to API keys.

#### List filters (allowlisted query params)

| Path | Filters (plus `limit`, `offset`) |
|------|----------------------------------|
| `GET /api/permissions` | `functionId` |
| `GET /api/user-permissions` | `userId`, `permissionId` |
| `GET /api/api-key-permissions` | `apiKeyId`, `permissionId` |

#### Example: list permissions for a function

```bash
curl "http://localhost:3000/api/permissions?functionId=<FUNCTION_ID>&limit=100&offset=0"
```

#### Example: list API key permission rows for one key

```bash
curl "http://localhost:3000/api/api-key-permissions?apiKeyId=1&limit=100&offset=0"
```

#### Example: assign a permission to a user

```bash
curl "http://localhost:3000/api/user-permissions" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "permissionId": "view_customer_listing"
  }'
```

