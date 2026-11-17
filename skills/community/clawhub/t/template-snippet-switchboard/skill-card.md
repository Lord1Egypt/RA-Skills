## Description:

Manages reusable templates and snippets, switching them by scenario, role, tone, and length while maintaining versioned, reviewable outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and writing teams use this skill to organize reusable writing templates, customer-service snippets, and sales scripts into structured Markdown drafts with scenarios, role variants, tone switches, maintenance rules, and retirement criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script includes local audit and pattern-scanning behavior that can inspect files beyond simple template formatting.

Mitigation: Review the script before installation and run it only on non-sensitive inputs or inside a constrained workspace.

Risk: The broader audit modes are under-documented relative to the template-management description.

Mitigation: Require the publisher to remove or clearly document the extra modes before relying on the skill in shared or production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/template-snippet-switchboard)
- [README](artifact/README.md)
- [Output template](artifact/resources/template.md)
- [Structured spec](artifact/resources/spec.json)
- [Smoke test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report by default, or a JSON object containing the generated report when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local input and bundled template/spec files; the optional script can write the report to a local output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
