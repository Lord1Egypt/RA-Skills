## Description:

Need a room right now? Find available hotels tonight at the lowest prices. Optimized for immediate check-in with real-time availability. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search for same-night hotel availability, compare options, and return booking links based on live flyai CLI results. It can also guide related travel service searches when supported by the same CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running a third-party travel CLI.

Mitigation: Review the package before installation and run the skill only in an isolated environment where global npm installs and third-party travel tools are acceptable.

Risk: Travel searches and bookings can involve sensitive personal or payment details.

Mitigation: Avoid entering sensitive personal or payment information into the agent session; complete payment or identity steps only through trusted booking pages.

Risk: The artifact describes hidden raw request logging without clear consent, redaction, or retention controls.

Mitigation: Disable or remove the hidden execution log unless the publisher adds clear consent, redaction, and retention controls.

Risk: The security review flagged the release as suspicious because it mandates CLI-backed booking-link output and user-visible results depend on third-party service availability.

Mitigation: Review the skill before installing, confirm each shown hotel result comes from CLI output, and report failures honestly instead of filling gaps from model knowledge.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/tonight-hotel)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown hotel recommendations with booking links and concise command-backed status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for hotel details; raw JSON is not intended for final user-facing responses.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
