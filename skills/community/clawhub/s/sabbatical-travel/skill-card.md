## Description:

Book flights for sabbatical and long-break travel using flyai CLI results, with support for related travel booking workflows such as hotels, trains, attractions, visas, insurance, and car rentals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to collect route and date details, run flyai travel searches, and return concise Markdown results with booking links. It is intended for sabbatical, career-break, long-break, and gap-year travel planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a third-party travel CLI globally without a pinned package version.

Mitigation: Ask for approval before installing software, pin and verify the package, and prefer an isolated installation over a global install.

Risk: User-derived travel parameters are inserted into command templates with weak safeguards.

Mitigation: Validate origin, destination, dates, and supported flags before execution, and reject unsupported CLI parameters.

Risk: Rendered booking links could direct users to provider-controlled destinations.

Mitigation: Check booking-link domains before rendering links and clearly label provider booking actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivan97/skills/sabbatical-travel)
- [Publisher Profile](https://clawhub.ai/user/ivan97)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output as the data source and includes provider booking links when results are available.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
