## Description:

Validate a SKILL.md before publishing by checking frontmatter completeness, semver, and whether every declared binary resolves on PATH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonting1010](https://clawhub.ai/user/leonting1010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to preflight a SKILL.md before publishing or troubleshooting missing requirements. It returns a machine-readable result that identifies manifest, version, and declared binary checks that pass or fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a real validation bug in the SKILL.md frontmatter parsing, so ok:true is only a convenience signal and not a full security or correctness guarantee.

Mitigation: Treat results as preflight guidance, review the SKILL.md manually before publishing, and use hierarchy-aware validation before relying on the check as a release gate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leonting1010/skills/tap-skill-preflight)
- [Publisher Profile](https://clawhub.ai/user/leonting1010)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled checker emits JSON containing ok, reason, and checks fields, with exit codes 0 for pass, 1 for validation failure, and 2 for usage or I/O error.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
