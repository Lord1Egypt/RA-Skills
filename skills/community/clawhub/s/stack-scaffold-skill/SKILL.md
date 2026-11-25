---
name: Stack Scaffold
description: Scaffold a runnable Next.js 15 app with Tailwind, a Supabase client, and Stripe checkout plus a signature-verified webhook. Runs in mock mode with zero keys, and an environment check blocks "done" until the required variables are present and valid. Use when asked to scaffold or start a new fullstack app.
---

# Stack Scaffold (manual edition)

This edition is the workflow and the file checklist. The paid edition adds two tested
scripts: `scaffold.ts` writes the whole tree in one command, and `env-doctor.ts` prints the
environment report and refuses to pass until real keys are valid.

## Ask first (one short round of questions)

1. App name?
2. Supabase: real project keys, or skip (mock mode)?
3. Stripe: real keys, or skip (mock mode)?

Do not start generating until you have all three answers.

## What to generate

A Next.js 15 app router project, TypeScript, Tailwind:

| Path | Must contain |
| --- | --- |
| `package.json` | next 15, react 19, `stripe`, `@supabase/supabase-js`, typescript, tailwind; `dev`/`build`/`start` scripts |
| `next.config.ts`, `tsconfig.json`, `postcss.config.mjs`, `tailwind.config.ts` | standard Next 15 + Tailwind config |
| `app/layout.tsx`, `app/globals.css` | Tailwind imports, page shell |
| `app/page.tsx` | home page with links to `/pricing` and `/protected` |
| `app/pricing/page.tsx` | client component; button POSTs `/api/checkout`; on `{url}` redirect; on `{mock}` show the message |
| `app/protected/page.tsx` | server component; reads the Supabase session; no session shows **Access denied** |
| `app/api/checkout/route.ts` | Stripe Checkout Session from `STRIPE_SECRET_KEY`, or a mock JSON response |
| `app/api/webhook/route.ts` | raw body, `constructEvent` signature check, 200 on success |
| `lib/supabase.ts` | browser client; exports a null client or `isSupabaseConfigured` when unset |
| `lib/stripe.ts` | Stripe client from `STRIPE_SECRET_KEY`; null when unset |
| `.env.example` | placeholders only, never real keys |
| `.gitignore` | `.env`, `.env.local`, `.next`, `node_modules` from commit one |
| `README.md` | run instructions, mock-mode note, webhook setup |

### Mock mode is the default

- No `STRIPE_SECRET_KEY`: `/api/checkout` returns `{ "mock": true, "message": "Mock checkout..." }`
  with status 200, and `/pricing` explains that checkout is mocked.
- No `STRIPE_WEBHOOK_SECRET`: `/api/webhook` answers 200 with `{ "received": true, "mock": true }`.
- No `NEXT_PUBLIC_SUPABASE_URL` or anon key: the Supabase client is disabled and
  `/protected` shows Access denied.
- `npm install && npm run dev` must work with zero accounts and zero keys. Do not remove
  the fallbacks to "simplify".

### Webhook correctness

Read the body with `await req.text()` before parsing. Verify it with
`stripe.webhooks.constructEvent(body, signature, secret)`. A missing secret means mock
acknowledge; a bad signature is a 400, not a 200.

## Environment check (do this by hand in the manual edition)

| Variable | Required for real mode | Valid when |
| --- | --- | --- |
| `NEXT_PUBLIC_APP_URL` | optional | an http(s) URL; defaults to `http://localhost:3000` |
| `NEXT_PUBLIC_SUPABASE_URL` | yes | an http(s) URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | yes | starts `sb_publishable_` or is a 3-part JWT |
| `STRIPE_SECRET_KEY` | yes | starts `sk_test_` or `sk_live_` |
| `STRIPE_WEBHOOK_SECRET` | yes | starts `whsec_` |

Print the table with status `ok` / `missing` / `invalid` and one hint per row. In mock mode,
missing is fine but invalid is still a failure. In real mode, do not call the scaffold done
until every required row is `ok`. If the user gave real keys, write them into `.env.local`
(never committed), not `.env`.

## Done when

- `npm install && npm run dev` serves the app (tell the user to run it if you cannot).
- `/pricing` shows the checkout button; in mock mode it explains the mock.
- `/api/webhook` answers 200 in mock mode; with real Stripe it verifies signatures.
- `/protected` shows Access denied for anonymous visitors.
- The environment table passes for the chosen mode.

## Hard rules

- Never commit secrets: `.env` and `.env.local` stay in `.gitignore`.
- Never invent keys and never echo key values back to the user.
- Never modify files outside the target directory.
- Target directory must be empty unless the user explicitly agrees to overwrite.
