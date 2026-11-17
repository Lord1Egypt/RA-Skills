# Publishing to SkillHub (stage 5b)

> Loaded by stage 5 of the pipeline. Kept out of the skill file on purpose — the skill file stays a routing surface; operational detail lives here.

SkillHub is the third platform in the unified-version rule. **There is no maintained CLI for it.** A helper named `skills_store_cli.py` used to exist and no longer ships anywhere on a typical machine — do not spend time searching for it. Build the request directly.

---

## Endpoint

```
POST https://api.skillhub.cn/api/v1/community/skills/publish
```

## Auth

Bearer token from `~/.skillhub/credentials.json` → **`user.token`**.
The file has no top-level `token` key; reading `d["token"]` yields null and produces a misleading 401/403.

## Request — multipart/form-data

**Part 1** — field `payload`, `Content-Type: application/json`:

```json
{
  "slug": "my-skill",
  "displayName": "My Skill",
  "version": "1.2.3",
  "description": "one-line English summary",
  "changelog": "what changed",
  "category": "",
  "subCategories": [],
  "source": "community",
  "tags": ["tag-a", "tag-b"]
}
```

**Parts 2..n** — one per file:

- field name **must be `files`** (`file` and `files[]` are wrong)
- `filename` = repo-relative path with forward slashes, e.g. `references/guardian-patterns.md`
- `Content-Type: text/markdown`

## Response

| Code | Meaning |
|---|---|
| **201** | accepted — body carries `ok:true`, `version`, `fileCount`, `skillId`, `fingerprint`, and `pending` review/scan statuses |
| 400 | frontmatter or payload validation failed |
| 409 | slug tombstoned, or version already exists → bump and retry. **Never delete a `source=community` skill to force a republish** — the slug becomes an unrecoverable tombstone |
| 429 | consecutive publishes rate-limited → wait ~90s (a single 90 s backoff has been the reliable fix in practice; 20 s retries can fail repeatedly) |
| 503 | transient → wait ~20s and retry once |

## Constraints

- **No read API.** Every `GET` under `/api/v1/community/skills/*` returns 405, including `/mine`, `/list`, and `/rankings`, with or without a Bearer token. You cannot verify remotely whether a skill is already on SkillHub. Use side evidence instead: `clawhub inspect <slug> --versions` plus the existence of the GitHub mirror repo.
- **Stricter frontmatter than ClawHub.** Required: leading `---` delimiter, `slug`, `displayName`, `version`. Files retrieved via `clawhub install` often lose the leading `---` in ClawHub storage — backfill it before publishing.
- **`LICENSE` is rejected.** Publish from a staging copy that excludes it.
- **Version must match ClawHub and GitHub exactly.** No platform-local version numbers.

## Ordering inside stage 5

1. ClawHub publish (async — settle with `inspect --json` → `latestVersion.version`)
2. **SkillHub publish (this file)**
3. GitHub sync from the staging dir (never from an install dir)
4. Install-check against ClawHub

Skipping step 2 is the most common way the three-platform version rule breaks: the skill lands on two platforms, the version registry drifts apart, and the next publish has to guess which number is authoritative.
