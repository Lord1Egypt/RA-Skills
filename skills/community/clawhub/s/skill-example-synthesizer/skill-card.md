## Description:

Generates reviewable positive, negative, edge-case, mis-trigger, documentation placement, and maintenance examples for skills to improve routing and clarity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to draft structured examples and anti-examples for skill documentation, routing, and release preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples can introduce incorrect or misleading routing guidance if accepted without review.

Mitigation: Review generated examples against the source skill before publishing or release.

Risk: Input snippets may appear in generated reports.

Mitigation: Redact personal, confidential, or sensitive material before using the skill.

Risk: The bundled script includes broader audit helpers beyond the default packaged mode.

Mitigation: Run the script only with intended local inputs and review generated output before relying on helper modes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/skill-example-synthesizer)
- [README](artifact/README.md)
- [Output template](artifact/resources/template.md)
- [Structured specification](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown by default, with optional JSON from the bundled local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewable drafts from local input; the script can write the generated report to a requested output file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
