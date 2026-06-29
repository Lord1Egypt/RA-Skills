## Description: <br>
当用户说「深度研究 X」「深入研究 X」或要求生成某产品、公司、概念、人物、产业链、政策、趋势的深度研究/发展研究报告时触发，自动进行联网搜索和研究，产出排版后的 PDF 文档，总字数通常 1-3 万字。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiaranbb](https://clawhub.ai/user/jiaranbb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, analysts, and developers use this skill to plan, research, draft, source-check, and render structured Chinese-first deep research reports as PDF deliverables. It supports product, company, concept, person, industry-chain, policy, and trend research workflows with configurable local output paths and byline settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs online research through the agent and may collect incomplete or outdated material. <br>
Mitigation: Use the built-in scope alignment, latest-data check, source citation rules, and review checklist before relying on generated reports. <br>
Risk: The skill saves intermediate materials, Markdown drafts, logs, and PDFs under configured local output paths. <br>
Mitigation: Configure output directories deliberately and avoid placing private paths, account identifiers, or sensitive material in shared configuration or prompts. <br>
Risk: Generated PDFs include a fixed report-helper attribution and contact footer. <br>
Mitigation: Review the footer behavior before using reports as neutral, client-facing, or regulated deliverables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiaranbb/skills/report-helper) <br>
- [Project homepage](https://github.com/Jiaranbb/report-helper) <br>
- [Workflow](references/workflow.md) <br>
- [Report template](references/report-template.md) <br>
- [Source citation rules](references/source-citation-rules.md) <br>
- [Delivery](references/delivery.md) <br>
- [Review checklist](references/review-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown research drafts and source notes, local report files, optional log entries, and rendered PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.9+ and local PDF rendering dependencies such as markdown with WeasyPrint or a configured Chrome fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
