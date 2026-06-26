## Description: <br>
Guides agents to search seasonal flights, summer routes, winter schedules, and holiday charter options using FlyAI results, then return concise travel comparisons with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to search seasonal, holiday, summer, winter, and off-season flights, compare available options, and present booking links from live FlyAI search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install or update the FlyAI CLI automatically, including fallback sudo installation. <br>
Mitigation: Require explicit approval for npm or sudo installation and prefer a pinned, non-global installation when possible. <br>
Risk: Travel search details may be sent to FlyAI or Fliggy-backed services. <br>
Mitigation: Use the skill only when users accept the external service dependency and understand that travel search parameters leave the local agent environment. <br>
Risk: The skill can store travel query execution details in .flyai-execution-log.json. <br>
Mitigation: Disable or delete the local execution log when users do not want travel queries retained locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivan97/seasonal-flight) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Seasonal flight playbooks](references/playbooks.md) <br>
- [Fallback handling](references/fallbacks.md) <br>
- [Execution log schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and summaries with booking links, plus FlyAI CLI commands when setup, retry, or troubleshooting steps are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live FlyAI CLI results for flight data; no raw JSON is intended for user-facing output.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
