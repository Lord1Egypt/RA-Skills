---
name: safeagentdb
description: Sets up and maintains SafeAgentDB-style database safety infrastructure for AFK agentic development. Use when integrating isolated local, develop, preview, and production database workflows; configuring Supabase/Vercel/GitHub Actions previews; adding migration guardrails; packaging SafeAgentDB into a project; or adapting branch-safe database infrastructure to another stack.
---

# SafeAgentDB

Use this skill when the user wants to install, adapt, audit, package, or maintain SafeAgentDB-style infrastructure in a project.

SafeAgentDB is database safety infrastructure for AFK agentic development. It helps multi-agent teams create testable PRs and live preview URLs backed by isolated database environments, without risking production or shared development data.

## Mission

Set up or adapt a workflow where:

```text
main      -> production app + production database
develop   -> staging app + persistent develop database
feature/* -> preview app + isolated preview database
agent/*   -> preview app + isolated preview database
local     -> local app + local Docker database
```

The default implementation is built for:

- Supabase for Postgres, Auth, Storage, migrations, and database branches
- Vercel for production, staging, and preview deployments
- GitHub Actions for branch and PR automation

If the target project does not use this stack, this skill is no longer prescriptive. Use the target codebase, target platform docs, and the user's judgment to design the equivalent infrastructure. Explain what this skill does not cover and what decisions the user needs to make before editing.

## Bundled Files

This skill is self-contained. Read the bundled references as needed:

- `references/setup-process.md` for the end-to-end install flow.
- `references/credentials.md` before asking for tokens or setting secrets.
- `references/data-hydration-policy.md` before creating develop or preview databases.
- `references/local-development.md` when adding local database development.
- `references/non-standard-stacks.md` if the target project is not Supabase + Vercel + GitHub Actions.
- `references/troubleshooting.md` when debugging previews, hydration, migrations, or costs after setup.
- `references/agent-operating-rules.md` when adding ongoing maintenance rules to the target project's docs.
- `references/agent-packaging.md` if the user wants Cursor, Codex, or Claude Code packaging.

Use bundled templates from:

- `templates/branching-config.example.json`
- `templates/package-scripts.json`
- `templates/package-dev-dependencies.json`
- `templates/docs/database-branching.md`
- `templates/scripts/supabase/`
- `templates/scripts/ci/`
- `templates/.github/workflows/`
- `templates/agent-instructions/`

## Required First Step

Inspect the target project before editing. Determine:

- framework and package manager
- database provider
- auth provider
- object storage provider
- deployment provider
- CI provider
- migration system
- branch model
- environment variable names
- whether production, develop/staging, preview, and local database workflows already exist
- whether Supabase CLI files exist: `supabase/config.toml`, `supabase/migrations/`, `supabase/seed.sql`
- whether migrations are committed or SQL is managed manually in a dashboard
- which database should initialize or hydrate persistent develop
- which database should hydrate feature/agent preview databases
- whether auth users, public table data, and storage objects should be copied into previews

After inspection, summarize the current state and proposed setup before making infrastructure changes. Do not start by copying templates.

## Infrastructure Map

Treat these concepts as the portable infrastructure:

```text
Git branch model
  main / develop / feature-* / agent-* / local

Database environment model
  production database
  persistent develop database
  disposable preview databases
  local Docker database

Migration model
  committed migration files
  local reset before push
  preview-only feature migrations
  develop migrations after merge
  production migrations from main

Preview deployment model
  create preview database
  hydrate or seed preview database
  set branch-scoped deployment env vars
  rebuild/redeploy preview app
  clean up preview database and env vars when branch closes

Credential model
  provider access tokens in secret stores
  non-secret project refs in config
  no committed service keys or local env files
```

Supabase, Vercel, and GitHub Actions are the default implementation, not the only possible implementation.

## Porting To Other Stacks

If the target project uses a different stack, map each concept before editing:

