## Description:

Provides Chinese-language QMS internal and external environment analysis guidance and local report generation for ISO 9001 audit and management review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality managers, auditors, and QMS engineers use this skill to structure internal and external context analysis, identify risks and opportunities, and generate SWOT/PESTEL charts and PDF reports from prepared JSON data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided QMS data may include confidential business context, and generated charts or PDF reports are written to a local output directory.

Mitigation: Use private output paths for sensitive analyses, avoid shared locations, and review generated files before distribution.

Risk: The Chinese-language templates and examples may not match every organization's terminology, regulatory context, or QMS procedures.

Mitigation: Review the templates for organizational fit and adapt the analysis fields before using outputs in audits or management reviews.

## Reference(s):

- [QMS analysis templates and data format](references/analysis-templates.md)
- [Analysis generator script](scripts/generate_analysis.py)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-qms-environment-analysis)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-qms-environment-analysis)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; local PNG charts and PDF report when the script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided JSON and writes swot_matrix.png, pestel_radar.png, risk_matrix.png, and qms_environment_report.pdf to the selected output directory.]

## Skill Version(s):

1.1.0 (source: frontmatter and release changelog; ClawHub release metadata: 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
