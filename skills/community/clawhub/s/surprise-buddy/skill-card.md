## Description: <br>
Look up curated gift ideas from the Surprise Buddy database: country-scoped product cards with title, image, price, and a ready-to-click product link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastian1747](https://clawhub.ai/user/sebastian1747) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to find curated gift ideas for a recipient when the country is known and filters such as occasion, age, interests, profession, color, or budget are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gift searches can involve personal details about recipients and returned product links may include marketplace tracking or affiliate-style query parameters. <br>
Mitigation: Avoid entering highly sensitive personal details about recipients, and review returned marketplace links before clicking or sharing them. <br>


## Reference(s): <br>
- [Surprise Buddy MCP endpoint](https://www.surprise-buddy.com/api/mcp) <br>
- [Surprise Buddy](https://www.surprise-buddy.com) <br>
- [OpenAPI 3.1 specification](https://www.surprise-buddy.com/openapi.yaml) <br>
- [MCP discovery manifest](https://www.surprise-buddy.com/.well-known/mcp.json) <br>
- [LLMs.txt](https://www.surprise-buddy.com/llms.txt) <br>
- [Developer landing page](https://www.surprise-buddy.com/en/agents) <br>
- [ClawHub skill page](https://clawhub.ai/sebastian1747/surprise-buddy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with JSON examples and marketplace links returned by the MCP service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a country code for gift searches; product prices are not live price quotes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
