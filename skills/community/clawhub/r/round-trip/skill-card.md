## Description: <br>
Helps agents book round-trip flights by collecting route and date details, querying the flyai CLI for outbound and inbound options, and formatting booking results with links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to search round-trip flight options, compare outbound and return choices, and produce bookable Markdown results from FlyAI/Fliggy data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to install a global npm package. <br>
Mitigation: Require user approval before installation and stop with manual installation instructions if the CLI remains unavailable. <br>
Risk: The skill can send travel searches to an external FlyAI service. <br>
Mitigation: Tell users that searches require external real-time data and avoid using the skill for sensitive travel details without consent. <br>
Risk: The runbook describes persisting raw travel queries to .flyai-execution-log.json. <br>
Mitigation: Avoid writing local execution logs unless the user explicitly asks for persistence. <br>
Risk: Round-trip results may be incomplete or misleading if return-date handling is omitted. <br>
Mitigation: Confirm both departure and return dates before relying on booking results, and verify that each displayed result includes a booking link. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>
- [ClawHub skill page](https://clawhub.ai/ivan97/round-trip) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking tables, inline shell commands, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses real-time flyai CLI results and should include booking links for every listed result.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
