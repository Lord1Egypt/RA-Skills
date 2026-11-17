## Description:

一个MCP服务器，使大型语言模型能够通过标准骰子符号（如1d20）进行骰子滚动，并返回单个滚动结果及其总和。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request standard dice rolls such as 1d20 or 2d6+3 and receive the remote service result with the roll total.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key for a simple dice-rolling task.

Mitigation: Install only when a service-backed dice roller is intentional; otherwise use a local dice roller that does not require credentials or network access.

Risk: The API key is stored in a local .env file in plaintext.

Mitigation: Use a scoped or disposable key where available, restrict local file access, and remove the key from .env when the skill is no longer needed.

Risk: Dice roll requests are sent to a remote XiaoBenYang service.

Mitigation: Avoid sending sensitive context with roll requests and review network use before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-dice)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP service endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Configuration]

**Output Format:** [Text summary derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a dice notation string and a XiaoBenYang API key.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
