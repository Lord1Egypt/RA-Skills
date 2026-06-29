## Description: <br>
Installs and configures a WeChat-to-Claude Code bridge on macOS, with health checks and repair scripts for common setup issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heavenchenggong](https://clawhub.ai/user/heavenchenggong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to install, diagnose, and maintain a local WeChat bridge for interacting with Claude Code from WeChat. It is primarily documented for macOS and includes guidance for account choice, API endpoint routing, and daemon management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persistent WeChat bridge can cause local Claude Code to read files, write files, and run commands. <br>
Mitigation: Install only when that behavior is intended, bind a trusted or test WeChat account, and do not share the bound account. <br>
Risk: Private WeChat conversations may be routed through a company or local proxy via ANTHROPIC_BASE_URL. <br>
Mitigation: Review the API endpoint before use and avoid routing private chats through a company proxy. <br>
Risk: Long-lived API tokens stored in LaunchAgent plists may be exposed locally. <br>
Mitigation: Avoid storing long-lived tokens in plist files unless the local exposure risk is understood and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heavenchenggong/skills/wechat-claude-code-installer) <br>
- [Publisher profile](https://clawhub.ai/user/heavenchenggong) <br>
- [Upstream bridge project referenced by the artifact](https://github.com/Wechat-ggGitHub/wechat-claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces macOS-focused installation, health-check, repair, daemon-management, and uninstall guidance for a local WeChat bridge.] <br>

## Skill Version(s): <br>
0.3.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
