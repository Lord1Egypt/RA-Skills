## Description: <br>
Extracts structured product data from e-commerce URLs with the Zyte API and generates side-by-side comparison tables with purchase recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apscrapes](https://clawhub.ai/user/apscrapes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to compare products from multiple e-commerce URLs, normalize extracted product attributes, and receive purchase-oriented recommendations based on stated intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes DNS troubleshooting guidance that could change system-wide network behavior. <br>
Mitigation: Do not run or allow an agent to run the /etc/resolv.conf DNS command; handle DNS issues through administrator-approved network settings. <br>
Risk: Product URLs and scraped product data are sent to the Zyte API. <br>
Mitigation: Use only public product URLs you are comfortable sending to Zyte, and avoid URLs containing sensitive account, cart, or session information. <br>
Risk: The skill requires a Zyte API key for authenticated API calls. <br>
Mitigation: Provide ZYTE_API_KEY through environment variables or a secure local secret store, and avoid placing the key directly in prompts or shared logs. <br>


## Reference(s): <br>
- [Zyte API Notes for Product Extraction](references/zyte-api-notes.md) <br>
- [Zyte API](https://www.zyte.com/zyte-api/) <br>
- [ClawHub Skill Page](https://clawhub.ai/apscrapes/zyte-ecommerce-products-compare-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/apscrapes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown comparison tables with JSON summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product recommendations, data notes, failed URL reasons, currency mismatch notes, and fetch timing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
