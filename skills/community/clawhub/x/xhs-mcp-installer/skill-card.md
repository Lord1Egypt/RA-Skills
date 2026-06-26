## Description: <br>
Installs and starts the Xiaohongshu MCP service on macOS or Linux by selecting a platform binary, configuring autostart, running health checks, and guiding login. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexduming](https://clawhub.ai/user/alexduming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to install and manage a local Xiaohongshu MCP service on macOS or Linux, including service startup, health checks, and login guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer makes persistent local service changes through launchd, systemd, and watchdog setup. <br>
Mitigation: Review the installer before execution and prefer user-level, low-privilege service configuration where possible. <br>
Risk: The installer can kill processes using port 18060, which may affect unrelated local services. <br>
Mitigation: Confirm what is listening on port 18060 before allowing restart or kill commands to run. <br>
Risk: The skill includes a cookie-import login path that can expose account access if cookies are pasted or stored carelessly. <br>
Mitigation: Prefer QR-code login and avoid cookie import unless the user understands the account-access implications. <br>
Risk: The skill downloads and runs an upstream binary as a local background service. <br>
Mitigation: Install only when the upstream project is trusted and the downloaded binary source is acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexduming/xhs-mcp-installer) <br>
- [Xiaohongshu MCP upstream project](https://github.com/xpzouying/xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON-RPC request examples, and service configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide creation of launchd, systemd, crontab/watchdog, log, and cookie files when a user follows its commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
