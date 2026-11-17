## Description:

Automates WeChat messaging on macOS through GUI control to send messages, read chat screenshots, monitor new-message indicators, batch send from CSV files, and export chat screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chairmanmiao](https://clawhub.ai/user/chairmanmiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users on macOS use this skill to operate WeChat through GUI automation for scheduled sends, batch messaging, message checks, and chat-record exports. It should be used only where the operator has authorization to access and act on the WeChat conversations involved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control WeChat and send messages, including batch-send and listen modes.

Mitigation: Use it only for authorized conversations, review generated or batch messages before sending, and prefer semi or manual mode for sensitive chats.

Risk: Screenshots, logs, and exported chat records may contain private messages and are written under /tmp/wechat_proxy.

Mitigation: Treat those files as private chat records, avoid shared machines, and clean /tmp/wechat_proxy after use.

Risk: The skill requires macOS Screen Recording and Accessibility permissions for GUI automation.

Mitigation: Grant permissions only when comfortable with a tool operating WeChat, monitor use, and revoke permissions when automation is no longer needed.

## Reference(s):

- [WeChat macOS Proxy GitHub repository](https://github.com/chairmanmiao/wechat-macos-proxy)
- [Peekaboo documentation](https://peekaboo.boo)
- [ClawHub skill page](https://clawhub.ai/chairmanmiao/skills/wechat-macos-proxy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown and text guidance with shell command examples; runtime commands can create screenshots, logs, CSV-driven sends, and Markdown chat exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, WeChat, peekaboo, jq, Screen Recording permission, and Accessibility permission.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
