## Description:

Optimize Tailwind CSS usage by detecting unused classes, identifying opportunities for @apply extraction, auditing responsive design, and reducing bundle size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Frontend developers use this skill to inspect Tailwind CSS configuration and class usage, identify dead or repeated utilities, and receive optimization recommendations for bundle size and design-system consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect local frontend source files, Tailwind configuration, and class usage while performing the optimization review.

Mitigation: Run the skill only in repositories where reading local source files is acceptable, and review proposed changes before applying them.

Risk: Optimization recommendations can affect styling, responsive behavior, or design-system consistency if applied without review.

Mitigation: Validate recommendations in the target application and test affected breakpoints, components, and generated CSS before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/tailwind-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional inline shell commands and CSS examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analysis and recommendations; the artifact does not claim to modify files automatically.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
