## Description:

当用户说「深度研究 X」「深入研究 X」或要求生成某产品、公司、概念、人物、产业链、政策、趋势的深度研究/发展研究报告时触发，自动进行联网搜索和研究，产出排版后的 PDF 文档，总字数通常 1-3 万字。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiaranbb](https://clawhub.ai/user/jiaranbb)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to guide an agent through Chinese-language deep research, source review, structured report drafting, and PDF delivery for products, companies, concepts, people, industries, policies, or trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forces a publisher contact footer into every PDF.

Mitigation: Remove or make the footer optional before using generated PDFs for professional or external reports.

Risk: Report Markdown is rendered into HTML and PDF without a sanitization step called out by the security review.

Mitigation: Render only trusted or sanitized Markdown in a sandboxed environment with restricted file and network access.

Risk: The skill uses web research through the host agent and writes intermediate files, drafts, PDFs, and optional logs locally.

Mitigation: Review the skill before installation and configure local output, work, intermediate, and log paths so sensitive information is not exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiaranbb/skills/report-helper)
- [Project homepage](https://github.com/Jiaranbb/report-helper)
- [研究与写作 Workflow](references/workflow.md)
- [Research Worker Prompt Template](references/subagent-research-prompt.md)
- [报告正文结构模板](references/report-template.md)
- [信息来源编号规则](references/source-citation-rules.md)
- [交付流程](references/delivery.md)
- [审核清单](references/review-checklist.md)
- [写作风格指南](references/writing-style.md)
- [按研究对象调整侧重点](references/adaptations-by-type.md)
- [踩坑记录](references/gotchas.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown research materials, internal Markdown drafts, PDF reports, optional log entries, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local configuration for output paths and report author; final PDF output includes a fixed tool signature.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
