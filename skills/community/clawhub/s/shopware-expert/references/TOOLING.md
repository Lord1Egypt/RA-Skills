# Tooling: HTTP, shell, browser, workspace

## Default stack (no companion plugin)

Until a dedicated OpenClaw Shopware plugin exists, prefer:

1. **`curl`** (or equivalent) for **Admin API** and **Store API** calls with OAuth tokens from env.
2. **`exec`** on the gateway for **Composer**, **bin/console**, **PHPUnit**, etc., when the user policy allows it and the Shopware project is on the same host.
3. **Browser** tools for **Admin UI** verification or merchant flows (with explicit user consent).
4. **Workspace file tools** for editing a **cloned** extension or theme repository.

## API calls (pattern)

- Obtain a **Bearer** token via your instance OAuth flow (see [AUTH.md](AUTH.md)).
- Send `GET` / `POST` / `PATCH` / `DELETE` with `Authorization: Bearer ...` and `Content-Type: application/json` as required.
- Always use **Search Criteria** and documented entity routes. **Do not invent** routes.

Example skeleton (placeholders only):

```bash
curl -sS -H "Authorization: Bearer $SHOPWARE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "$SHOPWARE_BASE_URL/api/..."
```

Replace `...` with the documented path for your Shopware version.

## Symfony / Shopware CLI

When the project is checked out on the gateway:

- `bin/console` for cache clear, migrations (read-only unless the user asked), fixture loading, etc.
- **Never** run destructive console commands without explicit approval.

## Where to read more in this skill

- `ADMIN_API.md`, `STORE_API.md`, `INTEGRATIONS_AND_SYNC.md`: bundled developer text and links
- [SAFETY.md](SAFETY.md): destructive operations
