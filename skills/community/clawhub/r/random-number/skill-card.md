## Description:

提供伪随机和加密安全的随机数生成功能，包括整数、浮点数、加权选择、列表洗牌和安全令牌生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to request random integers, floats, weighted choices, shuffled lists, samples, and hex tokens through a XiaoBenYang-backed API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a plaintext .env file.

Mitigation: Use only non-sensitive API credentials, restrict file access, rotate keys as needed, and avoid shared environments where plaintext credential storage is unacceptable.

Risk: Random-generation requests and parameters are sent to an external third-party service.

Mitigation: Do not submit private lists, secrets, passwords, reset tokens, session identifiers, or other sensitive values.

Risk: The security verdict is suspicious because the external API dependency is overbroad for a random-number skill.

Mitigation: Review before installing and deploy only where outbound requests to XiaoBenYang are allowed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cainingnk/skills/random-number)
- [XiaoBenYang API Key Site](https://xiaobenyang.com)
- [XiaoBenYang MCP API Endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, API Calls, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and sends random-generation parameters to an external service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
