## Description:

Codified expertise for returns authorization, receipt and inspection, disposition decisions, refund processing, fraud detection, and warranty claims management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nocodemf](https://clawhub.ai/user/nocodemf)

### License/Terms of Use:

Apache-2.0

## Use Case:

Returns, customer operations, logistics, and commerce teams use this skill to evaluate return requests, inspect and grade returned products, choose disposition paths, process refunds, detect fraud patterns, and manage vendor recovery or warranty claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer, order, warranty, or fraud details may expose sensitive information if copied into prompts or outputs unnecessarily.

Mitigation: Minimize or mask customer data, keep fraud notes internal, and follow company privacy rules before sharing or storing outputs.

Risk: Refund approvals, claim denials, seller actions, or fraud holds can affect customers and revenue if applied without review.

Mitigation: Use the skill as decision support and require human approval before issuing refunds, denying claims, suspending sellers, or reporting customers.

Risk: Returns, warranty, hazmat, and cross-border recommendations may depend on regional law and company policy.

Mitigation: Verify recommendations against applicable law, carrier requirements, vendor agreements, and the organization's current returns policy.

## Reference(s):

- [Decision Frameworks](references/decision-frameworks.md)
- [Communication Templates](references/communication-templates.md)
- [Edge Cases Reference](references/edge-cases.md)
- [Evaluation Rubric](evals/rubric.md)
- [Evaluation Results](evals/results/eval_results.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text with operational recommendations, decision frameworks, and communication drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include policy checks, grading rationale, disposition economics, fraud indicators, escalation guidance, and customer or internal message templates.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
