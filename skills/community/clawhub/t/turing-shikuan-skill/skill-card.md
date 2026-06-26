## Description: <br>
Recognizes product category, brand, series, and brief product details from image URLs by using a configured turing-shikuan-mcp service, without making authenticity, quality, or value judgments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyyyyyaa](https://clawhub.ai/user/xyyyyyaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to identify a product's category, brand, series, and short summary from an accessible image URL after configuring Turing MCP credentials. It is intended for product recognition only and should not be used for authenticity, quality, or value assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remote Turing MCP service receives submitted image URLs and uses user-provided API credentials. <br>
Mitigation: Confirm the endpoint is trusted, use limited credentials where possible, and submit only image URLs that are acceptable to share with the external service. <br>
Risk: MCP configuration may contain API key and secret headers. <br>
Mitigation: Keep generated MCP configuration and environment variables out of version control and avoid writing real credentials into repository files. <br>
Risk: The setup script installs or uses the mcporter package and registers a project-scoped MCP server. <br>
Mitigation: Review the mcporter package and setup script before running them, and run setup only in an environment where project-scoped MCP configuration is appropriate. <br>
Risk: Product recognition results could be mistaken for authenticity, quality, or value judgments. <br>
Mitigation: Use the fixed output framing that states results come from turing-shikuan-mcp for recognition only and do not represent an authenticity conclusion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xyyyyyaa/turing-shikuan-skill) <br>
- [Turing Shikuan MCP endpoint](https://turing-mcp-server-test.turingsenseai.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with a structured Chinese result template and shell or JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses image URLs and turing-shikuan-mcp responses; missing or empty response fields are reported without guessing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
