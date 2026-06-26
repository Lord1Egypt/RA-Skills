## Description: <br>
Book summer vacation flights for July and August holiday travel using flyai CLI results, with related support for hotels, trains, attraction tickets, itineraries, visas, car rental, and insurance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use this skill to collect route, date, and preference details, run flyai CLI flight searches, and return bookable summer travel options in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install a global npm CLI before performing searches. <br>
Mitigation: Ask for user confirmation before installing global packages and verify the package source before installation. <br>
Risk: Travel searches may send route, date, and preference details to the external flyai/Fliggy service. <br>
Mitigation: Confirm the user is comfortable sharing trip details with the provider and avoid entering sensitive travel information unless the provider is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liquanyu123/summer-vacation-flight) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results must come from flyai CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
