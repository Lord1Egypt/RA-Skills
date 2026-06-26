## Description: <br>
AI-assisted workflow for producing professional Chinese real-estate market research reports across residential, commercial, office, industrial, feasibility, investment-return, REITs, competitor-comparison, SWOT, and operations-forecasting use cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoar12](https://clawhub.ai/user/hoar12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and real-estate consulting teams use this agent skill to structure, draft, review, and export market research reports with staged project definition, framework design, source-backed writing, quality checks, and Markdown-to-DOCX delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create local Markdown and DOCX files and merge report parts. <br>
Mitigation: Run it in a dedicated project folder and review output paths before export. <br>
Risk: The workflow relies on web research and market data that may be incomplete, stale, or inconsistent. <br>
Mitigation: Review cited sources and use the built-in L1/L2/L3 checks for key data, logic, and external validation before delivery. <br>
Risk: The workflow can install dependencies and run bundled Python and Node scripts. <br>
Mitigation: Approve dependency installation and script execution explicitly, and inspect commands before running them. <br>
Risk: Real-estate reports may contain sensitive client, project, or transaction information. <br>
Mitigation: Avoid sensitive client data in shared workspaces and limit access to generated report files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hoar12/real-estate-report-workflow) <br>
- [README](README.md) <br>
- [Core Workflow](references/core_workflow.md) <br>
- [Execution Guardrail Protocol](references/protocol.md) <br>
- [Writing Principles](references/writing_principles.md) <br>
- [Macro Background Analysis Rules](references/section_rules/01_宏观背景分析.md) <br>
- [Mid-Market Analysis Rules](references/section_rules/02_中观市场分析.md) <br>
- [Micro-Market Analysis Rules](references/section_rules/03_微观市场分析.md) <br>
- [Competitor Comparison Rules](references/section_rules/04_竞品对比.md) <br>
- [SWOT Analysis Rules](references/section_rules/05_SWOT分析.md) <br>
- [Operations Forecast Rules](references/section_rules/06_运营预测.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, report-part files, quality-check output, shell commands, and DOCX exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local files, run Python and Node scripts, perform web research, and export Word documents when the host agent provides the required tools and approvals.] <br>

## Skill Version(s): <br>
1.5.6 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
