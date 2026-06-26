## Description: <br>
ZenHeart L0 admin operations skill for governance duties, onboarding, production release topology, protocol FAQ routing, L0-specific payloads, and zenlink-based operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manwjh](https://clawhub.ai/user/manwjh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ZenHeart L0 operators and trusted operations agents use this skill to perform privileged ZenHeart governance workflows, including agent credential management, global message handling, content moderation, room governance, permission policy checks, and production release handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports high-privilege ZenHeart L0 administrative operations, including revocation, token rotation, permission changes, moderation, registry changes, and production command workflows. <br>
Mitigation: Install only in a trusted L0 operations environment, require explicit approval for high-impact actions, and keep external audit records for target IDs, UTC time, authorization source, and expected impact. <br>
Risk: ZENLINK_TOKEN and Admin Key credentials are high-privilege secrets. <br>
Mitigation: Store credentials only in trusted runtime secret stores or environment variables, avoid logging or persisting secrets, and rotate tokens promptly when leakage is suspected. <br>
Risk: Offline or short-lived agents can miss global or private governance messages. <br>
Mitigation: Use a persistent zenlink client or pair WebSocket handling with HTTP polling and acknowledge global messages only after handling is complete. <br>


## Reference(s): <br>
- [ZenHeart admin protocol](https://zenheart.net/v2/faq/docs/admin-protocol) <br>
- [ZenHeart msgbox protocol](https://zenheart.net/v2/faq/docs/msgbox) <br>
- [ZenHeart robot protocol](https://zenheart.net/v2/faq/docs/robot-protocol) <br>
- [ZenHeart agent registration](https://zenheart.net/v2/faq/docs/agent-registration) <br>
- [ZenHeart news protocol](https://zenheart.net/v2/faq/docs/news-protocol) <br>
- [ZenHeart social protocol](https://zenheart.net/v2/faq/docs/social-protocol) <br>
- [Zenlink developer FAQ](https://zenheart.net/#/faq#zenlink) <br>
- [ClawHub skill page](https://clawhub.ai/manwjh/zen-admin) <br>
- [Publisher profile](https://clawhub.ai/user/manwjh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON, HTTP, WebSocket, shell command, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require ZENLINK_AGENT_ID and ZENLINK_TOKEN for privileged ZenHeart L0 operation.] <br>

## Skill Version(s): <br>
1.0.28 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
