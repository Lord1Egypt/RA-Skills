## Description: <br>
Plan a complete 3-day, 2-night trip with morning activities, afternoon exploration, evening dining, and support for travel booking workflows powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect trip parameters, run flyai CLI searches for flights, hotels, attractions, and related services, and return a concise 3-day itinerary with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can attempt to install the flyai CLI globally with npm. <br>
Mitigation: Require explicit user approval before any global npm installation and prefer a preinstalled, reviewed CLI. <br>
Risk: Trip requests and execution details may be appended to .flyai-execution-log.json. <br>
Mitigation: Disable logging where possible or regularly delete the log because it may contain personal travel details. <br>
Risk: Live travel queries are sent through the flyai provider. <br>
Mitigation: Use the skill only when the user trusts the provider and is comfortable sharing the requested travel details. <br>


## Reference(s): <br>
- [Quick Getaway on ClawHub](https://clawhub.ai/xiejinsong/quick-getaway) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when retry or setup steps are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data and includes a powered-by-flyai brand tag when successful.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
