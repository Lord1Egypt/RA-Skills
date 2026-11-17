## Description:

基于候选人真实经历生成风格化 PDF 简历，按 5 种 Skills 风格（双栏分类/侧栏pill/极简竖列/标签云/熟练度条）生成或优化简历、把项目经历写成有卖点不简化、支持还原 skills 结构与批量转 PDF。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yll-kb](https://clawhub.ai/user/yll-kb)

### License/Terms of Use:

MIT-0

## Use Case:

Job applicants and career-support agents use this skill to generate or optimize stylized, application-ready resume drafts while preserving supplied project details, ordering, and claims. It is also useful for creating several skills-section layouts and conversion guidance for HTML-to-PDF resume delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive resume details and the security evidence notes conflicting directions about using real details versus anonymized samples.

Mitigation: Confirm whether the task is for anonymized sample resumes or a real application before collecting details; only include personal, education, company, project, and metrics data the user intentionally provides.

Risk: Generated HTML or PDF resumes can expose personal information if shared through cloud, database, or external workflows without review.

Mitigation: Keep generated HTML and PDF files local unless the user explicitly approves a sharing, cloud, or database workflow.

Risk: Resume claims can become misleading if the agent embellishes beyond the candidate's supplied facts.

Mitigation: Use only user-provided projects, technologies, education, and metrics, and have the user review final claims before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yll-kb/skills/resume-styles-kit)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with HTML/CSS, Python, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce resume layout variants, HTML-to-PDF conversion steps, and final-review checklists; generated resume files should be reviewed locally before sharing.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
