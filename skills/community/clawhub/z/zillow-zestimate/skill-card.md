## Description: <br>
Zillow Zestimate provides property valuation and rent Zestimate lookups through Zillapi.com with a single focused tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikhonit](https://clawhub.ai/user/nikhonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home buyers, renters, real-estate professionals, and agents use this skill when a user explicitly asks for property valuation data, such as a Zestimate, rent Zestimate, tax-assessed value, or last sale price. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zillapi API key and sends property addresses or zpids to Zillapi for valuation lookups. <br>
Mitigation: Store ZILLAPI_KEY as an environment secret and use the skill only when the user explicitly wants a valuation. <br>
Risk: Incidental addresses or private property data could be sent to the external API if the skill is used too broadly. <br>
Mitigation: Follow the activation guidance and avoid lookups for incidental addresses or private property data unless the user has requested valuation data. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/nikhonit/zillow-zestimate) <br>
- [Zillapi](https://zillapi.com) <br>
- [Zillapi signup](https://zillapi.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON tool response with property valuation fields or structured error details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZILLAPI_KEY and either a zpid or an address; zpid is preferred when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
