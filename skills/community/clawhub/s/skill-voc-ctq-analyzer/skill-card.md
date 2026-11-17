## Description:

Converts customer voice feedback (VOC) into critical-to-quality (CTQ) characteristics through text analysis, requirement extraction, mapping, prioritization, and visual reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, product, and support teams use this skill to analyze customer feedback, extract CTQ candidates, map VOC items to CTQs, prioritize improvements, and generate JSON and HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include user-controlled CTQ names, and customer-feedback outputs may contain sensitive business or customer data.

Mitigation: Keep input and output paths in a controlled workspace, review or redact generated JSON and HTML before sharing, and avoid opening reports from untrusted CTQ data.

## Reference(s):

- [Source repository](https://github.com/duding-engicool/skill-voc-ctq-analyzer)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-voc-ctq-analyzer)
- [VOC-CTQ data format specification](references/format_spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python command examples; generated analyzer outputs include JSON and HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow supports VOC import, analysis, CTQ extraction, mapping, scoring, and visualization modes.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
