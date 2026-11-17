## Description:

Search for budget-friendly flights with travel wallet planning. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search live budget flight options, compare routes by price, speed, or directness, and return booking-oriented Markdown results from flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify the host by globally installing an unpinned npm CLI.

Mitigation: Require explicit approval before installation, pin the CLI version where possible, and run installation with least privilege.

Risk: The skill uses live external booking links in generated travel results.

Mitigation: Validate flight parameters and review booking links before use or sharing.

Risk: Unsafe shell-style command execution can expose users to operational mistakes.

Mitigation: Review proposed commands before execution and limit the CLI to the minimum required permissions.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown flight summaries with comparison tables, booking links, and inline CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must be based on flyai CLI output and include booking links when flight options are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
