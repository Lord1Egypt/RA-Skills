## Description:

Comprehensive Python/FastAPI backend code review with optional parallel agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review changed Python and FastAPI backend code, run configured local checks, load relevant companion review skills, and produce a structured Markdown review with findings and a verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local repository review commands such as ruff, mypy, pytest, git diff, and grep.

Mitigation: Use it in repositories where running those checks is acceptable and review command effects before execution.

Risk: The workflow loads companion review skills that can influence findings.

Mitigation: Ensure referenced companion skills come from trusted sources before relying on the review.

Risk: Code-review guidance can be incorrect or overstate issues if project context is missed.

Mitigation: Follow the skill's hard gates for linting, source re-reading, reference checks, and FILE:LINE evidence before accepting findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/review-python)
- [Publisher profile](https://clawhub.ai/user/anderskev)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review report with command outputs and structured findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped by severity, numbered sequentially, tied to FILE:LINE evidence, and end with a readiness verdict.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
