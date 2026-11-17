---
name: spraay-shopify-selfhost
description: Deploy and self-host the open-source Spraay Shopify app (batch USDC payouts on Base) for a merchant's store. Use this skill whenever a user wants to install, deploy, set up, self-host, or troubleshoot the Spraay Shopify app (github.com/plagtech/spraay-shopify) - including creating the custom app in the Shopify Dev Dashboard, deploying to Railway, configuring environment variables, setting up the Supabase/Postgres database, fixing 502 errors or OAuth redirect issues, or connecting a custom domain. Also use when a Shopify merchant asks how to add crypto payouts, USDC payments, or affiliate crypto payments to their store admin.
---

# Self-Host the Spraay Shopify App

Walk a merchant from zero to a working batch-USDC-payouts page inside their Shopify admin in ~15 minutes. The app is open source (MIT), non-custodial, and requests **zero Shopify scopes** — it cannot read or write any store data.

**Repo:** https://github.com/plagtech/spraay-shopify

## Audited version

| Field | Value |
|---|---|
| Commit | `3acf3b674a14500728c2607d8be937ad600887ad` |
| Audit date | 2026-10-30 |
| Batch contract | `0x1646452F98E36A3c9Cfc3eDD8868221E207B5eEC` (Base, verified) |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (Base) |

> **Supply-chain note:** this skill deploys third-party code that receives Shopify secrets, database credentials, and wallet-signing authority. Always deploy from the **pinned commit above** (or a newer tagged release you have personally reviewed). Do not deploy from an unpinned `main` branch — the code could change after this audit.

## Stack at a glance

- Remix + `@shopify/shopify-app-remix`, Vite, Polaris UI (fully embedded in admin)
- wagmi v3 + viem v2 — MetaMask and Coinbase Smart Wallet
- Base (chain 8453), USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Batch contract `0x1646452F98E36A3c9Cfc3eDD8868221E207B5eEC` (verified; never substitute another address)
- Supabase PostgreSQL via Prisma, isolated in a `shopify` schema
- Railway hosting (Dockerfile, node:20-alpine)

## Prerequisites checklist

Confirm the user has (or help them create) each of these before starting:

1. A Shopify store (dev store is fine for testing)
2. A free Shopify Partners account → https://dev.shopify.com
3. A Railway account (hobby tier is enough)
4. A Supabase project (free tier is enough)
5. A wallet holding USDC on Base (MetaMask or Coinbase Smart Wallet)

## Step 1 — Fork at the audited commit and deploy to Railway

1. Fork `plagtech/spraay-shopify` (Node 20+ required if running outside Docker: `>=20.19 <22 || >=22.12`).
2. **Pin to the audited commit** — in the fork, reset the default branch to the audited SHA before deploying:
   ```bash
   git clone https://github.com/<your-fork>/spraay-shopify.git
   cd spraay-shopify
   git reset --hard 3acf3b674a14500728c2607d8be937ad600887ad
   git push --force-with-lease
   ```
   If the user prefers not to pin and instead deploys from the latest `main`, advise them to review the diff between the audited commit and HEAD (`git diff 3acf3b6..HEAD`) before deploying, since the code will have access to their Shopify secret and database credentials.
3. Deploy: Railway → New Project → Deploy from GitHub repo → select the fork. The repo ships a `railway.json` and Dockerfile, so the build is automatic. Alternatively, the **Deploy on Railway** button in the README works — the template pre-prompts for every required env var, with PORT defaulted to 3000.
4. Generate a public domain for the service (Settings → Networking). Note the URL, e.g. `your-app.up.railway.app`.

The app will crash-loop until env vars are set — that's expected. Continue.

## Step 2 — Create the custom app in Shopify

1. Go to https://dev.shopify.com → Apps → **Create app** → **Custom distribution** (single merchant). Custom distribution is Shopify's intended path for merchant-specific tooling — no App Store review involved.
2. Set **App URL** to the Railway URL from Step 1 (https, no trailing slash).
3. Add all three OAuth redirect URLs (each prefixed by the App URL):
   - `https://your-domain/auth/callback`
   - `https://your-domain/auth/shopify/callback`
   - `https://your-domain/api/auth/callback`
4. Copy the **Client ID** and **Client Secret**.

## Step 3 — Environment variables

Set these in Railway → service → Variables. The repo's `.env.example` documents each one; the authoritative reference:

