## Description:

Wukong 是中文名人思维蒸馏与召唤技能，用六层框架保存并调用人物心智模型，辅助问题分析和决策参考。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-language users can distill public figures, leaders, scientists, artists, or other personas into reusable six-layer thinking models, then invoke those models for analysis, decision support, and perspective-taking. The skill is also useful for maintaining a local registry of saved persona-style Markdown templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: New persona distillations may persist prompt content into local Markdown files.

Mitigation: Avoid including sensitive private details in persona prompts unless local persistence is acceptable, and review generated persona files before sharing or publishing.

Risk: Persona-style analysis can sound authoritative even when it is speculative or loosely sourced.

Mitigation: Treat generated viewpoints as decision-support drafts and verify important claims against reliable sources before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/skills/wukong)
- [six-layer-template.md](artifact/references/six-layer-template.md)
- [registry.md](artifact/wukong/registry.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown analysis responses and Markdown persona files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save new distilled persona templates under wukong/personas/ and update the persona registry.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
