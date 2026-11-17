# Auto-merge small, safe changes

GitHub can merge a pull request by itself once the checks pass. Shipyard only allows that for small, low-risk changes. Anything that could hurt users waits for a human.

## The tiers in plain words

- **Merges itself after green checks:** small changes to ordinary app code, text, styles, docs, tests, and routine dependency updates (patch and minor versions from Dependabot).
- **Always waits for a person (label `needs-review`):**
  - anything touching sign-in or sessions (`src/lib/auth/`, `src/lib/session.ts`, `src/app/auth/`, `src/app/api/auth/`, `src/proxy.ts`) and the guards that protect it (`src/lib/safe-next.mjs`, `src/lib/same-origin.mjs`, `src/lib/rate-limit.mjs`)
  - the database: everything in `supabase/` (migrations, privacy rules, `isolation.json`) and `src/lib/supabase/`
  - payments (`src/lib/billing/`, `src/app/api/billing/`)
  - account deletion and profiles (`src/lib/account/`, `src/app/api/account/`, `src/app/api/profile/`)
  - the admin pages (`src/app/admin/`, `src/app/api/admin/`)
  - the modules that use the secret server key (`src/lib/newsletter/`, `src/app/api/newsletter/`, `src/lib/errors/`, `src/app/api/errors/`)
  - the tests (`tests/`): a pull request must not be able to delete the tests that would catch it
  - the automation itself (`.github/`)
  - `next.config.ts`, and `package.json` unless it is a Dependabot patch or minor update
  - any change over 400 changed lines
  - Dependabot major version updates
- It acts only on pull requests that carry the label `automerge`, or that Dependabot opened. Nothing merges unless someone opted in.
- A risky pull request gets one comment explaining why it is waiting. The student reviews it like any other.
- The robot owns the auto-merge switch on these pull requests. Every time a pull request changes (new commit, label added or removed, reopened) it first switches auto-merge off, then switches it on again only if the newest commit passes the rules. If the label is removed, or anything goes wrong, it stays off. To merge one yourself, press the merge button when the Tests check is green.

## Set it up

1. `node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-setup.mjs" <appDir> --only automerge,deps` writes `.github/workflows/automerge.yml` and `.github/dependabot.yml` (npm, weekly, grouped, at most 5 open pull requests).
2. The script reads the repo settings first and shows what it wants to change. Ask the student, then say yes for them: turn on "Allow auto-merge", turn on "Automatically delete head branches", and require the `Tests` check on `main`.
3. Branch, pull request (this one touches `.github/`, so it waits for the student's own review, which is correct), merge.
4. Try it: make a tiny text change on a branch, open a pull request with the label `automerge`, watch `gh pr checks --watch`. It should merge after green. Then try one that touches a migration and confirm it gets `needs-review`. Ask before opening test pull requests.

## The catch for free private repos

GitHub does not enforce required checks on free private repositories, so auto-merge cannot wait for them and does not work there. Choices: make the repo public (only if the code holds no secrets and the student is happy sharing it), upgrade to GitHub Pro, or skip auto-merge and merge by hand while watching for green. Never merge while red.

## Safety notes

- The workflow reads only file names and counts, never pull request titles or text in commands.
- It never checks out or runs the pull request's own code. That is what makes it safe to use the trigger `pull_request_target`, which makes GitHub run the workflow file from the main branch instead of the copy in the pull request. (A normal `pull_request` trigger would let a pull request rewrite the workflow to merge itself.) This is the one deliberate exception to "no `pull_request_target`" in Shipyard's rules, and it holds only while no step runs pull request code. Do not add one.
- The rule "wait for the Tests check" is tied to the GitHub Actions app, so a check named `Tests` that comes from anywhere else does not count.
- Pull requests from forks never auto-merge.
- Turning it off: delete the workflow file in a pull request, or remove the repo's auto-merge setting.
