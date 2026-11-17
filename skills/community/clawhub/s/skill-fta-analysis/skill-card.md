## Description:

故障树分析技能 supports system reliability and safety analysis through fault-tree construction, visualization, probability calculation, importance analysis, report generation, and JSON/YAML import and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reliability engineers, and quality teams use this skill to build and analyze fault trees, calculate top-event probabilities and importance rankings, visualize system failure paths, and generate quality analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted fault-tree input can become executable content in generated HTML reports.

Mitigation: Use trusted FTA files, keep outputs in a controlled project folder, and avoid opening or sharing generated HTML reports from untrusted data until report text fields are escaped.

Risk: Malformed trees can crash the calculator, especially in automated or high-volume use.

Mitigation: Validate DAG structure, probability ranges, and input size before running calculations at scale; add shared validation and resource limits for service use.

## Reference(s):

- [Fault-tree data format reference](references/fta_format.md)
- [Source repository](https://github.com/duding-engicool/skill-fta-analysis)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-fta-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; generated artifacts may include JSON, YAML, PNG, SVG, PDF, and HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local scripts read user-provided fault-tree data and write analysis, visualization, conversion, or report files.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
