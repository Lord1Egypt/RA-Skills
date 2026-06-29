# Non-Standard Stacks

Use this if the target project is not Supabase + Vercel + GitHub Actions.

## Principle

Do not force these templates onto a different stack. Outside Supabase + Vercel + GitHub Actions, this package is a conceptual guide only.

Use the target codebase, the target platform's documentation, and the user's judgment as the source of truth. Identify equivalent concepts, explain what this package does not cover, then propose an adapted plan before editing.

If you are unsure how the target platform handles a piece of the workflow, stop and ask the user or research the platform docs. Do not invent behavior or imply the templates will work unchanged.

## If Not Supabase

Find the equivalents for:

- database migrations
- branch or preview databases
- seed data
- auth users
- storage buckets/files
- service credentials
- local database development

Examples:

```text
Supabase migrations       -> Prisma/Drizzle/Rails/Laravel migrations
Supabase branches         -> Neon branches, PlanetScale branches, Railway DBs, Docker DBs
Supabase Auth             -> Clerk/Auth0/custom auth
Supabase Storage          -> S3/R2/GCS/local storage
```

Stop and ask before adapting any Supabase-specific scripts.

## If Not Vercel

Find the equivalents for:

- preview deployments
- branch-scoped env vars
- redeploying after env var changes
- deployment URL discovery
- PR comments or deployment summaries

Examples:

```text
Vercel previews -> Netlify deploy previews, Render preview environments, Railway environments, Fly apps
Vercel env API  -> platform env API or CI-injected env vars
```

If frontend public env vars are build-time values, preserve the same ordering: create preview DB, set env vars, then build/redeploy preview.

## If Not GitHub Actions

Find the equivalents for:

- branch push triggers
- pull request opened/synchronized/closed triggers
- repository secrets
- scheduled cleanup jobs
- manual workflow dispatch

Examples:

```text
GitHub Actions -> GitLab CI, CircleCI, Buildkite, Jenkins, Vercel/Netlify build hooks
GitHub Secrets -> CI secret store
```

Do not assume `gh secret set` or `.github/workflows/` exists.

## Required Output

Before editing a non-standard stack, tell the user:

- what parts can be reused directly
- what parts need adaptation
- what this package does not cover for their stack
- what assumptions you are making from their codebase
- what decisions require the user's judgment
- what credentials are needed
- what tradeoffs or limitations remain
- what validation path will prove the setup works

