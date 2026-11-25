---
name: vibe-code-security-guard
description: Security exposure scan for apps built with AI coding tools (Lovable, Bolt, v0, Replit, Cursor, Claude Code, Codex). Checks a deployed app's URL for leaked API keys (OpenAI, Anthropic, Gemini and 60+ other providers), exposed source maps, publicly readable Supabase tables, and missing security headers, and returns an A–F grade with fix prompts. Use when the user shares a deployed app URL and asks whether it is safe, wants a pre-launch check, or wants a re-scan after changes. Runs the magnova/vibe-code-security-scanner Actor through the Apify plugin for OpenClaw; each site scanned costs $0.05 on the user's own Apify account.
version: 1.0.0
homepage: https://apify.com/magnova/vibe-code-security-scanner
metadata:
  openclaw:
    requires:
      env:
        - APIFY_API_TOKEN
---

# Vibe Code Security Guard

AI app builders ship fast, and their most common failures are
silent: a live API key sitting in the page's JavaScript, a
Supabase table anyone can read, source maps that hand over the
original code. This skill runs a read-only exposure scan of a
deployed app's public surface and reports what a stranger can
already see — with a grade and a fix prompt for each problem.

## Prerequisites

1. The Apify plugin for OpenClaw is installed and allowlisted:
   `openclaw plugins install @apify/apify-openclaw-plugin`
2. `APIFY_API_TOKEN` holds the user's own Apify API token. All
   runs bill to that account.
3. You call Actors through the plugin's `apify` tool: `start`
   (returns a runId), then `collect` (returns the results).

If the plugin or token is missing, stop and tell the user
exactly what to install or set. Do not probe the site yourself
with ad-hoc requests in place of the scan.

**Cost, stated plainly:** $0.05 per site per scan, charged to
the user's Apify account. Tell the user the cost before the
first scan of a new site.

## Permission rule — read this first

Only scan sites the user owns or has written permission to
test. If the user gives you a URL and it is not clearly their
own app, ask one question — "Is this your site, or do you have
the owner's permission to test it?" — and wait for the answer.
The scanner's deeper checks (public-read tests on Supabase
tables) run only in owner mode, which requires the user's
explicit confirmation of ownership for that site.

## Scan procedure

1. Confirm the URL(s) and permission (above). One scan can take
   several URLs in a single run.
2. Start the Actor with the `apify` tool:
   - actorId: `magnova~vibe-code-security-scanner`
   - input: `urls`: the URL list. Add `iOwnThisSite: true`
     only when the user has confirmed they own the site(s) —
     this enables the read-only Supabase table checks. Leave
     `checkSourceMaps` at its default unless the user asks to
     skip it.
3. Collect the results and report per site (format below).

## Report format

```
🛡️ <site> — Grade: <A–F>

Critical / high findings first, in plain language:
- <what was found> — <where: file, table, or header>
  Fix: <the fix prompt or instruction the scan returned>

Then medium/low findings the same way. Close with the single
most important next step.
```

Rules for reporting:

- **Never print a full secret.** If a finding includes a leaked
  key or token value, name the provider and where it was found
  and mask the value (first 4 characters at most). Tell the
  user to treat that key as compromised and rotate it — deleting
  it from the site later does not un-leak it.
- Report only what the scan returned. Do not add vulnerabilities
  it did not find, and do not soften findings it did.
- If a site comes back clean, say what was checked and that
  nothing was found — a clean scan is a point-in-time exposure
  check, not a guarantee of safety.

## Re-scans and monitoring

- After the user fixes findings, offer a re-scan of the same
  URL to verify the grade improved.
- For ongoing watching of the user's own apps, offer a weekly
  scheduled re-scan. If the user picks (or creates) a key-value
  store in their Apify account for scan history and gives you
  its ID, pass it as `historyStore` with `onlyNewFindings: true`
  so weekly reports list only what changed.
- Keep a short local note of each scan (date, URL, grade) in
  `state/vibe-code-security-guard.json` so you can answer
  "did that site improve?" without re-scanning.

## Notes

- This is an automated check of a site's public surface —
  leaked secrets in shipped code, exposed source maps, public
  database reads, missing headers. It is not a penetration
  test and does not review server-side code the site does not
  expose.
- Owner mode's table checks are read-only: they test whether
  rows can be read with the site's own public key, and never
  write, modify, or delete anything.