| Variable | Value | Notes |
|---|---|---|
| `SHOPIFY_API_KEY` | App Client ID | Public — ships in the browser bundle; safe to share |
| `SHOPIFY_API_SECRET` | App Client Secret | Secret — signs webhook HMACs and OAuth. Never commit or paste into chat logs |
| `SHOPIFY_APP_URL` | `https://your-app.up.railway.app` | Must exactly match the App URL in Shopify settings; no trailing slash |
| `SCOPES` | *(empty)* | Intentional. The app never touches store data. Leave blank unless the fork adds Shopify API usage — then keep it in sync with `shopify.app.toml` |
| `DATABASE_URL` | `postgresql://user:pass@host:6543/postgres?schema=shopify&pgbouncer=true` | Supabase **pooled** connection (transaction pooler, port 6543) — used at runtime |
| `DIRECT_URL` | `postgresql://user:pass@host:5432/postgres?schema=shopify` | Supabase **direct** connection (port 5432) — used by `prisma migrate` |
| `NODE_ENV` | `production` | |
| `PORT` | `3000` | **Load-bearing.** See gotcha below |
| `SHOP_CUSTOM_DOMAIN` | *(optional)* | Only if the dev store uses a custom domain |

**The PORT=3000 gotcha (most common failure):** the Dockerfile's `EXPOSE 3000` sets Railway's domain target port to 3000. If `PORT` is unset, Railway injects `PORT=8080`, the app binds :8080, the proxy still routes to :3000, and **every route returns 502**. If the user reports 502s on all routes, check this first.

**Database notes:** keep `?schema=shopify` on **both** URLs so the app's tables stay isolated from anything else in the Supabase project. Both URLs point at the same database — only the port and pooling differ.

**Credential hygiene:** start with a dedicated Supabase database role limited to the `shopify` schema rather than the project-level `postgres` superuser. Rotate the Shopify client secret and database credentials immediately if you ever deploy an unreviewed revision of the app.

After saving variables, redeploy. Migrations run automatically on boot (`prisma generate && prisma migrate deploy`, then `remix-serve`). A clean boot — migrate succeeds and `remix-serve` prints its listen URL — means Steps 1–3 are done.

**Diagnostic tip:** a 502 while Railway shows the deployment "Online" is a port/proxy mismatch, not a crash. If the logs show a successful migrate and a listening server, fix `PORT`, don't debug the app.

## Step 4 — Install and test

1. From the Dev Dashboard, install the app on the store. Complete the OAuth prompt.
2. Open the app from the Shopify admin sidebar — the Polaris UI should render embedded.
3. **Start small:** run a test payout with 1–2 recipients and negligible amounts before processing real payroll. Header row is optional (first two columns are assumed address, amount); optional extra columns `name`, `email`, `memo` are supported, and the payout screen has a **Download CSV template** link and **Load sample data** button. Example:

   ```csv
   wallet_address,amount
   0xYourOtherWallet...,1.00
   ```

4. Review screen shows recipients, total, and the 0.3% protocol fee → connect wallet → approve USDC → execute → confirm the BaseScan link resolves.

## Optional — local development

For hacking on the app itself (not needed for a production deploy): `npm install && npm run dev`. The Shopify CLI creates a tunnel and injects `SHOPIFY_API_KEY`, `SHOPIFY_API_SECRET`, and `SHOPIFY_APP_URL`, so local `.env` only needs `DATABASE_URL` and `DIRECT_URL`.

## Optional — custom domain

Point a subdomain (e.g. `payouts.yourstore.com`) at the Railway service via CNAME, wait for the SSL cert to issue, then update `SHOPIFY_APP_URL` **and** the App URL + redirect URLs in Shopify settings to match. All three must agree or OAuth breaks.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| 502 on every route | Railway injected PORT=8080 | Pin `PORT=3000` |
| OAuth redirect error / "invalid redirect_uri" | App URL mismatch | `SHOPIFY_APP_URL`, Shopify App URL, and redirect URL prefixes must be identical (scheme, host, no trailing slash) |
| Prisma migrate fails | Using pooled URL for migrations | Migrations need `DIRECT_URL` (port 5432); runtime uses `DATABASE_URL` (port 6543) |
| App loads outside admin but not embedded | Wrong App URL or missing HTTPS | Embedded apps require the exact HTTPS App URL configured in Shopify |
| Wallet won't connect | Wrong network | The app targets Base (8453); switch network in the wallet |

## Security posture (tell the user)

- **Zero scopes:** the app requests no Shopify permissions — it structurally cannot access orders, customers, or products.
- **Non-custodial:** USDC moves only when the merchant's own wallet signs, in their browser. The server never holds keys or funds.
- **Self-hosted:** credentials, database, and infrastructure belong to the merchant.
- **Pinned source:** always deploy from the audited commit (`3acf3b6`) or a tagged release you have reviewed. The deployed app receives your Shopify secret and database credentials — deploying unreviewed code is a supply-chain risk.
- The 0.3% protocol fee is itemized on the review screen and collected on-chain by the batch contract. It is contract-enforced on Base, not app code — self-hosting or forking does not remove it, and there is no subscription or plan.
- Security issues → report privately to support@spraay.app, not a public issue.

## Related

- Running payouts after deployment → `shopify-batch-payouts` skill
- Protocol docs → https://docs.spraay.app
