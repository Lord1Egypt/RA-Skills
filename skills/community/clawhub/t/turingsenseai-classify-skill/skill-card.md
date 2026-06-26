## Description: <br>
Classifies product images through the configured turing-shikuan-mcp service and returns product category, brand, series, and a short summary without making authenticity, quality, or value judgments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turingsenseai](https://clawhub.ai/user/turingsenseai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to identify product category, brand, series, and a brief description from an accessible image URL. It also guides first-time setup of the required MCP credentials and explicitly avoids product authentication, genuineness, quality, or value judgments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a remote Turing MCP service with user-provided API credentials. <br>
Mitigation: Install only if the endpoint is trusted, use scoped or test credentials where possible, and review setup.sh before running it. <br>
Risk: Image URLs are sent to the external classification service. <br>
Mitigation: Only provide image URLs that are accessible and appropriate to share with the service. <br>
Risk: Product classification results could be mistaken for authentication or quality assessment. <br>
Mitigation: Keep outputs limited to category, brand, series, and summary, and state that results are not authenticity, genuineness, quality, or value conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/turingsenseai/turingsenseai-classify-skill) <br>
- [Turing Shikuan MCP endpoint](https://turing-mcp-server-test.turingsenseai.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Structured Markdown in Chinese, with setup shell commands or JSON configuration snippets when configuration is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured MCP endpoint, API credentials, and a valid accessible image URL; result fields are kind, brand, series, and summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
