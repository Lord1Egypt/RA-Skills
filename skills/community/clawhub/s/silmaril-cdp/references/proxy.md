# Proxy Workflow

Use these commands only when the task needs local response overrides or proxy-backed browsing.

## Commands

- `openurl-proxy`: open a page through the local mitmproxy workflow
- `proxy-override`: write or update a local override rule
- `proxy-switch`: switch an override between original and saved files

## Practical rules

- Prefer narrow URL regexes for override matching.
- Expect HTTPS interception to require a trusted mitmproxy certificate.
- Keep overrides local and temporary unless the user wants them persisted.
- Pass `--allow-mitm` for `openurl-proxy`, `proxy-override`, and `proxy-switch` unless `SILMARIL_ALLOW_MITM=1` is already set for a trusted local session.
- Keep `--listen-host` on loopback unless the user explicitly requests `--allow-nonlocal-bind`.
- Re-read the local docs before certificate or listener troubleshooting.

## Local documentation

Read `D:\silmairl cdp\tools\mitm\README.md` for setup details, certificate notes, and example commands.
