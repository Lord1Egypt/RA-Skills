## Description:

专业心理测评助手，提供 PHQ-9、GAD-7、PSS-10、RSES 和 BFI-10 的交互式答题、自动评分和可视化 HTML 评估报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to complete Chinese-language self-screening questionnaires for depression, anxiety, perceived stress, self-esteem, and Big Five personality traits, then receive scored results and a visual HTML report. It is a screening and self-understanding workflow, not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private mental-health answers and creates a sensitive HTML report.

Mitigation: Ask for explicit consent before starting, explain what information will be collected, and tell the user that an HTML report will be generated and previewed or delivered.

Risk: Generated reports may be written to an unexpected location or exposed through preview/delivery behavior.

Mitigation: Restrict or confirm output paths before writing the report and avoid encouraging users to share the generated file.

Risk: Report generation has an HTML-injection weakness when rendering report data.

Mitigation: Escape or validate all report data before injecting it into HTML templates.

## Reference(s):

- [心理测评量表参考数据](artifact/references/scales.md)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/psycho-assess)

## Skill Output:

**Output Type(s):** [text, JSON, HTML, shell commands, guidance]

**Output Format:** [Interactive questionnaire text, JSON scoring results, shell command invocations, and a generated HTML report file with brief human-facing summary guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces previewable and deliverable HTML reports that may contain sensitive mental-health answers and scores.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
