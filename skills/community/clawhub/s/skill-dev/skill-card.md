## Description:

Skill开发优化助手。当发现技能有漏洞/流程缺失/逻辑错误/经验教训需要沉淀时触发。自动分析问题、定位根源、修改技能、回归验证并记录影响。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this skill to analyze defects or missing workflow steps in existing skills, apply targeted skill-file updates, run regression checks, and record the impact of changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to actively edit other skills and persistent memory without asking first.

Mitigation: Require explicit confirmation before SkillManage modify actions or MEMORY.md writes, prefer workspace-scoped memory, and review each proposed change before applying it.

Risk: Incorrect fixes or undocumented workflow changes could be persisted into reusable skill instructions.

Mitigation: Review and scan modified skill files before deployment, and keep edits limited to SKILL.md, scripts, references, and intended memory records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/skill-dev)
- [Project homepage](https://github.com/bettermen/skill-dev-scene)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with targeted skill-file edits and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply changes to SKILL.md, scripts, references, and workspace-scoped memory records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
