## Description:

Sends proactive text, image, file, and video messages through a locally configured WorkBuddy ClawBot WeChat bot channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noaheleven](https://clawhub.ai/user/noaheleven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to send proactive WeChat notifications or media to a configured recipient through the user's local WorkBuddy ClawBot account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real WeChat messages and files through the user's local WorkBuddy ClawBot account.

Mitigation: Use it only for intentional outbound notifications to the configured recipient, and add an explicit confirmation step before routine or automated sends.

Risk: Local bot tokens, cursor files, context tokens, message contents, and recipient IDs are sensitive.

Mitigation: Keep settings and cursor files local, avoid sharing them, and redact recipient identifiers and token-derived values from logs or transcripts.

Risk: Credentials could be sent to an unexpected endpoint if local configuration is altered.

Mitigation: Verify that ~/.workbuddy/settings.json uses the official Weixin iLink base URL before running the skill.

Risk: Broad sandbox bypasses increase the chance of unintended network access.

Mitigation: Avoid disabling sandboxing broadly; grant only the network access needed for the intended WeChat send workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noaheleven/skills/weixinclawbot)
- [Publisher profile](https://clawhub.ai/user/noaheleven)
- [Weixin iLink endpoint](https://ilinkai.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown guidance with shell commands; runtime sends WeChat bot text or media messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send text, images, files, or videos using local WorkBuddy ClawBot credentials.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
