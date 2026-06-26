## Description: <br>
Searches and filters 1688 suppliers through the AlphaShop API using a 1688 product link, image URL, or text keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sourcing teams use this skill to find 1688 suppliers or factory listings from product links, image URLs, or keyword searches, then apply user-requested filters for price, minimum order quantity, or 48-hour shipping rate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search text, product links, and image URLs to the AlphaShop API. <br>
Mitigation: Do not submit private, internal, or signed image URLs unless sharing them with AlphaShop is acceptable. <br>
Risk: AlphaShop access and secret keys are required for API calls. <br>
Mitigation: Configure the keys through the skill environment and avoid pasting secrets into chat. <br>
Risk: Supplier results depend on AlphaShop API responses and may not satisfy every sourcing requirement. <br>
Mitigation: Review returned supplier details and only apply filters that the user explicitly requested. <br>


## Reference(s): <br>
- [AlphaShop AI Select Provider Search API](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/search-1688-supplier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the first matching supplier or product result after requested filters, with no-match guidance when filtering removes all results.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
