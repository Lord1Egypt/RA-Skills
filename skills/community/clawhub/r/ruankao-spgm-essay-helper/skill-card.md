## Description:

辅助备考软考高级资格「系统规划与管理师」的考生，根据用户输入的论文题目与本人真实项目背景，结合 IMA 备考资料库生成符合评分标准的论文框架与写作提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-language Ruankao System Planning and Management Engineer candidates use this skill to turn an exam essay prompt and their own real project background into a structured Markdown essay framework with writing prompts, terminology suggestions, and scoring self-checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional IMA lookup may query a named external exam-prep knowledge base.

Mitigation: Use the lookup only when the user asks for or authorizes exam-prep reference retrieval, and keep the user's actual project background grounded in their own provided experience.

Risk: Generated essay frameworks and prompts could be mistaken for a complete answer or substitute for the candidate's own writing.

Mitigation: Present outputs as reference frameworks and revision guidance, and require the candidate to write from their real project experience.

Risk: Reference essays or knowledge-base results could create plagiarism or similarity risk if copied directly.

Mitigation: Use retrieved materials only to extract structure, themes, terminology, and scoring cues; do not reproduce reference essays verbatim.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/ruankao-spgm-essay-helper)
- [IMA knowledge-base guide](artifact/references/ima_kb_guide.md)
- [Essay framework template](artifact/references/essay_framework_template.md)
- [Essay scoring criteria](artifact/references/essay_scoring_criteria.md)
- [Project background template](artifact/references/project_bg_template.md)
- [System Planning and Management Engineer terminology](artifact/references/spgm_terminology.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown essay framework with writing prompts, terminology suggestions, word-count guidance, and scoring self-checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally use a named IMA exam-prep knowledge base for prompts, past exam topics, reference structures, and terminology; user project background is required to come from the user's own real experience.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
