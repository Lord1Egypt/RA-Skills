## Description: <br>
Provides programmatic tools for fetching, searching, and reading RFC documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical readers use this skill to fetch full RFCs, search RFCs by keyword, and retrieve specific RFC sections through an external MCP-backed service. Use is appropriate when the user intentionally accepts the third-party XiaoBenYang service path and API-key handling requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RFC query parameters and the XBY API key are routed through a third-party XiaoBenYang MCP proxy rather than a direct ietf.org-only reader. <br>
Mitigation: Install only when that service path is intended, avoid sending sensitive query context, and disclose the third-party proxy behavior to users. <br>
Risk: The skill stores the XBY API key in a local .env file. <br>
Mitigation: Use a dedicated key, keep .env out of source control and shared artifacts, and rotate or revoke the key if it may have been exposed. <br>
Risk: Users may assume results are retrieved directly from authoritative RFC sources. <br>
Mitigation: Treat returned content as mediated by the proxy and verify important RFC text against authoritative sources when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/rfc-doc) <br>
- [XiaoBenYang service](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown summaries of JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY API key and sends RFC lookup parameters to the XiaoBenYang MCP proxy.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
