---
name: scan-now-tools
description: Use Scan.now when the user wants a passive security assessment of a website they are authorized to test, or wants to inspect a suspicious public link for phishing signals.
---

# Scan.now tools

Connect to the public Streamable HTTP MCP endpoint at `https://mcp.scan.now`.
No API key, account, or environment variable is required. Do not ask the user to obtain
a Scan.now credential, and do not invent REST endpoints; use the MCP tools exposed by
that server.

Use `scan_website_security` only after the user states that they own the target website
or have explicit permission to assess it. If that authorization is absent, ask for it
before calling the tool. Set `authorized` to true only after that confirmation.

Call it with:

- `url`: the public HTTP or HTTPS website to assess.
- `authorized`: `true` only after the user's confirmation.
- `scope`: optional; one of `full`, `tls`, `headers`, `email`, or `js`.

Choose the narrowest useful scope:

- `full` for a broad passive assessment.
- `tls` for certificates, protocol support, and HTTPS behavior.
- `headers` for HTTP security headers, cookies, CORS, and related page controls.
- `email` for SPF, DKIM, DMARC, DNSSEC, CAA, and email-domain posture.
- `js` for public JavaScript inventory and known vulnerable library versions.

Use `check_phishing_link` when the user wants to understand whether a public link looks
deceptive or where it redirects. Explain that a low score is not a guarantee: a new or
unreported phishing page may not yet appear on blocklists.

Call it with `url` and, optionally, `follow_redirects` (default `true`). This tool does
not require the website-ownership confirmation because it inspects a link rather than
assessing a user's website.

These tools are passive and read-only. They do not exploit findings, bypass access
controls, guess credentials, scan private networks, or prove that a target is secure.
Do not help use the results for unauthorized access. Prefer the finding's
`reference_url` when the user asks how to fix an issue.

Use `https://scan.now/methodology` when the user asks how the checks work and
`https://mcp.scan.now/privacy-policy` for MCP-specific data handling.
