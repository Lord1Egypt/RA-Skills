## Description:

Provides comprehensive Remix v2 code review with per-area review skills, parallel or sequential execution, project detection, and a verification protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to review changed Remix v2 project code across routing, data flow, forms, error boundaries, SSR/performance, metadata, sessions, types, and security before approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Effective review behavior depends on referenced sibling review skills and the shared verification protocol being present and trusted.

Mitigation: Install and use this skill only in environments where those referenced review skills and the verification protocol are trusted.

Risk: The skill reads project source files and may run normal project checks during post-fix verification.

Mitigation: Run it only against intended Remix project workspaces and review verification commands before execution.

## Reference(s):

- [Review Remix V2 ClawHub page](https://clawhub.ai/anderskev/skills/review-remix-v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured review output with severity-grouped findings, good patterns, a verdict, coverage notes, and post-fix verification commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
