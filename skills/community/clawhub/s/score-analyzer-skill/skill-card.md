## Description:

Analyze student score data from Excel files and generate professional analysis reports with data cleaning, statistical analysis, charts, narrative reporting, and packaged outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and school data staff use this skill to turn Excel score sheets into cleaned datasets, statistical diagnostics, charts, and professional student score reports. It is suited for exam, grade, and class-performance analysis where generated conclusions should be reviewed before distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Student score spreadsheets and generated reports may contain sensitive educational records.

Mitigation: Confirm the agent should access the spreadsheet and local output directory before installation or execution.

Risk: Generated conclusions may overstate causality or include unsupported educational recommendations.

Mitigation: Review generated conclusions before sharing and remove unsupported causal claims.

Risk: Optional system package installation may be requested for Chinese font rendering.

Mitigation: Approve package installation such as fonts-noto-cjk only when chart rendering requires it.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/flyboat403/score-analyzer-skill)
- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/score-analyzer-skill)
- [Analysis prompt reference](references/analysis_prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated report artifacts may include Markdown, HTML, DOCX, PNG charts, CSV/JSON data, and a ZIP package.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local report files under a reports directory and uses chart placeholders that must be replaced during assembly.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
