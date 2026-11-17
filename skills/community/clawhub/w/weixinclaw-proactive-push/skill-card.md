## Description:

Enables an agent to proactively send text, images, files, and videos through a configured WorkBuddy ClawBot WeChat bot channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noaheleven](https://clawhub.ai/user/noaheleven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent needs to send proactive WeChat bot notifications, media, or task results to the recipient configured in WorkBuddy. It is intended for environments where the user has already configured the weixinClawBot channel and accepts the credential and messaging risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local WorkBuddy WeChat bot credentials and cursor data.

Mitigation: Install only when you accept that access, keep credential and cursor files out of shares and repositories, and review the artifact before deployment.

Risk: The skill can send real WeChat text or media to the configured recipient.

Mitigation: Verify the recipient in settings.json and require explicit operator confirmation before running commands that send messages or media.

Risk: Network destination, sandboxing, and confirmation safeguards are under-scoped in the security evidence.

Mitigation: Avoid disabling the sandbox globally, keep network permissions narrow, and prefer a release that validates the Weixin API host exactly.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/noaheleven/skills/weixinclaw-proactive-push)
- [Weixin iLink API endpoint](https://ilinkai.weixin.qq.com)
- [Weixin CDN upload endpoint](https://novac2c.cdn.weixin.qq.com/c2c)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-line arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a Node.js script that sends real WeChat bot messages or encrypted media uploads using local WorkBuddy credentials.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
