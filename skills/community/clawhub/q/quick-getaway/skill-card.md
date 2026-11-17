## Description:

Plans complete 3-day, 2-night trips using flyai CLI results for flights, hotels, attractions, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to plan concise 3-day, 2-night getaways with current travel options, booking links, and fallback guidance when live data is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global installation of the third-party flyai CLI can affect the local agent environment.

Mitigation: Review the npm package and version before installation, and prefer running the skill in a contained environment.

Risk: Raw travel queries may be written to local diagnostic logs.

Mitigation: Disable or control logging where possible, and avoid entering sensitive personal travel details unless log handling is understood.

Risk: Travel recommendations depend on live third-party CLI data and booking links.

Mitigation: Verify generated CLI output and booking URLs before relying on prices, availability, or reservations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/quick-getaway)
- [Parameter and output templates](references/templates.md)
- [Scenario playbooks](references/playbooks.md)
- [Fallback and recovery guide](references/fallbacks.md)
- [Execution log runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for live travel data; every shown travel result must include a booking link.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
