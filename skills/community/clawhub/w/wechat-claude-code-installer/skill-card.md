## Description:

Installs and configures a WeChat-to-Claude Code bridge, then guides users through health checks and macOS-focused fixes for common setup issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heavenchenggong](https://clawhub.ai/user/heavenchenggong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to install a local WeChat bridge, run pre-install checks, bind a WeChat account, and apply configuration fixes for working directory, prompt, daemon, endpoint, and upstream drift issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs remote upstream code and npm dependencies.

Mitigation: Audit or pin the upstream repository and dependencies before running install.sh, then use check-upstream.sh to review later changes before upgrading.

Risk: The local daemon can access WeChat messages, files, commands, and credentials with the user's account permissions.

Mitigation: Use a disposable or non-work WeChat account, avoid sensitive chats and files, and treat the daemon as a local user-level automation process.

Risk: A configured ANTHROPIC_BASE_URL may route WeChat conversations through a company or third-party proxy.

Mitigation: Run doctor.sh before installation and verify the endpoint and logging policy before sending private or sensitive messages.

Risk: Persisting an Anthropic key in a LaunchAgent plist can expose credentials on the local machine.

Mitigation: Avoid storing a real Anthropic key in the plist where possible and rotate any key that may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/heavenchenggong/skills/wechat-claude-code-installer)
- [Upstream wechat-claude-code project](https://github.com/Wechat-ggGitHub/wechat-claude-code)
- [Tencent iLink AI](https://ilinkai.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS is the tested platform; Linux support is documented through the upstream project only.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
