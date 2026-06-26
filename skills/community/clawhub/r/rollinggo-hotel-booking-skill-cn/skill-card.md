## Description: <br>
使用 RollingGo CLI 查询酒店信息、筛选结果、读取酒店标签和获取房型价格，支持按目的地、日期、星级、预算、标签和距离搜索酒店并查看详情与房型报价。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search, compare, and inspect hotel options through RollingGo CLI data, including hotel tags, details, room availability, prices, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RollingGo API key, and command-line examples can expose credentials if copied into logs or shell history. <br>
Mitigation: Use skill-scoped environment configuration for RollingGo_API_KEY where possible and avoid passing API keys directly on the command line. <br>
Risk: The skill defaults to latest package versions for npm or uvx execution, which can reduce reproducibility. <br>
Mitigation: Pin a known RollingGo package version when reproducible runs or stricter change control are required. <br>
Risk: Hotel availability, prices, and booking links are external service results that may change after retrieval. <br>
Mitigation: Review current RollingGo output and booking-page details before relying on a final hotel choice or purchase. <br>


## Reference(s): <br>
- [RollingGo website](https://rollinggo.store) <br>
- [RollingGo API key application](https://mcp.agentichotel.cn/apply) <br>
- [ClawHub release page](https://clawhub.ai/rollinggo-ai/rollinggo-hotel-booking-skill-cn) <br>
- [Claw host environment reference](references/claw-host-env.md) <br>
- [RollingGo NPX reference](references/rollinggo-npx.md) <br>
- [RollingGo UV reference](references/rollinggo-uv.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides CLI execution that normally returns JSON on stdout and errors on stderr.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
