## Description:

Supports TH-BIO-001 bio-domain criteria for assessing agent memory-transfer identity and accountability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Agents and reviewers use this skill when explicitly asked to apply UIBC's TH-BIO-001 bio-domain criteria to memory-transfer identity, evidence, failure handling, and accountability. A local checker can confirm the criteria document's required structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic mentions of memory transfer or responsibility may invoke the wrong domain-specific criteria.

Mitigation: Use only for explicit TH-BIO-001 or bio-domain accountability requests; clarify ambiguous requests first.

Risk: A passing structural check may be mistaken for substantive proof of identity or accountability.

Mitigation: Treat PASS as confirmation of the criteria document's structure; review the underlying evidence and conclusion separately.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/uibc-team-bio)
- [TH-BIO-001 criteria summary](artifact/判据_BIO.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Text]

**Output Format:** [Markdown analysis and plain-text PASS/FAIL checker results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a judging rule, evidence package, failure response, and accountability statement.]

## Skill Version(s):

1.1.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
