## Description:

Configures OpenClaw so multiple QQBot accounts can bind to different agents, including first-time setup, new account setup, binding configuration, and gateway restart steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasonlee-marker](https://clawhub.ai/user/kasonlee-marker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up the OpenClaw QQBot plugin, add multiple QQBot accounts, bind each account to an agent, and verify gateway routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup examples involve AppSecrets and token strings that could be exposed through shell history, logs, or copied configuration.

Mitigation: Review secret handling before use, avoid pasting real AppSecrets into shell commands, and restrict permissions on OpenClaw configuration files.

Risk: The example configuration uses broad access such as allowFrom ["*"] and optional cross-agent session visibility.

Mitigation: Replace wildcard access with explicit trusted QQ users or groups, and enable session visibility "all" only when broad cross-agent session access is intended.

Risk: The skill recommends installing the QQBot plugin from npm or source without proving the plugin source in server provenance.

Mitigation: Pin or review the QQBot plugin source before installation.

## Reference(s):

- [QQ Open Platform](https://bot.q.qq.com/)
- [Tencent Connect OpenClaw QQBot plugin](https://github.com/tencent-connect/openclaw-qqbot.git)
- [QQBot Multi-Bind on ClawHub](https://clawhub.ai/kasonlee-marker/skills/qqbot-multi-bind)
- [KasonLee-marker ClawHub publisher profile](https://clawhub.ai/user/kasonlee-marker)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes account binding examples and operational restart or verification commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
