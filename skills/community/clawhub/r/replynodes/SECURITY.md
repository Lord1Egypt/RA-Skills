# Security reporting

Please report suspected vulnerabilities privately through [GitHub Security Advisories](https://github.com/replynodes/replynodes-agent-skills/security/advisories/new). Do not put secrets, ReplyNodes session tokens, social OAuth tokens, or personal data in a public issue or pull request. Include the affected commit/tag, reproduction steps, impact, and a safe contact method.

This repository contains documentation and deterministic validation scripts. It does not contain backend credentials, provider OAuth implementation, social tokens, or ReplyNodes session tokens. The installed host owns any expiring ReplyNodes session secret in its secure storage.

## Access and lifecycle boundaries

The skill can request the host's existing ReplyNodes workflow to start device authorization, read the authenticated session's channel capabilities, prepare content, and report receipts after explicit confirmation. It cannot grant permissions, choose another tenant, bypass browser approval, reconnect a provider, read arbitrary local files, expose tokens, or publish without the host's fresh confirmation.

Inspect a release from its explicit Git tag or commit and review `SKILL.md`, `README.md`, `PROVENANCE.md`, and the CI results before installing. Update by selecting a newer explicit tag. Revoke with `/replynodes disconnect` or `POST /public/v1/openclaw/session/revoke`; remove the host's stored session secret. Uninstall with the host skill manager. Uninstalling files alone does not revoke a server session.
