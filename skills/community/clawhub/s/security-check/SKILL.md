---
name: security-check
description: Run a free, read-only security check of the user's own web app or API through Rheono; the report arrives by email. Use when the user asks to check, scan, audit, or pentest their own site, app, or API.
homepage: https://rheono.dev
---

# Security Check

Sends the user's own web app to Rheono for a free, read-only security check.
A researcher confirms the request, probes the live surface, and the report is
emailed to the address the user gives. No local scanning, no API keys, no
account needed.

## Steps

1. **Consent gate (non-negotiable).** The check probes a live URL. Only
   continue if the user confirms they own the target or are authorized to
   test it. If unsure, ask: "I'm going to send `example.com` to Rheono for a
   free security check — confirm you own this site or are authorized to test
   it."

2. **Collect inputs.** You need:
   - `domain`: the bare root domain (e.g. `example.com` — strip scheme, path,
     subdomain specifics down to the registrable root).
   - `email`: where the report should be sent. Ask if not given.

3. **Submit the check.**

   ```bash
   curl -sS -X POST https://rheono.dev/api/check-request \
     -H 'content-type: application/json' \
     -d '{"domain": "example.com", "email": "you@example.com"}'
   ```

4. **Report back.**
   - `{"ok":true,...}` — tell the user the check was submitted and the report
     will arrive at their email. Do not promise a timeframe.
   - `400 invalid domain` / `invalid email` — fix the input and retry once.
   - `502 upstream` — the check service is unreachable; say so and stop.

## Boundaries

- Read-only probes only; Rheono runs them, this skill only submits the
  request. Never probe a target locally or via any other tool.
- Never submit a domain the user has not confirmed ownership/authorization
  for.
- One check per domain per conversation unless the user asks again.
