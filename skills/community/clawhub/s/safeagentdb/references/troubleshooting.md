# Troubleshooting

Use this checklist when a preview deployment, hydration run, or migration does not behave as expected. Add the relevant parts to the target project's branching doc so future agents can debug without rediscovering these.

## Preview App Is Not Using The Expected Database

Work through these in order:

1. Check whether the preview workflow ran for the Git branch (GitHub Actions run list).
2. Check whether the Supabase preview branch exists:

```bash
npx supabase branches list --project-ref <parent-project-ref>
```

3. Check row counts in the preview database for a few key tables:

```sql
select count(*) from public.<important-table>;
```

Compare against the hydration source. The provision script also writes per-table copied row counts into `preview-branch-summary.md`.

4. Check the branch-scoped Vercel preview env vars:

```bash
vercel env ls preview <git-branch> --scope <vercel-scope>
```

5. If env vars were added or changed after the preview was built, redeploy. Frontend public env vars (for example `NEXT_PUBLIC_*`) are baked in at build time, so a stale build keeps pointing at the old database:

```bash
vercel redeploy <deployment-url> --target preview --scope <vercel-scope>
```

## Login Fails On A Preview

- Copied auth users do not keep their original passwords. The Admin API cannot read password hashes, so every copied user's password is reset to the shared `PREVIEW_USER_PASSWORD`. A "wrong password" on a preview usually means the user typed their real password.
- The preview password must never be used for production or persistent develop users.

## Third-Party OAuth (Google etc.) Fails On A Preview

Each Supabase branch has its own callback URL:

```text
https://<branch-project-ref>.supabase.co/auth/v1/callback
```

Most OAuth providers (including Google) do not allow wildcard redirect URIs, so each preview branch that needs OAuth login requires its exact callback URL added to the provider's authorized redirect URIs. The provision summary prints the callback URL for this reason.

If the provider returns `redirect_uri_mismatch`, the branch callback URL is missing from the provider configuration. Email/password login still works if auth users were copied.

## Migration Failures

- Duplicate timestamp prefix: two migration files share the same 14-digit prefix. Rename one with a later timestamp.
- Destructive SQL scan blocked the PR: a human reviews the migration, then adds the `migration-reviewed` label to bypass.
- A feature migration appeared on shared develop: feature migrations must only apply to that feature's preview branch until merge. Check that nothing ran `migrations:apply` against develop from a feature branch.
- Migrations out of order after merging several branches: validate with `supabase db push --dry-run` (production) or `migrations:apply <develop-branch> dry-run` (develop) before deploying.

## Local Development Issues

- `supabase status -o json` key names vary across CLI versions (`anon key` vs `publishable key`, `service_role key` vs `secret key`). The env helper accepts both; if it still fails, run `supabase status -o json` and compare key names.
- Local schema drifted: `supabase db reset` re-runs all migrations plus seed.
- OAuth providers generally do not work against local Supabase without extra callback configuration; use email/password locally.
- Webhooks from external services need a tunnel to reach local services.

## Preview Branch Costs And Leftovers

- Database branching is billed per branch-hour by Supabase. Stale preview branches cost money.
- PR close should trigger cleanup; deleted-without-PR branches are caught by the scheduled orphan cleanup workflow.
- If branches accumulate anyway, run the orphan cleanup workflow manually (workflow_dispatch) and check that `GITHUB_TOKEN` and `SUPABASE_ACCESS_TOKEN` are valid.
- Persistent preview environments listed in `persistentPreviews` are intentionally skipped by both cleanup paths.
