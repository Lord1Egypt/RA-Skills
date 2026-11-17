## Description:

Book winter escape flights to warm destinations for a winter sun getaway using real-time flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to collect route and date preferences, run flyai for current winter escape flight options, and return booking-ready results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run a global third-party CLI.

Mitigation: Require explicit approval before installation, verify the package and version, and run the skill in a constrained environment.

Risk: The skill runs shell commands using user-derived travel parameters.

Mitigation: Use only documented flyai parameters, validate date and route inputs, and quote user-provided values before execution.

Risk: Returned booking links and prices are third-party commercial output.

Mitigation: Present them as third-party booking information and ask users to confirm prices and terms on the booking page.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liquanyu123/skills/winter-escape-flight)
- [Parameter collection and output templates](references/templates.md)
- [Scenario playbooks](references/playbooks.md)
- [Failure recovery](references/fallbacks.md)
- [Execution runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown tables with booking links and inline bash commands when setup or execution is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from flyai CLI output, and each displayed result must include a booking link.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
