## Description:

Parses medical device UDI strings, checks GS1 identifiers and dates, and identifies HIBCC and ICCBBA formats for preliminary review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Regulatory affairs and quality teams use this skill to spot malformed UDI strings and inspect GS1 identifiers, lot numbers, serial numbers, and dates before database submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Structural checks do not confirm that a UDI exists in a regulatory database.

Mitigation: Check UDI records against the relevant official regulatory database before relying on them.

Risk: HIBCC and ICCBBA identifiers are detected but not fully validated.

Mitigation: Use official issuing-agency tools for final HIBCC or ICCBBA verification.

Risk: The optional file input reads a user-supplied path.

Mitigation: Provide only intended local UDI files and review the results before use.

## Reference(s):

- [UDI Validator release on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/udi-validator)
- [Publisher profile on ClawHub](https://clawhub.ai/user/zhaoxinghua09-cell)
- [Agent Skills specification](https://agentskills.io)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain text validation results with per-field verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports detected issuing agency and parsed fields; can calculate a GTIN check digit.]

## Skill Version(s):

1.0.0 (source: ClawHub release; bundled skill frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
