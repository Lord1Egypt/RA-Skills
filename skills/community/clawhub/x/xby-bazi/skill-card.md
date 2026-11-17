## Description:

八字 MCP 是一款基于 AI 的八字计算器，提供精准的八字排盘数据，用于性格分析和命运预测。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request BaZi chart details, possible solar times from an eight-character chart, and Chinese calendar information through the XiaoBenYang API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local .env file.

Mitigation: Use a dedicated low-privilege API key, avoid sharing the workspace, and inspect or clear the .env file after use.

Risk: The skill sends birth date/time, gender, and BaZi data to an external service.

Mitigation: Use the skill only when the user accepts this data transfer and avoid entering sensitive personal details unless necessary.

Risk: Security evidence reports insufficient safeguards around key validation, dependency pinning, API host restriction, and packaging consistency.

Mitigation: Inspect the source before deployment and prefer a future version that validates keys, pins dependencies, restricts the API host, and fixes packaging inconsistencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-bazi)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API host](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Guidance]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY and user-supplied birth date/time, gender, BaZi, or calendar date parameters depending on the selected tool.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
