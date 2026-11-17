## Description:

Build helps agents execute implementation tasks from an existing plan using a TDD workflow, including progress tracking, local verification, and commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to continue from an existing implementation plan, select the next task, apply a TDD-oriented workflow, run local verification, update progress, and create commits. It is best suited to solo development and automated build-from-plan workflows rather than general project management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to run local commands, modify repository files, update plan files, and create commits.

Mitigation: Use it only in repositories where build-from-plan automation is intended, review the selected plan before execution, and inspect resulting diffs and commits.

Risk: The broad description text may make the skill appear suitable for general project management.

Mitigation: Use it for existing docs/plan implementation tracks, not for personnel evaluation or broad project governance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/solo-dev-companion)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, repository edits, shell commands, and concise status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update plan files, modify code, run local build and test commands, and create commits when used in a repository.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
