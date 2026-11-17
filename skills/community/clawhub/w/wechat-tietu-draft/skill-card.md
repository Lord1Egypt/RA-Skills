## Description:

Creates simplified WeChat Official Account tietu-style drafts from UTF-8 .txt files by guiding an agent through Chrome CDP setup, login checks, draft creation, and error feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[punkin6](https://clawhub.ai/user/punkin6)

### License/Terms of Use:

MIT-0

## Use Case:

External creators or operators managing WeChat Official Accounts use this skill to create image-forward simplified drafts from plain text files while receiving environment checks and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in WeChat Official Account browser session and can create remote drafts.

Mitigation: Run it only in an account and Chrome profile intended for this workflow, and review draft content in WeChat before publication.

Risk: Runtime logs and mp_login_screenshot.png may contain sensitive account, session, or draft information.

Mitigation: Treat generated logs and screenshots as sensitive files and delete them after each run.

Risk: The startup flow can force-kill processes on the selected local debugging port.

Mitigation: Review or change the port-killing behavior and use an isolated Chrome debugging port before running the skill.

Risk: The dependency declaration is broad.

Mitigation: Install dependencies in an isolated Python environment and pin reviewed package versions for operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/punkin6/skills/wechat-tietu-draft)
- [WeChat Official Account platform](https://mp.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text status messages with shell commands and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates remote WeChat draft content from one UTF-8 .txt file; runtime logs and screenshots may contain account or draft data.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
