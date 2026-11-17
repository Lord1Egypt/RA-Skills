## Description:

Guides an agent through multi-round independent deep thinking where each round produces a complete solution before final synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stofancy](https://clawhub.ai/user/stofancy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and decision makers use this skill to explore complex design, strategy, innovation, and risk-assessment problems through independent solution rounds followed by a synthesized final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow writes problem and round files in the workspace and deletes intermediate drafts by default.

Mitigation: Ask the agent to preserve intermediate files before using the skill when auditability, review, or retention is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stofancy/skills/reinforced-thinking-mode)
- [English skill definition](artifact/SKILL.md)
- [English publish description](artifact/README.md)
- [Chinese skill definition](artifact/skill_cn.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown files and synthesized report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a reinforced-thinking workspace with problem, round, and final report files; intermediate drafts are deleted by default unless retention is requested.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
