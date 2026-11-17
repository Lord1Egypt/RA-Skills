## Description:

A requirement gate checker for requirement completeness, acceptance criteria, and scope validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terr123123](https://clawhub.ai/user/terr123123)

### License/Terms of Use:

MIT

## Use Case:

Developers and product teams use this skill before requirement review or design handoff to check whether requirement objects have complete fields, measurable and testable acceptance criteria, and clear in-scope and out-of-scope boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation is primarily Chinese, which may lead to incorrect configuration or review expectations for teams that do not read Chinese.

Mitigation: Review or translate the documentation before deployment and confirm the configured thresholds match the intended requirement-review policy.

Risk: Requirement gate results can be mistaken for final approval even though they only check structural completeness, measurable criteria, and scope boundaries.

Mitigation: Use the results as an advisory pre-review signal and keep human requirement review as the approval authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terr123123/skills/requirement-gate)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Python objects and human-readable validation messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns per-check pass status, scores, messages, and details for completeness, acceptance criteria, and scope-boundary checks.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
