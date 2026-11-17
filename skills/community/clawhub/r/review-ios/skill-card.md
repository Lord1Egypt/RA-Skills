## Description:

Comprehensive iOS/SwiftUI code review with optional parallel agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review iOS and SwiftUI code changes for correctness, Swift quality, framework usage, tests, security, performance, and maintainability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to run build, lint, or test commands that execute project code.

Mitigation: Run those commands only in repositories where executing local project code is acceptable.

Risk: The skill depends on companion review skills for protocol and technology-specific review coverage.

Mitigation: Confirm referenced companion review skills in the local skills directory are trusted before use.

## Reference(s):

- [Review Ios ClawHub release](https://clawhub.ai/anderskev/skills/review-ios)
- [anderskev ClawHub publisher profile](https://clawhub.ai/user/anderskev)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown review report with issue severity sections, file and line references, recommendations, good patterns, and verdict.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local Swift build, SwiftLint, and test commands for verification when applicable.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
