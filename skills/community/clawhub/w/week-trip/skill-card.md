## Description: <br>
Plan an epic 7-day vacation with multi-city routes, intercity transportation, hotel transitions, daily itineraries, and booking-oriented travel searches powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-planning users and agents use this skill to collect trip parameters, run flyai CLI searches for week-long itineraries, and present bookable flights, hotels, attractions, and related travel options in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to install a global flyai CLI package before producing travel results. <br>
Mitigation: Review and approve any global npm install first, or install a trusted pinned version manually before using the skill. <br>
Risk: The skill can retain raw travel requests in a hidden local execution log when filesystem writes are available. <br>
Mitigation: Disable, inspect, or delete .flyai-execution-log.json if local retention of travel requests is not desired. <br>
Risk: Travel results depend on provider-specific flyai booking data and may be incomplete or unavailable when the CLI fails. <br>
Mitigation: Use the skill only when provider-specific results are acceptable, and follow the documented fallback or retry steps when real-time data is unavailable. <br>


## Reference(s): <br>
- [Week Trip skill page](https://clawhub.ai/xiejinsong/week-trip) <br>
- [Output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback guidance](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tables, booking links, concise recommendations, and inline shell commands when setup or retries are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output as the required data source and should include booking links for returned travel results.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
