## Description: <br>
SwipeNode is a web-extraction skill for AI agents that extracts structured JSON or cleaned text from modern web pages without using a headless browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nefas11](https://clawhub.ai/user/Nefas11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent users use SwipeNode to extract structured JSON or cleaned text from data-rich web pages for e-commerce, news, market research, content analysis, and API-less data collection when browser or raw HTML workflows are too costly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes anti-bot bypass behavior for web extraction. <br>
Mitigation: Use it only on sites you own or are authorized to access, respect site terms and rate limits, and avoid attempts to bypass access controls. <br>
Risk: The skill can register a persistent local MCP integration. <br>
Mitigation: Review the MCP registration before and after use, remove it when no longer needed, and avoid passing sensitive headers unless necessary. <br>
Risk: The scanner marked this release suspicious because its safety scoping is limited. <br>
Mitigation: Audit and pin the external source before installation, and run it in a controlled environment with clear network-use boundaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nefas11/swipenode-2) <br>
- [Publisher profile](https://clawhub.ai/user/Nefas11) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON or cleaned plain text from extraction commands, with Markdown command guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-URL extraction, batch extraction, and local MCP server setup.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
