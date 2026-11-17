## Description:

Control Android devices via MCP - tap, swipe, OCR, screenshot, UI automation, shell, file management, and AI agent orchestration for Android RPA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenanzong](https://clawhub.ai/user/chenanzong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to connect AI agents to Android devices for robotic process automation, UI inspection, screenshots, OCR, app management, file operations, shell execution, and on-device agent orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad Android device control, including shell commands, file deletion, APK installation, Python execution, pip changes, and agent_run tasks.

Mitigation: Use a dedicated test device and require manual review before high-impact actions are executed.

Risk: Example installation can fetch the npm MCP package without pinning a version.

Mitigation: Pin and verify the yyds-auto-mcp package version and avoid automatic npx -y fetching in controlled environments.

Risk: Remote WiFi or LAN connections can expose device automation beyond the local machine.

Mitigation: Limit remote access to trusted networks or localhost forwarding.

## Reference(s):

- [Yyds.Auto Website](https://yydsauto.com)
- [yyds-auto-mcp npm Package](https://www.npmjs.com/package/yyds-auto-mcp)
- [ClawHub Skill Page](https://clawhub.ai/chenanzong/skills/yyds-auto)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide an agent to invoke MCP tools that operate on a connected Android device.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
