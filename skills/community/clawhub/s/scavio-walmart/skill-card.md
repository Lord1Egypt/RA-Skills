## Description: <br>
Search Walmart products and look up product details by product ID. Supports delivery speed, ZIP code, and in-store availability filters. Returns structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scavio-ai](https://clawhub.ai/user/scavio-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Walmart products, retrieve product details, and compare price, fulfillment, delivery ZIP, and in-store pickup availability. Agents should return only API-sourced product data and include product URLs so users can verify before purchasing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, delivery ZIP codes, store filters, and product lookups may be sent to Scavio using the user's SCAVIO_API_KEY. <br>
Mitigation: Use an approved Scavio API key, avoid sending unnecessary sensitive location details, and follow the organization's credential-handling policy. <br>
Risk: Product prices, stock, and fulfillment speed can change, especially same-day availability. <br>
Mitigation: Verify prices and availability on Walmart through the returned product URL before making purchase decisions. <br>
Risk: The skill retrieves and presents shopping data but should not be treated as completing a purchase. <br>
Mitigation: Make purchase decisions outside the skill after reviewing the seller, product page, final price, and fulfillment terms. <br>


## Reference(s): <br>
- [Scavio Documentation](https://scavio.dev/docs) <br>
- [Scavio Walmart skill on ClawHub](https://clawhub.ai/scavio-ai/scavio-walmart) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, JSON] <br>
**Output Format:** [Markdown with shell, Python, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; release metadata sets a 90 second timeout and 1 request per second throttle.] <br>

## Skill Version(s): <br>
2.0.3 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
