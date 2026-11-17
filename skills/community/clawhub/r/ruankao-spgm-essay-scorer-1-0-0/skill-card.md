## Description:

对软考高级「系统规划与管理师」考生论文进行模拟阅卷，按五维评分、75 分制折算、红线检查和 IMA 资料对照给出 Markdown 评分报告与改进建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External exam candidates and reviewers use this skill to evaluate draft System Planning and Management Engineer essays, estimate whether they pass the 75-point scoring model, and receive targeted revision guidance grounded in the bundled rubric and optional IMA knowledge-base lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scoring reports include an off-platform WeChat promotion unrelated to essay scoring.

Mitigation: Review the skill before installation and approve, remove, or disclose the promotion according to organizational policy.

Risk: User essays and project backgrounds may contain private personal, exam, or workplace details.

Mitigation: Redact sensitive information before scoring and do not send details to the advertised off-platform contact unless that channel is independently trusted.

Risk: IMA lookup can use essay or query context for retrieval when the user requests source-backed suggestions.

Mitigation: Use IMA retrieval only with user authorization and fall back to bundled reference files when retrieval is unavailable or inappropriate.

Risk: Simulated scores and reference-backed improvement advice could be mistaken for official grading or used to support dishonest writing.

Mitigation: Present outputs as advisory simulation only, keep the user's own project experience as the basis, and avoid copying retrieved reference essays.

## Reference(s):

- [Scoring Rubric](references/scoring_rubric.md)
- [IMA Knowledge Base Guide](references/ima_kb_guide.md)
- [Project Background Template](references/project_bg_template.md)
- [ClawHub Skill Page](https://clawhub.ai/chesaram/skills/ruankao-spgm-essay-scorer-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown scoring report with tables, red-line checks, pass/fail judgment, and revision recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source labels from the configured IMA knowledge base when lookup is authorized; otherwise relies on bundled reference files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
