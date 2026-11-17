# Putting an app in a project other apps already use

Use this when the free plan allows no more projects, or the student wants one project for several small apps. The app gets its own space inside the project (a Postgres schema called `app_<app name>`). Everything else there stays as it is. For a project with real users in it (like the owner's), treat the dry run as required.

## Say this to the student first

"Apps in the same project share one login list: someone with an account in another app there can sign in here with the same email and password. Each app's data stays separate." The script prints the same sentence once.

To make people sign in once across apps on subdomains of one domain, see `shared-sign-in.md`.

## Steps

1. Find the project id: Supabase dashboard, the project, the address contains it (20 letters and numbers). Never ask for the access token in chat.
2. Dry run, change nothing: `node "${CLAUDE_PLUGIN_ROOT}/scripts/provision-supabase.mjs" <appDir> --shared <projectId> --dry-run`. It saves how the project looks now, then prints the database steps rewritten for the app's schema, the new API list and the redirect addresses it would add. Read it to the student in plain words (new space, nothing else changes). If it refuses a database file, fix that file (see below) and run the dry run again.
3. Real run: the same command without `--dry-run`. Add `--schema <name>` to pick the space name (letters, digits, underscores; the default is fine).
4. It checks afterwards that nothing else in the project changed (sign-in main address, email settings, the public schema, the sign-up trigger, the list of schemas the API serves for other apps). If it stops with "unexpected change", show the student the commands it printed to put things back, and do not run them without asking. Nothing is reverted automatically.
5. It writes `NEXT_PUBLIC_SUPABASE_SCHEMA` into `.env.local` and records `schema` and `shared` in `.shipyard-app.json`. `provision-vercel.mjs` then sends the schema name to Vercel too. Run the app's `verify`: it sends the schema on every database call.

Adding a module later: run `provision-supabase.mjs <appDir>` again (no flag needed). A shared app always goes through the shared flow.

## What shared mode never does

Never changes the main sign-in address (site URL), email settings, providers, the `public` schema, other apps' schemas, or any trigger on `auth.users`. It only adds: its own schema and tables, the schema in the API's list, and its own addresses in the redirect list.

## Rules for the app's database files

- Put `public.` in front of every table, function and policy target (`public.items`). Shared mode rewrites `public.` to the app's schema. A name without a schema is refused.
- No trigger on `auth.users` outside the marker lines `-- shipyard:auth-trigger:start` and `-- shipyard:auth-trigger:end` (the block is left out in shared mode; the app creates the profile row itself on first use).
- Extensions, Cron jobs and other whole-project changes go between `-- shipyard:project-wide:start` and `-- shipyard:project-wide:end` (left out in shared mode) or are refused.
- Do not write to `auth`, `storage` or other schemas.

## If something is off

- "another app already uses this name": pick another `--schema`.
- "paused": restore the project in the dashboard first.
- The snapshot of the project before the run is in `<appDir>/.shipyard/shared-snapshot-<time>.json` (no secrets in it).
