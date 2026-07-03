## Description: <br>
Analyzes class exam scores, generates visual charts and professional reports, and supports longitudinal comparison across multiple exams plus horizontal comparison with peer classes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yitutu](https://clawhub.ai/user/yitutu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Educators, school analysts, and developers use this skill to validate class exam data, compare performance across peer classes and exam periods, identify critical or subject-imbalanced students, and generate charts and Word reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process student grade records and write JSON, chart, report, and presentation outputs that may contain sensitive educational data. <br>
Mitigation: Use only with authorization for the student records involved, prefer de-identified inputs, restrict access to generated files, avoid broad report sharing, and delete outputs when they are no longer needed. <br>
Risk: Automatic header detection, score-line interpretation, or pass-line configuration errors could lead to misleading analysis or student recommendations. <br>
Mitigation: Require user verification of detected subject averages, student counts, anomalies, peer classes, and pass lines before analysis, then review generated reports before distribution. <br>


## Reference(s): <br>
- [Score Analysis Framework](references/analysis_framework.md) <br>
- [Score Analysis ClawHub Page](https://clawhub.ai/yitutu/score-analysis) <br>
- [matplotlib Documentation](https://matplotlib.org/) <br>
- [python-docx Documentation](https://python-docx.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python code and generated JSON, PNG chart, DOCX report, and optional PPTX artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow requires user verification of detected score data before analysis proceeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
