## Description:

QuickTicket creates or reconciles scoped, dependency-ordered tickets for an idea, task, or project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redrookai](https://clawhub.ai/user/redrookai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use QuickTicket to plan work or reconcile an existing backlog into actionable tickets with clear dependencies and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tickets may contain incorrect assumptions or unsuitable implementation guidance.

Mitigation: Review the saved tickets and acceptance checks before using them as implementation instructions.

Risk: Project inspection and ticket edits could affect an unintended project or destination.

Mitigation: Specify the project and authorized ticket destination when invoking the skill.

## Reference(s):

- [QuickTicket on ClawHub](https://clawhub.ai/redrookai/skills/quickticket)
- [Story splitting](https://agilealliance.org/glossary/story-splitting/)
- [Spec Kit feature decomposition](https://github.github.io/spec-kit/concepts/spec-of-specs.html)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Local Markdown tickets and index, plus a brief text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tickets include dependencies, acceptance conditions, and verification steps; existing plans may be reconciled.]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
