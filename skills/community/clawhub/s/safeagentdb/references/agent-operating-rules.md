# Agent Operating Rules

Add these rules to the target project's README, deployment docs, `AGENTS.md`, or project instructions after setup.

## When To Use These Rules

Use these rules whenever an AI agent changes:

- Supabase migrations
- Supabase branch scripts
- Vercel preview environment logic
- GitHub Actions workflows
- local Supabase development commands
- database hydration, seed, auth-copy, or storage-copy behavior

## Core Invariants

- Do not commit secrets, `.env.local`, service role keys, access tokens, or preview passwords.
- Ask permission before creating or updating GitHub secrets, Vercel env vars, Supabase branch settings, or CLI auth.
- Explain why each credential is needed before asking the user to provide it.
- Do not hardcode project-specific Supabase refs, Vercel IDs, domains, or passwords in reusable code unless the user approves storing non-secret config.
- Do not apply feature-branch migrations to persistent `develop` until the feature merges.
- Do not run destructive migrations without explicit review.
- Keep local development independent from GitHub pushes and cloud preview branches.
- Preserve unrelated user changes and untracked files.
- Do not delete database branches for environments listed in `persistentPreviews` in `branching-config.json`.
- Keep the repo's database branching doc up to date when changing any of this infrastructure.

## Local Development

Local development should work without GitHub or cloud preview branches:

```bash
supabase start
supabase db reset
npm run dev:local
```

The local env helper may update only the configured Supabase env keys. It must preserve all other `.env.local` values.

## Preview Branches

Preview provisioning should:

1. Create or reuse a preview database for the Git branch.
2. Apply pending migrations to that preview only.
3. Hydrate data from the configured source only when creating the preview or when explicitly forced.
4. Ensure required storage buckets exist.
5. Set branch-scoped Vercel preview env vars.
6. Redeploy the Vercel preview so public frontend env vars are baked into the build.

Do not copy production data or heavy storage buckets unless the user explicitly approves it.

## Optional Agent Memory

A project may convert these rules into a Cursor skill, Claude instruction file, `AGENTS.md`, or another agent memory format. That is optional. The setup works without a skill as long as these rules live somewhere future agents can read.

