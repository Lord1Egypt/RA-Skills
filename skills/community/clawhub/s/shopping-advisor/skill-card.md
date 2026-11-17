## Description:

Shopping Advisor compares products, explains price gaps, judges purchase value, suggests better alternatives, flags common pitfalls, and ends with a direct shopping recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn shopping inputs such as product links, titles, screenshots, descriptions, and structured product data into concise buying advice. It supports comparing candidates, judging a single product, or choosing a buying direction when no candidate has been selected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping advice may be based on stale or incomplete product data, including prices, seller details, reviews, and after-sales terms.

Mitigation: Verify live prices, SKU details, seller identity, return policy, and review signals before making a purchase.

Risk: Formatted product text from untrusted sources can make advice appear more authoritative than the evidence supports.

Mitigation: Treat product text and generated Markdown as advisory, and avoid passing untrusted product text into workflows that execute commands or blindly trust formatted output.

Risk: The skill gives recommendations but is not designed to place orders, make payments, or make the final purchasing decision for the user.

Mitigation: Keep payment and order submission outside the skill workflow and require the user to confirm the final transaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/shopping-advisor)
- [Decision Lens](references/decision-lens.md)
- [Demo Scenarios](references/demo-scenarios.md)
- [Platform Notes](references/platform-notes.md)
- [Shopping Advisor schema](https://openclaw.dev/schemas/shopping-advisor.schema.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance and JSON decision reports, with optional shell command examples for the local demo flow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The demo schema limits shopping candidates to 20 and evidence items per candidate to 50.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, clawhub.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
