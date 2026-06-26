## Description: <br>
Tariff calculation and HS code classification tool via the TurtleClassify API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncai519](https://clawhub.ai/user/simoncai519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, sourcing teams, and trade operations users use this skill to classify products, retrieve HS codes, estimate tariff rates, and prepare product-level tariff data for CSV or DataFrame workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product names, origin and destination country codes, and optional product metadata are sent to accio.com for classification. <br>
Mitigation: Use only with product data approved for third-party processing; avoid confidential catalogs or unreleased sourcing plans unless that processing is approved. <br>
Risk: Tariff classifications and rates returned by the external service may be incomplete, unavailable, or unsuitable as final compliance determinations. <br>
Mitigation: Review returned HS codes, rates, formulas, and calculation details before using them for operational, legal, or customs decisions. <br>


## Reference(s): <br>
- [TurtleClassify API Reference](references/api-reference.md) <br>
- [TurtleClassify classify endpoint](https://www.accio.com/api/turtle/classify) <br>
- [ClawHub release page](https://clawhub.ai/simoncai519/tariff-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Python return values as a flattened list of dictionaries or detailed metadata dictionary, with examples documented in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls a third-party API and may include HS code, tariff rate, tariff formula, calculation type, product identifiers, and raw calculation details.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
