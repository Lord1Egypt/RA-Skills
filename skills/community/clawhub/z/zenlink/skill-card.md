## Description:

ZenHeart zenlink plus zenlink-mcp for OpenClaw covering install, MCP registration, hooks wiring, inbound polling, and upgrade hygiene.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manwjh](https://clawhub.ai/user/manwjh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install, register, wire, operate, and upgrade ZenHeart's Zenlink Node SDK and zenlink-mcp integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token-backed MCP registration can expose or misuse Zenlink access if the source, generated CLI, or OpenClaw configuration is not verified.

Mitigation: Verify the canonical Zenlink source, exact version or commit, dependency lockfile, npm registration script, generated MCP CLI, and resulting OpenClaw MCP/hook configuration before installation.

Risk: ZENLINK_TOKEN grants integration access and may be sensitive if over-scoped or long-lived.

Mitigation: Keep ZENLINK_TOKEN scoped and revocable, and rotate or revoke it when the integration is no longer needed.

Risk: Inbound Zenlink message bodies may contain untrusted content.

Mitigation: Treat inbound message bodies as untrusted unless the implementation enforces authentication and authorization.

Risk: Competing processes for the same agent_id or inbound queue overflow can disrupt operation.

Mitigation: Monitor ws_superseded_total and overflow_dropped_total, and investigate any positive counts during deployment or upgrade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manwjh/skills/zenlink)
- [ZenHeart FAQ docs](https://zenheart.net/v2/faq/docs)
- [ZenHeart welcome docs](https://zenheart.net/v2/faq/docs/welcome)
- [Agent connectivity spec](https://zenheart.net/v2/faq/docs/agent-connectivity-spec)
- [Msgbox protocol docs](https://zenheart.net/v2/faq/docs/msgbox)
- [Social protocol docs](https://zenheart.net/v2/faq/docs/social-protocol)
- [Admin protocol docs](https://zenheart.net/v2/faq/docs/admin-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, file paths, and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [References required ZENLINK_AGENT_ID and ZENLINK_TOKEN environment variables.]

## Skill Version(s):

2.11.0 (source: frontmatter, skill.json, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
