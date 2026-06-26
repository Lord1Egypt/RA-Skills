## Description: <br>
Smart Search routes web searches across Exa MCP, optional local SearX, and optional Tavily summaries with no required API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lee920311](https://clawhub.ai/user/lee920311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Smart Search to retrieve web, technical, news, academic, and business research results. The skill can route privacy-sensitive queries to a configured local SearX instance and use Tavily for summaries or deeper research when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to Exa, Tavily, or a configured SearX instance. <br>
Mitigation: Do not search secrets, regulated personal data, or internal business information unless a local-only SearX setup has been verified and external fallback is disabled. <br>
Risk: TAVILY_API_KEY is an optional credential read from the local environment. <br>
Mitigation: Treat TAVILY_API_KEY as a secret, avoid printing it in terminals, and keep it out of committed files. <br>
Risk: A user-managed SearX deployment can create exposure if it is bound broadly or left unhardened. <br>
Mitigation: Bind SearX to 127.0.0.1 where possible, enable limits, and use a maintained image. <br>


## Reference(s): <br>
- [Smart Search on ClawHub](https://clawhub.ai/lee920311/smart-search) <br>
- [lee920311 publisher profile](https://clawhub.ai/user/lee920311) <br>
- [Exa MCP endpoint](https://mcp.exa.ai/mcp) <br>
- [Tavily](https://tavily.com) <br>
- [SearX deployment guide](README.searx.md) <br>
- [Tavily setup guide](TAVILY_SETUP.md) <br>
- [Security guidance](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style search results and setup guidance with shell commands and JSON-backed API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses optional SEARXNG_URL and TAVILY_API_KEY; search queries may be sent to Exa, Tavily, or a configured SearX instance.] <br>

## Skill Version(s): <br>
4.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
