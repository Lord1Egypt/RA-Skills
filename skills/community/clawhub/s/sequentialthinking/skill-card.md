## Description:

一个实现顺序思维协议的MCP服务器，提供结构化的问题解决方法，将复杂问题分解为可管理的步骤，并支持迭代优化和替代推理路径。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to route sequential-thinking requests to a structured reasoning tool that breaks complex problems into steps, supports revision, and returns organized results from the upstream API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reasoning inputs are sent to a third-party API.

Mitigation: Do not submit secrets, regulated data, private code, or confidential business context unless the publisher documents retention, deletion, endpoint controls, and privacy handling.

Risk: The required API key may be stored in a local plaintext .env file.

Mitigation: Use a scoped key where available, restrict file permissions, and rotate or delete the key when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/sequentialthinking)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [Xiaobenyang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown or text summarizing JSON returned by the upstream API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value before tool calls can succeed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
