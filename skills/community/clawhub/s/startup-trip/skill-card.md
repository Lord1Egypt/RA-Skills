## Description:

Helps agents search startup-event and entrepreneur travel flights through the flyai CLI and return Markdown results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to collect route parameters, run flight searches, and present startup travel options with booking links. It is intended for startup-event and entrepreneur travel planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install a global third-party npm package if the flyai CLI is missing.

Mitigation: Require explicit user approval and use a controlled environment or pinned local installation before running any third-party CLI.

Risk: Travel text can be transformed into shell commands for flight searches.

Mitigation: Validate origin, destination, date, and sort fields against the documented parameters before command construction, and reject unexpected flags or shell metacharacters.

Risk: The workflow depends on vendor booking links and third-party travel data.

Mitigation: Disclose third-party data sharing and booking-link behavior before execution, and let users decide whether to open external booking links.

Risk: The artifact references support files that are not included in the package.

Mitigation: Review the remaining single-file workflow before release and restore or remove references to missing playbooks, templates, fallbacks, and runbook files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/startup-trip)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with flight comparison tables, concise recommendations, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses flyai CLI output and detailUrl booking links when available.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
