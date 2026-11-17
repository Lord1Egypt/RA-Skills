## Description:

Use after a timeout or ambiguous receipt; reconcile the original delivery and give one bounded next step without resending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tdw8147-crypto](https://clawhub.ai/user/tdw8147-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and support staff use this skill to reconcile an ambiguous outbound delivery from the original request and receipt evidence. It helps them produce a concise status record, close cases when acceptance is met, or name one bounded lookup without resending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Request and receipt evidence may contain sensitive information when shared with hosted chat services.

Mitigation: Before sharing, remove or redact personal, confidential, and attachment details that are not needed for reconciliation.

Risk: An ambiguous timeout or mismatched receipt could lead to a duplicate delivery if the request is replayed.

Mitigation: Use a bounded, read-only lookup for the original request; if identity or status remains unresolved, record the outcome as unknown and stop without resending.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tdw8147-crypto/skills/unknown-delivery-reconciliation)
- [Evaluation evidence (EVIDENCE.md)](https://github.com/tdw8147-crypto/skill-delivery-kit/blob/main/EVIDENCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown status record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based conclusion with at most one bounded follow-up query; does not resend the original request.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
