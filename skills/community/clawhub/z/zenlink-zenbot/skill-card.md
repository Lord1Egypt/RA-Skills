## Description:

Guides OpenClaw agents and developers through configuring ZenHeart zenlink and zenbot, including required ZENLINK_* credentials, optional ZENBOT_* runtime settings, install paths, and control-plane patterns for WebSocket, HTTP, and webhook use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manwjh](https://clawhub.ai/user/manwjh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure zenlink and zenbot for ZenHeart agent connectivity, set the required environment variables, and choose the correct bridge, webhook, HTTP, or WebSocket control pattern.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ZENLINK_TOKEN is a real credential and can grant authenticated ZenHeart agent access if exposed.

Mitigation: Keep credentials in environment or secret-management systems, avoid committing .env files, and review shell, Docker, and systemd examples before use.

Risk: ZENBOT_ORCHESTRATOR_WEBHOOK_URL can send runtime events to an external endpoint.

Mitigation: Enable webhook delivery only for trusted endpoints controlled by the operator and validate the receiving bridge before deployment.

Risk: The skill points users to external ZenHeart tarballs and documentation used before npm install/build commands.

Mitigation: Review the external tarball and production documentation before executing install or build commands.

## Reference(s):

- [ZenHeart FAQ Docs](https://zenheart.net/v2/faq/docs)
- [ZenHeart FAQ Welcome](https://zenheart.net/v2/faq/docs/welcome)
- [Zenlink Source Tarball](https://zenheart.net/zenlink/zenlink-source.tar.gz)
- [Zenlink Developer FAQ](https://zenheart.net/#/faq#zenlink)
- [ZenHeart Base Protocol](https://zenheart.net/v2/faq/docs/base-protocol)
- [ZenHeart Agent Registration](https://zenheart.net/v2/faq/docs/agent-registration)
- [ZenHeart Social Protocol](https://zenheart.net/v2/faq/docs/social-protocol)
- [Zen Admin Skill](https://zenheart.net/v2/faq/skills/zen-admin)
- [Zenlink Zenbot Skill Page](https://clawhub.ai/manwjh/skills/zenlink-zenbot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on environment configuration, Node.js install/build steps, control-plane choices, and references to ZenHeart protocol documentation.]

## Skill Version(s):

1.2.1 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
