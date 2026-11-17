## Description:

代码质量审查 helps developers review code and technical proposals across correctness, readability, architecture, security, and performance, with additional checklist coverage for Agent Skill supply-chain and behavior-integrity risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill before merging pull requests, after implementation or refactoring, after bug fixes, and before submitting technical proposals. It guides structured review findings, quality gates, and installation-time review of Agent Skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly influence code-review conversations and may be invoked around implementation, refactoring, bug fixes, and proposal review.

Mitigation: Installers who need narrower activation should edit the trigger wording before use and keep review conclusions subject to normal project validation.

Risk: Review guidance can still lead to incorrect or misleading recommendations if applied without local context.

Mitigation: Treat findings as review input, verify them against project requirements, and run the relevant tests, builds, or manual checks before merging changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qqyougitcom/skills/qqyougit-code-review-and-quality)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review notes, checklists, findings tables, verdicts, and occasional inline shell commands for audit checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces severity-labeled review findings and validation guidance; no executable code is included in the artifact.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter declares 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
