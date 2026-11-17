## Description:

Turn rough workflows into standard operating procedures with roles, inputs, outputs, checkpoints, and exception handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and operations teams use this skill to turn rough workflow notes into usable SOP drafts, quick-start instructions, role matrices, and exception appendices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SOP drafts may be mistaken for approved operating procedures.

Mitigation: Review generated drafts with the responsible process owner before using them as official procedures.

Risk: The local helper writes an outline file to the path provided by the user.

Mitigation: Use an explicit output path and review the destination before running the helper.

## Reference(s):

- [SOP template resource](resources/sop_template.md)
- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/sop-factory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown and structured JSON outline files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled Python helper can write a local SOP outline JSON file when explicitly run with an output path.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
