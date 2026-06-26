## Description: <br>
Search UpKuaJing map merchant data by region, nearby location, industry, contact availability, or shop name, and retrieve geographic lists for country, province, and city parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upkuajing](https://clawhub.ai/user/upkuajing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External field sales, distributor, brand, and market intelligence teams use this skill to find geo-targeted merchants, analyze regional business presence, and prepare offline-to-online lead lists through UpKuaJing APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an UpKuaJing API key and sends merchant-search queries to a paid third-party API. <br>
Mitigation: Install only when the publisher is trusted, keep the API key protected or rotated, and confirm billable searches before execution. <br>
Risk: Large merchant searches can incur fees and may produce local result files containing sensitive business leads. <br>
Mitigation: Require explicit confirmation before large queries and periodically remove local task_data files that are no longer needed. <br>


## Reference(s): <br>
- [UpKuaJing skill page](https://clawhub.ai/upkuajing/upkuajing-map-merchants-search) <br>
- [UpKuaJing homepage](https://www.upkuajing.com) <br>
- [UpKuaJing Open Platform](https://developer.upkuajing.com/) <br>
- [UpKuaJing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html) <br>
- [Merchants Search API](references/merchants-search-api.md) <br>
- [Country List API](references/country-list-api.md) <br>
- [Province List API](references/province-list-api.md) <br>
- [City List API](references/city-list-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Merchant search results may be stored locally as task data for large or resumed queries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
