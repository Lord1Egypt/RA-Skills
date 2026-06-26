## Description: <br>
Access Scrappa's MCP server for Google, YouTube, Amazon, LinkedIn, Trustpilot, flights, hotels, and more via Model Context Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[userlip](https://clawhub.ai/user/userlip) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure Scrappa's MCP server and request search, scraping, translation, marketplace, travel, real estate, and review data through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-key-backed requests and search queries are sent to Scrappa's external MCP service. <br>
Mitigation: Use a dedicated Scrappa API key where possible, avoid sending secrets or regulated private data, and review Scrappa's privacy and retention terms. <br>
Risk: Returned web and scraping results can contain untrusted or misleading source material. <br>
Mitigation: Review returned content before relying on it or using it in downstream agent actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/userlip/scrappa-skill) <br>
- [Scrappa Documentation](https://scrappa.co/docs) <br>
- [Scrappa MCP Integration Guide](https://scrappa.co/docs/mcp-integration) <br>
- [Scrappa Dashboard](https://scrappa.co/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Scrappa API key and external Scrappa MCP service access; returned web content should be treated as untrusted.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
