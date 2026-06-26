## Description: <br>
Fetches Amazon product review data through Reveyes and helps analyze ratings, negative-review patterns, and listing improvement opportunities for e-commerce operators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuojiuya](https://clawhub.ai/user/zhuojiuya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce operators and agents use this skill to fetch Amazon reviews by ASIN across supported marketplaces, inspect review distributions, and produce practical negative-review and listing optimization reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amazon product, marketplace, and review queries are sent to an external review API provider. <br>
Mitigation: Install only if that provider is trusted for the products and research queries being submitted. <br>
Risk: Outputs may include public reviewer identifiers such as names and profile URLs. <br>
Mitigation: Avoid exporting raw reviewer records unless needed and redact reviewer profile links or names before sharing results. <br>
Risk: The Reveyes API key is required for operation. <br>
Mitigation: Keep the API key in an environment variable and do not paste it into prompts, reports, or shared artifacts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhuojiuya/reveyes-skill) <br>
- [Reveyes official site](https://www.reveyes.cn) <br>
- [Reveyes Python SDK](https://pypi.org/project/reveyes/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON review data followed by Markdown analysis and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVEYES_API_KEY and may include public reviewer names, profile URLs, ratings, review text, media links, and marketplace metadata.] <br>

## Skill Version(s): <br>
1.1.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
