## Description: <br>
Helps agents search hotels, refine filters, inspect hotel details and pricing, and retrieve hotel tags through the RollingGo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamtzlong](https://clawhub.ai/user/dreamtzlong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search for hotel candidates, compare current room pricing and availability, inspect hotel detail pages, and prepare booking links through the RollingGo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dreamtzlong/rollinggo-searchhotel) <br>
- [RollingGo service homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo NPX Reference](references/rollinggo-npx.md) <br>
- [RollingGo UV Reference](references/rollinggo-uv.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI result interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI result payloads are JSON by default; search results can also be shown as tables. Prefer setting RollingGo_API_KEY through an environment variable or secret manager instead of passing an API key on the command line.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
