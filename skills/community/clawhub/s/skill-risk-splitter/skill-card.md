## Description:

Skill Risk Splitter helps developers split over-broad agent skills into safer, enhanced, or multiple focused sub-skills to reduce scanning and maintenance risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review over-broad skills, identify risk sources, and plan splits into safer or more focused skill variants before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can summarize or audit files selected by the user, including sensitive local content if pointed at sensitive directories.

Mitigation: Use it only on intended inputs, redact sensitive material first, and avoid pointing it at private directories unless those files should be reviewed.

Risk: The support script can write generated reports to a user-selected output path.

Mitigation: Review the output path before writing and use dry-run or stdout output when checking behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/skill-risk-splitter)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)
- [Smoke test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local Python script can print to stdout, perform dry runs, or write reports to a user-selected output path.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
