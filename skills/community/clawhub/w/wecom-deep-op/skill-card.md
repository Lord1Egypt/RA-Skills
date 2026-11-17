## Description:

Wecom Deep Op is an OpenClaw skill that wraps WeCom MCP services for documents, schedules, meetings, todos, and contacts through a unified interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingbox](https://clawhub.ai/user/bingbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise workspace operators use this skill to let an agent manage WeCom documents, calendar events, meetings, todos, and visible contacts after authorized WeCom bot endpoints are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive business data can be sent to any endpoint configured through WECOM_*_BASE_URL.

Mitigation: Restrict WECOM_*_BASE_URL values to trusted HTTPS WeCom endpoints or an approved internal proxy before use.

Risk: Full operation payloads can be logged when debug logging is enabled.

Mitigation: Do not enable DEBUG_LEVEL=debug when handling real business data, and review log retention and access controls.

Risk: The skill can modify or delete WeCom data within the bot's granted permissions.

Mitigation: Use a least-privilege WeCom bot and periodically audit bot permissions in the WeCom administration console.

Risk: uaKeys grant access to configured WeCom MCP services if exposed.

Mitigation: Keep uaKeys out of source control and manage them through environment variables, encrypted configuration, or an approved secret store.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bingbox/skills/wecom-deep-op)
- [WeCom Administration Console](https://work.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, cancel, delete, and read WeCom resources within the configured bot permissions.]

## Skill Version(s):

2.0.2 (source: server release, frontmatter, skill.yml, changelog released 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
