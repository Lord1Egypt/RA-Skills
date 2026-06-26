## Description: <br>
TechSnif queries TechSnif's public tech news API through a bundled CLI for current articles and trends across AI, startups, venture, and robotics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coffeefuelbump](https://clawhub.ai/user/coffeefuelbump) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to retrieve, search, and summarize current technology news from TechSnif for briefings, research, and topical monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs bundled Node.js code. <br>
Mitigation: Install only from a trusted release and review or scan the bundled CLI before deployment. <br>
Risk: Tech-news search terms are sent to TechSnif or to the configured API endpoint. <br>
Mitigation: Avoid confidential queries and verify TECHSNIF_API_URL or --api-url before use when endpoint control matters. <br>


## Reference(s): <br>
- [TechSnif homepage](https://techsnif.com/) <br>
- [TechSnif CLI package](https://www.npmjs.com/package/@techsnif/cli) <br>
- [TechSnif categories](references/categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON data, Guidance] <br>
**Output Format:** [JSON responses from the bundled CLI, with optional markdown, text, or HTML article bodies.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API access; listing commands omit full article content until an article slug is requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
