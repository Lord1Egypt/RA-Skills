## Description:

Turns coding changes into risk-tiered requirements, design, and task plans with approval receipts and a resumable decision ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vxncxnx](https://clawhub.ai/user/vxncxnx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to plan, approve, and carry out feature, bug, or quick changes in a repository while preserving decisions and task traceability across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing or incorrect repository overlay can misclassify sensitive changes or omit deployment safeguards.

Mitigation: Review the repository overlay before use; specify high-risk surfaces, deployment steps, and hard stops.

Risk: An agent may execute tasks against changed or unapproved plans.

Mitigation: Review each required gate and run the approval validator before execution; stop if verification fails.

## Reference(s):

- [Worked spec example](references/example-spec.md)
- [Preuve](https://preuve.ai)
- [Spec skill on ClawHub](https://clawhub.ai/vxncxnx/skills/spec-skill)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands]

**Output Format:** [Markdown planning documents and JSON approval ledger; code changes after approval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Approval receipts are tied to document hashes; tasks include verification steps.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
