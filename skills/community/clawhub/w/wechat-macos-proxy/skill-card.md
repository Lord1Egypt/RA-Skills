## Description: <br>
Automates WeChat on macOS through GUI actions to send messages, read chat screenshots, check for new messages, and export chat history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chairmanmiao](https://clawhub.ai/user/chairmanmiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and automation developers use this skill to operate a local macOS WeChat client for personal message sending, chat checks, screenshots, exports, and cautious batch workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a live WeChat account and send messages, including batch sends. <br>
Mitigation: Review every recipient, message, and CSV file before execution; avoid unattended bulk-send or auto-reply workflows. <br>
Risk: The skill requires screen recording and accessibility control for GUI automation. <br>
Mitigation: Install only on machines and accounts where that access level is acceptable, and grant permissions only after reviewing the skill contents. <br>
Risk: The skill can save private chat screenshots, exports, and logs under /tmp/wechat_proxy and related log paths. <br>
Mitigation: Delete temporary screenshots, exports, and feedback or report logs after handling private chat data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chairmanmiao/wechat-macos-proxy) <br>
- [GitHub link from skill metadata](https://github.com/chairmanmiao/wechat-macos-proxy) <br>
- [Peekaboo documentation](https://peekaboo.boo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell command invocations and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create screenshots, logs, and Markdown exports under /tmp/wechat_proxy.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
