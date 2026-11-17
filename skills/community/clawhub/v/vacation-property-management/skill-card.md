## Description:

Manage vacation rental properties, guest reservations, and cleaning checklists with the TIDY platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mchusma](https://clawhub.ai/user/mchusma)

### License/Terms of Use:

MIT-0

## Use Case:

External short-term rental hosts, vacation property managers, and Airbnb/VRBO operators use this skill to manage TIDY properties, guest reservations, cleaning checklists, and related API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived TIDY_API_TOKEN credentials can expose TIDY property, reservation, and access-note data if mishandled.

Mitigation: Protect TIDY_API_TOKEN like a password, use a dedicated or least-privileged account where possible, and avoid sharing token values in prompts, logs, or examples.

Risk: The skill includes live create, update, and delete workflows for property and reservation records.

Mitigation: Require user confirmation before update or delete actions and review the target property, reservation, dates, and access notes before executing requests.

Risk: The optional global CLI installation may install an unpinned package.

Mitigation: Prefer direct API requests when package provenance is unclear, or verify and pin the CLI package source before installing it globally.

## Reference(s):

- [TIDY homepage](https://tidy.com)
- [ClawHub skill page](https://clawhub.ai/mchusma/skills/vacation-property-management)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TIDY_API_TOKEN for authenticated TIDY API requests.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
