## Description: <br>
输入一个 IP（动漫、影视、文创等）名称，自动获取其近两年电商销售数据，并生成含年度对比、趋势、潜力评估的专业报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoshanya](https://clawhub.ai/user/luoshanya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business analysts use this skill to evaluate IP merchandising performance from ecommerce sales data, compare recent yearly metrics, and produce a concise commercialization assessment with operating recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to place a paid bearer token in persistent MCP configuration. <br>
Mitigation: Use a dedicated revocable token with limited balance or scope where available, monitor paid usage, and rotate or revoke the token after testing. <br>
Risk: The configured MCP endpoint uses raw HTTP, which can expose bearer credentials in transit. <br>
Mitigation: Prefer an HTTPS endpoint on a verified domain before production use, and install only if the provider and endpoint are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoshanya/yuancangip) <br>
- [Yuancang IP service](https://www.yuancangip.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown report with configuration JSON guidance when setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the configured ip-data MCP service and use returned JSON sales fields to calculate year-over-year changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
