## Description: <br>
Fetches WeChat public-account reading growth rankings by date, displays the script output as a Markdown table, and can summarize growth patterns from the returned ranking data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, editors, and analysts use this skill to fetch recent WeChat public-account reading growth rankings and review high-growth accounts, representative articles, and content patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and sends it to the ranking service during requests. <br>
Mitigation: Use a scoped or session-only REDFOX_API_KEY where possible, confirm the key source and revocation path, and rotate the key if it may have been exposed. <br>
Risk: The helper script can search shell startup files for REDFOX_API_KEY when the environment variable is not already set. <br>
Mitigation: Avoid storing unrelated secrets in shell profile files and review local profile contents before installing or running the skill. <br>
Risk: Ranking data is fetched from an external service and may be unavailable, stale, or outside the supported 30-day query window. <br>
Mitigation: Treat only successful script output as evidence, preserve the returned table without rewriting it, and do not invent rankings when the service returns no data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/wechat-growth-ranking) <br>
- [Publisher profile](https://clawhub.ai/user/if530770) <br>
- [Core workflow](references/core_workflow.md) <br>
- [API specification](references/api-spec.md) <br>
- [RedFoxHub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables, prose summaries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranking queries are limited to the most recent 30 days and require a RedFox API key.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
