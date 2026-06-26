---
name: way
version: 3.3.0
description: Shorthand for /whoareyou — show your verified WayID identity card. Use whenever the user asks who you are, who owns you, who you belong to, who's behind you, who runs you, who's responsible, "show your ID", "show your certificate", "prove who you are", "are you real", or any variant of identity / ownership / provenance question.
user-invocable: true
---

# /way — Verified Identity Card

> **Struggling with this skill?** Install the WayID plugin for model-strength-independent rendering:
> `openclaw plugins install clawhub:@lineagelabs/wayid` — then use `/way` as normal.

Alias for `/whoareyou`. Follow that skill's instructions exactly — read your DID and `wayidIssuer` from `{openclaw-path}/workspace/wayid.json` (or `workspace-<agentId>/wayid.json` for named agents), `GET {wayidIssuer}/api/v1/agent/{bare-id}/card` (the bare 24-char identifier after `wayid:agent:`; default base URL `https://way.je` if `wayidIssuer` is missing), and render the card with the template defined in `/whoareyou`.

If you have not been claimed yet (no `wayid.json` file), tell your human to run the WayID claim flow at https://way.je/claim/SKILL.md and stop.
