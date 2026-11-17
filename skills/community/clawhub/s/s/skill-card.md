## Description:

智能代码助手 helps agents explain code, diagnose bugs, suggest refactors, and generate code documentation in Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to request Chinese-language code explanations, bug diagnosis, refactoring guidance, and generated function or API documentation. It is suited to code quality and maintainability workflows where outputs are reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad coding requests may match this skill and produce guidance that affects source code quality or behavior.

Mitigation: Review generated explanations, fixes, refactors, and documentation before applying them to a project.

Risk: Executable behavior may fail because the artifact's main.py contains HTML-escaped syntax.

Mitigation: Fix and test main.py before relying on executable runtime behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgta23/skills/s)
- [Publisher profile](https://clawhub.ai/user/hgta23)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown and plain text with code examples when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language responses focused on code explanation, diagnosis, refactoring, and documentation.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
