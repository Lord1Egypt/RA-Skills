## Description: <br>
Parse JSON-LD structured data from Shopify product pages to extract product information, offers, pricing, currency, availability, and inventory status from schema.org Product and Offer data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, ecommerce operators, and agents use this skill to analyze Shopify HTML or local product-page files and turn JSON-LD Product and Offer metadata into structured commerce data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports reliability bugs in the bundled parser script. <br>
Mitigation: Review or repair the parser before relying on it in automated workflows, and validate output against known Shopify product-page examples. <br>
Risk: The security guidance warns against piping untrusted stdin into the parser. <br>
Mitigation: Invoke the script only with explicit HTML files that the agent is intended to read. <br>
Risk: The artifact documents static HTML parsing only and does not handle JavaScript-rendered JSON-LD. <br>
Mitigation: Fetch or render pages so the expected JSON-LD is present in the HTML before parsing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igorganapolsky/shopify-jsonld-parser) <br>
- [Schema.org Product reference](https://schema.org/Product) <br>
- [Schema.org Product/Offer Reference](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, shell commands, guidance] <br>
**Output Format:** [JSON parser output with optional field-query results and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inventory status is inferred from schema.org availability values, not exact Shopify inventory quantities.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
