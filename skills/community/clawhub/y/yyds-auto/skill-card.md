## Description: <br>
Control Android devices via MCP, including tapping, swiping, OCR, screenshots, UI automation, shell access, file management, and AI agent orchestration for Android RPA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenanzong](https://clawhub.ai/user/chenanzong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and automation teams use this skill to connect AI agents to Android devices for RPA, app testing, UI inspection, OCR, file operations, and controlled device workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an AI agent broad control over a connected Android device, including touch input, OCR, screenshots, app control, file operations, and messaging-capable workflows. <br>
Mitigation: Use a dedicated test device or isolated profile, avoid sensitive personal accounts, and require manual approval before actions that affect accounts, messages, purchases, files, or installed apps. <br>
Risk: Shell access, file deletion, app install or uninstall, Python execution, and package management can change device state or expose sensitive data. <br>
Mitigation: Gate high-impact tools behind explicit approval, keep backups of important device data, and verify the intended command, path, package, or script before execution. <br>
Risk: The on-device automation engine may be reachable over USB forwarding or WiFi/LAN, which can increase exposure if used on untrusted networks. <br>
Mitigation: Keep the engine off untrusted networks, prefer local ADB forwarding or a trusted LAN, restrict host and port access, and verify the npm package and Android app provenance before use. <br>


## Reference(s): <br>
- [Yyds.Auto homepage](https://yydsauto.com) <br>
- [yyds-auto-mcp npm package](https://www.npmjs.com/package/yyds-auto-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/chenanzong/yyds-auto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell command examples, and MCP tool result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Android device observations such as screenshots, OCR text, UI hierarchy data, shell results, file operation results, and app or agent status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
