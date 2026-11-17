---
name: publish-skills
description: >
  Publish SKILL.md files to ClawHub (clawhub.ai) and diagnose publish failures
  across the three skill repos (history, ai-custom-skills, ai-thoughts). Use
  when the user wants to publish skills to ClawHub, manually trigger a publish,
  check why a publish failed or was skipped, or understand the ClawHub skill
  sync pipeline.
---

# ClawHub Skill Publish

Publish and maintain the ClawHub skill registry. All skills are published to a single ClawHub account (`j3ffyang`) through GitHub Actions; skills are never published manually.

## Scope

Skills come from three repos under the `negtivSpace` superproject. Each repo has its own `.github/workflows/clawhub-skill-sync.yml` that publishes its skills to ClawHub:

- `history/` — publishes only `.opencode/skills/chinese-history-literature-culture` (via a `skill_path` entry). The other skills in `history/.opencode/skills/` (`character-name-literary-origins`, `simplified-to-traditional`) are **local-only**: they stay in the repo for opencode to load but are not published to ClawHub. (`simplified-to-traditional` is published from its canonical `ai-thoughts` copy.)
- `ai-thoughts/.opencode/skills/` — publishes **every** `.opencode/skills/<slug>/SKILL.md` folder via a glob, so any new skill is published automatically and `publish-skills` self-publishes like any other. Untracked/uncommitted folders are not on ClawHub until they are committed and pushed.
- `ai-custom-skills/` — roots `openclaw/`, `hermes/`, `claude-code/` (each publishes its `*/SKILL.md` subfolders), plus the double-nested `claude-code/perplexity-downloader/perplexity-downloader` handled via a matrix `skill_path` entry. Folders without a `SKILL.md` (e.g. `openclaw/twitter-bookmarks-exporter`) are skipped automatically.

## Single-source rule — read before anything else

- **Only the `j3ffyang/*` copies of these repos publish.** The `negtivspace/*` copies keep the same workflow file (mirrors stay in sync) but are a no-op: every job is guarded with `github.repository_owner == 'j3ffyang'`.
- **Every skill update ships.** Whenever a `SKILL.md` is created or changed in any `negtivSpace` repo, commit it and push to **both** remotes (`j3ffyang` + `negtivspace`) in the same change — an unpushed skill is an unpublished one. The `j3ffyang` push runs `clawhub-skill-sync.yml`; afterwards, verify the new version is live via the skills API (`latestVersion`). Don't leave a skill edit uncommitted or only on one remote.
- Both copies are pushed on every change, so both repos run the workflow on push. Without the owner guard they would both publish to the *same* ClawHub account and race, producing `Version X already exists` collisions.
- Never create or run a manual publish path that could double-publish to ClawHub. If a skill edit is needed, edit it in the working repo, push to both remotes, and let the workflow publish once.
- `clawhub_token` (the `j3ffyang` ClawHub token) is set as a repo secret in all six repo copies; only the `j3ffyang` ones ever use it.

## Pipeline

- Workflow per repo: `clawhub-skill-sync.yml` with a `dry-run` job (pull requests only) and a `publish` job (pushes / `workflow_dispatch`).
- `history/` and `ai-custom-skills/` call the reusable workflow `openclaw/clawhub/.github/workflows/skill-publish.yml` pinned to tag `v0.23.3` (no `@v1` tag exists). Both their jobs need `permissions: {contents: read, id-token: write}`; callers fail with `startup_failure` (`id-token: none`) if the job-level permission is missing.
- `ai-thoughts/` instead runs the in-repo `scripts/clawhub_publish.py`, which invokes the pinned ClawHub CLI (`clawhub-source`, v0.23.3) directly with `bun` and a config file written from `secrets.clawhub_token`; its jobs need only `permissions: {contents: read}`.
- Publishing uses the caller repo's checkout; a new or changed skill is detected by fingerprint. Unchanged skills are skipped (`alreadySynced` / `unchanged`).

## Status & version semantics

