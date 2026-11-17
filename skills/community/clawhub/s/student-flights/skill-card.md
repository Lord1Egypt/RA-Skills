## Description:

Find student-friendly flight deals, budget travel options, and related booking information for young and student travelers using flyai/Fliggy CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-assistant agents use this skill to find student-friendly flight options and related travel booking information. The skill guides agents to collect route parameters, run flyai CLI searches, and return concise Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to install an unpinned global npm CLI.

Mitigation: Review the CLI package before installation and pin an approved version in managed environments.

Risk: Fallback instructions may suggest sudo for global installation.

Mitigation: Avoid sudo installation; use a user-scoped npm prefix, sandbox, or preapproved managed runtime.

Risk: The skill may persist raw travel queries to a local log.

Mitigation: Disable or remove raw-query logging unless users have notice and the log location, retention, and access controls are defined.

Risk: Results route users through flyai/Fliggy booking links.

Mitigation: Make the booking-link dependency clear to users and review destination links before use in sensitive or regulated travel workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/student-flights)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output and booking links for flight results; raw JSON is not intended for user-facing output.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
