## Description:

Constructs compliant test products by finding or cloning virtual items, adjusting prices, and cleaning item tags based on category, business identity, attributes, and tag requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpu-hammer](https://clawhub.ai/user/cpu-hammer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test operators use this skill to locate or construct virtual test products for commerce workflows, including category and attribute matching, test-account cloning, price updates, and tag cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger product-management actions including cloning, repricing, listing-state changes, and tag changes.

Mitigation: Require explicit user confirmation before each mutating action and verify that the target item is a test item immediately before mutation.

Risk: The skill depends on backing internal services to enforce test-only restrictions.

Mitigation: Install and run it only when the publisher and backing services are trusted to enforce those restrictions server-side.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cpu-hammer/skills/virtual-item-constructor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and a structured final product summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful results may include item ID, title, price, test seller, item tags, and an item URL.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
