# Kaleidoscope Infrastructure: Postgres + Prisma + Recoverable Server

**Date:** 2026-04-06
**Authors:** Parker Todd Brooks, cc-mini
**Status:** plan approved, building next
**Repo:** wip-ldm-os-private (src/hosted-mcp/)

## Why

We're taking real customers now. Passkeys are permanent. The JSON files on the VPS (`passkeys.json`, `tokens.json`, `wallets.json`) are production data with no backup, no encryption, no concurrent write safety. The nginx configs and PM2 config exist only on the VPS. If the server dies, we lose everything and can't recreate it.

## What we're building

1. **Postgres on the VPS** ... real database for production data
2. **Prisma in the app** ... type-safe ORM, schema migrations, works with Next.js
3. **All configs in the repo** ... nginx, PM2, so the server is recreatable
4. **`wip.computer/login`** ... real login page (not /demo/)
5. **`ldm pair` end-to-end test** ... pairing with the real database

## Database schema (Prisma)

```prisma
model User {
  id          String       @id @default(uuid())
  name        String
  createdAt   DateTime     @default(now())
  credentials Credential[]
  devices     Device[]
  wallets     Wallet[]
}

model Credential {
  id          String   @id // WebAuthn credential ID
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  publicKey   Bytes
  counter     Int      @default(0)
  transports  String[]
  createdAt   DateTime @default(now())
}

model Device {
  id          String   @id @default(uuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  token       String   @unique // dk-... device token
  deviceName  String
  agentId     String
  pairedAt    DateTime @default(now())
}

model Wallet {
  id          String   @id @default(uuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  balance     Int      @default(0) // cents
  currency    String   @default("USD")
  createdAt   DateTime @default(now())
}

model ApiKey {
  id          String   @id @default(uuid())
  key         String   @unique // ck-...
  agentId     String
  createdAt   DateTime @default(now())
}
```

Five tables. Clean. Ready for email, phone, sessions when we add them later.

## Implementation steps

### Step 1: Install Postgres on VPS

```bash
ssh wip-vps
sudo apt update && sudo apt install postgresql postgresql-client
sudo -u postgres createuser kaleidoscope
sudo -u postgres createdb kaleidoscope -O kaleidoscope
sudo -u postgres psql -c "ALTER USER kaleidoscope PASSWORD 'generated-password';"
```

Store the password in 1Password under "Postgres VPS" in Agent Secrets.

### Step 2: Add Prisma to hosted-mcp

```bash
cd src/hosted-mcp
npm install prisma @prisma/client
npx prisma init --datasource-provider postgresql
```

Creates `prisma/schema.prisma`. Paste the schema above. Set `DATABASE_URL` in `.env` (gitignored) and in the PM2 ecosystem config.

### Step 3: Run migration

```bash
npx prisma migrate dev --name init
```

Creates the tables on the VPS Postgres.

### Step 4: Migrate server.mjs from JSON to Prisma

Replace all `readFileSync(PASSKEY_FILE)` / `writeFileSync(PASSKEY_FILE)` calls with Prisma queries:

| Current (JSON) | New (Prisma) |
|---|---|
| `loadPasskeys()` | `prisma.credential.findMany()` |
| `savePasskeys()` | `prisma.credential.create()` |
| `loadPairedDevices()` | `prisma.device.findMany()` |
| `savePairedDevices()` | `prisma.device.create()` |
| `API_KEYS` object | `prisma.apiKey.findUnique({ where: { key } })` |
| `wallets.json` | `prisma.wallet.findFirst({ where: { userId } })` |

### Step 5: Seed existing data

Write a one-time migration script that reads the current JSON files and inserts into Postgres:

```bash
node src/hosted-mcp/migrate-json-to-postgres.mjs
```

Reads `passkeys.json`, `tokens.json`, `wallets.json`, `paired-devices.json`. Inserts into the Prisma-managed tables. Run once. Delete the script after.

Since we just wiped the passkeys, this step is mostly about `tokens.json` (the API keys).

### Step 6: Copy nginx configs into repo

```
src/hosted-mcp/nginx/
  wip.computer.conf         main site config
  mcp-server.conf           MCP proxy
  mcp-oauth.conf            OAuth + WebAuthn + pairing proxy
```

These are reference copies. The VPS reads from `/etc/nginx/`. Deploy updates via `scp` + `nginx -t && systemctl reload nginx`.

### Step 7: Copy PM2 config into repo

```
src/hosted-mcp/ecosystem.config.cjs
```

Reference copy. Deploy via `scp` + `pm2 restart`.

### Step 8: Build wip.computer/login

Real login page at the root path. Same design as the demo signup/signin. Passkey registration + authentication. Not under `/demo/`. This is production.

Served by the Node server (same as `/signup` and `/login` currently). Static HTML with inline JS, same pattern as the demo. Or served by nginx as a static file if we want to keep the server pure API.

### Step 9: Test ldm pair end-to-end

1. Register on `wip.computer/login` with passkey
2. Run `ldm pair` on Mac Mini
3. Go to `wip.computer/pair` (or use curl against `/api/pair/approve`)
4. Verify token stored at `~/.ldm/auth/kaleidoscope.json`
5. Verify device appears in Postgres

## File changes

| File | Change |
|---|---|
| `src/hosted-mcp/package.json` | Add prisma, @prisma/client |
| `src/hosted-mcp/prisma/schema.prisma` | CREATE (schema above) |
| `src/hosted-mcp/server.mjs` | Replace JSON file ops with Prisma queries |
| `src/hosted-mcp/migrate-json-to-postgres.mjs` | CREATE (one-time migration) |
| `src/hosted-mcp/nginx/` | CREATE (copy from VPS) |
| `src/hosted-mcp/ecosystem.config.cjs` | CREATE (copy from VPS) |
| `src/hosted-mcp/.env.example` | CREATE (DATABASE_URL template) |
| `.gitignore` | Add .env, *.json data files |

## Future: Docker

After this works bare-metal, wrap it in Docker:
- `Dockerfile` for the Node app
- `docker-compose.yml` for app + Postgres + nginx
- One `docker-compose up` recreates the entire stack

Not in scope for this step. Docker comes after bare-metal Postgres works.

## Security considerations

- Postgres password stored in 1Password, not in repo
- `.env` with DATABASE_URL is gitignored
- PM2 reads DATABASE_URL from ecosystem.config.cjs env block (or .env)
- Passkey data is public keys only (private keys never leave user devices)
- When we add email/phone later: encrypt PII columns at the application layer
- VPS disk encryption via provider (Linode supports this)

## Cross-references

- `ai/product/plans-prds/kaleidoscope/2026-04-06--cc-mini--kaleidoscope-architecture.md`
- `ai/product/plans-prds/bridge/2026-04-06--cc-mini--bridge-master-product-plan.md` Phase A
- `src/hosted-mcp/server.mjs` (the server being migrated)
