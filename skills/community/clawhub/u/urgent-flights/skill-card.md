## Description: <br>
Find flights departing within 48 hours for spontaneous trips or emergency travel with immediate availability and real-time seat status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to find urgent flight options, compare near-term availability, and format real-time travel results with booking links. It also guides agents through parameter collection, CLI execution, and fallback handling when results are unavailable or ambiguous. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run the flyai CLI and send travel search details to that provider. <br>
Mitigation: Review commands before execution, use an isolated environment where possible, and avoid sharing sensitive travel details unless the provider is acceptable for the use case. <br>
Risk: The skill documentation allows local request logging that may retain raw travel details. <br>
Mitigation: Delete, disable, or restrict access to .flyai-execution-log.json when travel details should not be retained. <br>
Risk: The skill suggests global installation and fallback sudo installation for the CLI. <br>
Mitigation: Prefer a project-local or otherwise isolated install and avoid sudo unless explicitly reviewed and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/urgent-flights) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight and travel results are expected to come from flyai CLI output, and every shown flight result must include a booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
