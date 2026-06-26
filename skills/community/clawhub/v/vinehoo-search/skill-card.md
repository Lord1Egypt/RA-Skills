## Description: <br>
Searches Vinehoo wine and alcohol products and retrieves same-day new-product statistics for agents helping users compare products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ligenhui](https://clawhub.ai/user/ligenhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Vinehoo wine, champagne, spirits, and related products by keyword, price, origin, category, and pagination. It can also summarize and drill into same-day new-product statistics by country, type, winery, or region. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search filters and product-interest details are sent to Vinehoo. <br>
Mitigation: Avoid entering sensitive personal information in search terms or filters. <br>
Risk: Product availability, prices, and purchase details may change after retrieval. <br>
Mitigation: Verify product pages and purchase terms on Vinehoo before buying. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ligenhui/vinehoo-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries with product links and JSON-derived result details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js scripts to query Vinehoo over HTTPS and returns product lists, statistics summaries, or filtered same-day product details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
