# Credentials And Permissions

Use this before provisioning branch databases, setting Vercel preview env vars, or installing GitHub Actions.

## Ask Permission First

Before requesting or setting credentials, explain:

- what credential is needed
- why it is needed
- where it will be stored
- what permissions/scopes it requires
- whether the agent will set it or the user will set it manually

Never commit secret values. Do not print secret values after the user provides them.

## Cost Check

Confirm costs with the user before the first provision:

- Supabase database branching is a paid feature billed per branch-hour and requires a plan with branching enabled.
- Every open feature/agent branch can hold a live preview branch; many parallel agents means many concurrent branches.
- PR-close cleanup and the scheduled orphan cleanup are what keep this bounded — do not skip installing them.

## Supabase

Needed:

```text
SUPABASE_ACCESS_TOKEN
SUPABASE_PARENT_PROJECT_REF
SUPABASE_PROD_PROJECT_REF
SUPABASE_DEVELOP_BRANCH_REF or develop branch name/ref
```

Used for:

- listing Supabase branches
- creating preview branches
- deleting preview branches
- reading branch URLs and API keys
- applying migrations
- linking production for `supabase db push`

Store access tokens in GitHub Actions secrets or local CLI auth. Non-secret project refs can be stored in config if the user approves.

## Vercel

Needed:

```text
VERCEL_TOKEN
VERCEL_PROJECT_ID
VERCEL_PROJECT_NAME
VERCEL_SCOPE
```

Used for:

- setting branch-scoped preview environment variables
- redeploying Vercel previews after env changes
- finding the right Vercel project

Store `VERCEL_TOKEN` in GitHub Actions secrets. Project ID/name/scope may be stored in config if the user approves.

## GitHub

Needed:

```text
GITHUB_TOKEN or authenticated gh CLI
```

Used for:

- adding repository secrets
- installing GitHub Actions workflows
- checking whether Git branches still exist during orphan preview cleanup
- optionally commenting preview URLs on PRs

If using GitHub CLI, first check:

```bash
gh auth status
```

Only after user approval, offer commands like:

```bash
gh secret set SUPABASE_ACCESS_TOKEN
gh secret set SUPABASE_PARENT_PROJECT_REF
gh secret set SUPABASE_PROD_PROJECT_REF
gh secret set SUPABASE_DEVELOP_BRANCH_REF
gh secret set VERCEL_TOKEN
gh secret set VERCEL_SCOPE
```

If the user prefers dashboards, provide exact secret names and dashboard paths instead.

## CLI Permission

The agent may need permission to run:

```bash
npx supabase --version
npx vercel --version
npx supabase init
npx supabase link --project-ref <project-ref>
```

Ask before installing global tools. Prefer `npx` or existing project dev dependencies when possible.

