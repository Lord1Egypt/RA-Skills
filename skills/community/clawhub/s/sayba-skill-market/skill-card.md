## Description: <br>
Sayba Skill Market MCP Server - Discover, invoke, publish, and rate AI Agent skills on Sayba's marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saybanet](https://clawhub.ai/user/saybanet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this MCP server to search Sayba's skill marketplace, inspect skill details, invoke skills, and manage marketplace publishing, ratings, and account history through an MCP client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated marketplace tools can publish skills, submit ratings or reviews, and send skill inputs to Sayba under the user's API key. <br>
Mitigation: Require MCP client approval before publish_skill, rate_skill, and invoke_skill run; avoid sending secrets or proprietary material as skill input or review text. <br>
Risk: The server requires a Sayba API key for account-specific and paid operations. <br>
Mitigation: Use a limited-scope or revocable API key when available and install only when the publisher and Sayba endpoint are trusted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/saybanet/sayba-skill-market) <br>
- [Sayba platform](https://ai.sayba.com) <br>
- [npm package](https://www.npmjs.com/package/sayba-skill-market) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Guidance] <br>
**Output Format:** [MCP tool responses as text with JSON payloads where returned by Sayba APIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated tools require SAYBA_API_KEY; SAYBA_BASE_URL can point to a custom Sayba instance.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
