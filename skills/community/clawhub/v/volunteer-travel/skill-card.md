## Description:

Book flights for volunteer travel and charity programs, with related travel booking support powered by Fliggy and FlyAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel coordinators use this skill to search volunteer or charity-trip flight options through the flyai CLI and format real-time results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global npm CLI before use.

Mitigation: Require explicit approval before installation and prefer a reviewed or pinned package source where deployment policy requires it.

Risk: Travel details are sent to an external flight-booking service.

Mitigation: Confirm user consent and avoid submitting unnecessary personal or sensitive travel data.

Risk: Shell commands are built from user-provided origins, destinations, and dates.

Mitigation: Validate origin, destination, and date inputs before command execution.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Localized to English or Chinese; flight results must include flyai booking links.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
