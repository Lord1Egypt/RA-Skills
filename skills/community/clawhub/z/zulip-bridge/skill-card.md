## Description: <br>
OpenClaw Zulip Bridge enables OpenClaw agents to send Zulip messages, monitor streams, and perform configured user or stream administration actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niyazmft](https://clawhub.ai/user/niyazmft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an OpenClaw agent to Zulip for stream and private-message workflows, monitored message intake, reaction feedback, and optional administrative operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge requires sensitive Zulip bot credentials and can monitor or post messages as that bot. <br>
Mitigation: Use a least-privilege bot account, store credentials securely, and review who can trigger the bot before enabling broad stream or DM access. <br>
Risk: The bridge exposes high-impact delete and administration actions when administrative capability is enabled. <br>
Mitigation: Keep enableAdminActions disabled unless explicitly needed, avoid admin credentials for routine use, and manually review any deployment that enables administrative actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niyazmft/zulip-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Zulip messaging targets, setup steps, and operational guidance for OpenClaw channel use.] <br>

## Skill Version(s): <br>
2026.4.13 (source: frontmatter, package.json, openclaw.plugin.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
