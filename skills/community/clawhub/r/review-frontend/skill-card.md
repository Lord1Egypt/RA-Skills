## Description:

Comprehensive React/TypeScript frontend code review with per-area review skills, run in parallel where the agent supports subagents and sequentially otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to perform React/TypeScript frontend code reviews across routing, shadcn/ui, state, Tailwind, test, and related technology areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced companion review skills may be unavailable or untrusted, which can make the review incomplete.

Mitigation: Before use, confirm the referenced review skills are installed from trusted sources and load successfully.

Risk: Frontend review findings can be incorrect if based on diff context alone or unverified framework assumptions.

Mitigation: Follow the skill's verification gates: re-read actual files, confirm references with search, and cite concrete FILE:LINE evidence before reporting issues.

## Reference(s):

- [Review Frontend ClawHub skill page](https://clawhub.ai/anderskev/skills/review-frontend)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown review report with file-line findings, severity sections, good patterns, and verdict.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include post-fix verification commands such as npm run lint, npm run typecheck, and npm run test.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
