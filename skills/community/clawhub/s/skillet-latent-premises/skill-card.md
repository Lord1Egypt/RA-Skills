## Description:

Reviews diffs or modules for hidden assumptions that are not enforced and could break under future inputs or changes; the review is read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this read-only review when examining a diff or module to identify unenforced assumptions, explain the concrete failure if one stops holding, and recommend a focused resolution. It complements reviews for defects that can already be triggered today.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review does not include separately installed companion skills or shared documentation, so their behavior is outside its assessed scope.

Mitigation: Review those components separately before authorizing changes that rely on them.

## Reference(s):

- [Alp-River correctness reviewer taxonomy reference](https://github.com/alp82/alp-river)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only findings with concrete failure conditions and one recommended resolution per finding.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
