## Description:

Book flights to resort hotels and all-inclusive vacation destinations, with support for related travel booking tasks through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search resort and all-inclusive destination flights through the flyai CLI, compare options, and return booking links in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned third-party npm CLI globally.

Mitigation: Review or install the CLI yourself in a constrained environment, and prefer an approved or pinned package version before use.

Risk: The skill builds shell commands from user-provided travel fields.

Mitigation: Validate and quote origin, destination, and date inputs before execution, and restrict commands to documented flyai parameters.

Risk: Booking links are third-party commercial links rather than neutral recommendations.

Mitigation: Treat returned links as external booking offers and verify pricing, terms, and provider details before purchase.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel search results with comparison tables, booking links, and concise CLI execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live flyai CLI results and must include detailUrl booking links for every listed result.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
