## Description:

Validates, stress-tests, and certifies OpenClaw skills against a 10-dimension quality framework before release or upgrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this skill to audit skill quality, design stress tests, run regression checks, and produce QA reports that approve, reject, or request fixes before a skill is shipped.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses broad gatekeeper language that could be mistaken for external publishing authority.

Mitigation: Use its approval or rejection as an internal QA signal and require explicit human or platform review for release decisions.

Risk: QA reports may contain incorrect or misleading recommendations if the target skill or test context is incomplete.

Mitigation: Review the generated QA report against the target skill source, relevant references, and release criteria before acting on required fixes or certification status.

## Reference(s):

- [Quality Framework Detail](references/quality-framework.md)
- [Certification Standards](references/certification-standards.md)
- [Test Design Guide](references/test-design.md)
- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/quality-assurance)
- [Publisher profile](https://clawhub.ai/user/pmuhammadagus-byte)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown QA reports with scoring tables, stress-test results, required fixes, strengths, weaknesses, recommendations, and certification verdicts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewer-facing quality assessments; it does not execute code or call external tools by itself.]

## Skill Version(s):

1.0.0 (source: _meta.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
