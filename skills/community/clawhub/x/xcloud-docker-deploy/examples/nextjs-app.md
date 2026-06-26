# Example: Next.js App → xCloud via Docker

## Project structure detected
- package.json ✓
- next.config.js ✓

Detected: Next.js | Recommended: Docker (requires build step)

## Step 1 — Add standalone output to next.config.js
```js
const nextConfig = { output: 'standalone' }
module.exports = nextConfig
```

## Step 2 — Add Dockerfile
Copy `dockerfiles/nextjs.Dockerfile` → rename to `Dockerfile` in repo root.

## Step 3 — Add docker-compose.yml
Copy `compose-templates/nextjs-postgres.yml` → rename to `docker-compose.yml`. Replace OWNER/REPO.

## Step 4 — Add GitHub Actions
Copy `assets/github-actions-build.yml` → `.github/workflows/docker-build.yml`

## Step 5 — Add .env.example
```env
POSTGRES_DB=myapp
POSTGRES_USER=myuser
POSTGRES_PASSWORD=
NEXTAUTH_URL=https://yourdomain.com
NEXTAUTH_SECRET=
```

## Step 6 — Push and wait for GHCR build (~3-5 min)
```bash
git add . && git commit -m "Add xCloud deployment" && git push origin main
```

## Step 7 — Deploy in xCloud
1. Server → New Site → Custom Docker
2. Connect repo, exposed port: 3000
3. Add env vars, Deploy
