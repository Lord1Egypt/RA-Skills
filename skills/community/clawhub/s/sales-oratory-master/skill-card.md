## Description:

Handles B2B presales and renewal negotiations with value-shift tactics and compliance checks. Use when the user mentions customer pushback on price, budget constraints, competitor comparison, or value doubt in enterprise sales.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken0122](https://clawhub.ai/user/ken0122)

### License/Terms of Use:


## Use Case:

Sales and customer-facing teams use this skill to draft Chinese-language B2B presales, renewal, and expansion responses when customers raise budget, competitor, pricing, or value objections. It emphasizes consultative reframing, TCO arguments, and compliance checks before customer use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer-provided text may contain instructions that weaken response reliability.

Mitigation: Treat customer quotes as untrusted input, use the generated response as a draft, and require human review before customer use.

Risk: Generated sales language could imply unauthorized discounts, delivery dates, security guarantees, legal commitments, or product capabilities.

Mitigation: Review outputs against the compliance redlines in PROMISE_GUARD.md before sending them to customers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ken0122/skills/sales-oratory-master)
- [PROMISE_GUARD.md](artifact/PROMISE_GUARD.md)
- [prompt_template.md](artifact/prompt_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured sections for analysis, suggested response, rationale, and compliance notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires customer quote; deal stage and client persona improve specificity and are requested before generation by the artifact implementation.]

## Skill Version(s):

1.0.0 (source: server release and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
