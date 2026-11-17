## Description:

Skill Optimizer 0330 analyzes, audits, and refactors SKILL.md files with a four-step pipeline and established skill design patterns while preserving the original skill intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxiaofeng0811-lgtm](https://clawhub.ai/user/dxiaofeng0811-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this agent to review, diagnose, and improve SKILL.md files by applying structured design patterns, adding confirmation checkpoints, and producing optimized skill definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-trigger and high-priority behavior can activate during ordinary skill or agent work.

Mitigation: Narrow or disable broad triggers and require explicit user confirmation before analyzing or rewriting any skill file.

Risk: Generated SKILL.md or reference-file changes can introduce incorrect, unclear, or misleading agent instructions.

Mitigation: Review generated content, compare it against the original skill intent, and scan the revised skill before deployment.

Risk: Install and dependency commands may fetch remote content or run unpinned dependencies.

Mitigation: Run install or dependency commands only in a sandbox and prefer pinned, reviewed sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxiaofeng0811-lgtm/skills/skill-optimizer-0330)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and structured checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rewritten SKILL.md content, change rationale, validation checklist, and optional install or verification commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
