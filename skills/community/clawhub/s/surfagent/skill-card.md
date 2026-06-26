## Description: <br>
Control a real Chrome browser via SurfAgent to navigate, click, type, capture screenshots, extract data, crawl sites, and automate web workflows through SurfAgent's MCP server or local HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentossoftware](https://clawhub.ai/user/agentossoftware) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use SurfAgent to operate a local Windows Chrome browser for web navigation, form interaction, screenshots, structured extraction, site crawling, and URL discovery. It is intended for workflows that need a persistent browser profile and real user sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate a real logged-in Chrome profile, including pages with personal accounts, cookies, or production access. <br>
Mitigation: Use a dedicated isolated browser profile and avoid personal or production accounts unless the workflow explicitly requires them. <br>
Risk: Browser automation can submit forms, change accounts, make purchases, access or change cookies, execute JavaScript, and extract data at scale. <br>
Mitigation: Require human approval before form submission, purchases, account changes, cookie access or changes, JavaScript execution, and bulk data extraction. <br>


## Reference(s): <br>
- [ClawHub SurfAgent Release](https://clawhub.ai/agentossoftware/surfagent) <br>
- [SurfAgent](https://surfagent.app) <br>
- [SurfAgent MCP Server](https://github.com/surfagentapp/surfagent-mcp) <br>
- [SurfAgent Documentation](https://github.com/surfagentapp/surfagent-docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, tool names, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide browser actions that return screenshots, page text, HTML, URLs, cookies, extracted JSON or markdown, and crawl results through the SurfAgent daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
