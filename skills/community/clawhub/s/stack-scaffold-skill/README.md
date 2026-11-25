# Stack Scaffold — a Next.js + Supabase + Stripe app that runs with zero keys

Free agent skill. Ask your agent to scaffold a fullstack app, and get a project that
actually starts before you have any accounts.

## The problem

Most "starter templates" fail in the same two places: they need real API keys before
anything renders, and the Stripe webhook is wired wrong (parsed JSON instead of the raw
body, so every signature check fails). You end up debugging the scaffold instead of
building the product.

This skill is built around two rules: **mock mode is the default**, and **no secrets ever
get committed**.

## What gets generated

- Next.js 15 app router, TypeScript, Tailwind
- `/` home, `/pricing` with a checkout button, `/protected` that shows **Access denied** to
  anonymous visitors
- `/api/checkout` — a real Stripe Checkout Session, or a mock response without keys
- `/api/webhook` — raw-body signature verification via `constructEvent`
- `lib/supabase.ts` and `lib/stripe.ts` — graceful fallbacks when keys are absent
- `.env.example` (placeholders only), `.gitignore` (secrets ignored from commit one),
  configs, README

`npm install && npm run dev` works immediately: no Supabase project, no Stripe account,
nothing.

## The environment check

The skill refuses to call the scaffold done until the required variables are present and
valid. It prints a table (variable, group, status, hint) and treats these as failures:

- `NEXT_PUBLIC_SUPABASE_URL` not an http(s) URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` not `sb_publishable_...` or a JWT
- `STRIPE_SECRET_KEY` not `sk_test_...` / `sk_live_...`
- `STRIPE_WEBHOOK_SECRET` not `whsec_...`

Missing values are fine in mock mode; invalid values are never fine. In real mode, every
required row must read `ok`.

## Install

```
npx skills add WinSoftLabs30/stack-scaffold-skill
```

On ClawHub (OpenClaw): `openclaw skills install @winsoftlabs30/stack-scaffold-skill`, or
`clawhub install @winsoftlabs30/stack-scaffold-skill`.

Or copy `SKILL.md` into:

- **OpenCode** — `.opencode/skills/stack-scaffold/` or `~/.config/opencode/skills/stack-scaffold/`
- **Claude Code** — `.claude/skills/stack-scaffold/`
- **Other agents** — any that read `SKILL.md`

No build step and no dependencies. Any Node version works for this manual edition.

## Use

Ask your agent:

- "scaffold a fullstack app"
- "start a Next.js + Supabase + Stripe project called acme"
- "give me a Stripe checkout and webhook that actually verify signatures"

It asks three questions (app name, Supabase real or mock, Stripe real or mock), generates
the tree, and checks the environment before reporting done.

## Manual edition

This repository is the workflow, the file checklist and the env rules. The paid edition
adds the two tested scripts that do the mechanical part:

- `scaffold.ts` — writes the whole tree in one command, with overwrite safety
- `env-doctor.ts` — parses `.env`/`.env.local`, validates every variable, exits non-zero in
  real mode until it passes, and prints the report

Both are dependency-free and run as TypeScript on Node 22.6+. The paid edition is backed
by 20 tests, including a generated app that was verified with `next build`.

## Honest limits

- One stack: Next.js 15 app router + Supabase + Stripe. It is not a universal generator.
- It scaffolds; it does not design your product, schema or pricing.
- Mock mode is for development. Going live still means creating the Supabase project, the
  Stripe products and the webhook endpoint.
- The manual edition leans on the agent's judgment. The paid scripts make the output
  identical every run.

## License

MIT-0 — see [LICENSE](LICENSE). Use it, modify it, redistribute it, no attribution
needed. (ClawHub requires MIT-0, so both free channels use one license.)
