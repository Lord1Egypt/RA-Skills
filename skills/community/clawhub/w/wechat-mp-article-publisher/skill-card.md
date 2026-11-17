## Description:

Complete the creation, editing, and publishing of WeChat Official Account articles through browser automation simulating manual operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to automate article creation, editing, preview, scheduling, and publishing in the WeChat Official Account backend while retaining required QR-code confirmation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates publishing choices on a live WeChat Official Account admin page.

Mitigation: Review the target account, article content, author, originality setting, mass notification setting, schedule, preview, and final publish action before scanning any final verification QR code.

Risk: Login and publishing verification cannot be fully automated and require the admin WeChat account holder to scan QR codes.

Mitigation: Pause for the account holder at each QR-code step and proceed only after the page state confirms the intended login, preview, or publishing action.

Risk: Mass notification and post-publish modification limits can make mistakes difficult to correct.

Mitigation: Keep mass notification off unless explicitly requested, confirm applicable account limits, and complete preview review before publishing.

## Reference(s):

- [WeChat Official Account Platform](https://mp.weixin.qq.com)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/wechat-mp-article-publisher)
- [Publisher profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown instructions with browser automation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user QR-code scans for login, preview, and final publishing verification.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
