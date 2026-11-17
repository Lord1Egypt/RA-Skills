## Description:

Generates smoke-test templates for skills that cover missing dependencies, empty inputs, and standard execution paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to draft reviewable smoke-test plans before release or during regression maintenance. It helps organize normal-path, missing-dependency, empty-input, output-validation, and regression checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated smoke-test drafts can be incomplete or misleading when the input skill description, dependencies, or entrypoint are missing.

Mitigation: Review the Markdown output before using it and resolve any listed missing information before release.

Risk: Sensitive skill details included in input can be carried into the generated Markdown or JSON output.

Mitigation: Redact sensitive input unless it is necessary for the smoke-test draft.

Risk: The script contains broader local audit/report modes in addition to the shipped smoke-test template mode.

Mitigation: Use the default structured-brief behavior for normal smoke-test drafting and review outputs from alternate modes before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/skill-smoke-test-author)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Skill Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown by default, with optional JSON from the local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write a local output file when an output path is provided.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
