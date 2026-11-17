## Description:

Conducts Amazon product research by analyzing market size, competition, profit margins, competitors, and risks to provide GO/NO-GO recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyondbright](https://clawhub.ai/user/beyondbright)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and product researchers use this skill to evaluate Amazon product ideas before launch. It produces a decision-oriented selection report covering market demand, competition, profit assumptions, competitors, and entry risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads an unaudited external Python module before running.

Mitigation: Package or pin the unified_data_layer_v2 dependency inside a trusted environment and keep the external scripts directory non-writable by untrusted users.

Risk: The skill depends on local data-layer and SellerSprite API access for product-research results.

Mitigation: Use only trusted provider configuration and review generated market, profit, competitor, and risk conclusions before making commercial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beyondbright/skills/walter-product-research)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown-style decision report with structured metrics and returned JSON-compatible analysis data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include a keyword, GO/CAUTION/NO-GO decision, score, market metrics, optional profit calculation, competitor summaries, and risk factors; the bundled script targets the US Amazon marketplace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
