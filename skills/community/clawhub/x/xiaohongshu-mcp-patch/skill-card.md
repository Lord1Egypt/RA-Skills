## Description: <br>
自动检测并修复小红书MCP部署常见问题，包括端口占用、cookie路径、服务状态及超时等待。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TinaDu-AI](https://clawhub.ai/user/TinaDu-AI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot Xiaohongshu MCP deployments by generating Bash repair scripts and command guidance for port conflicts, cookie placement, Chrome download waits, service restarts, and MCP connectivity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair commands may terminate processes using port 18060 without enough user control. <br>
Mitigation: Review every command before running it and confirm what process is using port 18060 before killing it. <br>
Risk: The scripts handle cookies.json, which may contain login credentials. <br>
Mitigation: Avoid copying cookies.json into shared temporary locations, restrict file permissions, and remove extra copies after troubleshooting. <br>
Risk: The one-click script can start a local Xiaohongshu MCP binary as a background service. <br>
Mitigation: Do not run the one-click script until the Xiaohongshu MCP binary and its source have been verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TinaDu-AI/xiaohongshu-mcp-patch) <br>
- [Xiaohongshu MCP project](https://github.com/xpzouying/xiaohongshu-mcp) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with Bash code blocks and troubleshooting instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes independent repair scripts and a one-click repair script for local Xiaohongshu MCP troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
