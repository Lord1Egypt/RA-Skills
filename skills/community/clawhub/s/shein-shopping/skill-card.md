## Description:

Help users make safer SHEIN shopping decisions based on style intent, price sensitivity, fit expectations, and quality-risk awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for public shopping decision support when deciding whether SHEIN fits their style goals, budget, fit expectations, and tolerance for quality variance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake public shopping guidance for live account, checkout, order, coupon, or logged-in page support.

Mitigation: Keep the skill limited to public decision support and route live prices, checkout state, orders, coupons, and logged-in pages to an explicitly user-controlled browser workflow.

Risk: SHEIN recommendations can be misleading when fit, material expectations, or quality variance differ by item.

Mitigation: Include fit and quality caveats and advise users to verify sizing, materials, return terms, and item-specific details before purchasing.

## Reference(s):

- [Fit Guide](references/fit-guide.md)
- [Output Patterns](references/output-patterns.md)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown recommendation with rationale, caveats, and final advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No account access, credential handling, browser automation, local persistence, or live checkout-state retrieval.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
