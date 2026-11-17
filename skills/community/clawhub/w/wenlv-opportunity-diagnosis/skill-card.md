## Description:

文旅项目机会诊断能力包基于“五维决策门 + 政策红线一票否决”框架，对文化旅游项目做投资前 go/no-go 初步判断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmh18518339959](https://clawhub.ai/user/hmh18518339959)

### License/Terms of Use:

MIT-0

## Use Case:

External project owners, investors, operators, planners, and cultural tourism teams use this skill to collect project facts, screen policy red lines, evaluate five opportunity dimensions, and decide whether a project should proceed, proceed with conditions, or stop before deeper execution work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces business, compliance, and investment screening conclusions that could be mistaken for final professional advice.

Mitigation: Treat outputs as preliminary diagnostics and verify legal, regulatory, financial, and site-specific conclusions with qualified professionals and competent authorities before acting.

Risk: The skill asks for project, finance, location, market, and operational details that may be sensitive.

Mitigation: Share only the minimum project information needed for screening and avoid unnecessary confidential financial or business details.

Risk: Broad project feasibility prompts may trigger the skill when the user did not intend a structured diagnostic workflow.

Mitigation: Confirm that the user wants this skill used before applying it to broad feasibility or opportunity-assessment requests.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hmh18518339959/skills/wenlv-opportunity-diagnosis)
- [文旅项目机会诊断 · 信息采集表](artifact/references/data_collection_form.md)
- [门0 · 政策合规红线核查清单](artifact/references/redline_policy.md)
- [门1-5 · 五维决策路径](artifact/references/diagnostic_rubric.md)
- [文旅项目五维决策门 · 诊断报告](artifact/assets/diagnosis_report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown diagnosis report with optional structured JSON input and text output from the diagnostic helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces preliminary screening guidance only; policy conclusions must be confirmed with competent authorities.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