- `unchanged` / `alreadySynced` — fingerprint matches ClawHub; nothing to do.
- New skill — first publish is version `1.0.0`.
- Changed skill — next patch version of the latest published version.
- `Error: Version X.Y.Z already exists. Increment the version number...` — the skill is already on ClawHub at that version (usually from a prior publish or a dual-remote race). Do not re-publish; the workflow will report it `alreadySynced` on the next run.
- **`pending-moderation`** — a slug on `scripts/clawhub_publish.py` → `KNOWN_PENDING`, failing with that exact "already exists" message. It means the upload is parked in ClawHub's moderation queue: the version row exists, so re-publishing collides, while `/api/v1/resolve` returns 404 (pending skills are not public), so the CLI derives `1.0.0` again on every run. Reported as pending, exit 0. Remove the entry once the skill is public — any other error on that slug still fails the run.
- `Invalid publish output: 'pending-publication'` — a false alarm. The publish actually succeeded; the upstream workflow's status map (v0.23.3) does not recognize the `pending-publication` status string and reports it as failed. Verify with the skills API before assuming a problem.

## Procedure

1. **Add or edit a skill**: create/update the `SKILL.md` (and sibling files) in the correct root of the correct repo. Respect that repo's conventions (e.g. `history/AGENTS.md` filename rules). Do not rename or convert skills; publish them as-is.
2. **Push to both remotes** of the submodule (`j3ffyang` and `negtivspace`). The push to `j3ffyang/*` triggers the publish; the `negtivspace/*` run is a no-op by design.
3. **Wait for the `j3ffyang/*` workflow run** to finish; check the publish summary for the affected slug.
4. **Manually trigger a publish** (e.g. after a failed run) via `workflow_dispatch` on the `j3ffyang/*` repo.
5. **Verify on ClawHub** (read-only, API): `curl -s -H "Authorization: Bearer $CLH_TOKEN" https://clawhub.ai/api/v1/skills/<slug>` — the `latestVersion` and `owner.handle` fields confirm what is live.

## Error Handling

- **`Version X.Y.Z already exists`** — confirm the skill already exists (skills API) and let the next run mark it `alreadySynced`; if the local content is genuinely newer, the workflow's next-patch bump handles it on its own.
- **`pending-publication` reported as failure** — treat as success; the wrapper script (v0.23.3) does not map this CLI status, so the run shows a red `X` even though the upload went through. **Verification has propagation lag**: the skills API may keep serving the *previous* `latestVersion` (and old `description`) for a few minutes, so a first check looks like a real miss. Re-poll `.../skills/<slug>` and `.../skills/<slug>/versions` for a few minutes; confirm `latestVersion` bumped *and* the new text is in `description` before concluding failure.
- **`startup_failure` / `id-token: none`** — the caller job is missing `permissions: {contents: read, id-token: write}`; add it.
- **Nested skill not found** — the matrix `skill_path` must point at the folder containing the `SKILL.md` (double-nested folders need the full path).
- **Slug collision** — `simplified-to-traditional` exists in both `history` and `ai-thoughts`. `ai-thoughts` publishes the canonical copy; `history`'s copy is local-only, kept out of ClawHub via `skill_path`. Never publish the same slug from two repos to the same owner.
- **Protected slug namespace** — ClawHub rejects any slug starting with `clawhub-` or ending with `-clawhub` (`Error: "... uses the protected "clawhub" slug namespace"`). This skill went `skill-publish` → `clawhub-publish` (rejected) → `publish-skills`. The original `skill-publish` slug is ambiguous across owners (other users have their own), so `publish-skills` is the canonical, unique slug; the legacy `@j3ffyang/skill-publish` stays on ClawHub (no delete-via-push).
- **Token missing** — publish fails without `clawhub_token`; it must be set as a secret on the `j3ffyang/*` repo.

## Verification

- All three workflow files carry `github.repository_owner == 'j3ffyang'` guards on both jobs.
- `actionlint` passes on every `clawhub-skill-sync.yml`.
- Every expected slug appears in the `j3ffyang/*` run's publish summary as `alreadySynced` or `published`.
- Skills API returns `owner.handle == 'j3ffyang'` and the expected `latestVersion` for every published skill.
