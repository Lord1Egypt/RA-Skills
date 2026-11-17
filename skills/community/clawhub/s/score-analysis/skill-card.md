## Description:

Analyzes class exam scores and generates visual charts and professional reports with longitudinal exam comparisons and peer-class comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yitutu](https://clawhub.ai/user/yitutu)

### License/Terms of Use:

MIT

## Use Case:

Educators, school analysts, and external users can use this skill to validate class score data, compare results across exams or peer classes, identify critical students and subject imbalance, and generate shareable reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes student score files and generates reports that may contain sensitive student records.

Mitigation: Use a virtual environment, minimize student names or IDs where possible, share outputs only with authorized recipients, and delete generated files when no longer needed.

Risk: Incorrectly parsed score data or pass-line assumptions can lead to misleading analysis.

Mitigation: Require user confirmation of class counts, subject averages, total averages, absences, anomalies, pass lines, and peer classes before running analysis.

Risk: Unpinned dependencies can introduce reproducibility and supply-chain risk.

Mitigation: Prefer pinned versions for python-docx, matplotlib, pandas, numpy, and openpyxl in an isolated Python environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yitutu/skills/score-analysis)
- [Analysis Framework](references/analysis_framework.md)
- [matplotlib](https://matplotlib.org/)
- [python-docx](https://python-docx.readthedocs.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON data, generated charts, Word reports, optional presentation files, Python code, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files may include standardized data JSON, analysis JSON, chart images, Word reports, and optional presentation files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
