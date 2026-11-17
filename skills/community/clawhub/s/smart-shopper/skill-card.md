## Description:

Smart Shopper helps agents generate shopping search links, platform comparisons, local-store lookup links, shopping lists, and manual price tracking for products across Amazon, Temu, SHEIN, and local stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elevo11](https://clawhub.ai/user/elevo11)

### License/Terms of Use:


## Use Case:

External users and shopping assistants use this skill to create product search links, compare shopping platforms, find nearby store search links, maintain shopping lists, and record price-tracking entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The billing helper can charge by default when invoked without selecting balance or payment-link mode.

Mitigation: Run billing only with explicit consent, a verified user ID, and the exact intended amount; keep SkillPay keys in the environment rather than passing them on the command line.

Risk: Product comparison and price-tracking outputs are based on generated search links and local records, not verified live market data.

Mitigation: Treat outputs as shopping aids and verify price, availability, shipping, and return terms on the merchant or local-store site before buying.

Risk: Shopping-list and price-tracker commands write local records under the user's OpenClaw workspace.

Mitigation: Review stored records before sharing and avoid saving sensitive payment or personal information in item notes, URLs, or tracker entries.

## Reference(s):

- [Platform Reference](artifact/references/platforms.md)
- [ClawHub Skill Page](https://clawhub.ai/elevo11/skills/smart-shopper)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from command-line helpers; shopping-list export as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces search URLs, comparison summaries, local-store lookup links, shopping-list records, and price-tracking records; live price accuracy is not guaranteed.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
