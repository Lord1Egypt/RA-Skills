## Description:

A Chinese-language real estate market research workflow that guides agents through project definition, report outlining, evidence-backed drafting, quality review, and Word document export for residential, commercial, office, industrial, and REITs-related reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoar12](https://clawhub.ai/user/hoar12)

### License/Terms of Use:

MIT-0

## Use Case:

External users and real estate professionals use this skill to produce structured market research, feasibility, investment return, competitor comparison, SWOT, operating forecast, and REITs-support reports. The workflow is designed for agent-assisted drafting with human confirmation at planning, review, and delivery checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run local commands and install dependencies.

Mitigation: Use a dedicated workspace, review each command before execution, and pin dependencies or use reviewed lockfiles.

Risk: The workflow may use external search while handling real estate client, deal, or account information.

Mitigation: Avoid entering confidential data unless authorized and comfortable with the search and data-handling environment.

Risk: The workflow creates, merges, exports, and may commit persistent report artifacts.

Mitigation: Confirm file paths and generated content before saving, exporting, merging, or committing report files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hoar12/skills/real-estate-report-workflow)
- [Publisher Profile](https://clawhub.ai/user/hoar12)
- [Complete Workflow](artifact/references/core_workflow.md)
- [Execution Guardrail Protocol](artifact/references/protocol.md)
- [Writing Principles](artifact/references/writing_principles.md)
- [Macro Background Analysis Rules](artifact/references/section_rules/01_宏观背景分析.md)
- [Market-Level Analysis Rules](artifact/references/section_rules/02_中观市场分析.md)
- [Micro Market Analysis Rules](artifact/references/section_rules/03_微观市场分析.md)
- [Competitor Comparison Rules](artifact/references/section_rules/04_竞品对比.md)
- [SWOT Analysis Rules](artifact/references/section_rules/05_SWOT分析.md)
- [Operating Forecast Rules](artifact/references/section_rules/06_运营预测.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report drafts with tables, review findings, shell command snippets, generated project files, and optional Word document export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python and Node scripts for report checks and document export when the user approves the workflow.]

## Skill Version(s):

1.5.6 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
