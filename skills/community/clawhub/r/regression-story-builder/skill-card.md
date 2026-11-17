## Description:

Generates regression test story sets, risk levels, and priorities from historical issue inputs for regression, testing, and QA workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and release reviewers use this skill to turn historical bugs, affected modules, and release timing into reviewable regression stories, high-risk scenarios, priorities, triggers, acceptance signals, and supplementary data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input issue histories or test-planning files may contain private or sensitive information.

Mitigation: Use the skill only with files intended for the local agent, and redact sensitive material before sharing or generating reports.

Risk: The bundled script can write generated reports to a chosen output path.

Mitigation: Prefer stdout or --dry-run while reviewing results, and provide an explicit output path only when file creation is intended.

Risk: The package is Chinese-first and includes inactive broader audit routines.

Mitigation: Review localized output for the target audience, and avoid using audit modes on broad private directories unless intentionally scoped.

Risk: Regression stories may be mistaken for executed test results.

Mitigation: Treat outputs as planning drafts and review checklists; do not represent them as completed test execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/regression-story-builder)
- [Skill README](artifact/README.md)
- [Output Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown report, with optional JSON output from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are reviewable drafts and checklists; the bundled script can print to stdout, dry-run, or write to a deliberate output path.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
