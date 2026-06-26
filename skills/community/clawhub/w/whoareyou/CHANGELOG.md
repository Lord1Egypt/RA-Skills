# Changelog

## 3.3.0 — 2026-06-08

Add plugin-alternative note at the top of the skill for operators whose model
struggles with string-munging or exact template formatting. The WayID plugin
(`@lineagelabs/wayid`) pre-renders the identity card in code and is
model-strength-independent. The skill itself is unchanged and remains the
fallback for agents that cannot install plugins.

## 3.2.0 — 2026-05-08

Recommend the bare 24-char identifier in the URL (issue
[#330](https://github.com/LineageLabs/openclaw-prototype/issues/330)) — the
route already implies the type, so callers no longer need to URL-encode
`wayid:agent:` as `wayid%3Aagent%3A`. The full DID form keeps working for
back-compat; only the example URL changes.

## 3.1.0 — 2026-05-06

Read `wayidIssuer` from `wayid.json` and use it as the API base URL (issue
[#228](https://github.com/LineageLabs/openclaw-prototype/issues/228)). Fixes
404 for agents claimed on `staging.way.je` or any non-prod WayID origin.
Falls back to `https://way.je` for older `wayid.json` files that predate the
field.

## 3.0.0 — 2026-05-01

DID-keyed lookup (issue
[#211](https://github.com/LineageLabs/openclaw-prototype/issues/211)). Reads
`wayidDid` from `{openclaw-path}/workspace/wayid.json` (default) or
`workspace-<agentId>/wayid.json` (named agents); calls
`GET /api/v1/agent/{did}/card`. No longer touches credentials. Replaces the
previous pubkey-keyed lookup.
