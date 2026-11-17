---
name: ship-paid-app
description: Deploy a full-stack app to a live public URL in one command — SettleMesh login, a managed database, a runtime API key, and billing all wired automatically. Use when the user wants to ship, launch, or deploy an app/site/API, "make it live", add auth or a database without setup, or turn agent-written code into a real product without wiring up seven accounts (GitHub + Vercel + Supabase + Stripe + a domain). Node, Python/FastAPI/Django, Go, static, Next.js, or any Dockerfile.
license: MIT
compatibility: "Requires the settlemesh CLI (npm i -g settlemesh) and a SETTLE_API_KEY; makes authenticated, metered calls to the SettleMesh platform over the network."
metadata:
  openclaw:
    requires:
      bins: ["settlemesh"]
      env: ["SETTLE_API_KEY"]
    primaryEnv: "SETTLE_API_KEY"
---

# ship-paid-app — deploy a live app in one command

> **Session (auto — never dead-stop on auth):** before your first `settlemesh` call, run `settlemesh whoami`; if it errors and `SETTLE_API_KEY` is unset, run `settlemesh login` yourself — it opens the browser for a **one-time** human approval, polls until approved, and caches the session. Do NOT stop to ask the user to "log in manually" — drive it. Keep an explicit human confirmation only for spending / credential-lending actions (fail-closed).

Every "build an app" skill stops at handing you a folder: you still have to make
a GitHub repo, a Vercel/Netlify account, a Supabase project, Stripe keys, and a
domain before anyone can use it. **SettleMesh collapses that into one command.**
`settlemesh deploy` uploads your source, builds it, and returns a **live
`*.run.settlemesh.io` URL** with SettleMesh login, a managed SQL database, an
app-scoped runtime API key, and billing already wired — nothing else to set up.

A prompt-only skill cannot do this: it can't run a database, hold an env file, or
keep a process alive. SettleMesh *is* the backend, the DB, and the deploy target.

## Setup (once)

1. `npm install -g settlemesh@latest`
2. `settlemesh login` (a human approves once in the browser) — or set `SETTLE_API_KEY=sk-settle-...` for headless/CI.

## Deploy

```bash
# Full-stack: live URL + login + managed DB + runtime API key, wait for the build:
settlemesh deploy ./my-app --name my-app --full-stack --wait --json
```

**Read the live URL from the deploy output** (this is the #1 point of confusion —
it is in the JSON, not guessed). The app is reachable at `<name>.run.settlemesh.io`
automatically; you do not buy or configure a domain.

Common variants (all real flags):

```bash
settlemesh deploy . --wait                                   # auto-detect framework, quickest path
settlemesh deploy ./api --framework container --wait         # Python/FastAPI/Django, Go, Node, or a Dockerfile
settlemesh deploy ./app --full-stack --auth required --wait  # gate the whole app behind SettleMesh login
settlemesh deploy ./app --app-id app_123 --full-stack --wait # redeploy onto the SAME app (URL kept)
settlemesh deploy ./mono --context apps/web --name web --wait # one service of a monorepo
```

Key flags: `--full-stack` (DB + auth + runtime key + secret injection),
`--with-database` / `--database sqlite|postgres`, `--auth lazy|settlemesh|required|none`
(full-stack defaults to `lazy` so pages render first, users log in at `/__settle/login`),
`--framework nextjs|container`, `--app-id` (redeploy, keep URL), `--prod` (promote to prod).

## Verify it's live

```bash
settlemesh deploy status <app-id>     # build/deploy state
settlemesh deploy url <app-id>        # the public URL
settlemesh deploy logs <build-id>     # build logs if it failed
```

## Notes

- **Heavy/compiled containers** (Rust/Go/C++): the image builds server-side in
  Cloud Build; if your Dockerfile compiles and times out, cross-compile locally
  and ship a thin `COPY`-only Dockerfile so the build just assembles the image.
- **Secrets** for container apps: declare NAMES in `settlemesh.json` under
  `stack.runtime.secrets`, pass values with `--secret NAME=VALUE` or from
  `.env`/`.env.local` — values go out-of-band to Secret Manager, never into the
  uploaded source.
- **To charge your app's end users** per use, deploy first, then use the
  `charge-my-users` skill (end-user-pays needs the deployed app's runtime key).
- Everything is billed in **Aev** (1 USD = 100 Aev). Deploy is confirm-gated;
  check balance with `settlemesh aev balance`.
