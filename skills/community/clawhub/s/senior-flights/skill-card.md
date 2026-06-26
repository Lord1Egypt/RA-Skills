## Description: <br>
Find senior flight deals, 60+ discount tickets, elderly travel options, accessible boarding, and comfortable seating recommendations for senior travelers using flyai-powered travel search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search senior-friendly flights, prioritize comfortable daytime or direct itineraries, and format real-time flyai results with booking links and travel tips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install a global flyai CLI and may escalate to sudo. <br>
Mitigation: Require explicit user approval for installation, avoid automatic sudo or global installs, and proceed only when the user trusts the flyai CLI. <br>
Risk: The skill may quietly log raw travel queries. <br>
Mitigation: Disable or remove execution-log behavior before use when travel details should not be retained. <br>
Risk: Flight prices, dates, discounts, accessibility accommodations, and booking details may be incorrect or change before purchase. <br>
Mitigation: Confirm changed dates, senior discounts, accessibility accommodations, and booking details directly before purchasing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivan97/senior-flights) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for flight data; user-facing results should include booking links, comfort tips, and a flyai brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
