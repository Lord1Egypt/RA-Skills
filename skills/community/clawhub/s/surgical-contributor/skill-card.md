## Description:

Surgical Contributor guides agents to deliver small, high-signal code or documentation contributions by isolating one real pain point, applying the narrowest safe change, adding regression protection, and writing a maintainer-friendly PR summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dj-shortcut](https://clawhub.ai/user/dj-shortcut)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to make one focused repository fix or documentation correction with reproduction, minimal patching, regression protection, self-review, and a PR-ready summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may propose an incorrect or incomplete code or documentation change.

Mitigation: Review proposed edits, regression protection, and verification notes before merging or deployment.

Risk: The skill can modify repository files when used by an agent with write access.

Mitigation: Use normal repository review controls and confirm that each changed line traces to the selected narrow issue.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dj-shortcut/skills/surgical-contributor)
- [Risk Map](references/risk-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with code changes, shell commands, verification notes, and PR-summary sections when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one focused contribution plan, patch, regression protection, self-review, and maintainer-facing summary.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
