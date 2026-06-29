# Database And Branching Architecture

<!--
SafeAgentDB plan/record document.

Fill this in BEFORE installing infrastructure and review it with the user.
After installation it stays in the repo as the source of truth for how Git
branches, deployments, and databases map to each other.

Replace every <placeholder>. Delete sections that do not apply.
-->

This document is the source of truth for how Git branches, deployments, and databases are intended to work for this repo.

## Environment Map

```text
<production-branch>
  -> <production deployment / URL>
  -> <production database>

<develop-branch>
  -> <staging deployment / URL>
  -> persistent <develop database>

<feature/** and agent/** branches>
  -> preview deployment per branch
  -> isolated preview database per branch
  -> data hydrated from <hydration source>

local
  -> local dev server
  -> local Docker database (migrations + seed)
```

## Identifiers (non-secret)

```text
Database provider:            <e.g. Supabase>
Production project ref:       <ref>
Persistent develop branch:    <name / ref>
Deployment provider:          <e.g. Vercel>
Deployment project:           <project name / id>
Deployment scope/team:        <scope>
CI provider:                  <e.g. GitHub Actions>
Repository:                   <owner/repo>
```

Secrets are NOT recorded here. Secret names and where they live:

```text
<SECRET_NAME>  -> <GitHub Actions secrets / CI secret store>
```

## Hydration Policy

```text
Branch creation source:    <e.g. production/default project>
Develop initialized from:  <source>
Previews hydrated from:    <source>
Auth user copy:            <yes/no; preview password resets apply>
Public table data copy:    <yes/no; include/exclude lists>
Storage bucket copy:       <buckets copied, buckets only created>
Seed/scrub policy:         <if applicable>
```

Note: the platform may not support creating a database branch from another
branch (Supabase returns "Cannot create preview branch from another branch
project"). That is why previews are created under the production/default
project but hydrated from develop. Do not "simplify" this split.

Production data is not copied into previews unless explicitly approved:
<approved/not approved, date, by whom>

## Persistent Preview Environments

Long-lived non-production environments (design/demo branches with their own domain):

```text
<git branch> -> <site URL> (listed in branching-config.json persistentPreviews)
```

These are skipped by PR-close cleanup and orphan cleanup.

## Migration Flow

```text
feature/agent branch migrations -> that branch's preview database only
merge to <develop-branch>       -> migrations applied to persistent develop
merge to <production-branch>    -> migrations applied to production
local                           -> supabase db reset before pushing
```

Guardrails: duplicate timestamp check and destructive SQL scan run on
migration PRs; the `migration-reviewed` label bypasses the scan after human
review.

## Preview Lifecycle

```text
push to feature/agent branch -> create/reuse preview DB, apply branch
                                migrations, hydrate (first run only),
                                set branch-scoped env vars, redeploy preview
PR closed                    -> preview DB and env vars deleted
nightly schedule             -> orphan preview DBs for deleted branches removed
FORCE_HYDRATE=true dispatch  -> re-copy hydration source data into a preview
```

Frontend public env vars are build-time values: after env vars change, the
preview must be redeployed.

## OAuth Callbacks

Each database branch has its own auth callback URL:

```text
https://<branch-project-ref>.<provider-domain>/auth/v1/callback
```

Branches that need third-party login require their callback URL added to the
OAuth provider manually. Known callback URLs:

```text
Production: <url>
Develop:    <url>
```

## Validation And Debugging

To validate provisioning without side effects:

```bash
npm run preview:provision -- <git-branch> --dry-run
```

For the full debugging checklist (preview pointing at wrong DB, login
failures, migration failures, cost leftovers), see the SafeAgentDB
troubleshooting reference or the equivalent section your installer added
below/alongside this doc.
