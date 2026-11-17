## Description:

Explore Southeast Asia travel options, including flights, hotels, attractions, itinerary planning, visa information, travel insurance, and car rental, using flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to plan Southeast Asia trips and compare flights, hotels, attractions, itinerary options, visa information, insurance, and car rental results from flyai CLI data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run an unpinned global third-party CLI.

Mitigation: Require explicit user approval before installing or running the CLI, and prefer a pinned, reviewed version where available.

Risk: Travel-search details may be sent to the third-party travel service.

Mitigation: Tell users what data will be submitted and avoid sending sensitive personal information unless needed for the search.

Risk: The artifact describes writing raw request details to a hidden plaintext execution log.

Mitigation: Disable the log where possible, or redact user queries and other sensitive fields before persisting execution details.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown travel results with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output; booking results should include detailUrl booking links and the flyai brand tag.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
