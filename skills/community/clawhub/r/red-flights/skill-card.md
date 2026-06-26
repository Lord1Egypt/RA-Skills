## Description: <br>
Searches for red-eye flights, overnight flights, late-night departures, and after-midnight arrival deals using flyai and Fliggy-powered travel data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to search current red-eye flight options, compare late-night departures, and format results with booking links. It is intended for flight-search workflows where fresh CLI data is required rather than model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask the agent to install flyai globally with npm, which may modify the local system. <br>
Mitigation: Install the CLI manually in a least-privilege environment and do not allow automatic global or sudo npm installs. <br>
Risk: Travel searches may disclose routes, dates, preferences, and command history to flyai or local execution logs. <br>
Mitigation: Use the skill only when comfortable sharing travel search details with flyai and treat .flyai-execution-log.json as sensitive if logging is enabled. <br>
Risk: Flight results may be incorrect if the agent answers from memory or omits booking links. <br>
Mitigation: Require fresh flyai CLI output and validate that every displayed result includes a detailUrl-backed booking link before responding. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ivan97/red-flights) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Red-eye flight playbooks](references/playbooks.md) <br>
- [Fallback handling](references/fallbacks.md) <br>
- [Execution log schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and concise text with booking links, plus inline shell commands when setup or troubleshooting is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data and should not emit raw JSON or fabricate prices, schedules, or booking links.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
