## Description:

Connects OpenClaw to Enterprise WeChat by generating a WeCom authorization link, waiting for user confirmation, polling for bot credentials, writing WeCom channel settings, and restarting the OpenClaw gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easelearnai](https://clawhub.ai/user/easelearnai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an OpenClaw gateway to Enterprise WeChat/WeCom through an authorization-link flow and enable the WeCom channel after credentials are returned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The WeCom bot secret is stored in the local OpenClaw configuration file.

Mitigation: Review local permissions for ~/.openclaw/openclaw.json and ask the agent to show the intended configuration change before it writes credentials.

Risk: The OpenClaw gateway is restarted after the WeCom channel is enabled.

Mitigation: Run the flow only when a gateway restart is acceptable and confirm the authorization step before polling, writing configuration, or restarting the gateway.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/easelearnai/skills/wecom-connect)
- [WeCom Authorization Generation Endpoint](https://work.weixin.qq.com/ai/qc/generate?source=wecom-cli&plat=3)
- [WeCom Authorization Result Endpoint](https://work.weixin.qq.com/ai/qc/query_result?scode=<scode>)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write WeCom botId and secret settings to ~/.openclaw/openclaw.json and restart the OpenClaw gateway after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
