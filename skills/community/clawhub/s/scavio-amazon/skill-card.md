## Description: <br>
Search Amazon products and retrieve product details by ASIN using Scavio, returning structured JSON with price, rating, Prime status, availability, and product metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scavio-ai](https://clawhub.ai/user/scavio-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Amazon listings, inspect product details by ASIN, and compare product pricing, ratings, availability, and marketplace-specific results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Scavio API credential. <br>
Mitigation: Use SCAVIO_API_KEY from the environment, avoid exposing it in prompts or logs, and confirm it is set before making API requests. <br>
Risk: Amazon product names, prices, ratings, and availability can be incorrect if generated without live API data. <br>
Mitigation: Return only data from the Scavio API, include product URLs for verification, and report API errors or empty results instead of fabricating values. <br>


## Reference(s): <br>
- [Scavio documentation](https://scavio.dev/docs) <br>
- [ClawHub skill page](https://clawhub.ai/scavio-ai/scavio-amazon) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with API endpoints, shell setup commands, Python examples, and structured JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; configured timeout is 90 seconds and throttle is 1 request per second.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
