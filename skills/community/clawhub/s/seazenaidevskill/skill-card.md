## Description:

新城控股 AI 研发统筹技能——基于 Prompt-as-Code 的智能体系统。四阶段渐进式落地（Phase 1~4），每个 Phase 配套引导、操作手册和验收标准。

This skill is ready for commercial/non-commercial use.

## Publisher:

[phoenixcastellan](https://clawhub.ai/user/phoenixcastellan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to install and guide a project-level AI研发统筹 workflow for requirements analysis, development coordination, testing review, and template updates. It creates a structured Prompt-as-Code file system and can optionally guide Feishu/Meegle project synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add persistent CLAUDE.md, seazenai.md, and .seazenai workflow prompts to a repository.

Mitigation: Review the generated files before committing them and confirm the project accepts persistent agent workflow prompts.

Risk: Optional Feishu/Meegle synchronization may send or modify requirement, task, status, defect, and user-mapping data in an external project system.

Mitigation: Keep auto_sync disabled until the integration is approved and configured with the intended project, work-item types, statuses, and role mappings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phoenixcastellan/skills/seazenaidevskill)
- [Architecture Reference](references/architecture.md)
- [Cold Start Guide](references/cold-start.md)
- [Knowledge Extraction Guide](references/knowledge-extraction.md)
- [Phase Guide](references/phase-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with file templates, command snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent project workflow files and may guide optional Feishu/Meegle synchronization when enabled.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; packaged skill frontmatter and changelog report 2.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
