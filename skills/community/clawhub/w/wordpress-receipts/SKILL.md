---
name: wordpress-receipts
description: "Publish WordPress posts with API and public URL receipts."
user-invocable: true
metadata:
  version: "0.1.2"
  license: "MIT"
  homepage: "https://github.com/LeoStehlik/wordpress-receipts"
  openclaw:
    requires:
      bins: ["node"]
---
# WordPress Receipts

Use this skill when publishing a WordPress post from an OpenClaw task, cron job, or agent workflow where success must mean a real public artifact exists.

This is a skill, not a plugin. It uses the WordPress REST API and deterministic helper scripts, so it stays portable and auditable.

## When To Use

- The user asks to publish a WordPress article, reflection, update, or draft.
- A scheduled job must publish to WordPress and prove completion.
- A previous run produced a draft, status message, or cron success without a public URL receipt.
- You need a post-run verifier that checks WordPress API state and the public page.

## Safety Rules

- Never treat cron success, model output, or a draft as publication proof.
- Publication is complete only when the WordPress REST API returns a post ID and the public URL returns HTTP 200.
- Do not print credentials, application passwords, tokens, cookies, or authorization headers.
- Keep secrets in environment variables or an env file outside the skill folder.
- Parse env files explicitly; do not rely on shell-sourcing when application passwords may contain spaces.
- Avoid duplicate posts: check the latest published posts before creating a new one.
- Log the receipt: title, URL, WordPress post ID, status, and public HTTP status.

## Expected Env

The helper scripts accept an env file passed with `--env-file`. The public helpers deliberately avoid ambient environment reads so static scanners do not see hidden credential access combined with network calls:

```text
WORDPRESS_API_BASE=https://example.com/wp-json/wp/v2
WORDPRESS_USERNAME=publisher-user
WORDPRESS_APPLICATION_PASSWORD=application password may contain spaces
WORDPRESS_AUTHOR_ID=123
WORDPRESS_DEFAULT_CATEGORY_ID=1
```

Only the first three are required. Author and category can also be supplied by flags.

## Publish Workflow

1. Load the draft from a Markdown file or explicit title/content fields.
2. Read WordPress env values with explicit parsing.
3. Query recent published posts to avoid duplicates.
4. POST JSON to the WordPress REST API.
5. Verify the returned API object and public URL.
6. Append or report a receipt containing title, URL, post ID, API status, and public HTTP status.

Recommended command:

```bash
node scripts/wp-publish-receipt.mjs \
  --env-file .env.wordpress \
  --title-file draft-title.txt \
  --content-file draft.md \
  --author 123 \
  --category 1
```

For one-off verification:

```bash
node scripts/wp-verify-receipt.mjs --env-file .env.wordpress --date 2026-07-01
node scripts/wp-verify-receipt.mjs --env-file .env.wordpress --url https://example.com/post-slug/
node scripts/wp-verify-receipt.mjs --env-file .env.wordpress --id 456
```

## Cron Guard Pattern

For recurring publishing jobs, add a second scheduled proof check after the publishing window. The proof check should run `wp-verify-receipt.mjs` for the expected local date and alert on failure.

Good success signal:

```json
{
  "ok": true,
  "id": 456,
  "status": "publish",
  "link": "https://example.com/post-slug/",
  "publicStatus": 200
}
```

Bad success signal:

```text
Cron run status: ok
```

That only proves the scheduler finished. It does not prove publication.

## Scheduler Environment Proof

Receipt checks only help if the scheduler can start the runtime. For recurring jobs, prove the publisher and verifier from the same scheduler environment that will run them unattended.

Rules:

- Set a known `PATH` in the scheduler definition, or call absolute paths to `node`, `openclaw`, and any wrapper scripts.
- Do not rely on an interactive shell profile for Homebrew, NVM, asdf, pnpm, or OpenClaw paths.
- Test the verifier under a stripped environment before trusting the schedule.
- After loading or changing the scheduled job, kick or run the scheduled verifier once and confirm exit `0`.
- Treat a watchdog that uses the same unproved runtime as unproved too.

Example stripped-env smoke:

```bash
env -i HOME="$HOME" USER="$USER" PATH="/usr/bin:/bin:/usr/sbin:/sbin" \
  /opt/homebrew/bin/node scripts/wp-verify-receipt.mjs \
  --env-file .env.wordpress \
  --date 2026-07-01
```

Example launchd environment block:

```xml
<key>EnvironmentVariables</key>
<dict>
  <key>PATH</key>
  <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
</dict>
```

For launchd jobs, verify with `launchctl print` that the loaded job has the expected environment, then use `launchctl kickstart` or another scheduler-native run path to prove the verifier exits successfully.

## Output Contract

When reporting back to the user, include:

- title
- URL
- WordPress post ID
- API status
- public HTTP status
- whether a duplicate was skipped

Keep the report short. If publishing failed, state whether a draft exists and what exact proof is missing.
