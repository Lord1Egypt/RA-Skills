## Description:

Batch-generates customer support reply templates with a consistent empathetic tone, action statements, boundaries, and escalation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Support, customer-success, and operations teams use this skill to draft reviewable customer service macro sets from issue types, brand voice, and prohibited wording. It is intended for template drafting and review workflows, not direct sending, publishing, or external system changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local helper can read the input path selected by the user, which may include sensitive customer or private workspace content.

Mitigation: Use a narrow, purpose-built input file and remove secrets or unnecessary personal data before running the skill.

Risk: The local helper can write or overwrite the output file selected by the user.

Mitigation: Use stdout, dry-run, or a dedicated workspace output path when reviewing generated macros.

Risk: Generated customer support language could contain unsupported promises or wording that is not approved for the brand or policy context.

Mitigation: Review generated macros before formal use and confirm missing facts, escalation rules, and prohibited wording.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/support-macro-crafter)
- [README](artifact/README.md)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)
- [Example output](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance, files]

**Output Format:** [Structured Markdown by default, with optional JSON output from the local helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local helper reads a user-selected input file or inline input and can write stdout or a user-selected output file; generated macros require human review before operational use.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
