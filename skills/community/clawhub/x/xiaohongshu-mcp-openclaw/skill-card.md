## Description: <br>
Provides an OpenClaw workflow for Xiaohongshu/XHS keyword search, note details, comment retrieval, and normalized engagement metrics through a local xiaohongshu-mcp server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glitterccc](https://clawhub.ai/user/Glitterccc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Xiaohongshu/XHS content from OpenClaw, collect note details and comments, and summarize engagement metrics after a user-authenticated login flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an account-backed local MCP service and can expose QR/login output or XHS session data if used on an untrusted machine. <br>
Mitigation: Install only on a trusted machine, keep the service reachable only from localhost or behind a firewall, and treat QR/login output and session data as sensitive. <br>
Risk: Setup may install or update the underlying XHS MCP runtime without an explicit pinned version. <br>
Mitigation: Pin XHS_MCP_VERSION before running setup when reproducibility or change control matters. <br>
Risk: The QR login helper can auto-open QR targets during login. <br>
Mitigation: Set XHS_QR_AUTO_OPEN=0 to review QR targets manually before opening them. <br>
Risk: The optional service installer can keep the MCP server running beyond a single interactive session. <br>
Mitigation: Avoid service_install.sh unless always-on behavior is required, and uninstall or disable the service when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Glitterccc/xiaohongshu-mcp-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/Glitterccc) <br>
- [Project repository cited by artifact README](https://gitea.leapinfra.cn/GlitterCCCC/xiaohongshu-mcp-openclaw) <br>
- [Field Mapping](references/field-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local QR file paths, open commands, search results, note details, comments, normalized engagement metrics, and summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
