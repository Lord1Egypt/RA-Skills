## Description: <br>
Scrapes real-time prices, discounts, and specification details from Tmall product pages for price monitoring and SKU comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgc-yj](https://clawhub.ai/user/kgc-yj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce operators use this skill to inspect Tmall product pages, extract current product prices, discounts, SKU-specific specifications, and sales or popularity indicators, then present the result in a structured table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tmall may require login to view product information, exposing account context to the browsing agent. <br>
Mitigation: Keep the session limited to the intended product page and do not authorize checkout, payment, order changes, cart changes, or unrelated account actions. <br>
Risk: Tmall page structure and SKU interactions may change, which can lead to incomplete or stale extracted prices. <br>
Mitigation: Verify price elements and SKU selections on the loaded page before relying on the extracted table for purchasing or monitoring decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kgc-yj/tmall-price-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/kgc-yj) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown table with concise notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product title, current prices, original prices, discounts, SKU-specific price variations, sales or popularity indicators, and login guidance when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
