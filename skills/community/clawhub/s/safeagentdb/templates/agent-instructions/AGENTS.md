# SafeAgentDB Agent Instructions

Use these instructions when working on database infrastructure, migrations, preview deployments, or local database development in this repository.

## SafeAgentDB Rules

- Keep production, develop, preview, and local databases separate.
- Do not point feature or agent branches at production.
- Do not apply feature-branch migrations to shared develop until merge.
- Do not copy production data into preview databases without explicit user approval.
- Do not commit secrets, service role keys, access tokens, preview passwords, or `.env.local`.
- Before changing GitHub Actions, Vercel env vars, Supabase branches, or database hydration behavior, explain the change and the credentials needed.
- When changing database schema, validate migrations locally or in preview before shared environments.

## Setup Reference

For the full setup and maintenance workflow, use the installed SafeAgentDB skill:

```text
safeagentdb
```

If this project does not use Supabase, Vercel, and GitHub Actions, treat SafeAgentDB as a conceptual model and adapt with the user's approval.

