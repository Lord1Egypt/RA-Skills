---
name: sentry-integration
description: Sentry error tracking — list, triage, and resolve issues; manage releases and source maps via CLI and REST API.
metadata: {"openclaw":{"requires":{"bins":["sentry-cli"]},"install":[{"id":"npm","kind":"npm","package":"@sentry/cli","global":true,"bins":["sentry-cli"],"label":"Install sentry-cli (npm)"},{"id":"pip","kind":"pip","package":"sentry-cli","bins":["sentry-cli"],"label":"Install sentry-cli (pip)"}]}}
---

# Sentry Integration

Use `sentry-cli` and the Sentry REST API to monitor errors, triage issues, manage releases, and upload source maps.

## Setup

```bash
# Install
npm i -g @sentry/cli
# — or —
pip install sentry-cli

# Auth (set once, used by all commands)
export SENTRY_AUTH_TOKEN="sntrys_..."   # Settings → Auth Tokens → Create
export SENTRY_ORG="my-org"
export SENTRY_PROJECT="my-project"

# Verify
sentry-cli info
```

Generate a token at **sentry.io → Settings → Auth Tokens** with scopes: `project:read`, `project:releases`, `org:read`, `event:read`.

## CLI Commands

### Releases

```bash
# Create a release (version from git)
sentry-cli releases new "$(sentry-cli releases propose-version)"

# Set commits (auto-detect from git)
sentry-cli releases set-commits "$VERSION" --auto

# Finalize (marks release as deployed)
sentry-cli releases finalize "$VERSION"

# Create + finalize in one step
sentry-cli releases new "$VERSION" --finalize

# Record a deploy
sentry-cli deploys new -r "$VERSION" -e production

# List releases
sentry-cli releases list
```

### Source Maps

```bash
# Upload source maps for a release
sentry-cli sourcemaps upload ./dist --release "$VERSION"

# With URL prefix (match hosted paths)
sentry-cli sourcemaps upload ./dist --release "$VERSION" --url-prefix "~/static/js"

# Validate before upload
sentry-cli sourcemaps explain --release "$VERSION" --org "$SENTRY_ORG" --project "$SENTRY_PROJECT"
```

### Send Test Event

```bash
sentry-cli send-event -m "Test event from CLI"
sentry-cli send-event -m "Deploy check" -t environment:production -t release:1.0.0
```

### Monitor (Cron Monitoring)

```bash
# Wrap a command — Sentry tracks if it runs and succeeds
sentry-cli monitors run <monitor-slug> -- <command>
sentry-cli monitors run backup-job -- ./run-backup.sh
```

## REST API (for queries the CLI doesn't cover)

Base URL: `https://sentry.io/api/0`
Auth header: `Authorization: Bearer $SENTRY_AUTH_TOKEN`

### List Issues

```bash
# All unresolved issues for a project
curl -s "https://sentry.io/api/0/projects/$SENTRY_ORG/$SENTRY_PROJECT/issues/?query=is:unresolved" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | jq '.[].title'

# Organization-wide issues (sorted by last seen)
curl -s "https://sentry.io/api/0/organizations/$SENTRY_ORG/issues/?query=is:unresolved&sort=date" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | jq '.[] | {id, title, count, lastSeen}'

# Filter by level, time, assignment
curl -s "https://sentry.io/api/0/organizations/$SENTRY_ORG/issues/?query=is:unresolved+level:error+lastSeen:>2d" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

### Get Issue Details + Events

```bash
# Issue details
curl -s "https://sentry.io/api/0/issues/$ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | jq '{title, status, count, firstSeen, lastSeen}'

# Latest events for an issue (stack traces, breadcrumbs)
curl -s "https://sentry.io/api/0/issues/$ISSUE_ID/events/?full=true" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | jq '.[0].entries'
```

### Resolve / Ignore Issues

```bash
# Resolve
curl -s "https://sentry.io/api/0/issues/$ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -X PUT -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'

# Resolve in next release
curl -s "https://sentry.io/api/0/issues/$ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -X PUT -H "Content-Type: application/json" \
  -d '{"status": "resolvedInNextRelease"}'

# Ignore for 24 hours
curl -s "https://sentry.io/api/0/issues/$ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -X PUT -H "Content-Type: application/json" \
  -d '{"status": "ignored", "statusDetails": {"ignoreDuration": 1440}}'

# Assign to team member
curl -s "https://sentry.io/api/0/issues/$ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -X PUT -H "Content-Type: application/json" \
  -d '{"assignedTo": "user@example.com"}'
```

### Bulk Resolve

```bash
# Resolve multiple issues at once
curl -s "https://sentry.io/api/0/projects/$SENTRY_ORG/$SENTRY_PROJECT/issues/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -X PUT -H "Content-Type: application/json" \
  -d '{"id": ["123","456","789"], "status": "resolved"}'
```

## Triage Workflow

When asked to check or triage Sentry errors:

1. List unresolved issues sorted by frequency: `query=is:unresolved&sort=freq`
2. For the top issues, fetch latest event with full stack trace
3. Analyze the stack trace — identify the failing function, file, and line
4. Check if the error is in code the agent can access (read the file, suggest a fix)
5. Classify: **critical** (data loss, crash), **high** (user-facing errors), **medium** (degraded experience), **low** (cosmetic, logs)
6. Resolve issues that have confirmed fixes deployed; ignore transient errors

## Notes

- Self-hosted Sentry: replace `sentry.io` with your instance URL
- Rate limits: 40 requests/min for free tier, respect `Retry-After` headers
- The CLI respects `.sentryclirc` files for project-level config
- Use `--log-level debug` on any CLI command for troubleshooting
