## Description:

输入一个 IP（动漫、影视、文创等）名称，自动获取其近两年电商销售数据，并生成含年度对比、趋势、潜力评估的专业报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoshanya](https://clawhub.ai/user/luoshanya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to look up IP ecommerce data and produce a structured commercial potential report with year-over-year comparisons, trend interpretation, and operating suggestions. Users may also use it to configure the required ip-data MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to configure a paid bearer token against a plaintext HTTP endpoint at a raw IP address.

Mitigation: Do not use a real or paid token with this endpoint unless the publisher provides HTTPS, clear data-handling terms, and safe secret storage guidance.

Risk: The skill may ask for an API token during setup.

Mitigation: Avoid pasting secrets into chat; configure credentials directly in the local MCP configuration using a disposable or least-privilege token where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoshanya/skills/yuancangip)
- [Yuancang IP service website](https://www.yuancangip.com/)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance, API calls]

**Output Format:** [Markdown report with optional JSON configuration snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces IP ecommerce analysis from MCP-returned JSON data; configuration guidance requires a user-provided bearer token.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
