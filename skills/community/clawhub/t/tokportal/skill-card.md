## Description: <br>
Automate TikTok and Instagram account creation, video distribution, content uploads, and analytics through TokPortal's API and MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naybu256](https://clawhub.ai/user/naybu256) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External operators and developers use TokPortal to configure, publish, upload, and monitor TikTok and Instagram account bundles through the TokPortal API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate TokPortal at scale, including account creation, publishing, uploads, and paid credit-consuming actions. <br>
Mitigation: Require explicit approval before account creation, publishing, uploads, credential retrieval, verification-code retrieval, or paid actions. <br>
Risk: The skill depends on a TokPortal API key and may return account credentials or verification codes. <br>
Mitigation: Use a restricted or low-credit API key where possible, keep returned credentials out of shared logs, and avoid exposing verification codes. <br>
Risk: The MCP package and upload tools can affect local execution and private file handling. <br>
Mitigation: Pin and review the tokportal-mcp package before running it, and do not upload private local files. <br>


## Reference(s): <br>
- [TokPortal developer documentation](https://developers.tokportal.com) <br>
- [TokPortal npm MCP package](https://www.npmjs.com/package/tokportal-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/naybu256/tokportal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and TokPortal API/tool results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKPORTAL_API_KEY for authenticated TokPortal operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, frontmatter, changelog released 2026-02-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
