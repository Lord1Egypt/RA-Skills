## Description:

Reviews serde serialization code for derive patterns, enum representations, custom implementations, and common serialization bugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Rust serde serialization code for derive usage, enum representation, field attributes, custom serialization, format-specific issues, and round-trip correctness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects local Rust project files, so review quality depends on current Cargo.toml context and file-level evidence.

Mitigation: Limit review to the intended Rust project, confirm serde and format-crate context from Cargo.toml, and require current file:line citations for each finding.

## Reference(s):

- [Derive Patterns](references/derive-patterns.md)
- [Custom Serialization](references/custom-serialization.md)
- [Serde Code Review on ClawHub](https://clawhub.ai/anderskev/skills/serde-code-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown issue report with file:line citations and severity labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings follow the skill's required ISSUE_TITLE, Severity, and description structure.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
