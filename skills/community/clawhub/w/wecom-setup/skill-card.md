## Description:

Set up WeCom (企业微信) as a chat channel for OpenClaw using the official Tencent plugin with WebSocket long-polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengtruman922-dotcom](https://clawhub.ai/user/pengtruman922-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to connect a WeCom AI Bot to OpenClaw, configure the WeCom channel, verify model availability, restart the gateway, and troubleshoot common connection issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example configuration defaults to broad WeCom direct-message and group access.

Mitigation: Restrict access to known users or groups by using allowlist policies instead of open wildcard defaults.

Risk: The WeCom bot secret is stored in the local OpenClaw configuration file.

Mitigation: Protect ~/.openclaw/openclaw.json with owner-only permissions and keep the secret out of repositories and shared backups.

Risk: The setup installs a mutable network-capable plugin.

Mitigation: Prefer a pinned or otherwise verified plugin version when available.

## Reference(s):

- [WeCom Open Platform](https://open.work.weixin.qq.com)
- [WeCom AI Bot documentation](https://open.work.weixin.qq.com/help?doc_id=21657)
- [ClawHub skill page](https://clawhub.ai/pengtruman922-dotcom/skills/wecom-setup)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash, PowerShell, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, access-control options, and troubleshooting guidance for WeCom channel configuration.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
