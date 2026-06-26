## Description: <br>
An out-of-the-box hotel search skill powered by Umy MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudwavego](https://clawhub.ai/user/cloudwavego) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to search hotels, inspect hotel details, and prepare structured hotel search calls with location, stay dates, budget, rating, and currency parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search parameters are sent to Umy. <br>
Mitigation: Use the skill only when sharing location, dates, budget, and related hotel search filters with Umy is acceptable. <br>
Risk: Personal details may be included in hotel queries if user input is forwarded without filtering. <br>
Mitigation: Remove names, phone numbers, email addresses, identifiers, and unrelated free-form text before calling the hotel search tool. <br>
Risk: A local UMY_API_KEY may be used by the CLI and consume the user's Umy quota. <br>
Mitigation: Check the runtime environment before use and unset UMY_API_KEY when the documented public key should be used instead. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cloudwavego/umy-hotel) <br>
- [Umy MCP server](https://mcp.umy.com/sse) <br>
- [Umy Hotel API base](https://api.umy.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON-formatted hotel search or detail results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hotel searches may include booking links and use a public Umy API key or a locally configured UMY_API_KEY.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
