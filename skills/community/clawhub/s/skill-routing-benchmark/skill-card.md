## Description:

Tests whether multiple Skill descriptions could create routing conflicts and generates positive examples, negative examples, revision suggestions, priorities, and regression test cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill during Skill design and release review to evaluate routing overlap, draft trigger examples, and prepare regression cases from provided Skill descriptions and target tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input files or directories may contain sensitive or personal information that could be summarized into generated reports.

Mitigation: Use intentionally scoped, redacted inputs and review generated Markdown or JSON before sharing it.

Risk: When an output path is provided, the local script can write a report to that path.

Mitigation: Use dry-run or stdout for review first, and write only to a dedicated output file.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/skill-routing-benchmark)
- [README](artifact/README.md)
- [Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)
- [Smoke Test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON reports, with optional shell command guidance for the local Python script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates review-oriented structured sections for potential conflicts, positive examples, negative examples, description suggestions, priorities, regression tests, pending confirmations, and next steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
