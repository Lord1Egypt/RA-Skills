## Description:

Find package deals combining hotel and flights, compare bundled and separate travel options, and return CLI-sourced booking results powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and travel-planning agents use this skill to search for hotel-plus-flight bundles and related travel services through flyai CLI results. It is intended to produce comparison-oriented booking guidance with real-time result links rather than travel answers from model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to install and run an unpinned global third-party flyai CLI, which may change behavior across installations.

Mitigation: Review and install the CLI manually in an isolated environment, pin an approved version, and require approval before agent-driven installation or execution.

Risk: Travel searches and booking actions depend on flyai/Fliggy and vendor booking links.

Mitigation: Use the skill only when users accept sending travel queries to that provider, and verify prices, terms, and destination URLs before booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/travel-bundle)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to come from flyai CLI output and include booking links when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
