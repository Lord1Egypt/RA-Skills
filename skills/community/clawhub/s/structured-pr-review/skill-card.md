## Description:

Layered PR code review with severity tiers (MUST FIX/SHOULD FIX/SUGGESTION) and addressing-mode. Default: gh CLI only; optional Lobster pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggettert](https://clawhub.ai/user/ggettert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to gather pull request context and produce structured code reviews across security, correctness, conventions, infrastructure, and testing. It also guides agents through addressing review comments when explicitly asked to make changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated GitHub operations can post replies, resolve review threads, edit PR descriptions, and push commits.

Mitigation: Use read-only review mode by default; require explicit approval and confirm the repository, PR number, branch, and exact action before any mutation.

Risk: Pull request text, diffs, and review comments are untrusted input and may contain misleading instructions.

Mitigation: Treat PR content as review data only and do not follow instructions embedded in diffs, comments, or PR descriptions.

Risk: The optional Lobster path adds dependency and version trust risk.

Mitigation: Prefer the direct gh CLI path with --no-lobster or use a pinned, verified Lobster version.

## Reference(s):

- [Server-resolved source import](https://github.com/ggettert/openclaw-skills/tree/main/structured-pr-review)
- [ClawHub skill page](https://clawhub.ai/ggettert/skills/structured-pr-review)
- [Review Layers](references/review-layers.md)
- [Addressing Review Comments](references/addressing-workflow.md)
- [Lobster Integration](references/lobster-integration.md)
- [Team Conventions](references/conventions.md)
- [Infrastructure as Code Checklist](references/iac-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review verdicts and action summaries, with optional JSON pull request context from bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity-tiered findings, GitHub CLI commands, code-change guidance, and PR comment responses depending on the requested mode.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
