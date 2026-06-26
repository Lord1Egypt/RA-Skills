## Description: <br>
在 macOS 本机从本地壁纸文件夹中立即换壁纸，或安装 launchd 定时轮换任务的可执行技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External macOS users use this skill to rotate desktop wallpaper from a trusted local image folder, either immediately or through a launchd schedule. It is intended for local desktop automation and does not fetch images from the Internet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Path expansion has a command-injection issue when handling user-provided paths. <br>
Mitigation: Install only after the path-expansion bug is fixed by removing eval, and use trusted local wallpaper folders with ordinary names. <br>
Risk: Installing automatic rotation creates a persistent macOS LaunchAgent that continues running until removed. <br>
Mitigation: Install the LaunchAgent only with explicit user intent, disclose the plist path, and use the bundled uninstall script to remove ~/Library/LaunchAgents/com.openclaw.wallpaperrotator.plist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/wallpaper-auto-switch-pro-executable) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and plain-text execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local macOS execution with bash, osascript, find, and gshuf/shuf-compatible random selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact CHANGELOG lists 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
