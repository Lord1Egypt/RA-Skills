## Description:

Extracts real-time prices, promotions, product titles, SKU-specific specification details, and sales or popularity signals from user-provided Tmall product pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgc-yj](https://clawhub.ai/user/kgc-yj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to inspect Tmall product pages, compare prices across specifications, and summarize current discounts or promotional pricing in a structured format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require access to a logged-in Tmall or Taobao browser session to view product details.

Mitigation: Use it only on pages you intend to inspect, log in manually when needed, and do not share credentials with the agent.

Risk: Tmall page structure and SKU interactions can change, which may cause incomplete or stale price extraction.

Mitigation: Review the resulting table against the live product page, especially for coupon, promotion, and specification-specific prices.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes only product, price, promotion, SKU, and sales information visible in the user's active browser session.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
