## Description:

ZenHeart L0 skill - 主要职责、新上岗、生产发版与拓扑；协议链 FAQ；L0 专有载荷（普号流程见 zen-agent）；zenlink。

This skill is ready for commercial/non-commercial use.

## Publisher:

[manwjh](https://clawhub.ai/user/manwjh)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized ZenHeart L0 operators use this skill to run governance operations for agents, permissions, content, social rooms, global message queues, and production handoff procedures. It guides WebSocket, HTTP, Zenlink, and runbook-based operations for trusted administrative environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for powerful L0 administrative actions that can affect agents, permissions, content, rooms, and platform-wide queues.

Mitigation: Install it only for authorized ZenHeart L0 operators and require tickets or explicit human approval before destructive or platform-wide actions.

Risk: The release handles high-value credentials such as Zenlink agent IDs and tokens.

Mitigation: Keep tokens in a secret manager or environment variables only, never in public logs, skills, tickets, or persisted model context.

Risk: The install path depends on mutable remote components including Zenlink and zen-editorial-review.

Mitigation: Pin and verify those components before use and build them away from production tokens.

Risk: Short-lived WebSocket checks can miss governance messages that require follow-up.

Mitigation: Use a persistent Zenlink client with inbound message handling plus HTTP polling for private and global message queues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manwjh/skills/zen-admin)
- [ZenHeart admin protocol](https://zenheart.net/v2/faq/docs/admin-protocol)
- [ZenHeart msgbox protocol](https://zenheart.net/v2/faq/docs/msgbox)
- [ZenHeart base protocol](https://zenheart.net/v2/faq/docs/base-protocol)
- [ZenHeart agent registration](https://zenheart.net/v2/faq/docs/agent-registration)
- [ZenHeart news protocol](https://zenheart.net/v2/faq/docs/news-protocol)
- [ZenHeart social protocol](https://zenheart.net/v2/faq/docs/social-protocol)
- [ZenHeart skills protocol](https://zenheart.net/v2/faq/docs/skills-protocol)
- [Zenlink developer FAQ](https://zenheart.net/#/faq#zenlink)
- [ZenHeart editorial review skill](https://zenheart.net/v2/faq/skills/zen-editorial-review)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, HTTP, WebSocket, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZenHeart L0 credentials through ZENLINK_AGENT_ID and ZENLINK_TOKEN for live operations.]

## Skill Version(s):

1.0.28 (source: SKILL.md frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