```text
Supabase branches       -> database branch/clone/ephemeral DB equivalent
Supabase migrations     -> target project's migration system
Supabase Auth           -> target auth provider or user seed/copy process
Supabase Storage        -> target object storage provider
Vercel previews         -> target preview deployment system
Vercel branch env vars  -> target environment variable mechanism
GitHub Actions          -> target CI/CD runner and secret store
```

Read `references/non-standard-stacks.md`, explain the adaptation plan to the user, and only then implement.

## Core Workflow

1. Summarize the target project's current state.
2. Copy `templates/docs/database-branching.md` into the project, fill in the placeholders as the proposed plan, and review that document with the user. The approved document stays in the repo as the source of truth and decision record.
3. Explain needed credentials and costs, and ask permission before using or setting anything. Database branching is billed per branch-hour; confirm the user's plan supports it.
4. Confirm the data hydration policy before copying data.
5. Install or adapt scripts, workflows, package scripts, config, and docs.
6. Validate with safe local and CI checks, including `npm run preview:provision -- <branch> --dry-run` for the cloud path.
7. Report changed files, remaining secrets/config, and testing steps.

## Install Or Adapt

Install or adapt:

- local database command that points env vars at local services without overwriting unrelated env values
- persistent develop/staging database workflow
- feature/agent preview database provisioning
- Vercel preview env-var wiring so each preview deployment points at its matching preview database
- preview redeploy behavior after env vars change, because frontend public env vars are build-time values
- migration deployment workflow for develop and main
- guardrails so feature migrations stay on feature previews until merge
- optional auth user copying with preview password reset
- optional public table data copying with include/exclude lists
- optional storage bucket creation and object copying
- cleanup automation for closed or deleted preview branches
- scheduled orphan preview cleanup for deleted Git branches
- optional persistent preview environments (long-lived design/demo branches with custom domains) that cleanup skips
- migration safety checks for duplicate timestamps and destructive SQL
- a committed branching architecture doc (from `templates/docs/database-branching.md`) covering branch model, hydration policy, secrets, OAuth callbacks, and debugging
- optional agent packaging as a Cursor/Codex/Claude Code skill or project instruction file, only if the user wants it

## Data Source Rule

Recommended hydration default:

```text
production/default schema -> persistent develop
persistent develop data   -> feature/agent previews
local Docker database     -> migrations + seed only
```

Do not copy production data into previews unless the user explicitly approves it and confirms privacy/compliance requirements.

Read `references/data-hydration-policy.md` before implementing hydration.

## Safety Rules

- Never commit secrets, `.env.local`, service role keys, access tokens, or preview passwords.
- Never point agent feature work at production.
- Never copy production data into previews without explicit user approval.
- Never apply feature-branch migrations to shared develop until merge.
- Keep production, develop, preview, and local databases separate.
- Preserve unrelated user changes.
- If the stack differs from Supabase/Vercel/GitHub Actions, stop and propose an adapted plan before editing.

## Credential Rule

Before running commands that require external access, explain what credentials are needed, why they are needed, where they will be stored, and ask the user for permission. Do not ask the user to paste secrets into committed files.

Read `references/credentials.md` for the exact checklist.

## Packaging Guidance

If the user asks to install SafeAgentDB as a skill:

- Cursor project skill: `.cursor/skills/safeagentdb/SKILL.md`
- Cursor/Codex cross-agent project skill: `.agents/skills/safeagentdb/SKILL.md`
- Claude Code project skill: `.claude/skills/safeagentdb/SKILL.md`
- Codex always-on instructions: `AGENTS.md`
- Claude Code always-on instructions: `CLAUDE.md`

If the user is using `npx skills add`, this skill should be discoverable from the repository `skills/safeagentdb/SKILL.md`.

Read `references/agent-packaging.md` before adding agent-specific files.

## Done Criteria

When finished, report:

- files changed
- credentials still required
- where secrets were stored, without revealing values
- what database develop is initialized from
- what database previews are hydrated from
- whether auth users, public data, and storage are copied or seeded
- how to test local dev, develop/staging, feature preview, and production migration paths
- validation commands run, including the provision dry-run output
- where the branching architecture doc lives in the repo

