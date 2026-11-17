## Description:

Helps an agent propose user-approved persistent behavior updates across memory, skill, and global-rule layers using keyword, failure, and review triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjj2026](https://clawhub.ai/user/sjj2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture durable user preferences and reusable lessons as approved memory, skill, or global-rule updates, with stricter review for changes that affect future agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to propose and apply persistent behavior changes that can affect future sessions or other agents.

Mitigation: Review every proposed diff before applying it, and require administrator approval for L2 or L3 changes.

Risk: Global-rule writes can have broad impact on future agent behavior.

Mitigation: Treat writes to CLAUDE.md or equivalent global-rule files as high-impact changes requiring double confirmation and a rollback plan.

## Reference(s):

- [Self-Evolve Skill on ClawHub](https://clawhub.ai/sjj2026/skills/shike-self-evolve)
- [AutoClaw self-evolution concept](https://autoglm.zhipuai.cn/autoclaw)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with structured request cards, file-change instructions, and optional Python helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposes persistent changes to memory, skill, and global rule files after user approval.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
