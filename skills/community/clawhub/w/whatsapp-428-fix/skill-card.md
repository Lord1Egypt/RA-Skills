## Description:

修复 WhatsApp Web 连接 428 错误和代理配置问题，适用于 WhatsApp 连接断开、需要配置代理或在新机器部署 OpenClaw 后遇到连接问题的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffreycheungrt](https://clawhub.ai/user/jeffreycheungrt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to troubleshoot WhatsApp Web status 428 in OpenClaw, configure proxy settings, and apply or review service and code-level changes that may restore connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic repair script can make persistent changes to the OpenClaw gateway service and installed OpenClaw code.

Mitigation: Review the script first, prefer the manual steps when possible, and keep or create backups so the service and code changes can be reversed.

Risk: The repair flow may install an npm package from the configured registry and restart the OpenClaw gateway.

Mitigation: Confirm the configured npm registry and package before running, and perform the restart during a maintenance window or after preparing a rollback path.

## Reference(s):

- [WhatsApp 428 quick reference](references/quick-ref.md)
- [ClawHub skill page](https://clawhub.ai/jeffreycheungrt/skills/whatsapp-428-fix)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, JavaScript, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an executable repair script and manual OpenClaw service configuration steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
