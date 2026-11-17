## Description:

QQ bot and open-platform development guide covering official Bot API route selection, authentication, WebSocket gateway events, message formats, Mini Program basics, OAuth, and the community OneBot ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to plan and implement QQ integrations, especially to choose between the official Bot API and community OneBot routes, configure bot authentication and event handling, and sketch Mini Program or OAuth flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample credential and event-handling snippets could expose AppSecret values, access tokens, or full event payloads if copied directly into production logging or client-side code.

Mitigation: Keep AppSecret values server-side, redact logs, avoid printing full event payloads, protect access tokens, and use least-privilege intents.

Risk: Skeleton API snippets may not cover all current QQ platform requirements, review states, OAuth parameters, or rate-limit behavior.

Mitigation: Validate permissions, OAuth parameters, endpoint behavior, and rate limits against current official QQ documentation before production use.

Risk: Community OneBot routes can carry account enforcement and compliance risk for external or commercial services.

Mitigation: Use the official Bot API for external or commercial products, and limit community implementations to personal or internal use where that risk is acceptable.

## Reference(s):

- [QQ Open Platform](https://q.qq.com)
- [QQ Bot API Documentation](https://bot.q.qq.com/wiki/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with Python and JavaScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes route-selection advice, API skeletons, configuration notes, and security hardening guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
