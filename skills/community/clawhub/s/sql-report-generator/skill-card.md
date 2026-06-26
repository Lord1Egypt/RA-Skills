## Description: <br>
Generates production-style SQL query result and chart reports with tables, matrices, slicers, multi-format exports, and statistics-driven insight recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqlskills](https://clawhub.ai/user/sqlskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business teams use this skill to turn SQL query outputs, tabular data, and chart artifacts into reusable operational, financial, product, marketing, and executive reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports may include untrusted data or report text. <br>
Mitigation: Use trusted inputs or sanitize and escape report text before opening or sharing generated HTML. <br>
Risk: Customer profiling or SMS/push marketing recommendations may raise privacy, consent, or legal review needs. <br>
Mitigation: Review privacy and legal requirements before acting on those recommendations and use only approved data. <br>
Risk: The skill installs local Python dependencies with version ranges. <br>
Mitigation: Pin and review dependencies in a controlled environment before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sqlskills/sql-report-generator) <br>
- [Chart Guidelines](artifact/references/chart-guidelines.md) <br>
- [Chart Planning](artifact/references/chart-planning.md) <br>
- [Insight Patterns](artifact/references/insight-patterns.md) <br>
- [Templates Index](artifact/references/templates-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python examples; generated report artifacts may be HTML, JSON, Markdown, or image-embedded files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python dependencies including pandas, numpy, matplotlib, and jinja2.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
