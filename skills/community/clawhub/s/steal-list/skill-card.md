## Description:

Steal List helps agents perform pre-development UI/UX and code reference research and produce a structured Markdown Steal List of concrete product and implementation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hybirdss](https://clawhub.ai/user/hybirdss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before building non-trivial products or features to research comparable products, open-source implementations, and implementation trade-offs. The skill guides the agent to produce a Steal List with patterns to adopt, patterns to avoid, and concrete recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read limited project context, perform external web and GitHub research, run shell commands, and write reports under .scout/.

Mitigation: Review the requested scouting scope before use and inspect generated reports before applying recommendations to a project.

Risk: Dynamic GitHub search command templates can become unsafe if untrusted project or user text is treated as shell source.

Mitigation: Treat project and user text as inert search arguments, quote command inputs, and review generated shell commands before execution.

Risk: Reference research can produce incorrect, outdated, or poorly matched recommendations.

Mitigation: Use the Steal List as guidance, verify cited products and repositories, and validate any adopted pattern against the target product requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hybirdss/skills/steal-list)
- [Publisher profile](https://clawhub.ai/user/hybirdss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Structured Markdown reference document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes research reports under .scout/ and may include product references, repository comparisons, implementation notes, and risk callouts.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
