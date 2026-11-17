# Acceptance

Walk every line. A checked template without an evidence-backed consumer adaptation is incomplete.

## Before deploy

- `node --import tsx evals/contract.mjs` passes against the adapted graph: a `claudeCode` harness on
  an Anthropic connector, one MCP client on `https://ora.ai/api/mcp` with no credential and its
  write tools and `run_checks` disabled, `website_audits` the only model and writable, no connector
  action but Slack `postMessage` with `channelId` locked, one cron, and `AUDIT_DOMAIN`,
  `COMPETITOR_DOMAINS` (at most three) and `WEBSITE_ROOT` in the repository env.
- `cargo-ai project check` prints `agent:website_auditor bound to <your repo>#<branch>` with no
  trailing subdirectory.
- `cargo-ai connection connector list` shows authorized GitHub, Slack and Anthropic connectors.
- `WEBSITE_ROOT` exists on the default branch and is the folder the site deploys from.
- `curl -s https://ora.ai/api/score/<domain>` answers for every configured domain, or the domain has
  never been scanned and the first run will scan it.
- `curl -sL -o /dev/null -w '%{http_code} %{url_effective}' https://<bare domain of AUDIT_DOMAIN>`
  ends on 200 at a URL whose host is exactly `AUDIT_DOMAIN`, `www.` included: Ora scans the apex,
  not `www.`, and a 200 that stays on the apex of a `www.` site is a forward or challenge page.

## First runs

Keep the Slack permalink, the pull request and the model rows as evidence.

- **Score.** One `website_audits` row per configured domain for this ISO week, with score, grade,
  `scanned_at`, `reached` and sorted `failing_checks`. The transcript shows `scan_domain` once per domain and
  never with `force`.
- **Fix.** One pull request on `website-auditing-<week>`, every changed file under `WEBSITE_ROOT`,
  every fix naming a failing check in our result: topFixes first in Ora's order, then the others by
  points lost, with Ora's estimate called an
  estimate. The site's build passes on the branch. Our row carries `fix_pr_url`.
- **Post.** One digest in the locked channel in the `references/digest.md` shape, the first week
  marked as the baseline. Our row carries `digest_ts`.
- **Re-run.** Once a SQL query on `website_audits` returns this week's rows (a model query can lag a
  write by several minutes), sending the trigger text again the same week writes no row, calls no `scan_domain`,
  opens no pull request and posts nothing.
- **Measure.** After the pull request is merged and deployed, the next week's row no longer lists
  the fixed checks in `failing_checks`, and the digest names them under Fixed.

## Isolation

- This is one root skill. Its supporting Markdown lives under `references/`, and no nested
  `SKILL.md` exists.
- No import leaves the folder.
- The run transcripts show no Ora feedback call, no `run_checks`, no merge, no push to the default
  branch, no change outside `WEBSITE_ROOT`, and no Slack call other than `postMessage`.
