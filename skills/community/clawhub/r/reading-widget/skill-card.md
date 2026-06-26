## Description: <br>
Installs and manages a macOS desktop widget that displays WeRead reading statistics, current-book progress, monthly goals, and rotating quotes using a local helper and WeRead API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinadu-ai](https://clawhub.ai/user/tinadu-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Claw, OpenClaw, and Claude Code users on macOS use this skill to install, open, customize, troubleshoot, or uninstall a personal WeRead desktop reading widget. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WeRead API key that identifies the user's WeRead account. <br>
Mitigation: Store the key only in local agent settings or the skill's local config, avoid shell startup files, and remove it from settings when uninstalling. <br>
Risk: The widget runs a local helper on 127.0.0.1:47900 to serve the card and persist goal edits. <br>
Mitigation: Install only if a local helper is acceptable, keep it bound to localhost, and stop or remove the widget directory when no longer needed. <br>
Risk: Optional LaunchAgent setup adds a background startup service. <br>
Mitigation: Enable startup persistence only with explicit user consent and remove the LaunchAgent plist during uninstall. <br>


## Reference(s): <br>
- [ClawHub Reading Widget release page](https://clawhub.ai/tinadu-ai/reading-widget) <br>
- [WeRead official skill package](https://cdn.weread.qq.com/skills/weread-skills.zip) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local files under ~/Desktop/reading-widget and configure a local WeRead API key when the user provides one.] <br>

## Skill Version(s): <br>
1.1.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
