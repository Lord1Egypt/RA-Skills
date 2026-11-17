## Description:

Turn ideas into comprehensive project specs through collaborative dialogue before planning or implementation for new projects, features, or significant changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and other builders use this skill before planning or implementation to turn fuzzy project ideas into standalone, implementation-free specifications. It guides collaborative questioning, scope assessment, direction selection, drafting, review, and final spec capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write a spec file under docs/specs and create a git commit for that document.

Mitigation: Review the generated spec and repository diff before allowing the write or commit, especially where commits trigger automation.

## Reference(s):

- [Spec Self-Review Checklist](references/spec-reviewer.md)
- [Spec Document Template](references/spec-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Collaborative dialogue and a standalone Markdown spec document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a spec under docs/specs after user approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
