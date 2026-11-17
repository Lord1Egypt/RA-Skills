## Description:

Reviews React Flow code for anti-patterns, performance issues, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review React Flow implementations for provider-boundary issues, unstable node or edge type references, missing memoization, performance problems, and common integration mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill causes the agent to inspect relevant project files during React Flow code reviews.

Mitigation: Use it only on intended review scopes and avoid providing files that should not be included in the review.

Risk: Review findings may be incorrect or incomplete if the agent misses context in the surrounding application.

Mitigation: Require cited file paths and line numbers for findings, then review recommendations before changing code.

## Reference(s):

- [React Flow Code Review on ClawHub](https://clawhub.ai/anderskev/skills/react-flow-code-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown review findings with cited file paths, line numbers, checklist status, and code-oriented recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks the agent to cite evidence for findings and close review checklist items as satisfied, not applicable, or open.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
