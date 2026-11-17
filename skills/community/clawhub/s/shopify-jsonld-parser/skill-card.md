## Description:

Parse JSON-LD structured data from Shopify product pages to extract product information, offers, pricing, currency, availability, and inventory status from schema.org Product and Offer data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce analysts use this skill to inspect Shopify or schema.org Product HTML and extract structured product, offer, price, and availability data. It is useful for agent workflows that need to fetch or read product pages, run a local parser, and summarize JSON-LD commerce signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The parser is reported as broken or overstated in places, including Python syntax and CLI option issues.

Mitigation: Treat the skill as nonfunctional until the parser syntax and documented CLI options are corrected and tested.

Risk: The workflow asks the agent to fetch or read Shopify HTML, write a temporary local file, and run a local parser on that input.

Mitigation: Use trusted or reviewed HTML inputs, keep temporary files scoped, and avoid piping untrusted text into the no-argument mode.

Risk: Inventory output reflects schema.org availability values, not exact stock quantity, and static HTML may omit JavaScript-rendered data.

Mitigation: Use the parsed availability as a structured-data signal and rely on Shopify APIs or other authoritative sources for exact inventory levels.

## Reference(s):

- [Schema.org Product/Offer Reference](artifact/references/schema.md)
- [Schema.org Product](https://schema.org/Product)
- [ClawHub Skill Page](https://clawhub.ai/igorganapolsky/skills/shopify-jsonld-parser)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, JSON]

**Output Format:** [Markdown guidance with shell commands; parser output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parser reads static HTML from a local file and returns product records or an error object.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
