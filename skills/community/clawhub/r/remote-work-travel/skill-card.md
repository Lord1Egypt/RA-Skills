## Description:

Book flights for remote work travel and workation destinations, with support for related travel planning grounded in FlyAI CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and agent users use this skill to collect travel parameters, run the flyai CLI for route availability and pricing, and return concise Markdown flight comparisons with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require a global npm install of the third-party flyai CLI.

Mitigation: Install the CLI from a trusted source, pin or review the package version where possible, and verify the CLI before using the skill.

Risk: The skill requires booking links from a third-party travel service.

Mitigation: Review booking links before clicking or purchasing, and confirm prices and itinerary details on the booking site.

Risk: Travel answers could be stale or fabricated if the CLI is bypassed.

Mitigation: Use flyai CLI output as the exclusive source for availability and pricing, and reject results that lack booking links.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output as the data source; flight results must include booking links and must not include raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
