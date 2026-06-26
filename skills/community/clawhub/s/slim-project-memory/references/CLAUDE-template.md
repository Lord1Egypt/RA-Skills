# {{PROJECT_NAME}}

> {{ONE_LINE_DESCRIPTION}}
> {{#PRODUCTION_URL}}Production: {{PRODUCTION_URL}}{{/PRODUCTION_URL}}
> Repo: {{REPO_URL}}

**Environment URLs and env var name references are in `CLAUDE.local.md` (gitignored, auto-loaded by Claude alongside this file).** Read it before any DB or hosting operation to know which env vars and service URLs to use. Actual secret values should be set in the hosting platform's environment variable manager, not in any project file.

---

## Hard rules (non-negotiable)

<!--
  PROJECT-SPECIFIC LOAD-BEARING RULES.
  Replace this comment with the actual rules for THIS project.
  Examples to consider:
  - "Default deploy/operation target is `{{DEFAULT_BRANCH}}`. Other branches require explicit user approval in the current turn."
  - "Never work directly on staging, canary, or production databases. Develop locally first."
  - "Dry-run is mandatory for all data scripts before live execution."
  - "Destructive operations (DELETE, TRUNCATE, DROP, force-push) require explicit user approval in the current turn."
  - "Never use `prisma db push` for changes going to staging/production. Use migrations."
  - "In `$queryRaw` / `$executeRaw`, always use snake_case columns."
  - Language-specific footguns: missing imports, raw SQL conventions, etc.
  - Reuse existing logic — don't reinvent.
-->

- Default deploy/operation target is `{{DEFAULT_BRANCH}}`. Other environments require explicit user approval *in the current turn*.
- Never work directly on remote databases. Develop locally first.
- Dry-run is mandatory for all data-modifying scripts before live execution.
- Destructive operations (DELETE, TRUNCATE, DROP, force-push) require explicit user approval.

---

## Branch → environment topology

<!--
  Replace with the actual branches and environments for this project.
  Don't include connection strings here — those go in CLAUDE.local.md.
-->

| Branch | Environment | Auto-deploy | Notes |
|--------|-------------|-------------|-------|
{{#BRANCHES}}
| {{branch}} | {{env}} | {{auto_deploy}} | {{notes}} |
{{/BRANCHES}}

(Connection strings → `CLAUDE.local.md`)

---

## Where to find things

<!--
  Add a one-line pointer here for every topical doc you create under docs/.
  Each pointer is loaded lazily by Claude when relevant.
  Start small and grow this list as the project grows.
  Do NOT inline content here — link to it.
-->

**Architecture**
- Tech stack & project structure → `docs/architecture/overview.md`
<!-- - Database schema → `docs/architecture/database.md` -->
<!-- - Authentication → `docs/architecture/auth.md` -->
<!-- - Caching strategy → `docs/architecture/caching.md` -->

**Features**
<!-- - Add per-feature deep dives here as you build them -->

**Pipeline / scripts** (delete this section if not applicable)
<!-- - Data pipeline → `docs/pipeline/README.md` -->
<!-- - Scripts catalog → `docs/scripts/README.md` -->

**Reference**
- Business context → `docs/BUSINESS-CONTEXT.md`
- Troubleshooting → `docs/TROUBLESHOOTING.md`
- State snapshot (dated entity counts) → `docs/STATE-SNAPSHOT.md`
- Recent sessions → `docs/recaps/`

---

## Contracts (the artifacts we treat as commitments)

Three layers of documentation act as contracts and must stay in sync as the codebase evolves. Updating them is part of finishing work, not a separate optional task.

| Contract | Location | Cadence | Purpose |
|----------|----------|---------|---------|
| **Plans** | `docs/plans/YYYY-MM-DD-<slug>.md` | Per feature | Pre-work contract: what we're building, acceptance criteria, linked docs to update |
| **Recaps** | `docs/recaps/SESSION-RECAP-YYYY-MM-DD.md` | Per session | Post-work journal: what shipped, criteria status, doc-update follow-ups |
| **Technical reference** | `TECHNICAL-DOCUMENTATION.md` (top level) | Per feature | Developer-onboarding contract: architecture, schema, API, deployment |
| **Functional reference** | `FUNCTIONAL-SPECIFICATIONS.md` (top level) | Per feature | User-flow contract: behavior, screens, edge cases |

**The cycle is**: draft a plan → implement → write a recap → update the technical and functional contracts. Each phase produces an artifact the next phase consumes. The recap skill prompts for the doc updates explicitly so they don't get skipped.

For trivial changes (typos, single-line fixes, dependency bumps), the cycle compresses: skip the plan, write a brief recap, no contract-doc updates needed. The methodology should match the size of the work.

---

## Common commands

```bash
# Replace these with the 5–10 commands you actually run often.
# Examples:
# docker-compose up -d                                       # local dev
# git checkout {{DEFAULT_BRANCH}} && git merge develop && git push
# npm test
# npm run build
```

---

## Today's state

<!--
  Small dynamic bullets — refresh from docs/STATE-SNAPSHOT.md when stale.
  Keep to 3-5 lines. NOT a place for stat tables.
-->

- (add current entity counts, recent activity, open gaps here once the project has data)

---

{{HOUSEKEEPING_PROTOCOL}}

## Session protocol

**At the start** of any non-trivial session, run `/warmup`. It loads CLAUDE.md, the latest session recap, all active plans in `docs/plans/`, and the relevant feature/architecture docs for the upcoming task before answering anything.

**At the end** of any session that touched anything, run `/wrapup`. It verifies a recap exists, checks "Today's state" freshness, asks for disposition on uncommitted changes, transitions plan status, escalates deferred-update debts, runs drift checks, and drafts a next-session preview that injects into "Today's state" and the recap.

For trivial sessions (typo fix, dependency bump, one-line change), skip warmup and skip the recap, but **still run `/wrapup`** — even a one-line fix benefits from a 30-second drift check and uncommitted-work disposition.

Otherwise:

1. Read this file (auto-loaded).
2. Read `CLAUDE.local.md` if you need an env var name reference or service URL (auto-loaded, contains no secret values — actual credentials are in the hosting platform's environment variables).
3. For task-specific context, read the relevant `docs/` file from the "Where to find things" map.
4. When changes are made, follow the housekeeping protocol above.

**The six-stage cycle**: `warmup → plan → build → recap → wrapup → next session`. Skills available: `/warmup`, `/plan-feature`, (build is yours), `/recap`, `/wrapup`. Skip `/plan-feature` for trivial work; skip `/warmup` and `/recap` for trivial sessions; **never skip `/wrapup`** if the session touched anything.
