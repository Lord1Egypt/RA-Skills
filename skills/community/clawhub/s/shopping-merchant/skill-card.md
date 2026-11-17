## Description:

Evaluate which merchant type a shopper should trust on Chinese ecommerce platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to compare Chinese ecommerce merchant types and choose the safer purchase option based on product risk, authenticity sensitivity, after-sales support, warranty coverage, shipping reliability, and price gap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included night-market food-stall example broadens the skill beyond shopper-facing merchant trust decisions.

Mitigation: Remove or split that example so the released skill stays focused on ecommerce merchant selection.

Risk: Recommendations could overstate confidence because the skill does not verify live store pages or account-only platform information.

Mitigation: Base advice on user-provided facts, state uncertainty clearly, and avoid claiming real-time seller verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/shopping-merchant)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown recommendation with short rationale and risk tiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask one short clarifying question when product value, authenticity sensitivity, or after-sales importance is unclear.]

## Skill Version(s):

1.4.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
